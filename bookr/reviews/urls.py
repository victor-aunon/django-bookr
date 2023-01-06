from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("book-search/", views.book_search),
    path("books/", views.book_list, name="book_list"),
    path("books/<int:id>/", views.book_details, name="book_details")
]
