from rest_framework import generics

from .models import Book
from .serializers import BookSerializer


# @api_view()
# def all_books(request):
#     books = Book.objects.all()
#     # many=True indicates books is a query_set or a list of objects
#     book_serializer = BookSerializer(books, many=True)

#     return Response(book_serializer.data)

class AllBooks(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
