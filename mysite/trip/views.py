from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Location
from .form import SearchForm
from django.urls import reverse_lazy

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.forms import DateInput

from django.contrib.auth.mixins import LoginRequiredMixin
 
import folium
import geocoder

# Create your views here.

class TripList(LoginRequiredMixin,ListView):
    model = Location
    fields = '__all__'
    template_name = 'trip/trip_list.html'
    context_object_name = "trips"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trips'] = context['trips'].filter(user=self.request.user)

        locations = context['trips']
        m = folium.Map(location=[19, -12], zoom_start=2)

        for location in locations:
            spot = geocoder.osm(location.destination)
            lat = spot.lat
            lng = spot.lng

            if lat is not None and lng is not None:
                country = spot.country
                folium.Marker([lat, lng], tooltip='Click for more', popup=country).add_to(m)
        
        
        m = m._repr_html_()

        context['map_html'] = m
        return context

class TripDetail(LoginRequiredMixin, DetailView):
    model = Location
    fields = ['title', 'destination', 'origin', 'note', 'start_date', 'end_date']
    template_name = 'trip/trip_detail.html'
    context_object_name = "trip"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        location = context['trip']
        
        m = folium.Map(location=[19, -12], zoom_start=2)

        destination_spot = geocoder.osm(location.destination)
        folium.Marker([destination_spot.lat, destination_spot.lng,], tooltip='Click for more',popup=destination_spot.country).add_to(m)

        original_spot = geocoder.osm(location.origin)
        folium.Marker([original_spot.lat, original_spot.lng], tooltip='Click for more',popup=original_spot.country).add_to(m)
        
        m = m._repr_html_()

        context['map_html'] = m
        return context

class EditTrip(LoginRequiredMixin,UpdateView):
    model = Location
    fields =['title', 'destination', 'origin', 'note', 'start_date', 'end_date']
    context_object_name = "trip"
    template_name = 'trip/trip_form.html'

    def get_success_url(self):
        return reverse_lazy('tripdetail', kwargs={'pk': self.object.pk})
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['start_date'].widget = DateInput(attrs={'type': 'date'})
        form.fields['end_date'].widget = DateInput(attrs={'type': 'date'})
        return form

class AddTrip(LoginRequiredMixin,CreateView):
    model = Location
    fields = ['title', 'destination', 'origin', 'note', 'start_date', 'end_date']
    template_name = 'trip/trip_form.html'
    success_url = reverse_lazy('member:triplist')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddTrip, self).form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['start_date'].widget = DateInput(attrs={'type': 'date'})
        form.fields['end_date'].widget = DateInput(attrs={'type': 'date'})
        return form

class DeleteTrip(LoginRequiredMixin,DeleteView):
    model = Location
    context_object_name = "trip"
    template_name = 'trip/delete_trip.html'
    success_url = reverse_lazy('member:triplist')
