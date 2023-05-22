from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.SignupView.as_view()),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.signout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('locations/', views.location),
    path('locations/createLocation/', views.create_location),
    path('locations/delete/<int:id>/', views.delete_location, name='location_delete'),
    path('locations/edit/<int:id>', views.update_location, name='location_update'),
    path('locations/<int:id>', views.delete_location),
    path('events/', views.event, name='event'),
    path('events/<str:order_by>/', views.event, name='event'),
    path('createEvent/', views.create_event, name="create_event"),
    path('events/reserve/<int:id>/', views.reserve_event, name='reserve_event'),
    path('events/delete/<int:id>', views.delete_event, name='delete_event'),
    path('events/edit/<int:id>', views.update_event, name='update_event'),
]