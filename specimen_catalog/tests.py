from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Expedition, Taxonomy, Specimen
from django.urls import reverse, resolve
from .views import index, AllSpecimensView, SpecimenUpdateView, SpecimenDetailView, ExpeditionUpdateView, TaxonomyUpdateView, SpecimenDeleteView, NewSpecimenView, NewTaxonomyView, NewExpeditionView
from .serializers import ExpeditionSerializer, TaxonomySerializer, SpecimenSerializer
from .filters import SpecimenFilter
from .forms import SpecimenForm


#Testing the models
# Expedition
class ExpeditionModelTest(TestCase):
    def setUp(self):
        # Set up data for the tests
        self.expedition_data = {
            'expedition': 'Test Expedition',
            'continent': 'Test Continent',
            'country': 'Test Country',
        }

    def test_expedition_creation(self):
        # Test if an Expedition instance is created correctly
        expedition = Expedition.objects.create(**self.expedition_data)

        self.assertEqual(expedition.expedition, 'Test Expedition')
        self.assertEqual(expedition.continent, 'Test Continent')
        self.assertEqual(expedition.country, 'Test Country')

    def test_expedition_str_method(self):
        # Test the __str__ method of the Expedition model
        expedition = Expedition.objects.create(**self.expedition_data)

        self.assertEqual(str(expedition), 'Test Expedition')

class TaxonomyModelTest(TestCase):
    def setUp(self):
        # Set up data for the tests
        self.taxonomy_data = {
            'kingdom': 'Test Kingdom',
            'phylum': 'Test Phylum',
            'highest_biostratigraphic_zone': 'Test Zone',
            'class_name': 'Test Class',
            'identification_description': 'Test Description',
            'family': 'Test Family',
            'genus': 'Test Genus',
            'species': 'Test Species',
        }

    def test_taxonomy_creation(self):
        # Test if a Taxonomy instance is created correctly
        taxonomy = Taxonomy.objects.create(**self.taxonomy_data)

        self.assertEqual(taxonomy.kingdom, 'Test Kingdom')
        self.assertEqual(taxonomy.phylum, 'Test Phylum')
        self.assertEqual(taxonomy.highest_biostratigraphic_zone, 'Test Zone')
        self.assertEqual(taxonomy.class_name, 'Test Class')
        self.assertEqual(taxonomy.identification_description, 'Test Description')
        self.assertEqual(taxonomy.family, 'Test Family')
        self.assertEqual(taxonomy.genus, 'Test Genus')
        self.assertEqual(taxonomy.species, 'Test Species')

    def test_taxonomy_str_method(self):
        # Test the __str__ method of the Taxonomy model
        taxonomy = Taxonomy.objects.create(**self.taxonomy_data)

        expected_str = (
            "(Test Kingdom/"
            "Test Phylum/"
            "Test Zone/"
            "Test Class/"
            "Test Description/"
            "Test Family/"
            "Test Genus/"
            "Test Species)"
        )

        self.assertEqual(str(taxonomy), expected_str)

#Specimen
class SpecimenModelTest(TestCase):
    def setUp(self):
        # Set up data for the tests
        self.expedition_data = {
            'expedition': 'Test Expedition',
            'continent': 'Test Continent',
            'country': 'Test Country',
        }

        self.taxonomy_data = {
            'kingdom': 'Test Kingdom',
            'phylum': 'Test Phylum',
            'highest_biostratigraphic_zone': 'Test Zone',
            'class_name': 'Test Class',
            'identification_description': 'Test Description',
            'family': 'Test Family',
            'genus': 'Test Genus',
            'species': 'Test Species',
        }

        self.specimen_data = {
            'catalog_number': 'Test Catalog Number',
        }

    def test_specimen_creation(self):
        # Test if a Specimen instance is created correctly
        expedition = Expedition.objects.create(**self.expedition_data)
        taxonomy = Taxonomy.objects.create(**self.taxonomy_data)

        specimen = Specimen.objects.create(
            catalog_number=self.specimen_data['catalog_number'],
            expedition=expedition,
            taxonomy=taxonomy,
        )

        self.assertEqual(specimen.catalog_number, 'Test Catalog Number')
        self.assertEqual(specimen.expedition, expedition)
        self.assertEqual(specimen.taxonomy, taxonomy)

    def test_specimen_str_method(self):
        # Test the __str__ method of the Specimen model
        expedition = Expedition.objects.create(**self.expedition_data)
        taxonomy = Taxonomy.objects.create(**self.taxonomy_data)

        specimen = Specimen.objects.create(
            catalog_number=self.specimen_data['catalog_number'],
            expedition=expedition,
            taxonomy=taxonomy,
        )

        expected_str = f"Specimen {specimen.specimen_id}"

        self.assertEqual(str(specimen), expected_str)


#Testing all the urls
class TestUrls(TestCase):
    def test_url_mapping(self):
        # Test the URL mapping for the 'all_specimens' view
        url = reverse('all_specimens')
        self.assertEqual(url, '/all_specimens/')
        resolver = resolve('/all_specimens/')
        self.assertEqual(resolver.func.view_class, AllSpecimensView)

        # Test the URL mapping for the 'specimen_detail' view with a sample specimen ID
        url = reverse('specimen_detail', args=[1])
        self.assertEqual(url, '/specimen/detail/1/')
        resolver = resolve('/specimen/detail/1/')
        self.assertEqual(resolver.func.view_class, SpecimenDetailView)

        # Test the URL mapping for the 'expedition_update' view with a sample expedition ID
        url = reverse('expedition_update', args=[1])
        self.assertEqual(url, '/expedition_update/1/')
        resolver = resolve('/expedition_update/1/')
        self.assertEqual(resolver.func.view_class, ExpeditionUpdateView)

        # Test the URL mapping for the 'taxonomy_update' view with a sample specimen ID
        url = reverse('taxonomy_update', args=[1])
        self.assertEqual(url, '/taxonomy_update/1/')
        resolver = resolve('/taxonomy_update/1/')
        self.assertEqual(resolver.func.view_class, TaxonomyUpdateView)

        url = reverse('new_specimen')
        self.assertEqual(url, '/new_specimen/')
        resolver = resolve('/new_specimen/')
        self.assertEqual(resolver.func.view_class, NewSpecimenView)

    def test_url_resolves_to_correct_view(self):
        # Test if the URL resolves to the correct view function for 'index'
        resolver = resolve('/')
        self.assertEqual(resolver.func, index)

        # Test if the URL resolves to the correct view function for 'all_specimens'
        resolver = resolve('/all_specimens/')
        self.assertEqual(resolver.func.view_class, AllSpecimensView)

        # Test if the URL resolves to the correct view function for 'specimen_detail' with a sample specimen ID
        resolver = resolve('/specimen/detail/1/')
        self.assertEqual(resolver.func.view_class, SpecimenDetailView)

        # Test if the URL resolves to the correct view function for 'specimen_update' with a sample specimen ID
        resolver = resolve('/specimen/1/update/')
        self.assertEqual(resolver.func.view_class, SpecimenUpdateView)

        # Test if the URL resolves to the correct view function for 'expedition_update' with a sample expedition ID
        resolver = resolve('/expedition_update/1/')
        self.assertEqual(resolver.func.view_class, ExpeditionUpdateView)

        # Test if the URL resolves to the correct view function for 'taxonomy_update' with a sample specimen ID
        resolver = resolve('/taxonomy_update/1/')
        self.assertEqual(resolver.func.view_class, TaxonomyUpdateView)

        # Test if the URL resolves to the correct view function for 'specimen_delete' with a sample specimen ID
        resolver = resolve('/specimen/1/delete/')
        self.assertEqual(resolver.func.view_class, SpecimenDeleteView)

        # Test if the URL resolves to the correct view function for 'new_specimen'
        resolver = resolve('/new_specimen/')
        self.assertEqual(resolver.func.view_class, NewSpecimenView)

        # Test if the URL resolves to the correct view function for 'new_taxonomy'
        resolver = resolve('/new_taxonomy/')
        self.assertEqual(resolver.func.view_class, NewTaxonomyView)

        # Test if the URL resolves to the correct view function for 'new_expedition'
        resolver = resolve('/new_expedition/')
        self.assertEqual(resolver.func.view_class, NewExpeditionView)

    def resolve_by_name(self, name, args=None):
        # Helper function to resolve URLs by name
        url = reverse(name, args=args)
        resolver = self.client.resolve(url)
        return resolver



class SpecimenSerializerTest(TestCase):
    def setUp(self):
        self.expedition = Expedition.objects.create(expedition='Sample Expedition', continent='Sample Continent', country='Sample Country')
        self.taxonomy = Taxonomy.objects.create(kingdom='Sample Kingdom', phylum='Sample Phylum', highest_biostratigraphic_zone='Sample Zone',
                                                class_name='Sample Class', identification_description='Sample Description',
                                                family='Sample Family', genus='Sample Genus', species='Sample Species')
        self.specimen_data = {'catalog_number': 'Sample Catalog', 'expedition': self.expedition.expedition_id, 'taxonomy': self.taxonomy.taxonomy_id}
        self.serializer = SpecimenSerializer(data=self.specimen_data)

    def test_valid_data(self):
        self.assertTrue(self.serializer.is_valid())

    def test_serialized_data(self):
        self.serializer.is_valid()
        data = self.serializer.data
        self.assertEqual(data, self.specimen_data)

class TaxonomySerializerTest(TestCase):
    def setUp(self):
        self.taxonomy_data = {'kingdom': 'Sample Kingdom', 'phylum': 'Sample Phylum', 'highest_biostratigraphic_zone': 'Sample Zone',
                              'class_name': 'Sample Class', 'identification_description': 'Sample Description',
                              'family': 'Sample Family', 'genus': 'Sample Genus', 'species': 'Sample Species'}
        self.serializer = TaxonomySerializer(data=self.taxonomy_data)

    def test_valid_data(self):
        self.assertTrue(self.serializer.is_valid())

    def test_serialized_data(self):
        self.serializer.is_valid()
        data = self.serializer.data
        self.assertEqual(data, self.taxonomy_data)

class SpecimenSerializerTest(TestCase):
    def setUp(self):
        self.expedition_data = {'expedition': 'Sample Expedition', 'continent': 'Sample Continent', 'country': 'Sample Country'}
        self.taxonomy_data = {'kingdom': 'Sample Kingdom', 'phylum': 'Sample Phylum', 'highest_biostratigraphic_zone': 'Sample Zone',
                              'class_name': 'Sample Class', 'identification_description': 'Sample Description',
                              'family': 'Sample Family', 'genus': 'Sample Genus', 'species': 'Sample Species'}
        self.specimen_data = {'catalog_number': 'Sample Catalog', 'expedition': self.expedition_data, 'taxonomy': self.taxonomy_data}
        self.serializer = SpecimenSerializer(data=self.specimen_data)

    def test_valid_data(self):
        self.assertTrue(self.serializer.is_valid())

    def test_serialized_data(self):
        self.serializer.is_valid()
        data = self.serializer.data
        expected_data = {'catalog_number': 'Sample Catalog', 'expedition': self.expedition_data, 'taxonomy': self.taxonomy_data}
        self.assertEqual(data, expected_data)

# Tests for forms
class SpecimenFormTest(TestCase):
    def test_valid_form(self):
        # Create valid data for the form
        form_data = {
            'catalog_number': '1234.56.78.9012',
        }

        # Create the form instance with the valid data
        form = SpecimenForm(data=form_data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Create invalid data for the form
        form_data = {
            'catalog_number': 'invalid_catalog_number',
        }

        # Create the form instance with the invalid data
        form = SpecimenForm(data=form_data)

        # Check if the form is not valid
        self.assertFalse(form.is_valid())

    def test_clean_catalog_number(self):
        # Create a form instance
        form = SpecimenForm()

        # Set a valid catalog number
        valid_catalog_number = '1234.56.78.9012'
        form.cleaned_data = {'catalog_number': valid_catalog_number}

        # Call the clean_catalog_number method
        cleaned_catalog_number = form.clean_catalog_number()

        # Check if the cleaned catalog number is equal to the original valid catalog number
        self.assertEqual(cleaned_catalog_number, valid_catalog_number)

class SpecimenFilterTest(TestCase):
    def setUp(self):
        # Create taxonomy instances
        taxonomy1 = Taxonomy.objects.create(kingdom="Animalia", phylum="Charadriiformes",
                                           highest_biostratigraphic_zone="Vertebrata", class_name="Aves",
                                           identification_description="Charadriiformes", family="Stercorariidae",
                                           genus="Stercorarius", species="Stercorarius maccormicki")
        
        # Create expedition instance
        expedition1 = Expedition.objects.create(expedition="Sample Expedition", continent="Europe", country="Spain")

        # Create specimen instance and associate it with taxonomy and expedition
        Specimen.objects.create(catalog_number="10451524", taxonomy=taxonomy1, expedition=expedition1)

    def test_filter_by_species(self):
        filter = SpecimenFilter({'taxonomy__species': 'Stercorarius maccormicki'}, queryset=Specimen.objects.all())
        self.assertEqual(len(filter.qs), 1)

    def test_filter_by_continent(self):
        filter = SpecimenFilter({'expedition__continent': 'Europe'}, queryset=Specimen.objects.all())
        self.assertEqual(len(filter.qs), 1)

#testing admin page

class AdminPageTest(TestCase):
    def setUp(self):
        # Create a superuser for logging into the admin interface
        self.admin_user = User.objects.create_superuser(username='coder', password='coder12', email='code@mail.com')
        
        # Create some sample data for the models
        self.expedition = Expedition.objects.create(expedition='Sample Expedition', continent='Sample Continent', country='Sample Country')
        self.taxonomy = Taxonomy.objects.create(kingdom='Sample Kingdom', phylum='Sample Phylum', highest_biostratigraphic_zone='Sample Zone',
                                                class_name='Sample Class', identification_description='Sample Description',
                                                family='Sample Family', genus='Sample Genus', species='Sample Species')
        self.specimen = Specimen.objects.create(catalog_number='Sample Catalog', expedition=self.expedition, taxonomy=self.taxonomy)

    def test_admin_page_accessible(self):
        # Log in with the superuser credentials
        self.client.force_login(self.admin_user)
        
        # Access the admin page for Expedition
        response = self.client.get('/admin/specimen_catalog/expedition/')
        self.assertEqual(response.status_code, 200)

        # Access the admin page for Taxonomy
        response = self.client.get('/admin/specimen_catalog/taxonomy/')
        self.assertEqual(response.status_code, 200)

        # Access the admin page for Specimen
        response = self.client.get('/admin/specimen_catalog/specimen/')
        self.assertEqual(response.status_code, 200)

    def test_admin_page_displays_data(self):
        # Log in with the superuser credentials
        self.client.force_login(self.admin_user)
        
        # Check if the Expedition data is displayed on the admin page
        response = self.client.get('/admin/specimen_catalog/expedition/')
        self.assertContains(response, 'Sample Expedition')

        # Check if the Taxonomy data is displayed on the admin page
        response = self.client.get('/admin/specimen_catalog/taxonomy/')
        self.assertContains(response, 'Sample Kingdom')

        # Check if the Specimen data is displayed on the admin page
        response = self.client.get('/admin/specimen_catalog/specimen/')
        self.assertContains(response, 'Sample Catalog')