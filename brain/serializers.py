from rest_framework.serializers import ModelSerializer
from brain.models import Search


class SearchSerializer(ModelSerializer):

    class Meta:
        model = Search
        fields = ('id', 'title', 'url', 'webpages', 'created', 'updated', 'owner')
        read_only_fields = ('id', 'created', 'updated')
