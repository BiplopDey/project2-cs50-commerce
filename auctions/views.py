from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import fields
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required

from .models import User, AuctionList, Watchlist, Bid

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
        exclude = ['user', 'date', 'closed']
        #fields = ['name', 'image', 'description', 'bid', 'category']

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid']

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
    display = True # si no esta logeado
    if(request.user.is_authenticated):
        #if user has the item in his watchlist dont display "add watchlist", ie display=false
        #si ya existe auction en watchlist entoces display=False
        display = not auction.interested.all().filter(user=request.user).exists()
    
    return render(request, "auctions/listing.html", {
        "auction": auction,
        'display': display,
        'bid': BidForm()
    })

@login_required
def watchlist(request, auction_id):
    if(request.method == 'POST'):
        if (request.POST['watchlist']=='add'):
            auction = AuctionList.objects.get(pk=auction_id)
            Watchlist.objects.create(user=request.user, auction = auction)
        elif (request.POST['watchlist']=='remove'):
            auction = AuctionList.objects.get(pk=auction_id)
            Watchlist.objects.get(user=request.user, auction = auction).delete()
        else:
            return HttpResponse('Internal Error')#poner algun error

    return HttpResponseRedirect(reverse('listing', args=(auction_id,)))

# def removeWatchlist(request, auction_id):
#     if (AuctionList.objects.filter(pk=auction_id).exists()):
#         auction = AuctionList.objects.get(pk=auction_id)
#         Watchlist.objects.filter(user=request.user, auction = auction).delete()
#         return HttpResponseRedirect(reverse('listing', args=(auction_id,)))
#     else:
#         return HttpResponse('Item Not found')
    

@login_required
def bid(request, auction_id):
    pass