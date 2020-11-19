from django.contrib.auth import authenticate, login, logout
import json
from django.db import IntegrityError, Error
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django import forms
from django.db.models import Max, Min, Avg
from . models import User, person, service, service_type, exercise, booking
import datetime
from django.core.exceptions import ObjectDoesNotExist

from django.db import connection
# Create your views here.

#Create Class Form

#Members' Views
#home page
def index(request):
    if request.user.is_authenticated:
        person_obj = person.objects.get(user_id=request.user.id)
        if person_obj.type_person == 'Member':
            return render(request, "members/index.html")
        else:
            return render(request, "members/trainer_services.html")
    else:
        return render(request, "members/index.html")

#sign-in page
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            person_obj = person.objects.get(user_id=user.id)
            if person_obj.type_person == 'Member':
                return HttpResponseRedirect(reverse("your_classes"))
            else:
                return HttpResponseRedirect(reverse("trainer_services"))
        else:
            return render(request, "members/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "members/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

#registration form
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        dob = request.POST["dob"]
        fullname = request.POST["fullname"]
        gender = request.POST["gender"]
        type_person = request.POST["type"]
        description = request.POST["description"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "members/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
        except IntegrityError:
            return render(request, "members/register.html", {
                "message": "Username already taken."
            })
        try: 
            new_person = person(
                user_id=user.id,
                dob=dob,
                gender= gender,
                type_person=type_person,
                fullname=fullname,
                description=description)
            user.save()
            new_person.save()
            login(request, user)
            #pages will be rendered depending on the type of user
            if type_person == 'Member':
                return HttpResponseRedirect(reverse("your_classes"))
            else:
               return render(request, "members/trainer_services.html")
        except Error:
            return render(request, "members/register.html", {
                "message": "Please fill all the details carefully."
            })
    else:
        return render(request, "members/register.html")

#search a service view page
def booking_view(request):
    service_types = service_type.objects.all()
    services = service.objects.all()
    exercises = exercise.objects.all()
    max_price_dic = service.objects.aggregate(Max('charges'))
    max_price = max_price_dic.get('charges__max')
    min_price_dic = service.objects.aggregate(Min('charges'))
    min_price = min_price_dic.get('charges__min')
    return render(request, "members/booking.html",{
        "service_types":service_types,
        "services": services,
        "exercises": exercises,
        "max_price": max_price,
        "min_price": min_price
    })
    return render(request, "members/booking.html")

#about us view page
def about_us(request):
    return render(request, "members/about_us.html")

#our team view page
def our_team(request):
    trainers = person.objects.filter(type_person="Trainer")
    #today = datetime.date.today()

    cursor=connection.cursor()
    '''trainers=cursor.execute('ret_trainer()').fetchall()
    return HttpResponse(f"{trainers}")'''

    return render(request, "members/our_team.html", {
        "trainers": trainers,
        #"today": today
    })


def confirm_booking(request, service_id):

    '''cursor.execute('call trial()')
    date = cursor.fetchall()'''
    service_obj = service.objects.get(id=service_id)
    return render(request, "members/confirm_booking.html", {
            "service": service_obj
        })


def enroll(request, service_id):
    if request.user.is_authenticated:
        booking_person = person.objects.get(user=request.user)
        try:
            booking.objects.get(person_field=booking_person, service_field_id=service_id)
            message = "Sorry! You are already enrolled in the class"
            bookings = booking.objects.filter(person_field=booking_person)
            return render(request, "members/your_classes.html", {
                "message": message,
                "bookings":bookings
            })
        except booking.DoesNotExist:
            book = booking(person_field=booking_person, service_field_id=service_id)
            book.save()
            message = "Yay! You are successfully enrolled in the class"
            bookings = booking.objects.filter(person_field=booking_person)
            return render(request, "members/your_classes.html", {
                "message": message,
                "bookings":bookings
            })

    else:
        return render(request, "members/login.html", {"message": "Please login first"})
#user dashboard
def your_classes(request):
    booking_person = person.objects.get(user=request.user)
    try:
        bookings = booking.objects.filter(person_field_id=booking_person.id)
        return render(request, "members/your_classes.html", {
           "bookings": bookings
        })
    except ObjectDoesNotExist:
        return render(request, "members/your_classes.html")

def cancel_class(request, class_id):
    booking_person = person.objects.get(user=request.user)
    booking_obj = booking.objects.get(person_field_id=booking_person.id, service_field_id = class_id)
    booking_obj.delete()
    message = "Your class has been successfully deleted"
    bookings = booking.objects.filter(person_field=booking_person)
    return render(request, "members/your_classes.html", {
        "message": message,
        "bookings":bookings
    })


#Trainers' Views
def trainer_services(request):
    trainer = person.objects.get(user_id=request.user.id)
    services = service.objects.filter(service_provider_field_id=trainer.id)
    return render(request, "members/trainer_services.html",{
        "services":services
    })

def create_class(request):
    if request.method == "POST":
        service_type_id = int(request.POST.get("serviceType"))
        check_online = int(request.POST.get("check_online"))
        check_group = int(request.POST.get("check_group"))
        days = request.POST.get("days")
        timing = request.POST.get("timing")
        exercise_name = request.POST.get("exercise")
        class_link = request.POST.get("link")
        duration =request.POST.get("duration")
        if duration == '':
            duration = None
        else:
            duration = int(duration)
        charges = int(request.POST.get("charges"))
        if check_online == 1:
            is_online = True
        elif check_online == 2:
            is_online = False
        else:
            is_online = None
        if check_group == 1:
            is_oneToOne = True
        elif check_group == 2:
            is_oneToOne = False
        else:
            is_oneToOne = None

        if exercise_name != '':
            #ex_name = exercise(exercise_name = exercise_name)
            #ex.save()
            ex = exercise.objects.get(exercise_name = exercise_name)
        else:
            ex = None
        trainer = person.objects.get(user=request.user)
        service_obj = service(
            type_field_id=service_type_id,
            service_provider_field = trainer,
            is_online = is_online,
            is_oneToOne = is_oneToOne,
            days= days,
            timings = timing,
            duration = duration,
            excercise_field_id = ex.id,
            class_link = class_link,
            charges = charges
        )
        service_obj.save()
        message = "You have successfully created a class."
        services = service.objects.filter(service_provider_field=trainer)
        return render(request, "members/trainer_services.html", {
            "message": message,
            "services": services
        })
    else:
        exercises = exercise.objects.all()
        return render(request, "members/create_class.html", {
            "exercises": exercises
            })

def delete_service(request, service_id):
    service.objects.get(id=service_id).delete()
    trainer = person.objects.get(user=request.user)
    message = "Your class has been successfully deleted"
    services = service.objects.filter(service_provider_field=trainer)
    return render(request, "members/trainer_services.html", {
        "message": message,
        "services": services
    })

#API Function
def selected_services(request, type_id, service_loc, days, timing, exID, maxCharges):
    try:
        services = service.objects.filter(charges__lte=maxCharges)
        if type_id != 0:
            services = services.filter(type_field_id= type_id)
        if service_loc != 'both':
            is_online = False
            if service_loc == 'online':
                is_online = True
            services = services.filter(is_online= is_online)
        if days != 'all':
            services = services.filter(days=days)
        if timing != 'all':
            services = services.filter(timings= timing)
        if exID != 0:
            services = services.filter(excercise_field_id = exID)
        services = services.order_by("-startdate").all()
        '''cur = connections["gym_database"].cursor()
        cur.callproc("serv_filter", [service_loc, int(maxCharges), int(exID),int(type_id),days,timing])
        services = next(cur.stored_results()).fetchall()'''
        return JsonResponse([ser.serialize() for ser in services], safe=False)
    except service.DoesNotExist:
        return JsonResponse({"error": "Service not found."}, status=404)