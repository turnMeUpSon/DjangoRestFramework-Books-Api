from django.test import TestCase
from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer, UserBookRelationSerializer
from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg, Max, Min, ExpressionWrapper, F, DecimalField

class BookSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(username='user1',
                                    first_name='Ivan', last_name='Petrov')
        user2 = User.objects.create(username='user2',
                                    first_name='Ivan', last_name='Sidorov')
        user3 = User.objects.create(username='user3',
                                    first_name='1', last_name='2')

        book_1 = Book.objects.create(name='Test book 1', price=25, discount=10,
                                     author='Author 1', owner=user1)
        book_2 = Book.objects.create(name='Test book 2', price=55, discount=5,
                                     author='Author 2')

        UserBookRelation.objects.create(user=user1, book=book_1, like=True, in_bookmarks=True,
                                        rate=5)
        UserBookRelation.objects.create(user=user2, book=book_1, like=True, in_bookmarks=True,
                                        rate=5)
        UserBookRelation.objects.create(user=user3, book=book_1, like=True, in_bookmarks=True,
                                        rate=4)

        UserBookRelation.objects.create(user=user1, book=book_2, like=True, in_bookmarks=True,
                                        rate=3)
        UserBookRelation.objects.create(user=user2, book=book_2, like=True, in_bookmarks=True,
                                        rate=4)
        UserBookRelation.objects.create(user=user3, book=book_2, like=False)

        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            annotated_in_bookmarks_count=Count(Case(When(userbookrelation__in_bookmarks=True, then=1))),
            rating=Avg('userbookrelation__rate'),
            max_rating=Max('userbookrelation__rate'),
            min_rating=Min('userbookrelation__rate'),
            discounted_price=ExpressionWrapper(F('price') * (1 - F('discount') / 100), output_field=DecimalField()),
            owner_name=F('owner__username')
        ).order_by('id')
        data = BooksSerializer(books, many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test book 1',
                'price': '25.00',
                'discount': '10.00',
                'discounted_price': '22.50',
                'author': 'Author 1',
                'annotated_likes': 3,
                'annotated_in_bookmarks_count': 3,
                'rating': '4.67',
                'max_rating': '5.00',
                'min_rating': '4.00',
                'owner_name': 'user1',
                'readers': [
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Petrov'
                    },
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Sidorov'
                    },
                    {
                        'first_name': '1',
                        'last_name': '2'
                    },
                ]
            },
            {
                'id': book_2.id,
                'name': 'Test book 2',
                'price': '55.00',
                'discount': '5.00',
                'discounted_price': '52.25',
                'author': 'Author 2',
                'annotated_likes': 2,
                'annotated_in_bookmarks_count': 2,
                'rating': '3.50',
                'max_rating': '4.00',
                'min_rating': '3.00',
                'owner_name': None,
                'readers': [
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Petrov'
                    },
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Sidorov'
                    },
                    {
                        'first_name': '1',
                        'last_name': '2'
                    },
                ]
            },
        ]
        self.assertEqual(expected_data, data)

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