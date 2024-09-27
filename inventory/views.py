from core.exception_handler import api_exception_handler
from core.utils import message_response
from inventory.authenticate import CryptoJWTAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Item
from .serializers import ItemSerializer
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from core.messages import CREATE_ITEM, DELETE_ITEM, DELETED_SUCCESSFULLY, GET_ITEM, UPDATE_ITEM

class ItemView(APIView):
    # authentication_classes = [CryptoJWTAuthentication]

    @staticmethod
    @api_exception_handler(GET_ITEM)
    def get(request, item_id=None):
        # Try fetching the item from Redis cache first
        if item_id:
            cached_item = cache.get(f'item_{item_id}')
            if cached_item:
                return Response(cached_item)
        
        # Fetch from DB if not found in cache
        item = get_object_or_404(Item, id=item_id)
        serializer = ItemSerializer(item)
        
        # Store the item in cache
        cache.set(f'item_{item_id}', serializer.data, timeout=60*60)  # Cache for 1 hour
        return Response(serializer.data)
    
    @staticmethod
    @api_exception_handler(CREATE_ITEM)
    def post(request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @api_exception_handler(UPDATE_ITEM)
    def put(request, item_id):
        item = get_object_or_404(Item, id=item_id)
        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    @api_exception_handler(DELETE_ITEM)
    def delete(request, item_id):
        item = get_object_or_404(Item, id=item_id)
        item.delete()
        return Response(message_response(DELETED_SUCCESSFULLY), status=status.HTTP_204_NO_CONTENT)
