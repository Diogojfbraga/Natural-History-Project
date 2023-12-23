# specimen_catalog/forms.py
import django_filters
from django import forms
from .models import Specimen, Taxonomy, Expedition

class SpecimenForm(forms.ModelForm):
    class Meta:
        model = Specimen
        fields = ['catalog_number', 'created']

class ExpeditionForm(forms.ModelForm):
    class Meta:
        model = Expedition
        fields = ['expedition', 'continent', 'country', 'state_province', 'term']

class TaxonomyForm(forms.ModelForm):
    class Meta:
        model = Taxonomy
        fields = ['kingdom', 'phylum', 'highest_biostratigraphic_zone', 'class_name','identification_description', 'family', 'genus', 'species']

class NewSpecimenForm(forms.ModelForm):
    class Meta:
        model = Specimen
        fields = ['catalog_number', 'created', 'expedition', 'taxonomy']