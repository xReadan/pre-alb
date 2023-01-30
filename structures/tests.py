from django.test import TestCase
from .models import Structures
from users.models import User
from rooms.models import StructureRooms
from reservations.models import Reservations
from .views import search_structure
from rest_framework.request import HttpRequest
from django.test import Client

# Create your tests here.
class StructuresMethodsTests(TestCase):
    def setUp(self):
        """
            Create mock data
        """
        # Create fake data
        self.fake_user = User.objects.create(username="test", email="test@test.it", password="test", type="Client", avatar="")
        self.fake_owner = User.objects.create(username="test_owner", email="test_owner@test.it", password="test_owner", type="Owner", avatar="")
        self.fake_structure = Structures.objects.create(
            name="owner hotel",
            city="modena",
            image="",
            address="Via Capi 213",
            rooms=1,
            description="owner hotel",
            restaurants = False,
            pool = False,
            spa = False,
            owner_id=self.fake_owner.id
            )
        self.fake_room = StructureRooms.objects.create(name="suite", description="suite", price=50, image="", structure=self.fake_structure)
        # Init request factory
        self.client = Client()

    def test_search_structure_with_no_reservation(self):
        # Fake request
        response = self.client.post('/api/v1/structures/search', {"location":"modena", "date_from":"2023-01-01", "date_to":"2023-01-05"})
        # Request submitted succesfully
        self.assertEqual(response.status_code, 200)
        # Request returned only 1 record
        self.assertEqual(len(response.json()), 1)
        # Availability shold be false
        self.assertEqual(response.json()[0]['available'], True)

    def test_search_structure_with_reservation(self):
        # Create fake reservation
        fake_reservation_response = self.client.post('/api/v1/reservations/create', {
                "user_id":self.fake_user.id,
                "structure_id":self.fake_structure.id,
                "room_id":self.fake_room.id,
                "date_from":"2023-01-01",
                "date_to":"2023-01-05"
            })
        # Request submitted succesfully
        self.assertEqual(fake_reservation_response.status_code, 200)
        # Submit request
        response = self.client.post('/api/v1/structures/search', {"location":"modena", "date_from":"2023-01-01", "date_to":"2023-01-05"})
        # Request submitted succesfully
        self.assertEqual(response.status_code, 200)
        # Request returned only 1 record
        self.assertEqual(len(response.json()), 1)
        # Availability shold be false
        self.assertEqual(response.json()[0]['available'], False)
