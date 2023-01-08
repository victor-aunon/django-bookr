from django.shortcuts import render, get_object_or_404

from .models import Book, Contributor
from .utils import average_rating
from .forms import SearchForm


def index(request):
    return render(request, "base.html")


def book_search(request):
    search_text = request.GET.get("search", "")
    form = SearchForm(request.GET)
    books = set()
    if form.is_valid():
        search = form.cleaned_data["search"]
        search_in = form.cleaned_data.get("search_in") or "title"
        if search_in == "title":
            books = Book.objects.filter(title__contains=search)
        else:
            # Contributor query combination
            contributors = Contributor.objects.filter(
                first_name__contains=search
            ) | Contributor.objects.filter(last_name__contains=search)
            for contributor in contributors:
                for book in contributor.book_set.all():
                    books.add(book)
    return render(
        request,
        "search-results.html",
        {"search_text": search_text, "form": form, "books": books},
    )


def book_list(request):
    books = Book.objects.all()
    book_list = []
    for book in books:
        reviews = book.review_set.all()
        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0
        book_list.append(
            {
                "book": book,
                "book_rating": book_rating,
                "number_of_reviews": number_of_reviews,
            }
        )
    context = {"book_list": book_list}

    return render(request, "reviews/books_list.html", context)


def book_details(request, id):
    book = get_object_or_404(Book, id=id)
    reviews = book.review_set.all()
    if reviews:
        book_rating = average_rating([review.rating for review in reviews])
        context = {"book": book, "book_rating": book_rating, "reviews": reviews}
    else:
        context = {"book": book, "book_rating": None, "reviews": None}

    return render(request, "reviews/book_details.html", context)
