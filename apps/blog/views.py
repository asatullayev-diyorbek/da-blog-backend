import threading
import requests
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F, Q, Sum
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import Category, Tag, Post, Comment
from .serializers import (
    CategorySerializer, TagSerializer,
    PostListSerializer, PostDetailSerializer,
    CommentSerializer, CommentCreateSerializer,
)


def _send_telegram(text):
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    if not token or not chat_id:
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
            timeout=5,
        )
    except Exception:
        pass


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    pagination_class = None


class TagListView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class PostListView(ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Post.objects.filter(published=True).select_related("category", "author").prefetch_related("tags")
        category = self.request.query_params.get("category")
        tag = self.request.query_params.get("tag")
        search = self.request.query_params.get("search")
        if category:
            qs = qs.filter(category__id=category)
        if tag:
            qs = qs.filter(tags__slug=tag)
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(short_description__icontains=search))
        return qs


class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.filter(published=True).select_related("category", "author").prefetch_related("tags")
    serializer_class = PostDetailSerializer
    lookup_field = "slug"
    permission_classes = [AllowAny]


class PostViewView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, slug):
        updated = Post.objects.filter(slug=slug, published=True).update(views=F("views") + 1)
        if not updated:
            return Response(status=404)
        return Response({"ok": True})


class FeaturedPostView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        post = Post.objects.filter(published=True, featured=True).select_related("category", "author").prefetch_related("tags").first()
        if not post:
            return Response(None)
        return Response(PostListSerializer(post, context={"request": request}).data)


class StatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        from apps.courses.models import Course
        posts_count = Post.objects.filter(published=True).count()
        courses_count = Course.objects.filter(published=True).count()
        total_views = Post.objects.filter(published=True).aggregate(total=Sum("views"))["total"] or 0
        comments_count = Comment.objects.filter(approved=True).count()
        return Response({
            "posts": posts_count,
            "courses": courses_count,
            "views": total_views,
            "comments": comments_count,
        })


class CommentListCreateView(ListCreateAPIView):
    permission_classes = [AllowAny]
    pagination_class = None

    def get_post(self):
        return get_object_or_404(Post, slug=self.kwargs["slug"], published=True)

    def get_queryset(self):
        return Comment.objects.filter(post=self.get_post(), approved=True)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CommentCreateSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        post = self.get_post()
        comment = serializer.save(post=post)
        text = (
            f"💬 <b>Yangi izoh!</b>\n\n"
            f"📝 <b>Maqola:</b> {post.title}\n"
            f"👤 <b>Kim:</b> {comment.name}\n"
            f"🗒 <b>Izoh:</b> {comment.content}"
        )
        threading.Thread(target=_send_telegram, args=(text,), daemon=True).start()
