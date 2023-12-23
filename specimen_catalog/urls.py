# I wrote this code #


from django.urls import path
from . import views
from .views import AllSpecimensView, SpecimenDetailView, SpecimenView, ExpeditionUpdateView, TaxonomyUpdateView, SpecimenDeleteView, NewSpecimenView

urlpatterns = [
    path('', views.index, name='index'),
    path('all_specimens/', AllSpecimensView.as_view(), name='all_specimens'),
    path('specimen/detail/<int:pk>/', SpecimenDetailView.as_view(), name='specimen_detail'),
    path('specimen/<int:pk>/', SpecimenView.as_view(), name='specimen'),
    path('specimen/<int:pk>/update/', views.SpecimenUpdateView.as_view(), name='specimen_update'),
    path('expedition_update/<int:pk>/', ExpeditionUpdateView.as_view(), name='expedition_update'),
    path('taxonomy_update/<int:specimen_pk>/', TaxonomyUpdateView.as_view(), name='taxonomy_update'),
    path('specimen/<int:pk>/delete/', SpecimenDeleteView.as_view(), name='specimen_delete'),
    path('new_specimen/', NewSpecimenView.as_view(), name='new_specimen'),
]

# End of the code I wrote #