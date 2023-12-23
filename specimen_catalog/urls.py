# I wrote this code #

# Importing necessary libraries
from django.urls import path
from . import views
from .views import AllSpecimensView, SpecimenDetailView, SpecimenView, ExpeditionUpdateView, TaxonomyUpdateView, SpecimenDeleteView, NewSpecimenView

# URL patterns defines routes for specimen_catalog app
urlpatterns = [
    # Home page
    path('', views.index, name='index'),  
    # Displays all specimens listed in a table                                                                 
    path('all_specimens/', AllSpecimensView.as_view(), name='all_specimens'),  
    # View details of a specific specimen                            
    path('specimen/detail/<int:pk>/', SpecimenDetailView.as_view(), name='specimen_detail'), 
    # View a specific specimen               
    path('specimen/<int:pk>/', SpecimenView.as_view(), name='specimen'),    
    # Update a specific specimen record
    path('specimen/<int:pk>/update/', views.SpecimenUpdateView.as_view(), name='specimen_update'),
    # Update a expediation associated with a specimen
    path('expedition_update/<int:pk>/', ExpeditionUpdateView.as_view(), name='expedition_update'),
    # Update a taxonomy associated with a specimen
    path('taxonomy_update/<int:specimen_pk>/', TaxonomyUpdateView.as_view(), name='taxonomy_update'),
    # Delete a specific specimen
    path('specimen/<int:pk>/delete/', SpecimenDeleteView.as_view(), name='specimen_delete'),
    # Creates a new specimen
    path('new_specimen/', NewSpecimenView.as_view(), name='new_specimen'),
]

# End of the code I wrote #