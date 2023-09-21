from django.urls import path

from .views import TripList, TripDetail, AddTrip, EditTrip, DeleteTrip

app_name = 'trip'

urlpatterns = [
    path("trip/", TripList.as_view(), name="triplist"),
    path("trip/<int:pk>/", TripDetail.as_view(), name="tripdetail"),
    path("addtrip/", AddTrip.as_view(), name="addtrip"),
    path("edittrip/<int:pk>/", EditTrip.as_view(), name="edittrip"),
    path('deletetrip/<int:pk>/', DeleteTrip.as_view(), name='deletetrip')

]