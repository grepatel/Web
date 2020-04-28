from django.contrib.auth import authenticate, login, logout
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Flight, Passenger


# Create your views here.


def index(request):
    # remove authentication for test code or handle it in the tests
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": None})
    context = {
        "flights": Flight.objects.all(),
        "user": request.user
    }
    return render(request, "flights/index.html", context)


def flight(request, flight_id):
    try:
        obj = Flight.objects.get(id=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight does not exist.")
    context = {
        "flight": obj,
        "passengers": obj.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=obj).all()
    }
    return render(request, "flights/flight.html", context)


def book(request, flight_id):
    try:
        passenger_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(id=passenger_id)
        flight = Flight.objects.get(id=flight_id)
    except KeyError:
        return render(request, "flights/error.html", {"message": "No selection made.."})
    except Passenger.DoesNotExist:
        return render(request, "flights/error.html", {"message": "No Passenger found.."})
    except Flight.DoesNotExist:
        return render(request, "flights/error.html", {"message": "No flight found.."})

    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("flight", args=(flight_id,)))


def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "users/login.html", {"message": "Invalid credentials.."})


def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {"message": "Logged out..."})
