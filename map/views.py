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

# @login_required(login_url='/accounts/login/')
# def pharmacies(request):
#     pharmacies = Pharmacy.objects.all()
#     return render(request,'pharmacies.html',{'pharmacies':pharmacies})
    
# @login_required(login_url='/accounts/login/') 
# def pharm_details(request,pharm_id):
#     pharm=Pharmacy.objects.get(id=pharm_id)
#     print(pharm.name)
#     return render(request,"pharmacy.html",{"pharm":pharm})

# def registration(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             new_user = form.save()
#             profile=Profile.objects.create(user=new_user,email=new_user)
#             return redirect('login')
#     else:
#         form = RegisterForm()
#     context = {
#         'form':form,
#     }
#     return render(request, 'registration/registration_form.html', context)

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

    # profile = Profile.objects.get(user=request.user)
    # if 'drug' in request.GET and request.GET["drug"]:
    #     search_term = request.GET.get("drug")
    #     searched_drugs = Drug.search(search_term)
    #     message = f"{search_term}"
    #     if 'location' in request.GET and request.GET["location"]:
    #         loc = request.GET.get("location")
    #         location = Location.objects.get(name=loc)
    #         if profile.location != location:  
    #             profile.location=location
    #             profile.save()
    #     if searched_drugs:
    #         profile = Profile.objects.get(user=request.user)
    #         location = profile.location
    #         drug = Drug.objects.get(id=searched_drugs.id)
    #         pharmacies = drug.pharmacy.all()
    #         nearest = pharmacies.filter(location=location).all()
    #         others=[]
    #         for pharm in pharmacies:
    #             if pharm.location != location.name:
    #                 others.append(pharm)
    #         return render(request, 'search.html',{"message":message,"drugs": searched_drugs,"drug":drug, "pharmacies":pharmacies,"nearest":nearest,"others":others})
    #     else:
    #         return render(request, 'search.html',{"message":message,"drugs": searched_drugs})

    # else:
    #     return render(request, 'search.html')

# @login_required(login_url='/accounts/login/') 
# def get_details(request,drugs_id):
#     profile = Profile.objects.get(user=request.user)
#     location = profile.location
#     drug = Drug.objects.get(id=drugs_id)
#     pharmacies = drug.pharmacy.all()
#     nearest = pharmacies.filter(location=location).all()
#     others=[]
#     for pharm in pharmacies:
#         if pharm.location != location.name:
#             others.append(pharm)
    
#     return render(request,"details.html",{"drug":drug, "pharmacies":pharmacies,"nearest":nearest,"others":others,})

# @login_required(login_url='/accounts/login/')
# def profile(request):
#     user = request.user
#     profile = Profile.objects.get(user=user)
#     print(profile.user)
#     form=ProfileUpdateForm(instance=profile)
    
#     if request.method == 'POST':
#         form = ProfileUpdateForm(request.POST, request.FILES,instance=profile)
#         if form.is_valid():
#             form.save()
#     context={
#         'form':form,
#         'profile':profile,
#     }
#     return render(request,"profile/profile.html",context=context)

