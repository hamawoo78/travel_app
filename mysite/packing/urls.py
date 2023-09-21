from django.urls import path

from .views import ItemList, ItemDetail, AddItem, DeleteItem, EditItem

urlpatterns = [
    path("packing/<int:pk>/", ItemList.as_view(), name="itemlist"),
    path("item/<int:pk>/", ItemDetail.as_view(), name="itemdetail"),
    path("additem/<int:pk>/", AddItem.as_view(), name="additem"),
    path("edititem/<int:pk>/", EditItem.as_view(), name="edititem"),
    path('delete/<int:pk>/', DeleteItem.as_view(), name='deleteitem')
]