from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<str:auction_id>", views.listing, name="listing"),
    path("watchlist/<str:auction_id>", views.watchlist, name="watchlist"),
    path("bid/<str:auction_id>", views.bid, name="bid"),
    
]
