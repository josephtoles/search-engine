from rest_framework.serializers import ModelSerializer
import rest_framework.serializers
from brain.models import Search


class SearchSerializer(ModelSerializer):
    owner = rest_framework.serializers.ReadOnlyField()

    class Meta:
        model = Search
        fields = ('id', 'title', 'url', 'webpages', 'created', 'updated', 'owner')
        read_only_fields = ('id', 'created', 'updated')
