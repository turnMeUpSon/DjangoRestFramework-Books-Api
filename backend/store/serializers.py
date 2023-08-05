from rest_framework.serializers import ModelSerializer
from store.models import Book, UserBookRelation
from rest_framework import serializers
from django.contrib.auth.models import User

class BookReaderSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class BooksSerializer(ModelSerializer):
    discounted_price = serializers.DecimalField(max_digits=7, decimal_places=2, read_only=True)
    annotated_likes = serializers.IntegerField(read_only=True)
    annotated_in_bookmarks_count = serializers.IntegerField(read_only=True)
    mark = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    max_rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    min_rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    owner_name = serializers.CharField(read_only=True)
    readers = BookReaderSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'discount', 'discounted_price', 'author', 'annotated_likes', 
                'annotated_in_bookmarks_count', 'mark', 'max_rating', 'min_rating', 'owner_name', 'readers')
    
    
class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmarks', 'rate')