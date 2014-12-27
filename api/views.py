import rest_framework.permissions
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from brain.models import Search
from brain.serializers import SearchSerializer
# Create your views here.


class SearchViewSet(ModelViewSet):
    queryset = Search.objects.all()
    serializer_class = SearchSerializer
    # permission_classes = (,)  # add later
    permission_classes = (rest_framework.permissions.AllowAny,)
    filter_backends = (filters.OrderingFilter,)
