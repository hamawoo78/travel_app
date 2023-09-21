from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Address, Hotel, Plan
from django.urls import reverse_lazy

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.forms import DateInput
from django import forms

from django.contrib.auth.mixins import LoginRequiredMixin
 
import folium
import geocoder

# Create your views here.

class PlanList(LoginRequiredMixin,ListView):
    model = Plan
    fields = '__all__'
    template_name = 'planner/plan_list.html'
    context_object_name = "plans"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip_id =self.kwargs['pk']
        context['plans'] = context['plans'].filter(trip=trip_id)
        context['hotels'] = Hotel.objects.filter(trip=trip_id)

        locations = []

        for plan in context['plans']:
            locations.append(plan)
        
        for hotel in context['hotels']:
            locations.append(hotel)

        m = folium.Map(location=[12, -19], zoom_start=2)

        for location in locations:
            city = location.address.city
            spot = geocoder.osm(city)
            lat = spot.lat
            lng = spot.lng

            if lat is not None and lng is not None:
                city = spot.city
                folium.Marker([lat, lng], tooltip='Click for more', popup=city).add_to(m)
    
        
        m = m._repr_html_()

        context['map_html'] = m
        context['trip_id'] = trip_id
        return context

# class TripDetail(LoginRequiredMixin, DetailView):
#     model = Location
#     fields = ['title', 'destination', 'origin', 'note', 'start_date', 'end_date']
#     template_name = 'trip/trip_detail.html'
#     context_object_name = "trip"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         location = context['trip']
        
#         m = folium.Map(location=[19, -12], zoom_start=2)

#         destination_spot = geocoder.osm(location.destination)
#         folium.Marker([destination_spot.lat, destination_spot.lng,], tooltip='Click for more',popup=destination_spot.country).add_to(m)

#         original_spot = geocoder.osm(location.origin)
#         folium.Marker([original_spot.lat, original_spot.lng], tooltip='Click for more',popup=original_spot.country).add_to(m)
        
#         m = m._repr_html_()

#         context['map_html'] = m
#         return context

# class EditTrip(LoginRequiredMixin,UpdateView):
#     model = Location
#     fields =['title', 'destination', 'origin', 'note', 'start_date', 'end_date']
#     context_object_name = "trip"
#     template_name = 'trip/trip_form.html'

#     def get_success_url(self):
#         return reverse_lazy('tripdetail', kwargs={'pk': self.object.pk})
    
#     def get_form(self, form_class=None):
#         form = super().get_form(form_class)
#         form.fields['start_date'].widget = DateInput(attrs={'type': 'date'})
#         form.fields['end_date'].widget = DateInput(attrs={'type': 'date'})
#         return form

class CombinedPlanForm(forms.ModelForm):
    street_address = forms.CharField(max_length=200)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=50)
    postal_code = forms.CharField(max_length=20)
    
    class Meta:
        abstract = True

class AddPlanForm(CombinedPlanForm):
    class Meta(CombinedPlanForm.Meta):
        model = Plan
        fields = ['place', 'note']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class AddHotelForm(CombinedPlanForm):
    class Meta(CombinedPlanForm.Meta):
        model = Hotel
        fields = ['name', 'start_date', 'end_date']  # No need to specify fields for Hotel
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        

class AddPlan(LoginRequiredMixin,CreateView):
    model = Plan
    form_class = AddPlanForm
    template_name = 'planner/plan_form.html'
    success_url = reverse_lazy('planlist')

    def form_valid(self, form):
        form.instance.user = self.request.user
        trip =self.kwargs['pk']

        address = Address.objects.create(
            street_address=form.cleaned_data['street_address'],
            city=form.cleaned_data['city'],
            state=form.cleaned_data['state'],
            postal_code=form.cleaned_data['postal_code']
        )

        # Assign the created Address instance to the Plan's address field
        plan = form.save(commit=False)
        plan.address = address
        plan.user = self.request.user
        plan.save()       
        # return super().form_valid(form)

        return super(AddPlan, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('planlist', args=[self.object.trip_id])

class AddHotel(LoginRequiredMixin,CreateView):
    model = Hotel
    form_class = AddHotelForm
    template_name = 'planner/plan_form.html'
    success_url = reverse_lazy('planlist')

    def form_valid(self, form):
        form.instance.user = self.request.user
        trip =self.kwargs['pk']

        address = Address.objects.create(
            street_address=form.cleaned_data['street_address'],
            city=form.cleaned_data['city'],
            state=form.cleaned_data['state'],
            postal_code=form.cleaned_data['postal_code']
        )

        # Assign the created Address instance to the Plan's address field
        plan = form.save(commit=False)
        plan.address = address
        plan.user = self.request.user
        plan.save()       

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('plan:planlist', args=[self.object.pk])

# class DeleteTrip(LoginRequiredMixin,DeleteView):
#     model = Location
#     context_object_name = "trip"
#     template_name = 'trip/delete_trip.html'
#     success_url = reverse_lazy('member:triplist')
