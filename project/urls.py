from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("project/<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("project/<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("project/<int:question_id>/vote/", views.vote, name="vote"),
    path("project/add_quest/", views.add_quest, name="add_quest"),
    path("accounts/signup/", views.SignUpView.as_view(), name="signup"),
]
