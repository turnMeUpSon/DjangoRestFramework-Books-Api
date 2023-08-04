from rest_framework.viewsets import ModelViewSet
from store.permissions import IsOwnerOrStaffOrReadOnly
from store.models import Book, UserBookRelation, User
from store.serializers import BooksSerializer, UserBookRelationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from django.shortcuts import render
from django.db.models import Count, Case, When, Avg, Max, Min, ExpressionWrapper, F, DecimalField, Prefetch

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            annotated_in_bookmarks_count=Count(Case(When(userbookrelation__in_bookmarks=True, then=1))),
            rating=Avg('userbookrelation__rate'),
            max_rating=Max('userbookrelation__rate'),
            min_rating=Min('userbookrelation__rate'),
            discounted_price=ExpressionWrapper(F('price') * (1 - F('discount') / 100), output_field=DecimalField()),
            owner_name=F('owner__username')
        ).prefetch_related(Prefetch('readers', queryset=User.objects.all().only('first_name', 'last_name'))).order_by('id')
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filter_fields = ['price']
    search_fields = ['name', 'author']
    ordering_fields = ['price', 'author']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class UserBooksRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    lookup_field = 'book'

    def get_object(self):
        obj, created = UserBookRelation.objects.get_or_create(user=self.request.user, book_id=self.kwargs['book'])
        print('created', created)
        return obj


def auth(request):
    return render(request, 'oauth.html')