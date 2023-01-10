from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer


@api_view()
def all_books(request):
    books = Book.objects.all()
    # many=True indicates books is a query_set or a list of objects
    book_serializer = BookSerializer(books, many=True)

    return Response(book_serializer.data)
