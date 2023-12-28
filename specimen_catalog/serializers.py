# serializers.py
from rest_framework import serializers
from .models import Expedition, Taxonomy, Specimen

class ExpeditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expedition
        fields = '__all__'

class TaxonomySerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxonomy
        fields = '__all__'

class SpecimenSerializer(serializers.ModelSerializer):
    expedition = ExpeditionSerializer()
    taxonomy = TaxonomySerializer()

    class Meta:
        model = Specimen
        fields = '__all__'
