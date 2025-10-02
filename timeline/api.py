from rest_framework import serializers, viewsets

from .models import Influence, TimelineEvent


class TimelineEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineEvent
        fields = ["id", "title", "year", "category", "description"]


class TimelineEventViewSet(viewsets.ModelViewSet):
    queryset = TimelineEvent.objects.all()
    serializer_class = TimelineEventSerializer


class InfluenceSerializer(serializers.ModelSerializer):
    influencer = serializers.StringRelatedField()
    influenced = serializers.StringRelatedField()

    class Meta:
        model = Influence
        fields = ["id", "title", "year", "category", "description", "figure"]


class InfluenceViewSet(viewsets.ModelViewSet):
    queryset = Influence.objects.all()
    serializer_class = InfluenceSerializer
