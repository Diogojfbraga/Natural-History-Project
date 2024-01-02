import pycountry    # For country validation
from django import forms
from django.core.exceptions import ValidationError
from .models import Specimen, Taxonomy, Expedition

class SpecimenForm(forms.ModelForm):
    class Meta:
        model = Specimen
        fields = ['catalog_number']
        labels = {
            'catalog_number': 'Catalog Number',
        }

    # Cleans and validate the catalog_number field
    def clean_catalog_number(self):
       
        # Gets the catalog_number from the cleaned_data dictionary
        catalog_number = self.cleaned_data['catalog_number']

        # Validates catalog number format (four parts separated by dots)
        parts = catalog_number.split('.')

        if len(parts) != 4:
            # Raises a ValidationError if the format is not correct
            raise ValidationError('Invalid catalog number format. Should have 4 parts separated by dots.')

        # Defines maximum lengths for each part
        max_lengths = [4, 2, 2, 4]

        for part, max_length in zip(parts, max_lengths):
            try:
                # Checks if each part is a non-negative integer and within the specified maximum length
                value = int(part)
                if value < 0 or len(part) > max_length:
                    # Raises a ValueError if the part is not a valid integer or exceeds the maximum length
                    raise ValueError
            except ValueError:
                # Raises a ValidationError if the part is not a valid integer
                raise ValidationError(f'Invalid catalog number. Parts must be non-negative integers with a maximum length of {max_length}.')

        # Returns the cleaned catalog_number if it passes validation
        return catalog_number

# Form for Expedition model, includes expedition, continent, country, state_province, and term fields
class ExpeditionForm(forms.ModelForm):
    class Meta:
        model = Expedition
        fields = ['expedition', 'continent', 'country']

        labels = {
            'expedition': 'Expedition', 
            'continent': 'Continent', 
            'country': 'Country', 
        }

    ALLOWED_CONTINENTS = ['Africa', 'Antarctica', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']

    def clean_expedition(self):
        expedition = self.cleaned_data['expedition'].strip()

        # Check if the field is not empty
        if not expedition:
            return expedition  # No further validation needed

        # Check if "expedition" is contained anywhere in the string
        if 'expedition' not in expedition.lower():
            raise ValidationError('Invalid expedition format. Should contain "Expedition".')

        # Validate the format if "expedition" is contained in the string
        if not expedition.lower().startswith('expedition '):
            raise ValidationError('Invalid expedition format. Should start with "Expedition" followed by a space and another word.')

        return expedition

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

# Form for Taxonomy model, includes all fields
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

    # Custom validation to ensure the length of a field is at least min_length characters
    def clean_field_length(self, field_name, min_length):

        # Gets the field_value from the cleaned_data dictionary
        field_value = self.cleaned_data[field_name]
        # Gets the label for the field from the form's fields
        label = self.fields[field_name].label

        # Ensures field_value is at least min_length characters long
        if len(field_value) < min_length:
            # Raises a ValidationError if the length is less than min_length
            raise ValidationError(f'{label} must be at least {min_length} characters long.')

        # Returns the field_value if it passes validation
        return field_value

    def clean_kingdom(self):
        # Cleans and validate the 'kingdom' field length
        return self.clean_field_length('kingdom', 3)

    def clean_phylum(self):
        # Cleans and validates the 'phylum' field length
        return self.clean_field_length('phylum', 3)
    
    def clean_highest_biostratigraphic_zone(self):
        # Cleans and validates the 'highest_biostratigraphic_zone' field length
        return self.clean_field_length('highest_biostratigraphic_zone', 3)
    
    def clean_class_name(self):
        # Cleans and validates the 'class_name' field length
        return self.clean_field_length('class_name', 3)
    
    def clean_identification_description(self):
        # Cleans and validates the 'identification_description' field length
        return self.clean_field_length('identification_description', 3)
    
    def clean_family(self):
        # Cleans and validates the 'family' field length
        return self.clean_field_length('family', 3)
    
    def clean_genus(self):
        # Cleans and validates the 'genus' field length
        return self.clean_field_length('genus', 3)

    def clean_species(self):
        # Cleans and validates the 'species' field length
        return self.clean_field_length('species', 3)

# Form for new specimen view
class NewSpecimenForm(forms.ModelForm):
    class Meta:
        model = Specimen
        fields = ['catalog_number', 'expedition', 'taxonomy']
        labels = {
            'catalog_number': 'Catalog Number',
            'expedition': 'Expedition',
            'taxonomy': 'Taxonomy',
        }

    def clean(self):
        # Custom validation for the entire form

        # Gets the cleaned_data dictionary after the default cleaning
        cleaned_data = super().clean()
        # Retrieves the 'expedition' field value from the cleaned_data
        expedition = cleaned_data.get('expedition')

        # Checks if 'expedition' is not provided
        if not expedition:
            # Raises a ValidationError if 'expedition' is missing
            raise forms.ValidationError('Expedition is required.')

        # Returns the cleaned_data dictionary
        return cleaned_data

    def clean_catalog_number(self):
        # Customs validation for the 'catalog_number' field

        # Retrieves the 'catalog_number' field value from the cleaned_data
        catalog_number = self.cleaned_data['catalog_number']

        # Returns the 'catalog_number' value
        return catalog_number
    
    # Custom save method to handle additional operations before saving
    def save(self, commit=True):

        # Calls the parent class's save method with commit=False to get the unsaved instance
        instance = super().save(commit=False)

        # Ensures that the Specimen model has the `specimen_id` field set as AutoField(primary_key=True)
        # This should automatically handle incrementing the specimen_id.
        instance.specimen_id = Specimen.objects.latest('specimen_id').specimen_id + 1

        # Saves the instance if commit is True
        if commit:
            instance.save()

        # Returns the saved instance
        return instance