from django.shortcuts import render
from typing import Any, Dict
from .models import Item, Location

from django.urls import reverse_lazy

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from django.forms import DateInput

from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class ItemList(LoginRequiredMixin,ListView):
    model = Item
    fields = '__all__'
    template_name = 'packing/item_list.html'
    context_object_name = "items"

    def get_context_data(self, **kwargs):
        # figure passing trip pk to show trip packing items
        context = super().get_context_data(**kwargs)

         # Get the Item object using the pk parameter from the URL
        trip_id =self.kwargs['pk']

        context['items'] = context['items'].filter(user=self.request.user, trip=trip_id)
        context['count'] = context['items'].filter(is_completed=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['items'] = context['items'].filter(
                title__icontains=search_input)
                # title__startswith=search_input)
            
        context['search_input'] = search_input
        context['trip_id'] = trip_id
        return context

class ItemDetail(LoginRequiredMixin,DetailView):
    model = Item
    fields = '__all__'
    template_name = 'packing/item_detail.html'
    context_object_name = "items"

class EditItem(LoginRequiredMixin,UpdateView):
    model = Item
    fields =['title', 'note', 'is_completed']
    # context_object_name = "items"
    template_name = 'packing/item_form.html'
    success_url = reverse_lazy('itemlist')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
    
    def get_success_url(self):
        item = self.get_object()  # Get the item being edited
        trip_id = item.trip_id
        return reverse_lazy('itemlist', args=[trip_id])

class AddItem(LoginRequiredMixin,CreateView):
    model = Item
    fields = ['title', 'note']
    template_name = 'packing/item_form.html'
    success_url = reverse_lazy('itemlist')
    context_object_name = "items"
    context = {
            'is_edit': False,  # Indicate that it's not an edit operation
        }

    def form_valid(self, form):
        # Set the user of the item to the currently logged-in user
        form.instance.user = self.request.user

        # Get the trip ID from the URL parameters
        trip =self.kwargs['pk']

        # Retrieve the Trip (Location) object from the database using the trip_id
        trip= Location.objects.get(pk=trip)

        # Associate the retrieved Trip (Location) with the form instance's 'trip' field
        form.instance.trip = trip

        # Call the form_valid method of the parent class and pass the updated form instance
        return super(AddItem, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('itemlist', args=[self.object.trip_id])
    

class DeleteItem(LoginRequiredMixin,DeleteView):
    model = Item
    context_object_name = "item"
    template_name = 'packing/delete_item.html'
    context = {
        'pk': False,  # Indicate that it's not an edit operation
    }
    def get_success_url(self):
        trip_pk = self.object.trip.pk  # Access the trip's primary key
        print(trip_pk)
        return reverse_lazy('itemlist', kwargs={'pk': trip_pk})