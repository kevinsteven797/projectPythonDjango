from django.shortcuts import render, redirect
from .models import Location, Event, Ticket
from django.shortcuts import render
from .forms import createNewLocation, createNewEvent, createNewTicket, loginForm, SignupForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Count, Sum
from django import template


# Create your views here.
def home(request):
    return render(request,'home.html')

class SignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = SignupForm
    success_url = '/login/'  # URL a la que se redirige después del registro exitoso

    def form_valid(self, form):
        # Obtener los datos del formulario
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        
        # Crear un nuevo usuario
        user = User.objects.create_user(username=username,password=password, email=email, is_superuser=0)
        
        return super().form_valid(form)
    

def loginUser(request):
    authentication_form = loginForm
    if request.method == 'GET':
        return render(request, 'registration/login.html', {"form": authentication_form})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        
        if user is None:
            return render(request, 'registration/login.html', {"form": authentication_form, "error": "Username or password is incorrect."})
        
        login(request, user)
        return redirect(reverse('profile'))


@login_required
def signout(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    user = User.objects.get(id=request.user.id)
    context = {
        'user': user
    }
    return render(request, 'index.html', context)

#Muestra todas las locaciones creadas 
@login_required
def location(request):
    locations = Location.objects.all()
    user = User.objects.get(id=request.user.id)
    return render(request, 'locations/locations.html', {
        'locations': locations,
        'user': user
    })

#Crear nuevas locaciones y las agrega a la base de datos
@login_required
@csrf_protect
def create_location(request):
    if request.method == 'POST':
        formLocation = createNewLocation(request.POST)
        if formLocation.is_valid():
            name = formLocation.cleaned_data['name']
            max_tickets = formLocation.cleaned_data['max_tickets']
            location = Location(name=name, max_tickets=max_tickets)
            location.save()
            return redirect('/locations')
    else:
        print('No fue válido')
        formLocation = createNewLocation()
    
    return render(request, 'locations/create_location.html', {'formulario': formLocation})

@login_required
def delete_location(request, id):
    location = Location.objects.get(id=id)
    if request.method == 'POST':
        location.delete()
        return redirect('/locations')
    
    return render(request,'locations/location_confirm_delete.html',{
        'location': location
    })

@login_required
def update_location(request, id):
    location = Location.objects.get(id=id)
    if request.method == 'POST':
        formLocation = createNewLocation(request.POST, instance=location)  # Vincular el formulario con la instancia de ubicación existente
        if formLocation.is_valid():
            formLocation.save()  # Guardar los cambios en la ubicación
            return redirect('/locations')
    else:
        formLocation = createNewLocation(instance=location)  # Pasar la instancia de ubicación al formulario
    
    return render(request, 'locations/create_location.html', {
        'formulario': formLocation,
        'location': location
    })



#Myuestra todos los eventos creados
@login_required
def event(request, order_by=None):
    events = Event.objects.values()
    locations = Location.objects.all()

    # Ordenar por fecha
    if order_by == 'date':
        events = events.order_by('date')

    # Ordenar por tickets vendidos
    if order_by == 'tickets':
        events = events.annotate(ticket_count=Sum('ticket__numTickets')).order_by('-ticket_count')

    ticketResev = {}
    porcentTickets = {}
    ticket_counts = Event.objects.annotate(ticket_count=Sum('ticket__numTickets'))
    for event in ticket_counts:
        eventIter = Event.objects.get(id=event.id)
        maxTicket_location = eventIter.idLocation_id
        locationIter = Location.objects.get(id=maxTicket_location)
        ticketResev[event.id] = event.ticket_count
        if event.ticket_count is not None:
            porcentTickets[event.id] = round((locationIter.max_tickets-event.ticket_count)/(locationIter.max_tickets)*100,2)
        else:

            porcentTickets[event.id] = round((locationIter.max_tickets-0)/(locationIter.max_tickets)*100,2)

    user = User.objects.get(id=request.user.id)
    return render(request, 'events/events.html', {
        'events' : events,
        'locations': locations,
        'user': user,
        'ticketResev': ticketResev,
        'porcentTickets': porcentTickets,
    })

#Crea nuevos eventos y los guarda en la base de datos 
@login_required
@csrf_protect
def create_event(request):
    locations = Location.objects.all()
    if request.method == 'POST' :
        formEvent = createNewEvent(request.POST)
        if formEvent.is_valid():
            name = formEvent.cleaned_data['name']
            date = formEvent.cleaned_data['date']
            idLocation = formEvent.cleaned_data['idLocation']

            event = Event(name=name, date=date, idLocation=idLocation)
            event.save()

            return redirect('event')
    else:
        print('No fue válido')
        formEvent = createNewEvent()
    
    return render(request, 'events/create_event.html',{'formulario': formEvent, 'locations': locations} )


def delete_event(request, id):
    event = Event.objects.get(id=id)
    if request.method == 'POST':
        event.delete()
        return redirect('/events')
    
    return render(request,'events/event_confirm_delete.html',{
        'event': event
    })
    
@login_required
def update_event(request, id):
    event = Event.objects.get(id=id)
    if request.method == 'POST':
        formEvent = createNewEvent(request.POST, instance=event)

        if formEvent.is_valid():
            formEvent.save()
            
            return redirect('event')
    else:
        formEvent = createNewEvent(instance=event)
    
    return render(request, 'events/create_event.html',{
        'formulario': formEvent,
        'event': event,
        'locations': Location.objects.all()
    })
        
@login_required
@csrf_protect
def reserve_event(request, id):
    event = Event.objects.get(id=id)
    location = Location.objects.get(id=event.idLocation_id)
    
    if request.method == 'POST':
        formTicket = createNewTicket(request.POST)
        
        if formTicket.is_valid():
            nameUser = formTicket.cleaned_data['nameUser']
            email = formTicket.cleaned_data['email']
            numTickets = formTicket.cleaned_data['numTickets']
            idEvent = formTicket.cleaned_data['idEvent']
            
            ticket = Ticket(idEvent=idEvent, nameUser=nameUser, email=email, numTickets=numTickets)
            ticket.save()
            
            return redirect('/events')
    else:
        formTicket = createNewTicket()
        
    return render(request, 'events/event_detail.html', {
        'formulario': formTicket,
        'event': event,
        'location': location
    })


