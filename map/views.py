from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,Http404
from django.http import HttpResponseRedirect,JsonResponse
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.exceptions import ObjectDoesNotExist
#from .email import send_welcome_email



def index(request):
    locs = Other_loc.objects.all()
    rooms = Room.objects.all()
    buildings = Building.objects.all()
    events = Event.objects.all()
    context = {
        'rooms':rooms,
        'buildings':buildings,
        'events' : events,
        'locs':locs
    }
    return render(request,'index.html',context)

@login_required(login_url='/accounts/login/')
def about_us(request):
    return render(request,'about.html')

def search_results(request):

    if 'email' in request.GET and request.GET["email"]:
        email = request.GET.get("email")
        user_loc = request.GET.get("currentloc")
        source = Room.objects.get(name=user_loc)
        user_destination = request.GET.get("destination")
        destination = Room.objects.get(name=user_destination)
        try:
            user_email = Location_Access.objects.get(user_email=email, location = destination)
            directions = Direction.objects.get(source = source, destination = destination)
            directions = directions
            return render(request, 'search.html',{"directions":directions})
        except ObjectDoesNotExist:
            message = f"Invalid access key to {destination} room"
            return render(request, 'search.html',{"message":message})

    elif 'currentloc' in request.GET and request.GET["currentloc"]:
        user_loc = request.GET.get("currentloc")
        source = Room.objects.get(name=user_loc)
        if 'destination' in request.GET and request.GET["destination"]:
            user_destination = request.GET.get("destination")
            destination = Room.objects.get(name=user_destination)
            if destination.accessible == False:
                message = f"{destination} room is not accessible to the public"
                return render(request, 'search.html',{"message":message, "user_loc":user_loc, "destination":destination})
            try:
                directions = Direction.objects.get(source = source, destination = destination)
                directions = directions
                return render(request, 'search.html',{"directions":directions})
            except ObjectDoesNotExist:
                message = "There is no direction for the entered location"
                return render(request, 'search.html',{"message":message, "user_loc":user_loc})

        elif 'event' in request.GET and request.GET["event"]:
            event = request.GET.get("event")
            event_obj  = Event.objects.get(name = event)
            event_venue = event_obj.venue
            destination = Room.objects.get(name=event_venue)
            if destination.accessible == False:
                message = f"{destination} room is not accessible to the public"
                return render(request, 'search.html',{"message":message, "user_loc":user_loc,"destination":destination, "event":event_obj})
            directions = Direction.objects.get(source = source, destination = destination)
            directions = directions
            if directions:
                try:
                    directions = directions
                    return render(request, 'search.html',{"directions":directions, "event":event_obj})
                except ObjectDoesNotExist:
                    message = "There is no direction for the entered location"
                    return render(request, 'search.html',{"message":message, "user_loc":user_loc })
            

           
        else:
            return render(request, 'search.html',{"user_loc":user_loc})
        

    else:
        return render(request, 'search.html')

    