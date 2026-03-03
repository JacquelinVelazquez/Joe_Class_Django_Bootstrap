from django.urls import path
from . import views

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="all_articles"),
    path("new/", views.NewArticleForm.as_view(), name="new_article"),
    path("article/<int:pk>/", views.ArticleDetailView.as_view(), name="article_detail"),
    path("article/<int:pk>/edit/", views.EditArticleForm.as_view(), name="edit_article"),
]