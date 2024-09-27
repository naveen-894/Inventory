from django.urls import path

from inventory.views import ItemView


urlpatterns = [
    path('items/', ItemView.as_view(), name='item-list'),        # Create item
    path('items/<int:item_id>/', ItemView.as_view(), name='item-detail'),  # Read, update, delete item
]