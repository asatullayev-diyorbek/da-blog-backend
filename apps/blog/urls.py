from django.urls import path
from .views import CategoryListView, TagListView, PostListView, PostDetailView, PostViewView, FeaturedPostView, CommentListCreateView, StatsView

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("tags/", TagListView.as_view(), name="tag-list"),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/featured/", FeaturedPostView.as_view(), name="post-featured"),
    path("posts/<slug:slug>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/<slug:slug>/view/", PostViewView.as_view(), name="post-view"),
    path("posts/<slug:slug>/comments/", CommentListCreateView.as_view(), name="post-comments"),
    path("stats/", StatsView.as_view(), name="stats"),
]
