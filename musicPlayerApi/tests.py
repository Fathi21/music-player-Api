from rest_framework.test import APIClient
from django.test import TestCase

class TestModel1Api(TestCase):

   def test_hello_world(self):
       self.assertEqual("hello world", "hello world")