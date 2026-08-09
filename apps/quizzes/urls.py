from django.urls import path

from .views import ArenaCreateView, ArenaDetailView, ArenaGameView, ArenaJoinView, ArenaQuestionPoolView, ArenaStartView, ClaimGuestAttemptsView, GamificationMeView, LeaderboardView, MyAttemptsView, QuizAttemptView, QuizDetailView, QuizListView, QuizStartView, QuizSubmitView

urlpatterns = [
    path("", QuizListView.as_view(), name="quiz-list"),
    path("attempts/claim/", ClaimGuestAttemptsView.as_view(), name="quiz-attempts-claim"),
    path("my-attempts/", MyAttemptsView.as_view(), name="my-attempts"),
    path("gamification/me/", GamificationMeView.as_view(), name="gamification-me"),
    path("leaderboard/", LeaderboardView.as_view(), name="leaderboard"),
    path("arena/questions/", ArenaQuestionPoolView.as_view(), name="arena-question-pool"),
    path("arena/create/", ArenaCreateView.as_view(), name="arena-create"),
    path("arena/<str:code>/", ArenaDetailView.as_view(), name="arena-detail"),
    path("arena/<str:code>/join/", ArenaJoinView.as_view(), name="arena-join"),
    path("arena/<str:code>/start/", ArenaStartView.as_view(), name="arena-start"),
    path("arena/<str:code>/play/", ArenaGameView.as_view(), name="arena-play"),
    path("<slug:slug>/start/", QuizStartView.as_view(), name="quiz-start"),
    path("<slug:slug>/", QuizDetailView.as_view(), name="quiz-detail"),
    path("attempts/<uuid:attempt_id>/submit/", QuizSubmitView.as_view(), name="quiz-submit"),
    path("attempts/<uuid:attempt_id>/", QuizAttemptView.as_view(), name="quiz-attempt"),
]
