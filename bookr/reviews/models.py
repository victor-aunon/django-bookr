from django.db import models
from django.contrib import auth


class Publisher(models.Model):
    """A company that publishes books."""

    name = models.CharField(max_length=50, help_text="The name of the publisher")
    website = models.URLField(help_text="The publisher's website")
    email = models.EmailField(help_text="The publisher's email address")

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    """A published book."""

    title = models.CharField(max_length=100, help_text="The title of the book")
    publication_date = models.DateField(verbose_name="Date the book was published")
    isbn = models.CharField(max_length=20, verbose_name="ISBN number of the book")
    # Many to one relationship (Publisher has many books)
    # CASCADE: delete the publisher's books if the publisher is deleted
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    # Many to many relationship (A book can have many contributors
    # and a contributor many books)
    contributors = models.ManyToManyField("Contributor", through="BookContributor")

    def __str__(self) -> str:
        return self.title


class Contributor(models.Model):
    """A contributor to a book (author, editor, co-author)"""

    first_name = models.CharField(
        max_length=50, help_text="The contributor's first name"
    )
    last_name = models.CharField(max_length=50, help_text="The contributor's last name")
    email = models.EmailField(help_text="The contributor's email contact")

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class BookContributor(models.Model):
    class ContributionRole(models.TextChoices):
        AUTHOR = "AUTHOR", "Author"
        CO_AUTHOR = "CO_AUTHOR", "Co-author"
        EDITOR = "EDITOR", "Editor"

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    role = models.CharField(
        verbose_name="The role this contributor had in the book",
        choices=ContributionRole.choices,
        max_length=20,
    )


class Review(models.Model):
    content = models.TextField(help_text="The review text")
    rating = models.IntegerField(help_text="The rating the reviewer has given")
    date_created = models.DateTimeField(
        auto_now_add=True, help_text="The date and time the review was created"
    )
    date_edited = models.DateTimeField(
        auto_now_add=True, help_text="The date and time the review was edited"
    )
    creator = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, help_text="The book that this is review is for"
    )
