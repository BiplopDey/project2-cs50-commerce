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
    path("category/<str:cat>", views.category, name="category"),
    path("comment/<str:auction_id>", views.comment, name="comment"),
    path("user_watchlist", views.user_watchlist, name="user_watchlist" )
]
