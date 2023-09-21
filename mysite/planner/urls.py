from django.urls import path

from .views import PlanList, AddPlan, AddHotel

app_name = 'plan'

urlpatterns = [
    path("plan/<int:pk>", PlanList.as_view(), name="planlist"),
    path("addplan/<int:pk>", AddPlan.as_view(), name="addplan"),
    path("addhotel/<int:pk>", AddHotel.as_view(), name="addhotel"),
]