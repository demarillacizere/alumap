from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.signals import post_save
import datetime as dt

class Building(models.Model):
    name=models.CharField(max_length=30)
    pic=models.ImageField(upload_to='pictures/',blank=True)

    def save_building(self):
        self.save()

    def delete_building(self):
        self.delete()

    @classmethod
    def search(cls,searchterm):
        search = Building.objects.filter(Q(name__icontains=searchterm)).first()
        return search

    def __str__(self):
        return self.name

class Room(models.Model):
    name=models.CharField(max_length=30)
    pic=models.ImageField(upload_to='pictures/',blank=True)
    building=models.ForeignKey(Building,on_delete=models.CASCADE)
    accessible = models.BooleanField(default=True)
    def save_room(self):
        self.save()

    def delete_room(self):
        self.delete()

    @classmethod
    def search(cls,searchterm):
        search = Room.objects.filter(Q(name__icontains=searchterm)).first()
        return search

    def __str__(self):
        return self.name

class Other_loc(models.Model):
    name=models.CharField(max_length=30)
    pic=models.ImageField(upload_to='pictures/',blank=True)
    accessible = models.BooleanField(default=True)
    def save_loc(self):
        self.save()

    def delete_loc(self):
        self.delete()

    @classmethod
    def search(cls,searchterm):
        search = Room.objects.filter(Q(name__icontains=searchterm)).first()
        return search

    def __str__(self):
        return self.name

class Event(models.Model):
    name=models.CharField(max_length=30)
    venue=models.ForeignKey(Room,on_delete=models.CASCADE)
    def save_event(self):
        self.save()

    def delete_event(self):
        self.delete()

    @classmethod
    def search(cls,searchterm):
        search = Event.objects.filter(Q(name__icontains=searchterm)).first()
        return search

    def __str__(self):
        return self.name

class Direction(models.Model):
    source=models.ForeignKey(Room,on_delete=models.CASCADE,related_name='source_location')
    destination=models.ForeignKey(Room,on_delete=models.CASCADE,related_name='destination_location')
    directions = models.CharField(max_length=250)
    pic=models.ImageField(upload_to='pictures/',blank=True)
    
    def save_direction(self):
        self.save()

    def delete_direction(self):
        self.delete()

    @classmethod
    def search(cls,searchterm):
        search = Direction.objects.filter(Q(name__icontains=searchterm)).first()
        return search

    def __str__(self):
        return f'{self.source.name} to {self.destination.name}'

class Location_Access(models.Model):
    user_email = models.EmailField(max_length=50)
    location=models.ManyToManyField(Room)
    
    def save_access(self):
        self.save()

    def delete_access(self):
        self.delete()

    @classmethod
    def search(cls,searchterm):
        search = Location_Access.objects.filter(Q(name__icontains=searchterm)).first()
        return search

    def __str__(self):
        return self.user_email
