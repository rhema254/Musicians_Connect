from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    path("accounts/login/", LandingPage, name="landingpage"),
    path("aboutus/", about_us, name="AboutUs"),
    path("restricted_page/", restricted_page, name="restricted_page"),
    ####
    # path("CreateAccount/", Register, name="register"),  # Musician (Original)
    path("CreateAccount/", Register, name="register"),  # Musician (Testing)
    path("registerclients/", registerclients, name="registerclients"),  # Clients
    path("check_username/", check_username, name="check_username"),  # Musician
    path("Login/", Login, name="Login"),  # Clients
    path("loginclients/", loginclients, name="loginclients"),

    
    # path("password/", auth_views.PasswordChangeView. as_view(template_name='accounts/ChangePassword.html')),
    path("password/", PasswordsChangeView.as_view(template_name='accounts/ChangePassword.html'), name='password_change'),
    path("reset_password/", auth_views.PasswordResetView.as_view(), name="reset_password"),
    path("reset_password_sent/",auth_views.PasswordResetDoneView.as_view(),name="password_reset_done",),
    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm",),
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    ####

    path("home/", home, name="home"),

    ## Trial Dashboards 
    path("dashboard/", dashboard, name="dashboard"),
    # path("trial_dashboard/", trial_dashboard, name="trial_dashboard"),
    # path("application_review/", application_review, name="application_review"),
    path("application_review/", trial_application_review, name="trial_application_review"),
    
    ###
    path("musicianspage/", musicianspage, name="musicianspage"),
    # path("musicians/", musicians_list, name="musicians_list"),  # The listing functionality and the page to present
    
    path("gigspage/", gigs, name="gigspage"),
    # path("apply_gig/", apply_gig, name="apply_gig"),

    path("logout", user_logout, name="logout"),
    path("mygigs/", cGigs, name="clientgigs"),
    # Auxiliary paths such as Search, job count
    path("search_gigs/", search_gigs, name="search_gigs"),
    path("search_musicians/", search_musicians, name="search_musicians"),
    path("job_count/", job_count, name="job_count"),
    path("base/", base, name="base"),
   
    # NEWAPP
    path("AccountSetup/", account_setup, name="account_setup"),
    path("AccountDetails/", accountdetails, name="account_details"),
    path("SaveSelectedGenres/", save_selected_genres, name="save_selected_genres"),

    ##PROFILES URLS
    path("EditProfile/", edit_profile, name="edit_profile"),
    path("ViewProfile/", view_profile, name="view_profile"),
    path('view_musician_profile/<int:musician_id>/', view_musician_profile, name='view_musician_profile'),

    path("ReviewPage/", review_rating, name="reviews_ratings"),
    path("carouselview/", carousel_view, name="carouselview"),
    
    
    ###DARAJA API URLs
     path("services/", services, name="servicespage"),
    path('daraja/stk_push', stk_push_callback, name='stk_push_callback'),
   
    ## Trial Dashboards 


]
