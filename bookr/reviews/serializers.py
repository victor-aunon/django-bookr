from rest_framework import serializers

from .models import Book, Publisher, BookContributor, Contributor


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer()

    class Meta:
        model = Book
        fields = ["title", "publication_date", "isbn", "publisher"]


class ContributionSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = BookContributor
        fields = ["book", "role"]


class ContributorSerializer(serializers.ModelSerializer):
    bookcontributor_set = ContributionSerializer(read_only=True, many=True)
    # ReadOnlyField since this value is updated by adding books to the Contributor
    number_contributions = serializers.ReadOnlyField()

    class Meta:
        model = Contributor
        fields = [
            "first_name",
            "last_name",
            "email",
            "bookcontributor_set",
            "number_contributions",
        ]
