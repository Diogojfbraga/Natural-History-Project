from django.shortcuts import render, get_object_or_404, redirect

# I wrote this code #

# Importing libraries
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage
from .models import Specimen, Expedition, Taxonomy
from .forms import SpecimenForm, ExpeditionForm, TaxonomyForm, NewSpecimenForm
from .filters import SpecimenFilter

# Index page view
def index(request):
    return render(request, 'specimen_catalog/index.html')

# Displays all specimens listed in a table
class AllSpecimensView(ListView):
    model = Specimen
    template_name = 'specimen_catalog/all_specimens.html'
    context_object_name = 'specimens'
    queryset = Specimen.objects.all()
    filterset_class = SpecimenFilter 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = SpecimenFilter(self.request.GET, queryset=self.get_queryset())

        ## PAGINATOR REFERENCE https://docs.djangoproject.com/en/5.0/topics/pagination/ ##
        # Paginate the specimens queryset with 20 specimens per page #
        paginator = Paginator(filter.qs, 20)
        page = self.request.GET.get('page', 1)

        try:
            specimens = paginator.page(page)
        except EmptyPage:
            specimens = paginator.page(paginator.num_pages)

        context['specimens'] = specimens
        context['page_obj'] = specimens
        context['filter'] = filter
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

class SpecimenDetailView(DetailView):
    model = Specimen
    template_name = 'specimen_catalog/specimen_detail.html'
    context_object_name = 'specimen'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class SpecimenView(DetailView):
    model = Specimen
    template_name = 'specimen_catalog/specimen.html'
    context_object_name = 'specimen'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class SpecimenUpdateView(UpdateView):
    model = Specimen
    template_name = 'specimen_catalog/specimen_update.html'
    form_class = SpecimenForm  # Replace with your actual form

    def get_success_url(self):
        return reverse_lazy('specimen_detail', kwargs={'pk': self.object.pk})


class ExpeditionUpdateView(View):
    template_name = 'specimen_catalog/expedition_update.html'

    def get(self, request, pk):
        expedition = get_object_or_404(Expedition, pk=pk)
        form = ExpeditionForm(instance=expedition)
        return render(request, self.template_name, {'form': form, 'expedition': expedition})

    def post(self, request, pk):
        expedition = get_object_or_404(Expedition, pk=pk)
        form = ExpeditionForm(request.POST, instance=expedition)
        
        if form.is_valid():
            form.save()
            # Redirect to specimen detail with the updated expedition's specimen ID
            return redirect('specimen_detail', pk=expedition.specimen_set.first().pk)

        return render(request, self.template_name, {'form': form, 'expedition': expedition})
    
class TaxonomyUpdateView(View):
    template_name = 'specimen_catalog/taxonomy_update.html'

    def get(self, request, specimen_pk):
        specimen = get_object_or_404(Specimen, pk=specimen_pk)
        taxonomy = specimen.taxonomy
        form = TaxonomyForm(instance=taxonomy)
        return render(request, self.template_name, {'form': form, 'specimen': specimen})

    def post(self, request, specimen_pk):
        specimen = get_object_or_404(Specimen, pk=specimen_pk)
        taxonomy = specimen.taxonomy
        form = TaxonomyForm(request.POST, instance=taxonomy)

        if form.is_valid():
            form.save()
            return redirect('specimen_detail', pk=specimen_pk)

        return render(request, self.template_name, {'form': form, 'specimen': specimen})


class SpecimenDeleteView(DeleteView):
    model = Specimen
    template_name = 'specimen_catalog/specimen_delete_confirm.html'
    success_url = reverse_lazy('all_specimens')


class NewSpecimenView(View):
    template_name = 'specimen_catalog/new_specimen.html'

    def get(self, request):
        form = NewSpecimenForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = NewSpecimenForm(request.POST)
        if form.is_valid():
            # Save the new specimen to the database
            new_specimen = form.save()
            # Redirect to the detail page of the newly created specimen
            return redirect('specimen_detail', pk=new_specimen.pk)

        return render(request, self.template_name, {'form': form})

# End of the code I wrote #
    

# TO DELETE
# from django.http import HttpResponseRedirect
# from django.contrib import messages
# from django.forms import inlineformset_factory
# from django.db.models import Q