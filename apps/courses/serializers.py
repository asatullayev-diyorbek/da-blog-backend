from rest_framework import serializers
from apps.blog.serializers import CategorySerializer
from apps.users.serializers import UserSerializer
from .models import Course, Lesson


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "order", "title", "slug", "duration", "is_free", "video_id"]


class LessonDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "order", "title", "slug", "duration", "is_free", "video_id", "content"]


class CourseListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    instructor = UserSerializer(read_only=True)
    lessons_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = [
            "id", "title", "slug", "short_description", "cover",
            "category", "instructor", "level", "price",
            "duration", "students", "featured", "lessons_count", "created_at",
        ]


class CourseDetailSerializer(CourseListSerializer):
    lessons = LessonListSerializer(many=True, read_only=True)

    class Meta(CourseListSerializer.Meta):
        fields = CourseListSerializer.Meta.fields + ["lessons"]
