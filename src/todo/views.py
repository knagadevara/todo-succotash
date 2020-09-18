## default django imports
from django.shortcuts import render

## Application dependant package Import
from rest_framework import status
from rest_framework import viewsets
from rest_framework.reverse import reverse
from rest_framework.decorators import list_route
from rest_framework.response import Response

## Application Classes import
from todo.models import ToDoItem
from todo.serializers import ToDoItemSerializer

# Create your views here.
class ToDoViewSet(viewsets.ModelViewSet):
    queryset = ToDoItem.objects.all()
    serializer_class = ToDoItemSerializer

    def perform_create(self, serializer):
        ## Save instance to get the key and update Url
        instance = serializer.save()
        instance.url = reverse('todoitem-detail' , args=[instance.pk] , request=self.request)
        instance.save()

    def delete(self, request):
        ToDoItems.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
