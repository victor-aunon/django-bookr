from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Book, Contributor, Publisher, Review
from .utils import average_rating
from .forms import SearchForm, PublisherForm, ReviewForm


# Validators
def is_staff_user(user):
    return user.is_staff


def index(request):
    return render(request, "base.html")


def book_search(request):
    search_text = request.GET.get("search", "")
    search_history = request.session.get("search_history", [])
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
        if request.user.is_authenticated:
            search_history.append([search_in, search])
            request.session["search_history"] = search_history
    # In case there is no data in the form and there is history, select the
    # previously selected option (title or contributor)
    elif search_history:
        initial = {"search": search_text, "search_in": search_history[-1][0]}
        form = SearchForm(initial=initial)

    return render(
        request,
        "search_results.html",
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

    if request.user.is_authenticated:
        max_viewed_books_length = 10
        viewed_books = request.session.get("viewed_books", [])
        viewed_book = [book.id, book.title]
        # Remove the book if it is already in viewed_books list
        if viewed_book in viewed_books:
            viewed_books.pop(viewed_books.index(viewed_book))
        # Add the book to the beginning of viewed_books list
        viewed_books.insert(0, viewed_book)
        # Select the last 10 books viewed
        viewed_books = viewed_books[:max_viewed_books_length]
        request.session["viewed_books"] = viewed_books

    return render(request, "reviews/book_details.html", context)


# @permission_required("edit_publisher")
@user_passes_test(is_staff_user)
def publisher_edit(request, id=None):
    if id is not None:
        publisher = get_object_or_404(Publisher, id=id)
    else:
        publisher = None

    if request.method == "POST":
        form = PublisherForm(request.POST, instance=publisher)

        if form.is_valid():
            updated_publisher = form.save()
            if publisher is None:
                messages.success(request, f"Publisher {updated_publisher} was created.")
            else:
                messages.success(request, f"Publisher {updated_publisher} was updated.")

            return redirect("publisher_edit", updated_publisher.id)
    else:
        form = PublisherForm(instance=publisher)

    return render(
        request,
        "instance_form.html",
        {
            "method": request.method,
            "form": form,
            "instance": publisher,
            "model_type": "Publisher",
        },
    )


@login_required
def review_edit(request, book_id, review_id=None):
    book = get_object_or_404(Book, id=book_id)

    if review_id is not None:
        review = get_object_or_404(Review, id=review_id, book_id=book_id)
        user = request.user
        if not user.is_staff and review.creator.id != user.id:
            raise PermissionDenied
    else:
        review = None

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)

        if form.is_valid():
            # commit = False since we need to add some extra fields here
            updated_review = form.save(False)
            updated_review.book = book

            if review is None:
                messages.success(request, f"Review for {book} was created.")
            else:
                updated_review.date_edited = timezone.now()
                messages.success(request, f"Review for {book} was updated.")

            updated_review.save()

            return redirect("book_details", book.id)
    else:
        form = ReviewForm(instance=review)

    return render(
        request,
        "instance_form.html",
        {
            "form": form,
            "instance": review,
            "model_type": "Review",
            "related_instance": book,
            "related_model_type": "Book",
        },
    )
