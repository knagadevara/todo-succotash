from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from todo.models import ToDoItem

# Create your tests here.

def createItem(client):
    url = reverse('todoitem-list')
    data = { 'title' : 'Walk a Dog' }
    return client.post(url, data, format='json')

class TestCreateToDoItem(APITestCase):
    """
    Test if items can be created
    """

    def setUp(self):
        self.response = createItem(self.client)
    
    def test_recieved_201_created_status_code(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
    
    def test_recieved_location_header_hyperlink(self):
        self.assertRegexpMatches(self.response['Location'], '^http://.+/todos/[\d]+$')

    def test_item_was_created(self):
        self.assertEqual(ToDoItem.objects.count() , 1)

    def test_item_has_correct_title(self):
        self.assertEqual(ToDoItem.objects.get().title, 'Walk a Dog')

class TestUpdateToDoItem(APITestCase):
    """
    Test if update functionality works with PUT 
    """

    def setUp(self):
        response = createItem(self.client)
        self.assertEqual(ToDoItem.objects.get().completed , False)
        url = response['Location']
        data = { 'title' : 'Walk a Dog', 'completed' : True }
        self.response = self.client.put(url, data, format='json')

    def test_received_200_created_status_code(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
    
    def test_item_was_updated(self):
        self.assertEqual(ToDoItem.objects.get().completed, True)

class TestPatchToDoItem(APITestCase):
    """
    Test if patch functionality works with PUT 
    """

    def setUp(self):
        response = createItem(self.client)
        self.assertEqual(ToDoItem.objects.get().completed , False)
        url = response['Location']
        data = { 'title' : 'Walk a Dog', 'completed' : True }
        self.response = self.client.patch(url, data, format='json')

    def test_received_200_updated_status_code(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
    
    def test_item_was_patched(self):
        self.assertEqual(ToDoItem.objects.get().completed, True)

class TestDeleteToDoItem(APITestCase):
    """
    Test if delete functionality works with PUT 
    """

    def setUp(self):
        response = createItem(self.client)
        self.assertEqual(ToDoItem.objects.count() , 1)
        url = response['Location']
        self.response = self.client.delete(url)

    def test_received_204_no_content_status_code(self):
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_item_was_deleted(self):
        self.assertEqual(ToDoItem.objects.count(), 0)

class TestDeleteAllToDoItem(APITestCase):

    def setUp(self):
        createItem(self.client)
        createItem(self.client)
        self.assertEqual(ToDoItem.objects.count(), 2)
        self.response = self.client.delete(reverse('todoitem-list'))

    def test_recieved_204_no_content(self):
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

    def test_item_was_deleted(self):
        self.assertEqual(ToDoItem.objects.count(), 0)         
        

