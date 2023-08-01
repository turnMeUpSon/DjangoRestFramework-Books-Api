from django.test import TestCase
from store.models import Book, UserBookRelation
from store.serializers import BookSerializer, UserBookRelationSerializer
from django.contrib.auth.models import User

class BookSerializerTestCase(TestCase):
    def setUp(self):
        self.book_1 = Book.objects.create(name='Test book 1', price=25, author='Author 1')
        self.book_2 = Book.objects.create(name='Test book 2', price=55, author='Author 5')
        self.book_3 = Book.objects.create(name='Test book Author 1', price=55, author='Author 2')

    def test_ok(self):
        data = BookSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        excepcted_data = [
            {
                'id': self.book_1.id,
                'name': 'Test book 1',
                'price': '25.00',
                'author': 'Author 1',
            },
            {
                'id': self.book_2.id,
                'name': 'Test book 2',
                'price': '55.00',
                'author': 'Author 5',
            },
            {
                'id': self.book_3.id,
                'name': 'Test book Author 1',
                'price': '55.00',
                'author': 'Author 2',
            }
        ]
        self.assertEqual(excepcted_data, data)


class UserBookRelationSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.book_1 = Book.objects.create(name='Test book 1', price=25, author='Author 1')
        self.relation = UserBookRelation.objects.create(user=self.user, book=self.book_1, like=True, in_bookmarks=True, rate=4)
    
    def test_ok(self):
        data = UserBookRelationSerializer(self.relation).data
        excepted_data = {
            'book': self.book_1.id,
            'like': True,
            'in_bookmarks': True,
            'rate': 4
        }
        self.assertEqual(excepted_data, data)