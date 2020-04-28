from django.db.models import Max
from django.test import TestCase, Client
from .models import Airport, Flight, Passenger


# Create your tests here.

class ModelTestCase(TestCase):

    def setUp(self):
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=100)
        Flight.objects.create(origin=a1, destination=a2, duration=-100)

    def test_departure_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 3)

    def test_invalid_flight(self):
        a = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a, destination=a)
        self.assertFalse(f.is_valid())

    def test_index(self):
        c = Client()
        response= c.get("/")
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context["flights"].count(),3)

    def test_invalid_flight_page(self):
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]

        c= Client()
        response = c.get(f"/{max_id + 1}")
        self.assertEqual(response.status_code,404)

