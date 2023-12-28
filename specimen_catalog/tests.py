from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.messages import get_messages
from django.contrib.auth.models import User

from .models import Expedition, Taxonomy, Specimen
from .filters import SpecimenFilter
from .views import AllSpecimensView
from .forms import TaxonomyForm, NewSpecimenForm, SpecimenForm 

class IndexViewTests(TestCase):
    def test_index_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'specimen_catalog/index.html')

    def test_index_view_returns_200_status_code(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

class AllSpecimensViewTests(TestCase):
    def setUp(self):
        # Create some Specimen instances for testing
        Specimen.objects.create(catalog_number='ABC123', created=20220101)
        Specimen.objects.create(catalog_number='XYZ456', created=20220102)

    def test_view_rendered_successfully(self):
        response = self.client.get(reverse('all_specimens'))
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'View rendered successfully!')

    def test_valid_filter_parameters(self):
        # Add valid filter parameters
        response = self.client.get(reverse('all_specimens'), {'taxonomy__kingdom': 'Animal'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'specimen_catalog/all_specimens.html')

    def test_pagination(self):
        # Add enough specimens to require pagination
        for i in range(30):
            Specimen.objects.create(catalog_number=f'Test-{i}', created=20220101)

        response = self.client.get(reverse('all_specimens'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'specimen_catalog/all_specimens.html')
        self.assertContains(response, 'pagination')
        self.assertContains(response, 'Page 1 of')

class SpecimenDetailViewTests(TestCase):
    def setUp(self):
        # Create sample data for testing
        self.expedition = Expedition.objects.create(expedition='Test Expedition')
        self.taxonomy = Taxonomy.objects.create(species='Test Species')
        self.specimen = Specimen.objects.create(
            catalog_number='Test-1',
            created=20220101,
            expedition=self.expedition,
            taxonomy=self.taxonomy
        )

    def test_specimen_detail_view_uses_correct_template(self):
        response = self.client.get(reverse('specimen_detail', kwargs={'pk': self.specimen.pk}))
        self.assertTemplateUsed(response, 'specimen_catalog/specimen_detail.html')

    def test_specimen_detail_view_returns_200_status_code(self):
        response = self.client.get(reverse('specimen_detail', kwargs={'pk': self.specimen.pk}))
        self.assertEqual(response.status_code, 200)

class SpecimenUpdateViewTests(TestCase):
    def setUp(self):
        # Create sample data for testing
        self.expedition = Expedition.objects.create(expedition='Test Expedition')
        self.taxonomy = Taxonomy.objects.create(species='Test Species')
        self.specimen = Specimen.objects.create(
            catalog_number='Test-1',
            created=20220101,
            expedition=self.expedition,
            taxonomy=self.taxonomy
        )

    def test_specimen_update_view_uses_correct_template(self):
        response = self.client.get(reverse('specimen_update', kwargs={'pk': self.specimen.pk}))
        self.assertTemplateUsed(response, 'specimen_catalog/specimen_update.html')

    def test_specimen_update_view_returns_200_status_code(self):
        response = self.client.get(reverse('specimen_update', kwargs={'pk': self.specimen.pk}))
        self.assertEqual(response.status_code, 200)

class ExpeditionUpdateViewTests(TestCase):
    def setUp(self):
        # Create sample data for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.expedition = Expedition.objects.create(expedition='Test Expedition')
        self.specimen = Specimen.objects.create(
            catalog_number='Test-1',
            created=20220101,
            expedition=self.expedition
        )
        self.client.login(username='testuser', password='testpassword')

    def test_expedition_update_view_uses_correct_template(self):
        response = self.client.get(reverse('expedition_update', kwargs={'pk': self.expedition.pk}))
        self.assertTemplateUsed(response, 'specimen_catalog/expedition_update.html')

    def test_expedition_update_view_returns_200_status_code(self):
        response = self.client.get(reverse('expedition_update', kwargs={'pk': self.expedition.pk}))
        self.assertEqual(response.status_code, 200)

    def test_expedition_update_view_updates_expedition(self):
        new_expedition_name = 'Updated Expedition'
        response = self.client.post(
            reverse('expedition_update', kwargs={'pk': self.expedition.pk}),
            {'expedition': new_expedition_name}
        )
        self.expedition.refresh_from_db()
        self.assertEqual(self.expedition.expedition, new_expedition_name)
        self.assertRedirects(response, reverse('specimen_detail', kwargs={'pk': self.expedition.specimen_set.first().pk}))

class TaxonomyUpdateViewTests(TestCase):
    def setUp(self):
        # Create sample data for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.expedition = Expedition.objects.create(expedition='Test Expedition')
        self.specimen = Specimen.objects.create(
            catalog_number='Test-1',
            created=20220101,
            expedition=self.expedition
        )
        self.taxonomy = Taxonomy.objects.create(
            kingdom='Test Kingdom',
            phylum='Test Phylum',
            highest_biostratigraphic_zone='Test Zone',
            class_name='Test Class',
            identification_description='Test Description',
            family='Test Family',
            genus='Test Genus',
            species='Test Species'
        )
        self.specimen.taxonomy = self.taxonomy
        self.specimen.save()
        self.client.login(username='testuser', password='testpassword')

    def test_taxonomy_update_view_uses_correct_template(self):
        response = self.client.get(reverse('taxonomy_update', kwargs={'specimen_pk': self.specimen.pk}))
        self.assertTemplateUsed(response, 'specimen_catalog/taxonomy_update.html')

    def test_taxonomy_update_view_returns_200_status_code(self):
        response = self.client.get(reverse('taxonomy_update', kwargs={'specimen_pk': self.specimen.pk}))
        self.assertEqual(response.status_code, 200)

    def test_taxonomy_update_view_updates_taxonomy(self):
        new_kingdom = 'Updated Kingdom'
        response = self.client.post(
            reverse('taxonomy_update', kwargs={'specimen_pk': self.specimen.pk}),
            {'kingdom': new_kingdom}
        )
        self.taxonomy.refresh_from_db()
        self.assertEqual(self.taxonomy.kingdom, new_kingdom)
        self.assertRedirects(response, reverse('specimen_detail', kwargs={'pk': self.specimen.pk}))

class SpecimenDeleteViewTests(TestCase):
    def setUp(self):
        # Create sample data for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.expedition = Expedition.objects.create(expedition='Test Expedition')
        self.specimen = Specimen.objects.create(
            catalog_number='Test-1',
            created=20220101,
            expedition=self.expedition
        )
        self.taxonomy = Taxonomy.objects.create(
            kingdom='Test Kingdom',
            phylum='Test Phylum',
            highest_biostratigraphic_zone='Test Zone',
            class_name='Test Class',
            identification_description='Test Description',
            family='Test Family',
            genus='Test Genus',
            species='Test Species'
        )
        self.specimen.taxonomy = self.taxonomy
        self.specimen.save()
        self.client.login(username='testuser', password='testpassword')

    def test_specimen_delete_view_uses_correct_template(self):
        response = self.client.get(reverse('specimen_delete', kwargs={'pk': self.specimen.pk}))
        self.assertTemplateUsed(response, 'specimen_catalog/specimen_delete_confirm.html')

    def test_specimen_delete_view_returns_200_status_code(self):
        response = self.client.get(reverse('specimen_delete', kwargs={'pk': self.specimen.pk}))
        self.assertEqual(response.status_code, 200)

class NewSpecimenViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_new_specimen_view(self):
        response = self.client.get(reverse('new_specimen'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'specimen_catalog/new_specimen.html')
        self.assertIsInstance(response.context['form'], NewSpecimenForm)

    def test_post_valid_new_specimen_form(self):
        data = {
            'catalog_number': 'Test-123',
            'created': 20220101,
            # Include other required fields based on your form
        }
        response = self.client.post(reverse('new_specimen'), data)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertRedirects(response, reverse('specimen_detail', kwargs={'pk': Specimen.objects.latest('specimen_id').pk}))
        self.assertEqual(Specimen.objects.count(), 1)

class NewTaxonomyViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_new_taxonomy_view(self):
        response = self.client.get(reverse('new_taxonomy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'specimen_catalog/new_taxonomy.html')
        self.assertIsInstance(response.context['taxonomy_form'], TaxonomyForm)

    def test_post_valid_new_taxonomy_form(self):
        data = {
            'kingdom': 'Animalia',
            'phylum': 'Chordata',
        }
        response = self.client.post(reverse('new_taxonomy'), data)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertRedirects(response, reverse('new_specimen'))
        self.assertEqual(Taxonomy.objects.count(), 1)

class NewExpeditionViewTests(TestCase):
    def test_post_valid_expedition_form(self):
        # Prepare valid form data
        valid_form_data = {
            'expedition': 'Test Expedition',
            'continent': 'Test Continent',
            'country': 'Test Country',
            'state_province': 'Test State',
            'term': 'Test Term',
        }

        # Send a POST request to the view with valid form data
        response = self.client.post(reverse('new_expedition'), data=valid_form_data)

        # Check if the response redirects to the 'new_specimen' page
        self.assertRedirects(response, reverse('new_specimen'))

        # Check if the new expedition is created in the database
        self.assertTrue(Expedition.objects.filter(expedition='Test Expedition').exists())