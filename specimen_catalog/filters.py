import django_filters
from .models import Specimen

# Filter specimens table by the following
class SpecimenFilter(django_filters.FilterSet):
    taxonomy__kingdom = django_filters.CharFilter(label="Kingdom", lookup_expr="icontains")
    taxonomy__phylum = django_filters.CharFilter(label="Phylum", lookup_expr="icontains")
    taxonomy__highest_biostratigraphic_zone = django_filters.CharFilter(label="Sub-Phylum", lookup_expr="icontains")
    taxonomy__class_name = django_filters.CharFilter(label="Class", lookup_expr="icontains")
    taxonomy__family = django_filters.CharFilter(label="Family", lookup_expr="icontains")
    taxonomy__genus = django_filters.CharFilter(label="Genus", lookup_expr="icontains")
    taxonomy__species = django_filters.CharFilter(label="Species", lookup_expr="icontains")

    class Meta:
        model = Specimen
        fields = ['taxonomy__kingdom', 
                  'taxonomy__phylum', 
                  'taxonomy__highest_biostratigraphic_zone', 
                  'taxonomy__class_name', 
                  'taxonomy__family', 
                  'taxonomy__genus', 
                  'taxonomy__species'
                  ]