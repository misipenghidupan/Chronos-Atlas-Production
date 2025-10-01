from rest_framework import serializers, viewsets

from .models import Field, Figure


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ["id", "name"]


class FigureSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True, read_only=True)

    class Meta:
        model = Figure
        fields = [
            "id",
            "name",
            "slug",
            "wikidata_id",
            "summary",
            "birth_date",
            "death_date",
            "normalized_birth_year",
            "normalized_death_year",
            "instance_of_QIDs",
            "fields",
        ]


class FigureViewSet(viewsets.ModelViewSet):
    queryset = Figure.objects.all()
    serializer_class = FigureSerializer
