from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Item

class ItemTests(APITestCase):
    def test_create_item(self):
        url = reverse('item-list')
        data = {'name': 'Item 1', 'description': 'good product', 'quantity': 10}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_item(self):
        item = Item.objects.create(name='Item 1', description='Description', quantity=10)
        url = reverse('item-detail', args=[item.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        # Create an item
        item = Item.objects.create(name='Item 1', description='Description', quantity=10)
        url = reverse('item-detail', args=[item.id])
        
        # Update the item
        updated_data = {'name': 'Item 2', 'description': 'poor quality', 'quantity': 5}
        response = self.client.put(url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Item')
        self.assertEqual(response.data['description'], 'Updated Description')
        self.assertEqual(response.data['quantity'], 5)

    def test_delete_item(self):
        # Create an item
        item = Item.objects.create(name='Item 1', description='Description', quantity=10)
        url = reverse('item-detail', args=[item.id])
        
        # Delete the item
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Verify the item no longer exists
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
