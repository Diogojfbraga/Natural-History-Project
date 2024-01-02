# Importing necessary libraries
from django.urls import path, include
from . import views
from .views import (IndexView, AllSpecimensView, SpecimenDetailView, ExpeditionUpdateView, TaxonomyUpdateView, 
                    SpecimenDeleteView, NewSpecimenView, NewTaxonomyView, NewExpeditionView,
                    )

# URL patterns defines routes for specimen_catalog app
urlpatterns = [
    # Home page
    path('', IndexView.as_view(), name='index'), 
    # Displays all specimens listed in a table                                                                 
    path('all_specimens/', AllSpecimensView.as_view(), name='all_specimens'),  
    # View details of a specific specimen                            
    path('specimen/detail/<int:pk>/', SpecimenDetailView.as_view(), name='specimen_detail'),  
    # Updates a specific specimen record
    path('specimen/<int:pk>/update/', views.SpecimenUpdateView.as_view(), name='specimen_update'),
    # Updates a expediation associated with a specimen
    path('expedition_update/<int:pk>/', ExpeditionUpdateView.as_view(), name='expedition_update'),
    # Updates a taxonomy associated with a specimen
    path('taxonomy_update/<int:specimen_pk>/', TaxonomyUpdateView.as_view(), name='taxonomy_update'),
    # Deletes a specific specimen
    path('specimen/<int:pk>/delete/', SpecimenDeleteView.as_view(), name='specimen_delete'),
    # Creates a new specimen
    path('new_specimen/', NewSpecimenView.as_view(), name='new_specimen'),
    # Creates a new taxonomy
    path('new_taxonomy/', NewTaxonomyView.as_view(), name='new_taxonomy'),
    # Creates a new expedition
    path('new_expedition/', NewExpeditionView.as_view(), name='new_expedition'),

    # API views #
    # SPECIMENS
    path('api/specimens/', views.SpecimenListAPIView.as_view(), name='specimen-list'),
    path('api/specimens/<int:pk>/', views.SpecimenDetailAPIView.as_view(), name='specimen-detail'),
    # EXPEDITION
    path('api/expeditions/', views.ExpeditionListAPIView.as_view(), name='expedition-list'),
    path('api/expeditions/<int:pk>/', views.ExpeditionDetailAPIView.as_view(), name='expedition-detail'),
    # TAXONOMIES
    path('api/taxonomies/', views.TaxonomyListAPIView.as_view(), name='taxonomy-list'),
    path('api/taxonomies/<int:pk>/', views.TaxonomyDetailAPIView.as_view(), name='taxonomy-detail'),
]
