from rest_framework import serializers
from apps.blog.serializers import CategorySerializer
from apps.users.serializers import UserSerializer
from .models import Course, Lesson
from apps.quizzes.serializers import QuizListSerializer


class LessonListSerializer(serializers.ModelSerializer):
    quizzes_count = serializers.IntegerField(source="quizzes.count", read_only=True)

    class Meta:
        model = Lesson
        fields = ["id", "order", "title", "slug", "duration", "is_free", "video_id", "quizzes_count"]


class LessonDetailSerializer(serializers.ModelSerializer):
    quizzes = QuizListSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ["id", "order", "title", "slug", "duration", "is_free", "video_id", "content", "quizzes"]


class LessonCRUDSerializer(serializers.ModelSerializer):
    course_id = serializers.PrimaryKeyRelatedField(
        source="course",
        queryset=Course.objects.all(),
        write_only=True,
    )
    course = serializers.IntegerField(source="course_id", read_only=True)

    class Meta:
        model = Lesson
        fields = [
            "id", "course_id", "course", "order", "title", "slug",
            "duration", "is_free", "video_id", "content", "created_at",
        ]
        read_only_fields = ["id", "course", "created_at"]

    def validate(self, attrs):
        course = attrs.get("course") or getattr(self.instance, "course", None)
        order = attrs.get("order", getattr(self.instance, "order", None))
        if course and order:
            duplicate = Lesson.objects.filter(course=course, order=order)
            if self.instance:
                duplicate = duplicate.exclude(pk=self.instance.pk)
            if duplicate.exists():
                raise serializers.ValidationError({
                    "order": "Bu kursda ushbu tartib raqami allaqachon ishlatilgan."
                })
        return attrs


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
