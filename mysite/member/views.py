from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm

from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin

from trip.models import Location
from trip.form import SearchForm
import folium
import geocoder

# Create your views here.

class TripList(ListView):
    model = Location
    fields = '__all__'
    template_name = 'member/index.html'
    context_object_name = "trips"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trips'] = context['trips']
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

class CustomLoginView(LoginView):
    template_name = 'member/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('member:triplist')
        # return render(request, "users/index.html")
        

class RegisterPage(FormView):
    template_name = 'member/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('member:triplist')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage,self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('member:triplist')
        return super(RegisterPage, self).get(*args, **kwargs)
