import factory
import random
from .models import Expedition, Taxonomy, Specimen
from factory.django import DjangoModelFactory

# Expedition testing data
class ExpeditionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Expedition

    expedition_id = factory.Sequence(lambda n: n)
    expedition = factory.Faker('sentence', nb_words=3)
    continent = factory.LazyFunction(lambda: random.choice(["Asia", "Europe", "Africa"]))
    country = factory.LazyFunction(lambda: random.choice(["Country1", "Country2", "Country3"]))

# Taxonomy testing data
class TaxonomyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Taxonomy

    taxonomy_id = factory.Sequence(lambda n: n)
    kingdom = factory.LazyFunction(lambda: random.choice(["Animalia", "Plantae", "Fungi"]))
    phylum = factory.LazyFunction(lambda: random.choice(["Phylum1", "Phylum2", "Phylum3"]))
    highest_biostratigraphic_zone = factory.LazyFunction(lambda: random.choice(["Zone1", "Zone2", "Zone3"]))
    class_name = factory.LazyFunction(lambda: random.choice(["Class1", "Class2", "Class3"]))
    identification_description = factory.LazyFunction(lambda: random.choice(["Desc1", "Desc2", "Desc3"]))
    family = factory.LazyFunction(lambda: random.choice(["Family1", "Family2", "Family3"]))
    genus = factory.LazyFunction(lambda: random.choice(["Genus1", "Genus2", "Genus3"]))
    species = factory.LazyFunction(lambda: random.choice(["Species1", "Species2", "Species3"]))

# Specimen testing data
class SpecimenFactory(DjangoModelFactory):
    class Meta:
        model = Specimen

    catalog_number = factory.Sequence(lambda n: f'Catalog-{n}')  # Ensure unique catalog numbers
    expedition = factory.SubFactory(ExpeditionFactory)
    taxonomy = factory.SubFactory(TaxonomyFactory)

    
