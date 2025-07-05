from django.urls import path
from . import views

urlpatterns = [
    path("generate/", views.trainer_generate_polls, name="trainer_generate_polls"),
    path("save/", views.save_selected_polls, name="save_selected_polls"),
    path("<int:poll_id>/", views.poll_detail, name="poll_detail"),  # if you have this
]
