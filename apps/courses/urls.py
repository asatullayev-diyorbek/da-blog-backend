from django.urls import path
from .views import CourseListView, CourseDetailView, LessonDetailView

urlpatterns = [
    path("", CourseListView.as_view(), name="course-list"),
    path("<slug:slug>/", CourseDetailView.as_view(), name="course-detail"),
    path("<slug:course_slug>/lessons/<slug:lesson_slug>/", LessonDetailView.as_view(), name="lesson-detail"),
]
