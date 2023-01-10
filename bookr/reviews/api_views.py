from rest_framework import viewsets
# from rest_framework.pagination import LimitOffsetPagination

from .models import Book, Review
from .serializers import BookSerializer, ReviewSerializer


# @api_view()
# def all_books(request):
#     books = Book.objects.all()
#     # many=True indicates books is a query_set or a list of objects
#     book_serializer = BookSerializer(books, many=True)

#     return Response(book_serializer.data)

# ReadOnlyModelViewSet ensures that the view is used for the GET operation only
class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.order_by("-date_created")
    serializer_class = ReviewSerializer
