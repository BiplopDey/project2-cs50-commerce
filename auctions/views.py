import auctions
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm

from .models import User, AuctionList, Watchlist


def index(request):
    auctions = AuctionList.objects.all()

    return render(request, "auctions/index.html",{
        'auctions': auctions
    })


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
        #fields = ['name', 'image', 'description', 'bid', 'category']

#@login_required, poner login decorator
def create(request):
    if request.method == "POST":
        form = AuctionListForm(request.POST)
        if form.is_valid:
            auctionItem = form.save(commit=False)
            # commit=False tells Django that "Don't send this to database yet.
            # I have more things I want to do with it.")

            auctionItem.user = request.user # Set the user object here
            auctionItem.save() # Now you can send it to DB
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "auctions/create.html",{
                "auction": form
            })
    else:
        return render(request, "auctions/create.html", {
            "auction": AuctionListForm()
            })

def listing(request, auction_id):#muestra el item seleccionado
    auction = AuctionList.objects.get(pk=auction_id)
    if request.method == 'POST':
        if 'watchlist' in request.POST:
            w = Watchlist(user=request.user, watchlist = auction)
            w.save()
            return HttpResponseRedirect(reverse('listing', args=(auction_id,)))
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "auctions/listing.html", {
            "auction": auction
        })

