from django.urls import path
from . import views 

urlpatterns = [
	#Members' routes
	path("", views.index, name="index"),
	path("register", views.register, name = "register"),
	path("login", views.login_view, name = "login"),
	path("logout", views.logout_view, name = "logout"),
	path("booking", views.booking_view, name = "booking"),
	path("about_us", views.about_us, name = "about_us"),
	path("our_team", views.our_team, name = "our_team"),
	path("confirm_booking/<int:service_id>", views.confirm_booking, name="confirm_booking"),
	path("enroll/<int:service_id>", views.enroll, name="enroll"),
	path("your_classes", views.your_classes, name="your_classes"),
	path("cancel_class/<int:class_id>", views.cancel_class, name="cancel_class"),
	#Trainers' Routes
	path("trainer_services", views.trainer_services, name="trainer_services"),
	path("create_class", views.create_class, name="create_class"),
	path("delete_service/<int:service_id>", views.delete_service, name="delete_service"),
	#API Routes
	path("selected_services/<int:type_id>/<str:service_loc>/<str:days>/<str:timing>/<int:exID>/<int:maxCharges>", views.selected_services, name="selected_services")
]