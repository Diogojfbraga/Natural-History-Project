from django.db import models

#This code defines a Django model named Expedition and it's information
class Expedition(models.Model):
    expedition_id = models.AutoField(primary_key=True)
    expedition = models.CharField(max_length=255, null=False, blank=True)
    continent = models.CharField(max_length=255, null=False, blank=True)
    country = models.CharField(max_length=255, null=False, blank=True)
    state_province = models.CharField(max_length=255, null=False, blank=True)
    term = models.CharField(max_length=255, null=False, blank=True)

    def __str__(self):
        return self.expedition
    
#This code defines a Django model named Taxonomy and it's information
class Taxonomy(models.Model):
    taxonomy_id = models.AutoField(primary_key=True)
    kingdom = models.CharField(max_length=255, null=False, blank=True)
    phylum = models.CharField(max_length=255, null=False, blank=True)
    highest_biostratigraphic_zone = models.CharField(max_length=255, null=False, blank=True)
    class_name = models.CharField(max_length=255, null=False, blank=True)
    identification_description = models.CharField(max_length=255, null=False, blank=True)
    family = models.CharField(max_length=255, null=False, blank=True)
    genus = models.CharField(max_length=255, null=False, blank=True)
    species = models.CharField(max_length=255, null=False, blank=True)

    def __str__(self):
        return f"Taxonomy {self.species}"
 
#This code defines a Django model named Specimen and it's information
class Specimen(models.Model):
    specimen_id = models.AutoField(primary_key=True)
    catalog_number = models.CharField(max_length=255, null=False, blank=True)
    created = models.IntegerField()
    expedition = models.ForeignKey('Expedition', on_delete=models.CASCADE, null=True, blank=True)
    taxonomy = models.ForeignKey(Taxonomy, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-specimen_id']    

    def __str__(self):
        return f"Specimen {self.specimen_id}"