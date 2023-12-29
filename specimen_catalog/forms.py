import pycountry    # For country validation
from django import forms
from django.core.exceptions import ValidationError
from .models import Specimen, Taxonomy, Expedition

# Form for Specimen model, includes catalog_number and created fields
class SpecimenForm(forms.ModelForm):
    class Meta:
        model = Specimen
        fields = ['catalog_number', 'created']

        labels = {
            'created': 'Specimen Number',
        }

    def clean_catalog_number(self):
        catalog_number = self.cleaned_data['catalog_number']
        # Validates catalog number format (4 digits.2 digits.2 digits)
        parts = catalog_number.split('.')

        if len(parts) != 3:
            raise ValidationError('Invalid catalog number format. Should be 4 Digits.2 Digits.2 Digits.')

        try:
            first_part, second_part, third_part = map(int, parts)
        except ValueError:
            raise ValidationError('Invalid catalog number. Parts must be integers.')

        # Validates the length of each part
        if not (len(str(first_part)) == 4 and len(str(second_part)) == 2 and len(str(third_part)) == 2):
            raise ValidationError('Invalid catalog number. Parts should have the correct length.')

        return catalog_number

    def clean_created(self):
        created = self.cleaned_data['created']

        # Validates that created is an integer
        try:
            created = int(created)
        except ValueError:
            raise forms.ValidationError('Invalid value for Specimen Number. Must be an integer.')

        # Checks if the created value is unique in the database
        if Specimen.objects.filter(created=created).exists():
            raise forms.ValidationError('Specimen with this number already exists.')

        return created

        return created

# Form for Expedition model, includes expedition, continent, country, state_province, and term fields
class ExpeditionForm(forms.ModelForm):
    class Meta:
        model = Expedition
        fields = ['expedition', 'continent', 'country', 'state_province', 'term']

        labels = {
            'expedition': 'Expedition', 
            'continent': 'Continent', 
            'country': 'Country', 
            'state_province': 'State', 
            'term': 'Term',
        }

    def clean_expedition(self):
        expedition = self.cleaned_data['expedition']
        # Example: Validates expedition format (e.g., Expedition2023-001)
        if not expedition.lower().startswith('expedition'):
            raise ValidationError('Invalid expedition format. Should start with "Expedition".')

        return expedition
       
    ALLOWED_CONTINENTS = ['Africa', 'Antarctica', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']

    def clean_continent(self):
        continent = self.cleaned_data['continent']
        # Validates that the continent is in the list of allowed continents (case-insensitive)
        if continent.title() not in self.ALLOWED_CONTINENTS:
            raise ValidationError('Invalid continent entered.')

        return continent

    def clean_country(self):
        country = self.cleaned_data['country']
        # Validates that the country is a valid country code or name
        try:
            pycountry.countries.lookup(country)
        except LookupError:
            raise ValidationError('Invalid country entered.')

        return country

    def clean_state_province(self):
        state_province = self.cleaned_data['state_province']
        # Example: Ensures state_province is not empty
        if not state_province:
            raise ValidationError('State/Province cannot be empty.')

        return state_province

    def clean_term(self):
        term = self.cleaned_data['term']
        # Example: Ensures term is not empty
        if not term:
            raise ValidationError('Term cannot be empty.')

        return term

# Form for Taxonomy model, includes various taxonomy-related fields
class TaxonomyForm(forms.ModelForm):
    class Meta:
        model = Taxonomy
        fields = ['kingdom', 'phylum', 'highest_biostratigraphic_zone', 'class_name',
                  'identification_description', 'family', 'genus', 'species']
        
        labels = {
            'kingdom': 'Kindgom',
            'phylum': 'Phylum',
            'highest_biostratigraphic_zone': 'Sub-phylum',
            'class_name' : 'Class',
            'identification_description': 'Order',
            'family': 'Family',
            'genus': 'Genus',
            'species': 'Species',
        }

class TaxonomyForm(forms.ModelForm):
    class Meta:
        model = Taxonomy
        fields = ['kingdom', 'phylum', 'highest_biostratigraphic_zone', 'class_name',
                  'identification_description', 'family', 'genus', 'species']

        labels = {
            'kingdom': 'Kingdom',
            'phylum': 'Phylum',
            'highest_biostratigraphic_zone': 'Sub-phylum',
            'class_name': 'Class',
            'identification_description': 'Order',
            'family': 'Family',
            'genus': 'Genus',
            'species': 'Species',
        }

    def clean_field_length(self, field_name, min_length):
        field_value = self.cleaned_data[field_name]
        label = self.fields[field_name].label
        # Ensures field_value is at least min_length characters long
        if len(field_value) < min_length:
            raise ValidationError(f'{label} must be at least {min_length} characters long.')

        return field_value

    def clean_kingdom(self):
        return self.clean_field_length('kingdom', 3)

    def clean_phylum(self):
        return self.clean_field_length('phylum', 3)
    
    def clean_highest_biostratigraphic_zone(self):
        return self.clean_field_length('highest_biostratigraphic_zone', 3)
    
    def clean_class_name(self):
        return self.clean_field_length('class_name', 3)
    
    def clean_identification_description(self):
        return self.clean_field_length('identification_description', 3)
    
    def clean_family(self):
        return self.clean_field_length('family', 3)
    
    def clean_genus(self):
        return self.clean_field_length('genus', 3)

    def clean_species(self):
        return self.clean_field_length('species', 3)


# Form for creating a new Specimen, includes catalog_number, created, expedition, and taxonomy fields
class NewSpecimenForm(forms.ModelForm):
    class Meta:
        model = Specimen
        fields = ['catalog_number', 'created', 'expedition', 'taxonomy']

        labels = {
            'catalog_number': 'Catalog Number',
            'created': 'Specimen Creator',
            'expedition': 'Expedition',
            'taxonomy': 'Taxonomy',
        }

    def clean_catalog_number(self):
        catalog_number = self.cleaned_data['catalog_number']
        # Validates catalog number format (4 digits.2 digits.2 digits)
        parts = catalog_number.split('.')

        if len(parts) != 3:
            raise ValidationError('Invalid catalog number format. Should be 4 Digits.2 Digits.2 Digits.')

        try:
            first_part, second_part, third_part = map(int, parts)
        except ValueError:
            raise ValidationError('Invalid catalog number. Parts must be integers.')

        # Validate the length of each part
        if not (len(str(first_part)) == 4 and len(str(second_part)) == 2 and len(str(third_part)) == 2):
            raise ValidationError('Invalid catalog number. Parts should have the correct length.')

        return catalog_number

    def clean_created(self):
        created = self.cleaned_data['created']
        # Example: Validates that created is an integer
        try:
            created = int(created)
        except ValueError:
            raise ValidationError('Invalid value for Specimen Number. Must be an integer.')

        return created