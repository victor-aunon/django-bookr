from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views, api_views


router = DefaultRouter()
router.register("books", api_views.BookViewSet)
router.register("reviews", api_views.ReviewViewSet)

urlpatterns = [
    path("", views.index),
    path("book-search/", views.book_search, name="book_search"),
    path("books/", views.book_list, name="book_list"),
    path("books/<int:id>/", views.book_details, name="book_details"),
    path("publishers/<int:id>/", views.publisher_edit, name="publisher_edit"),
    path("publishers/new/", views.publisher_edit, name="publisher_create"),
    path(
        "books/<int:book_id>/reviews/<int:review_id>/",
        views.review_edit,
        name="review_edit",
    ),
    path("books/<int:book_id>/reviews/new/", views.review_edit, name="review_create"),
    # path("api/all_books", api_views.all_books, name="all_books"),
    # path("api/all_books", api_views.AllBooks.as_view(), name="all_books"),
    # path(
    #     "api/all_contributors",
    #     api_views.AllContributors.as_view(),
    #     name="all_contributors",
    # ),
    path("api/", include((router.urls, "api"))),
    path("api/login", api_views.Login.as_view(), name="login")
]
