import pytest
from model_bakery import baker
from account.models import User
from property.models import Property, Category
from property.permissions import CanAddOrUpdateProperty
from rest_framework.test import APIClient
from rest_framework import status


class PropertyBakery():
    id = 1
    name = 'Classic Villa'
    description = 'Classic Villa Description'
    slug = 'classic-villa'
    category = 'classic'
    address = 'Turkey'
    owner = 1
    location = '0.0060424799336766975,0.004669191548600793'
    number_of_bedrooms = 1
    number_of_beds = 1
    number_of_baths = 1
    capacity_for_adults = 1
    capacity_for_children = 1
    available = True
    available_from = '2023-02-16T21:24:00Z'
    available_to = '2023-02-20T10:23:00Z'


class UserBakery():
    id = 1
    username = 'user@user.com'
    email = 'user@user.com'
    password = 'user@0123456789'
    role = 'guest'


@pytest.mark.django_db
class TestCreateProperty():
    """
    Test cases for creating a property api endpoint
    """

    def test_if_anonymous_return_401(self):
        api_client = APIClient()
        response = api_client.get('/api/v1/properties/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.skip
    def test_user_is_not_admin_or_host_return_403(self):
        category = baker.make(Category)
        property = baker.make(Property, category=1, location='0.0060424799336766975,0.004669191548600793')
        api_client = APIClient()
        api_client.force_authenticate(user=User(role='guest'))
        response = api_client.get(f'/api/v1/properties/{property.id}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
