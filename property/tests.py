from django.test import TestCase
from property.models import Property


class PropertyTest(TestCase):
    def setUp(self) -> None:
        Property.objects.create()
