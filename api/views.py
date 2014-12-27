import rest_framework.permissions
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from brain.models import Search
from brain.serializers import SearchSerializer
import rest_framework.permissions


class SearchViewSet(ModelViewSet):
    queryset = Search.objects.all()
    serializer_class = SearchSerializer
    # permission_classes = (,)  # add later
    permission_classes = (rest_framework.permissions.AllowAny,)
    filter_backends = (filters.OrderingFilter,)

    def pre_save(self, obj):
        print 'pre-saving'
        if obj:
            print 'there is an object'
            obj.creator = self.request.user
