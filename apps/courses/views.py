from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, PermissionDenied
from django.db.models import Q
from .models import Course, Lesson
from .serializers import (
    CourseListSerializer,
    CourseDetailSerializer,
    LessonDetailSerializer,
    LessonCRUDSerializer,
)


def can_manage_course(user, course):
    return user.is_staff or course.instructor_id == user.id


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


class LessonCRUDView(APIView):
    """Instructor/staff CRUD endpoint for creating and editing course lessons."""

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Lesson.objects.select_related("course").order_by("course_id", "order")
        if self.request.user.is_staff:
            return qs
        return qs.filter(course__instructor=self.request.user)

    def get_object(self, pk):
        try:
            lesson = Lesson.objects.select_related("course").get(pk=pk)
        except Lesson.DoesNotExist:
            raise NotFound("Dars topilmadi.")
        if not can_manage_course(self.request.user, lesson.course):
            raise PermissionDenied("Bu darsni boshqarish huquqingiz yo'q.")
        return lesson

    def get(self, request, pk=None):
        if pk is None:
            return Response(LessonCRUDSerializer(self.get_queryset(), many=True).data)
        return Response(LessonCRUDSerializer(self.get_object(pk)).data)

    def post(self, request):
        serializer = LessonCRUDSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course = serializer.validated_data["course"]
        if not can_manage_course(request.user, course):
            raise PermissionDenied("Bu kursga dars qo'shish huquqingiz yo'q.")
        lesson = serializer.save()
        return Response(LessonCRUDSerializer(lesson).data, status=201)

    def put(self, request, pk):
        return self._update(request, pk, partial=False)

    def patch(self, request, pk):
        return self._update(request, pk, partial=True)

    def _update(self, request, pk, partial):
        lesson = self.get_object(pk)
        serializer = LessonCRUDSerializer(lesson, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        course = serializer.validated_data.get("course", lesson.course)
        if not can_manage_course(request.user, course):
            raise PermissionDenied("Darsni boshqa kursga ko'chirish huquqingiz yo'q.")
        lesson = serializer.save()
        return Response(LessonCRUDSerializer(lesson).data)

    def delete(self, request, pk):
        lesson = self.get_object(pk)
        lesson.delete()
        return Response(status=204)
