# Imports the models 
from django.contrib import admin
from .models import Expedition, Taxonomy, Specimen

# Register the Expedition model with the Django Admin interface
@admin.register(Expedition)
class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ('expedition_id', 'expedition', 'continent', 'country')
    
# Register the Taxonomy model with the Django Admin interface
@admin.register(Taxonomy)
class TaxonomyAdmin(admin.ModelAdmin):
    list_display = ('taxonomy_id', 'kingdom', 'phylum','highest_biostratigraphic_zone', 
                    'class_name', 'family', 'genus', 'species')

# Register the Specimen model with the Django Admin interface
@admin.register(Specimen)
class SpecimenAdmin(admin.ModelAdmin):
    list_display = ('specimen_id', 'catalog_number', 'taxonomy', 'expedition')
