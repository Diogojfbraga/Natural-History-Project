# Imports libraries
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib import messages     # Messages
from django.urls import reverse_lazy, reverse    # URL Handing
from django.core.paginator import Paginator, EmptyPage  # Paginator
from django.core.exceptions import ValidationError
from .models import Specimen, Expedition, Taxonomy      # Models
from .forms import SpecimenForm, ExpeditionForm, TaxonomyForm, NewSpecimenForm  # Forms
from .filters import SpecimenFilter     # Filters
from django.http import Http404, HttpResponseServerError, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from .serializers import SpecimenSerializer, ExpeditionSerializer, TaxonomySerializer
from rest_framework import generics
from django.views.generic import TemplateView


# Index page view
class IndexView(TemplateView):
    template_name = 'specimen_catalog/index.html'

class AllSpecimensView(ListView):
    model = Specimen
    template_name = 'specimen_catalog/all_specimens.html'
    context_object_name = 'specimens'
    queryset = Specimen.objects.all()
    filterset_class = SpecimenFilter 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        filter = None
        try:
            filter = SpecimenFilter(self.request.GET, queryset=self.get_queryset())
        except ValidationError as e:
            messages.error(self.request, f"Invalid filter parameters: {e}")
            filter = SpecimenFilter(queryset=Specimen.objects.none())

        paginator = Paginator(filter.qs, 20)
        page = self.request.GET.get('page', 1)

        try:
            specimens = paginator.page(page)
        except EmptyPage:
            specimens = paginator.page(paginator.num_pages)
        
        context['specimens'] = specimens
        context['page_obj'] = specimens
        context['filter'] = filter

        messages.success(self.request, "View rendered successfully!")

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        
        filter_params = {
            'expedition__continent__icontains': self.request.GET.get('expedition__continent', ''),
            'expedition__country__icontains': self.request.GET.get('expedition__country', ''),
        }

        return queryset.filter(**filter_params).order_by('-specimen_id')

# Displays a single speciment with its details, taxonomy and expedtion
class SpecimenDetailView(DetailView):
    model = Specimen
    template_name = 'specimen_catalog/specimen_detail.html'
    context_object_name = 'specimen'

    def get_object(self, queryset=None):
        # Error Handling
        try:
            # Attempts to get the object based on the provided queryset
            return super().get_object(queryset=queryset)
        except Http404 as e:
            # Handles the case where the object is not found
            raise e from None

    def get_context_data(self, **kwargs):
        # Error Handling
        try:
            # Calls the superclass method to get the default context data
            context = super().get_context_data(**kwargs)
            return context
        except Exception as e:
            # Handles other exceptions that may occur during context data retrieval
            messages.error(self.request, f"Error fetching specimen details: {e}")
            return context  # Return the context without additional data

# View that allows to update the specimen record
class SpecimenUpdateView(UpdateView):
    model = Specimen
    template_name = 'specimen_catalog/specimen_update.html'
    form_class = SpecimenForm  # Replace with your actual form

    def get_object(self, queryset=None):
        try:
            # Attempts to get the object based on the provided queryset
            return super().get_object(queryset=queryset)
        except Http404:
            # Handles the case where the object is not found
            raise Http404("Specimen not found")

    def form_valid(self, form):
        try:
            # Calls the superclass method to handle the form validation
            response = super().form_valid(form)
            return response
        except Exception as e:
            # Handle other exceptions that may occur during form validation
            messages.error(self.request, f"Error updating specimen: {e}")
            return self.form_invalid(form)  # Redirect to the form with error messages

    def get_success_url(self):
        # Redirect to specimen_detail with the updated specimen's ID
        return reverse_lazy('specimen_detail', kwargs={'pk': self.object.pk})
    
    def get(self, request, *args, **kwargs):
            try:
                # Attempts to get the object based on the provided queryset
                return super().get(request, *args, **kwargs)
            except Http404:
                # Handles the case where the object is not found
                messages.error(request, "Specimen not found")
                return HttpResponseNotFound(render(request, '404.html'))

# View that allows to update the expedition record
class ExpeditionUpdateView(View):
    template_name = 'specimen_catalog/expedition_update.html'

    def get(self, request, pk):
        try:
            expedition = get_object_or_404(Expedition, pk=pk)
            form = ExpeditionForm(instance=expedition)
            return render(request, self.template_name, {'form': form, 'expedition': expedition})
        except Http404:
            messages.error(request, "Expedition not found")
            return redirect('all_specimens')

    def post(self, request, pk):
        expedition = get_object_or_404(Expedition, pk=pk)
        form = ExpeditionForm(request.POST, instance=expedition)
        
        if form.is_valid():
            try:
                form.save()

                # Update associated specimen's expedition
                specimen = expedition.specimen_set.first()
                if specimen:
                    specimen.expedition = expedition
                    specimen.save()

                # Redirect to specimen detail with the updated expedition's specimen ID
                return redirect('specimen_detail', pk=specimen.pk)

            except Exception as e:
                messages.error(request, f"Error updating expedition: {e}")
                return redirect('all_specimens')

        return render(request, self.template_name, {'form': form, 'expedition': expedition})

# View that allows to update the taxonomy record    
class TaxonomyUpdateView(View):
    template_name = 'specimen_catalog/taxonomy_update.html'

    def get(self, request, specimen_pk):
        try:
            specimen = get_object_or_404(Specimen, pk=specimen_pk)
            taxonomy = specimen.taxonomy
            form = TaxonomyForm(instance=taxonomy)
            return render(request, self.template_name, {'form': form, 'specimen': specimen})
        except Http404:
            # Handles the case where the specimen is not found
            messages.error(request, "Specimen not found")
            return redirect('specimen_detail', pk=specimen_pk)  # Redirects to specimen_detail with the same ID

    def post(self, request, specimen_pk):
        specimen = get_object_or_404(Specimen, pk=specimen_pk)
        taxonomy = specimen.taxonomy
        form = TaxonomyForm(request.POST, instance=taxonomy)

        if form.is_valid():
            try:
                form.save()
                return redirect('specimen_detail', pk=specimen_pk)
            except Exception as e:
                # Handles other exceptions that may occur during form saving
                messages.error(request, f"Error updating taxonomy: {e}")
                return redirect('specimen_detail', pk=specimen_pk)  # Redirects to specimen_detail with the same ID

        return render(request, self.template_name, {'form': form, 'specimen': specimen})

# View that allows to delete the specimen record
class SpecimenDeleteView(DeleteView):
    model = Specimen
    template_name = 'specimen_catalog/specimen_delete_confirm.html'
    success_url = reverse_lazy('all_specimens')

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            messages.error(request, "Specimen not found")
            return redirect('all_specimens')

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, 'Specimen deleted successfully.')
            return render(self.request, 'specimen_catalog/specimen_deleted.html')
        except Exception as e:
            messages.error(self.request, f"Error deleting specimen: {e}")
            return redirect('all_specimens')

    def form_invalid(self, form):
        messages.error(self.request, 'Error deleting specimen. Please try again.')
        return super().form_invalid(form)
    
# View that allows to create a new specimen record
class NewSpecimenView(View):
    template_name = 'specimen_catalog/new_specimen.html'

    def get(self, request):
        form = NewSpecimenForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = NewSpecimenForm(request.POST)

        try:
            # Check if the form is not empty
            if request.POST:
                if form.is_valid():
                    new_specimen = form.save()

                    # Debug print
                    print(f"New specimen created: {new_specimen}")

                    # Add a success message
                    messages.success(request, f'New specimen (Specimen {new_specimen.specimen_id}) created successfully.')

                    # Debug print
                    print(f"Redirecting to SpecimenDetailView for Specimen {new_specimen.pk}")

                    # Redirect to the SpecimenDetailView with the newly created specimen's ID
                    return redirect(reverse('specimen_detail', kwargs={'pk': new_specimen.pk}))

                # If the form is not valid, handle the error
                else:
                    # Debug print
                    print("Form is not valid")

                    # Handles form validation errors
                    messages.error(request, "Error creating specimen. Please correct the form errors.")
            else:
                # Display an error message if the form is empty
                messages.error(request, "Error creating specimen. Form is empty.")

        except Exception as e:
            # Debug print
            print(f"Error creating specimen: {e}")

            # Handles other exceptions that may occur during form submission
            messages.error(request, f"Error creating specimen: {e}")

        # Render the page with the form and error messages
        return render(request, self.template_name, {'form': form})

    
# View that allows to create a new taxonomy record 
class NewTaxonomyView(View):
    template_name = 'specimen_catalog/new_taxonomy.html'

    def get(self, request):
        taxonomy_form = TaxonomyForm()
        return render(request, self.template_name, {'taxonomy_form': taxonomy_form})

    def post(self, request):
        taxonomy_form = TaxonomyForm(request.POST)
        try:
            if taxonomy_form.is_valid():
                # Saves the new taxonomy to the database
                new_taxonomy = taxonomy_form.save()

                # Adds a success message
                messages.success(request, 'New taxonomy created successfully.')

                # Redirects to the "Create New Specimen" page
                return redirect('new_specimen')
        except Exception as e:
            # Handles other exceptions that may occur during form submission
            messages.error(request, f"Error creating taxonomy: {e}")

        return render(request, self.template_name, {'taxonomy_form': taxonomy_form})

# View that allows to create a new expedition record     
class NewExpeditionView(View):
    template_name = 'specimen_catalog/new_expedition.html'

    def get(self, request):
        expedition_form = ExpeditionForm()
        return render(request, self.template_name, {'expedition_form': expedition_form})

    def post(self, request):
        expedition_form = ExpeditionForm(request.POST)

        try:
            if expedition_form.is_valid():
                # Saves the new expedition to the database
                new_expedition = expedition_form.save()

                # Adds a success message
                messages.success(request, 'New expedition created successfully.')

                # Redirects to the "Create New Specimen" page
                return redirect('new_specimen')
            else:
                # Forms is not valid, re-render the page with validation errors
                raise ValidationError('Invalid form data. Please check the errors.')

        except ValidationError as e:
            # Handles validation errors
            messages.error(request, f"Validation Error: {e}")
        except Exception as e:
            # Handles other unexpected errors
            messages.error(request, f"An error occurred: {e}")
            return HttpResponseServerError("500 Server Error")

        # Render the page with the form and error messages
        return render(request, self.template_name, {'expedition_form': expedition_form})
    
# Serializers API views
class SpecimenListAPIView(generics.ListCreateAPIView):
    queryset = Specimen.objects.all()
    serializer_class = SpecimenSerializer

class SpecimenDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Specimen.objects.all()
    serializer_class = SpecimenSerializer

class ExpeditionListAPIView(generics.ListCreateAPIView):
    queryset = Expedition.objects.all()
    serializer_class = ExpeditionSerializer

class ExpeditionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expedition.objects.all()
    serializer_class = ExpeditionSerializer

class TaxonomyListAPIView(generics.ListCreateAPIView):
    queryset = Taxonomy.objects.all()
    serializer_class = TaxonomySerializer

class TaxonomyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Taxonomy.objects.all()
    serializer_class = TaxonomySerializer


