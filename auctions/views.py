import auctions
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import fields
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Comment, User, AuctionList, Watchlist, Bid
import datetime

def index(request):
    auctions = AuctionList.objects.all()

    return render(request, "auctions/index.html",{
        'auctions': auctions,
        'message': "Active Listing",
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

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

#@login_required, poner login decorator
def create(request):
    if request.method == "POST":
        form = AuctionListForm(request.POST)
        if form.is_valid():
            auctionItem = form.save(commit=False)
            # commit=False tells Django that "Don't send this to database yet.
            # I have more things I want to do with it.")

            auctionItem.date = datetime.datetime.now()
            auctionItem.user = request.user # Set the user object here
            auctionItem.save() # Now you can send it to DB
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "auctions/create.html",{
                "auction": form.as_ul()
            })
    
    return render(request, "auctions/create.html", {
            "auction": AuctionListForm().as_p()
        })

def listing(request, auction_id):#muestra el item seleccionado
    auction = AuctionList.objects.get(pk=auction_id)
    if(request.method=='POST'):#si se cierra el auction
        auction.closed = True
        auction.save()
        return HttpResponseRedirect(reverse('listing', args=(auction_id,)))

    #display add watchlist
    display = True # si no esta logeado
    if(request.user.is_authenticated):
        #if user has the item in his watchlist dont display "add watchlist", ie display=false
        #si ya existe auction en watchlist entoces display=False
        display = not auction.interested.all().filter(user=request.user).exists()
    
    current_bid=auction.bid
    bidding = Bid.objects.filter(auction=auction_id).first()
    if(bidding):
        current_bid = bidding.bid

    return render(request, "auctions/listing.html", {
        "auction": auction,
        'display': display,
        'bid': BidForm(),
        'your_bid_current': Bid.objects.filter(user = request.user, auction = auction).exists(),
        'current_bid': current_bid,
        #mostrar el boton de cerrar solo para el creador
        'creatorAuction': auction.user == request.user,
        'bidding': bidding,
        'comment': CommentForm(),
        'comments': auction.comments.all()
    })

@login_required
def watchlist(request, auction_id):
    if(request.method == 'POST'):
        if (request.POST['watchlist']=='add'):
            auction = AuctionList.objects.get(pk=auction_id)
            Watchlist.objects.create(user=request.user, auction = auction)
        elif (request.POST['watchlist']=='remove'):
            #auction = AuctionList.objects.get(pk=auction_id)
            Watchlist.objects.get(auction = auction_id).delete()
        else:
            return HttpResponse('Internal Error')#poner algun error

    return HttpResponseRedirect(reverse('listing', args=(auction_id,)))

@login_required
def bid(request, auction_id):
    if (request.method=='POST'):
        form = BidForm(request.POST)
        if form.is_valid():
            user_bid = form.cleaned_data["bid"]
            #bucar la puja segun auction, he usado filter porque en get si no existe da error
            bidding = Bid.objects.filter(auction=auction_id).first()
            if(bidding):#si existe el bid
                if(user_bid>bidding.bid):
                    bidding.user = request.user
                    bidding.bid = user_bid
                    bidding.save()#hacer el update
                #poner error si no cumple
            else:#como no existe comprovamos que user_bid es mayor que es starting bid
                auction = AuctionList.objects.get(pk=auction_id)
                if(user_bid>auction.bid):#si cumple crear bid
                    Bid.objects.create(user = request.user, bid = user_bid, auction = auction)
        else:
            return HttpResponse('Wrong bid')#hacer que salga algun mensaje de error
    
    return HttpResponseRedirect(reverse('listing', args=(auction_id,)))

class CategoryForm(forms.Form):
    category = forms.ChoiceField(choices=AuctionList.CATEGORY_CHOICES)


def category(request, cat):
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data["category"]
            return HttpResponseRedirect(reverse('category', args=(category,)))
        else:
            return render(request, "auctions/category.html",{
            'form': form,
        })

    if cat in AuctionList.values:
        return render(request, "auctions/category.html",{
                'form': CategoryForm(),
                'auctions': AuctionList.objects.filter(category = cat),
                'message': "Category"
            } )
    else:
        return render(request, "auctions/category.html",{
            'form': CategoryForm(),
        })

@login_required
def comment(request, auction_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            Comment.objects.create(
                user=request.user,
                auction=AuctionList.objects.get(pk=auction_id),
                comment = comment,
                date = datetime.datetime.now()
            )
    
    return HttpResponseRedirect(reverse('listing', args=(auction_id,)))
    
@login_required
def user_watchlist(request):
    return render(request, "auctions/index.html",{
        'message': "Watchlist",
        'auctions': [w.auction for w in Watchlist.objects.filter(user=request.user)]#se puede buscar en django o hacer un lapply
    })