from django.contrib.admin import AdminSite


class BookrAdminSite(AdminSite):
    site_header = "Bookr administration"
    site_title = "Bookr administration"
    index_title = "Bookr site admin"
