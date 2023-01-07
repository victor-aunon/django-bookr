from django.contrib import admin

from reviews.models import Publisher, Contributor, Book, BookContributor, Review

# Register models
admin.site.register(Publisher)
admin.site.register(Contributor)
admin.site.register(Book)
admin.site.register(BookContributor)
admin.site.register(Review)
