from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Create your models here.

#person table
class person(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField()
    gender_choices = [
        ("Male","Male"),
        ("Female", "Female"),
        ("Other", "Other")
    ]
    gender = models.CharField(
        max_length = 124,
        choices = gender_choices,
        default = "Male"
    )
    type_choices = [
        ("Memeber","Member"),
        ("Trainer", "Trainer")
    ]
    type_person = models.CharField(
        max_length = 124,
        choices = type_choices,
        default = "Member"
    )
    fullname = models.CharField(max_length=124, default="")
    description = models.TextField(default="", null=True)
    def __str__(self):
        return f"person ID: {self.id}, User: {self.user}, DOB is: {self.dob}, gender: {self.gender}, Type: {self.type_person} "

#service table
class service(models.Model):
    id = models.AutoField(primary_key=True)
    type_what = models.ForeignKey('service_type', on_delete=models.CASCADE, name="type_field")
    service_provider = models.ForeignKey('person', on_delete= models.CASCADE, name="service_provider_field")
    is_online = models.BooleanField(default=False, null=True)
    is_oneToOne = models.BooleanField(default=False, null=True)
    startdate = models.DateTimeField(auto_now_add=True)
    days_choices = [
        ("Weekdays","Regular Weekdays"),
        ("Alternate Days", "Alternate Days on Weekdays"),
        ("Weekends", "Weekends")
    ]
    days = models.CharField(
        max_length = 124,
        choices = days_choices,
        default = "Weekdays",
        null=True
    )
    timings_choices = [
        ("8am","8am"),
        ("5pm", "5pm"),
        ("8pm", "8pm")
    ]
    timings = models.CharField(
        max_length = 124,
        choices = timings_choices,
        default = "5pm",
        null=True
    )
    duration = models.IntegerField(default=0, null=True)
    excercise = models.ForeignKey('exercise', on_delete=models.CASCADE, name="excercise_field", null=True)
    class_link = models.URLField(max_length = 200, null=True)
    charges = models.IntegerField(default=0, validators= [MinValueValidator(1)])
    #admin_approved = models.BooleanField(default=True)
    #rating = models.IntegerField(default=0, validators= [MinValueValidator(1)])
    def serialize(self):
        return {
            "id": self.id,
            "type": self.type_field.service_name,
            "serviceProvider": self.service_provider_field.fullname,
            "is_Online": self.is_online,
            "is_oneToOne": self.is_oneToOne,
            "startdate": self.startdate.strftime("%b %d %Y, %I:%M %p"),
            "days": self.days,
            "timings": self.timings,
            "duration": self.duration,
            "exercise": self.excercise_field.exercise_name,
            "class_link": self.class_link,
            "charges": self.charges,
            #"admin_approved": self.admin_approved,
            #"rating": self.rating
        }
    def __str__(self):
        return f"service type: {self.type_field.service_name}, Service Provider: {self.service_provider_field.fullname}, charges: {self.charges}"

#service_type table
class service_type(models.Model):
    id = models.AutoField(primary_key=True)
    service_name = models.CharField(default="",max_length=124)
    #description = models.TextField(default="")
    def __str__(self):
        return f"ID: {self.id}, service name: {self.service_name}"

#exercise table
class exercise(models.Model):
    id = models.AutoField(primary_key=True)
    exercise_name = models.CharField(default="",max_length=124)
    #description = models.TextField(default="")
    def __str__(self):
        return f"ID: {self.id}, exercise name: {self.exercise_name}"

#booking
class booking(models.Model):
    id = models.AutoField(primary_key=True)
    booking_person = models.ForeignKey('person', on_delete=models.CASCADE, name="person_field")
    service = models.ForeignKey('service', on_delete=models.CASCADE, name="service_field")
    time_of_booking = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"ID: {self.id}, person who booked: {self.person_field.fullname}, Service: {self.service_field.type_field.service_name}, Service Provider: {self.service_field.service_provider_field.fullname}"

