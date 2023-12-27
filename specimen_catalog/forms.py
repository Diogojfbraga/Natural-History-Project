from django import forms
from .models import Specimen, Taxonomy, Expedition

# Form for Specimen model, includes catalog_number and created fields
class SpecimenForm(forms.ModelForm):
    class Meta:
        model = Specimen
        fields = ['catalog_number', 'created']

        labels = {
            'created': 'Specimen Number',
        }

# Form for Expedition model, includes expedition, continent, country, state_province, and term fields
class ExpeditionForm(forms.ModelForm):
    class Meta:
        model = Expedition
        fields = ['expedition', 'continent', 'country', 'state_province', 'term']

# Form for Taxonomy model, includes various taxonomy-related fields
class TaxonomyForm(forms.ModelForm):
    class Meta:
        model = Taxonomy
        fields = ['kingdom', 'phylum', 'highest_biostratigraphic_zone', 'class_name',
                  'identification_description', 'family', 'genus', 'species']
        
        labels = {
            'highest_biostratigraphic_zone': 'Sub-phylum',
            'class_name' : 'Class',
            'identification_description': 'Order',
        }

# Form for creating a new Specimen, includes catalog_number, created, expedition, and taxonomy fields
class NewSpecimenForm(forms.ModelForm):
    class Meta:
        model = Specimen
        fields = ['catalog_number', 'created', 'expedition', 'taxonomy']

        labels = {
            'created': 'Specimen Number',
        }