from django.urls import path
from .views import *

urlpatterns = [
    path('', PostView.as_view(), name="post_view"),
    path('rate/', RatingView.as_view(), name="rating_view"),
]