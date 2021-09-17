from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<str:auction_id>", views.listing, name="listing"),
    path("addWatchlist/<str:auction_id>", views.addWatchlist, name="addListing"),
    path("removeWatchlist/<str:auction_id>", views.removeWatchlist, name="removeListing"),
    path("bid/<str:auction_id>", views.bid, name="bid"),
    
]
