from rest_framework.test import APITestCase
from django.urls import reverse
from store.serializers import BooksSerializer, UserBookRelation
from store.models import Book
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
import json
from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg, Max, Min, ExpressionWrapper, F, DecimalField
from django.test.utils import CaptureQueriesContext
from django.db import connection

class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.book_1 = Book.objects.create(name='Test book 1', price=25, discount=10,
                                          author='Author 1',
                                          owner=self.user)
        self.book_2 = Book.objects.create(name='Test book 2', price=55, discount=5,
                                          author='Author 5')
        self.book_3 = Book.objects.create(name='Test book Author 1', price=55, discount=0,
                                          author='Author 2')
        UserBookRelation.objects.create(user=self.user, book=self.book_1, like=True, in_bookmarks=True,
                                        rate=5)

    def test_get(self):
        url = reverse('book-list')
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            print('queries', len(queries))
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            annotated_in_bookmarks_count=Count(Case(When(userbookrelation__in_bookmarks=True, then=1))),
            mark=Avg('userbookrelation__rate'),
            max_rating=Max('userbookrelation__rate'),
            min_rating=Min('userbookrelation__rate'),
            discounted_price=ExpressionWrapper(F('price') * (1 - F('discount') / 100), output_field=DecimalField()),
            owner_name=F('owner__username')
        ).order_by('id')
        serializer_data = BooksSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(serializer_data[0]['mark'], '5.00')
        self.assertEqual(serializer_data[0]['annotated_likes'], 1)
        self.assertEqual(serializer_data[0]['annotated_in_bookmarks_count'], 1)
        self.assertEqual(serializer_data[0]['discounted_price'], '22.50')
        self.assertEqual(serializer_data[0]['owner_name'], 'test_username')
    
    def test_get_filter(self):
        url = reverse('book-list')
        books = Book.objects.filter(id__in=[self.book_2.id, self.book_3.id]).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            annotated_in_bookmarks_count=Count(Case(When(userbookrelation__in_bookmarks=True, then=1))),
            mark=Avg('userbookrelation__rate'),
            max_rating=Max('userbookrelation__rate'),
            min_rating=Min('userbookrelation__rate'),
            discounted_price=ExpressionWrapper(F('price') * (1 - F('discount') / 100), output_field=DecimalField()),
            owner_name=F('owner__username')
        ).order_by('id')
        response = self.client.get(url, data={'price': 55})
        serializer_data = BooksSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
    
    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'Author 1'})
        books = Book.objects.filter(id__in=[self.book_1.id, self.book_3.id]).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            annotated_in_bookmarks_count=Count(Case(When(userbookrelation__in_bookmarks=True, then=1))),
            mark=Avg('userbookrelation__rate'),
            max_rating=Max('userbookrelation__rate'),
            min_rating=Min('userbookrelation__rate'),
            discounted_price=ExpressionWrapper(F('price') * (1 - F('discount') / 100), output_field=DecimalField()),
            owner_name=F('owner__username')
        ).order_by('id')
        serializer_data = BooksSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
    
    def test_create(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-list')
        data = {
            "name": "Programming in Python3",
            "price": 150,
            "author": "Mark Summerfield"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.all().count())
        self.assertEqual(self.user, Book.objects.last().owner) 
    
    def test_update(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 575,
            "author": self.book_1.author
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(575, self.book_1.price)
    
    def test_update_not_owner(self):
        self.user2 = User.objects.create(username='test_username2',)
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 575,
            "author": self.book_1.author
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')})
        self.book_1.refresh_from_db()
        self.assertEqual(25, self.book_1.price)
    
    def test_update_not_owner_but_staff(self):
        self.user2 = User.objects.create(username='test_username2', is_staff=True)
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 575,
            "author": self.book_1.author
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(575, self.book_1.price)
    
    def test_delete(self):
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 575,
            "author": self.book_1.author
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.delete(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Book.objects.all().count())
    
    def test_delete_not_owner(self):
        self.user3 = User.objects.create(username='test_username3')
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 575,
            "author": self.book_1.author
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user3)
        response = self.client.delete(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')})
        self.assertEqual(3, Book.objects.all().count())
    
    def test_delete_not_owner_but_staff(self):
        self.user3 = User.objects.create(username='test_username3', is_staff=True)
        self.assertEqual(3, Book.objects.all().count())
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 575,
            "author": self.book_1.author
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user3)
        response = self.client.delete(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Book.objects.all().count())


class BooksRelationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.user2 = User.objects.create(username='test_username2')
        self.book_1 = Book.objects.create(name='Test book 1', price=25, author='Author 1', owner=self.user)
        self.book_2 = Book.objects.create(name='Test book 2', price=55, author='Author 5')
    
    def test_like(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        data = {
            "like": True,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertTrue(relation.like)

        data = {
            "in_bookmarks": True,
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertTrue(relation.in_bookmarks)
    
    def test_rate(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        data = {
            "rate": 3,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertEqual(3, relation.rate)
    
    def test_rate_wrong(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        data = {
            "rate": 6,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code, response.data)