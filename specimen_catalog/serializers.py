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

    def create(self, validated_data):
        expedition_data = validated_data.pop('expedition', None)
        taxonomy_data = validated_data.pop('taxonomy', None)

        specimen = Specimen.objects.create(**validated_data)

        if expedition_data:
            Expedition.objects.create(specimen=specimen, **expedition_data)

        if taxonomy_data:
            Taxonomy.objects.create(specimen=specimen, **taxonomy_data)

        return specimen