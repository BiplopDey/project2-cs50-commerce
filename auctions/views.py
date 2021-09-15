from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm

from .models import User, AuctionList


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

class AuctionListForm(ModelForm):
    class Meta:
        model = AuctionList
        exclude = ['user']
        #fields = ['name', 'image', 'description', 'bid', 'category']# 

def create(request):
    if request.method == "POST":
        form = AuctionListForm(request.POST)
        if form.is_valid:
            #form.user = request.user
            #form.save()#mirar la forma mas simple, aun que me he matado y no he llegado y al
            #final he acado haciendo lo de abajo que en realidad lo podria hacerlo desdel principio
            name = request.POST['name']
            description = request.POST['description']
            bid = request.POST['bid']
            category = request.POST['category']
            image = request.POST['image']
            auctionCreated = AuctionList(
                user=request.user,
                name=name, 
                description=description, 
                bid=bid,
                category=category,
                image=image,
            )
            auctionCreated.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "auctions/create.html",{
                "auction": form
            })
    else:
        return render(request, "auctions/create.html", {
            "auction": AuctionListForm()
            })