from django.contrib import admin
from store.models import Book
from django.contrib.admin import ModelAdmin


@admin.register(Book)
class BookAdmin(ModelAdmin):
    pass