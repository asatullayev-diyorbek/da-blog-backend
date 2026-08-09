from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, PermissionDenied
from django.db.models import Q
from .models import Course, Lesson
from .serializers import CourseListSerializer, CourseDetailSerializer, LessonDetailSerializer


class CourseListView(ListAPIView):
    serializer_class = CourseListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = Course.objects.filter(published=True).select_related("category", "instructor")
        category = self.request.query_params.get("category")
        level = self.request.query_params.get("level")
        price = self.request.query_params.get("price")
        search = self.request.query_params.get("search")
        if category:
            qs = qs.filter(category__id=category)
        if level:
            qs = qs.filter(level=level)
        if price:
            qs = qs.filter(price=price)
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(short_description__icontains=search))
        return qs


class CourseDetailView(RetrieveAPIView):
    queryset = Course.objects.filter(published=True).select_related("category", "instructor").prefetch_related("lessons")
    serializer_class = CourseDetailSerializer
    lookup_field = "slug"
    permission_classes = [AllowAny]


class LessonDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, course_slug, lesson_slug):
        try:
            course = Course.objects.get(slug=course_slug, published=True)
        except Course.DoesNotExist:
            raise NotFound("Kurs topilmadi.")

        try:
            lesson = Lesson.objects.prefetch_related("quizzes__questions__options").get(course=course, slug=lesson_slug)
        except Lesson.DoesNotExist:
            raise NotFound("Dars topilmadi.")

        is_paid = course.price == "Pullik"
        if is_paid and not lesson.is_free and not request.user.is_authenticated:
            raise PermissionDenied("Bu darsni ko'rish uchun kursga yozilish kerak.")

        return Response(LessonDetailSerializer(lesson).data)
