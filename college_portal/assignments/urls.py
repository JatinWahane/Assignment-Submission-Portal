from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),

    # Assignment CRUD
    path('assignments/', views.assignment_list, name="assignment_list"),
    path('assignments/create/', views.assignment_create, name="assignment_create"),
    path('assignments/<int:id>/edit/', views.assignment_edit, name="assignment_edit"),
    path('assignments/<int:id>/delete/', views.assignment_delete, name="assignment_delete"),

    # Submissions
    path('assignments/<int:id>/submit/', views.submit_assignment, name="submit_assignment"),
    path('submissions/', views.submission_list, name="submission_list"),
]
