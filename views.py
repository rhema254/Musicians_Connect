from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from django.db.models import Q , Count
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .functions import client_required, musician_required 
from .forms import *
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django_daraja.mpesa.core import MpesaClient



# Create your views here.
def base(request):
    return render(request, "base.html")


def LandingPage(request):
    return render(request, "accounts/LandingPage.html")


def about_us(request):
    return render(request, "accounts/AboutUs.html")


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = '/home'
    

@login_required
def account_setup(request):
    genres = Genre.objects.all()

    if request.method == "POST":
        selected_genres = request.POST.getlist("selected_genres")
        user = request.user  # Access user only if authenticated

        selected_genres = request.POST.getlist("selected_genres")
        for genre_id in selected_genres:
            genre = Genre.objects.get(id=genre_id)
        if user.is_client:
            user.genre.add(genre)
        elif user.is_musician:
            user.genre.add(genre)
        
        return redirect("home")

    context = {"genres": genres}

    return render(request, "accounts/AccountSetup2.html", context)

def accountdetails(request):
    return render(request, "accounts/AccountDetails.html")

def restricted_page(request):
    return render(request, "accounts/RestrictedPage.html")


@login_required(login_url="login")
def edit_profile(request):
    return render(request, "accounts/EditProfiles.html")

@login_required(login_url="login")
def view_profile(request):
    if request.user.is_authenticated:
        user = request.user

    musician = Musician.objects.all()

    return render(request, "accounts/ViewProfile.html", {'musician': musician})

@login_required(login_url="login")
def view_musician_profile(request, musician_id):
    # musician = get_object_or_404(Musician, pk=musician_id)
    # print(musician_id)
    # # pass
    musician = Musician.objects.filter(id=musician_id)
    return render(request, "accounts/MusicianProfile.html",  {'musician': musician})

@login_required(login_url="login")
def review_rating(request):
    return render(request, "accounts/ReviewPage.html")


def check_username(request):
    username = request.GET.get("username")
    if User.objects.filter(username=username).exists():
        return JsonResponse({"available": False})
    else:
        return JsonResponse({"available": True})


# Ile ya Kwanza... Original
def Register(request):

    if request.user.is_authenticated:  # This is a Guard Clause.
        return redirect("home")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            fname = form.cleaned_data['fname']
            lname = form.cleaned_data['lname']
            username = form.cleaned_data['uname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['pass']
            dob = form.cleaned_data['date']

            user = User.objects.create_user(username, email, password, first_name=fname, last_name=lname)

            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            Musician.objects.create(user=user, dob=dob)

            if age < 13:
                messages.error(request, "You should be over 13 years.")
                return redirect('Register')
            else:
                user.save()
                messages.success(request, f"Hello {user.username}! You have created your account successfully. Now login using your details")
                return redirect("account_setup")
    else:
        form = RegistrationForm()


    return render(request, "accounts/RegisterMusicians.html")

def Login(request):

    if request.user.is_authenticated:  # This is a Guard Clause.
        return redirect("home")
    

    if request.method == "POST":
        username = request.POST.get("uname")
        password = request.POST.get("pass")
        print(username)
        print(password)

        user = authenticate(request, username=username, password=password)

        print(User.pk)
        if user is not None:

            auth_login(request, user)
            messages.success(request, f"Welcome Back {user.username}")
            return redirect("home")

        else:
            messages.error(request, "Error, wrong email or password")

    return render(request, "accounts/LoginMusicians.html")

def registerclients(request):

    if request.user.is_authenticated:  # This is a Guard Clause.
        return redirect("home")

    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        username = request.POST.get("uname")
        email = request.POST.get("email")
        password = request.POST.get("pass")
        dob = request.POST.get("date")
        dob = datetime.strptime(dob, "%Y-%m-%d")
      
        new_user = User.objects.create_user(username, email, password, first_name=fname, last_name=lname)   
        Client.objects.create(user=new_user, dob=dob)
        
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
         # Check if age is less than 13
        if age < 13:
            messages.error(request, "You should be over 13years.")
        else:
            # Render the page the user is allowed to access
            new_user.save()
            messages.success(request, f" Hello {new_user.username}! You have created your account successfully. Now login using your details")
            
       
        user = authenticate(request, username=username, password=password)
        login = request.user
            
        return redirect("home")

    return render(request, "accounts/RegisterClients.html")


def loginclients(request):
    if request.user.is_authenticated:  # This is a Guard Clause.
        return redirect("home")
    

    if request.method == "POST":
        username = request.POST.get("uname")
        password = request.POST.get("pass")
       
        user = authenticate(request, username=username, password=password)
      
        if user is not None:

            auth_login(request, user)
            messages.success(request, f"Welcome Back {user.username}")
            return redirect("home")

        else:
            messages.error(request, f"Error, wrong email or password")

    return render(request, "accounts/LoginClients.html")

@login_required
def save_selected_genres(request):
    if request.user.is_authenticated:
            user = request.user
            
    if not request.user.is_authenticated:
        return redirect("Login")

    if request.method == "POST":
                
        user = request.user.get("id")


        selected_genres = request.POST.getlist("selected_genres[]")

        # Assuming the selected genres are sent as a list

        # Check if the user is a musician or a client
        if hasattr(user, "musician"):
            musician = user.musician
            musician.genres.clear()  # Clear existing genres

            for genre_name in selected_genres:
                genre, created = Genre.objects.get_or_create(name=genre_name)
                musician.genres.add(genre)
            return JsonResponse({"message": "Selected genres saved successfully for musician."})

        elif hasattr(user, "client"):
            client = user.client
            client.genres.clear()  # Clear existing genres
            for genre_name in selected_genres:
                genre, created = Genre.objects.get_or_create(name=genre_name)
                client.genres.add(genre_name)
            return JsonResponse(
                {"message": "Selected genres saved successfully for client."}
            )

        else:
            return JsonResponse(
                {"error": "User is neither a musician nor a client."}, status=400
            )

    return JsonResponse({"error": "Invalid request method."}, status=405)


def user_logout(request):
    logout(request)
    return redirect("Login")


def home(request):
    return render(request, "accounts/Homepage.html")


def musicianspage(request):
    musicians = Musician.objects.all()

    return render(request, "accounts/Musicianspage.html", {"musicians": musicians})


@musician_required
def dashboard(request):
    applications = Application.objects.filter(musician=request.user.musician, status__in=['Pending', 'Submitted']).order_by('-date_applied')
    

    if applications.count() == 0:
        messages.info(request, "No applications found.")

    accepted_applications = Application.objects.filter(musician=request.user.musician, status='Accepted').order_by('date_applied')


    return render(request, "accounts/Dashboard.html", {"applications": applications, 'accepted_applications': accepted_applications})

# @musician_required
# def trial_dashboard(request):
#     applications = Application.objects.filter(musician=request.user.musician).order_by('-date_applied')
    

#     if applications.count() == 0:
#         messages.info(request, "No applications found.")


#     return render(request, "accounts/TrialDashboard.html", {"applications": applications})

# @client_required
# def application_review(request):
#     applications = Application.objects.filter(client=request.user.client).order_by('-date_applied')
#     no_of_applications = Application.objects.filter(gig_id=gig_id).count()
#     if applications.count() == 0:
#         messages.info(request, "No applications found.")


#     return render(request, "accounts/ApplicationReview.html", {"applications": applications, 'no_of_applications': no_of_applications})

@client_required
def trial_application_review(request):
    applications = Application.objects.filter(client=request.user.client).order_by('-date_applied')
    
    if request.user.is_authenticated:
        client = request.user.client
        genres_list =  list(client.genres.values_list('name', flat=True))

    if request.user.is_authenticated:
        client = request.user.client
        total_gigs = client.gigs.count()
        gigs_list = Gig.objects.filter(client=client)


    if applications.count() == 0:
        messages.info(request, "No applications found.")


    return render(request, "accounts/TrialApplicationReview.html", {"applications": applications, 'genres_list':genres_list, 'total_gigs':total_gigs, 'gigs_list':gigs_list })

@musician_required
def gigs(request):
    gigs = Gig.objects.all()
    gig_count = gigs.count()
    
    
    if request.method == "POST":
        gig_id = request.POST.get("gig_id")
        gig = Gig.objects.get(id=gig_id)
        musician = request.user.musician
        
        print(gig)
        
        try:
            application = Application.objects.create(
                gig=gig,
                musician=musician,
                client=gig.client
            )
            messages.success(request, "Application submitted successfully.")
        except IntegrityError:
            messages.error(request, "You have already applied to this gig.")
            return redirect('gigspage')
            
        return redirect("dashboard")  # Redirect after successful application

    return render(request, "accounts/M-Gigs.html", {"gigs": gigs , "gig_count": gig_count})



@client_required
def cGigs(request):
    
    ####### Creating A Gig code: Receive inputs from FrontEnd, Process and Save.  
       
    try:
        if request.method == "POST":
            # Retrieve data from the request
            title = request.POST.get("title")
            description = request.POST.get("description")
            genre = request.POST.get("genre")
            location = request.POST.get("location")
            status = request.POST.get("status")
            budget = request.POST.get("budget")
            l_budget = request.POST.get("l_budget")
            h_budget = request.POST.get("h_budget")
            profession_category = request.POST.get("profession_category")
            dry_run = request.POST.get("dry_run")
            payment_policy = request.POST.get("payment_policy")
            Gemail = request.POST.get("email")
            event_date = request.POST.get("event_date")
            expiry_date = request.POST.get("deadline")


           # Create a new Gig object
            new_gig = Gig.objects.create(
                title=title,
                description=description,
                genre="Jazz",
                location=location,
                status="Open",
                budget=budget,
                l_budget=l_budget,
                h_budget=h_budget,
                profession_category=profession_category,
                dry_run=dry_run,
                payment_policy=payment_policy,
                event_date=event_date,
                expiry_date=expiry_date,
                # Gemail=Gemail,
            )
            new_gig.save()  # Save the new Gig object
            return redirect("gigspage")  # Redirect to a success page
    except:
        print("error")


    ## NEW SECTION ####
    
    # This code retrieves a queryset of objects that are associated with request.user. Present all gigs of a client.
    gigs = Gig.objects.filter(client=request.user.client)

    applications = Application.objects.filter(client=request.user.client, status = 'Pending')
    applications_count = applications.count()

    gig_ids = [application.gig.id for application in applications]
    shortlisted_applicants = Application.objects.filter(status='Pending', client=request.user.client, gig__in=gig_ids)
    

    

            
              
    # if shortlisted_applicants.count() == 0:
    #     messages.info(request, 'You have not selected a job. <br>Select a job and Shortlist your choice Musician.')
        
    #     #debug code 
    #     for applicant in shortlisted_applicants:
    #         print(applicant.musician.user.username)
        
    musicians = []
    for application in applications:
        musician = application.musician
        musician_name = musician.user.username
        musician_email = musician.user.email
        musicians.append({
            'name': musician_name,
            'email': musician_email,
        })
    
    if gigs.count() == 0:
        messages.info(request, "No Gigs found.")
    
    # Accepted GIgs



    ########## Code for shortlisting or Immediate Rejection. Receives a decision from the 
    ## frontend, processes it and updates the status field.

    if request.method == 'POST' and 'Accept_application' in request.POST:
            
            decision = request.POST.get('Accept_application')
            application_id = request.POST.get('applicationId')
            application = Application.objects.get(id=application_id)

            if decision == 'True':
                application.status = 'Pending'     
                application.save()
                
            elif decision == 'False':
                application.status = 'Rejected'
                application.save()
                
            else:
                print('Ata mimi sijui niweke nini hapa')       
    
       ########## Code For Final Hire or Final Rejection. 

    if request.method == 'POST' and 'final_decision' in request.POST:
        final_decision = request.POST.get('final_decision')
        application_id = request.POST.get('applicationId')
        application = Application.objects.get(id=application_id)

        if final_decision == 'True':
            application.status = 'Accepted'     
            application.save()
                
        elif final_decision == 'False':
            application.status = 'Rejected'
            application.save()
                
        else:
            print('Ata mimi sijui niweke nini hapa')        
    
    #  return render(request, "accounts/C-Gigs.html", {'gigs': gigs, 'applications':applications, 'shortlisted_applicants':shortlisted_applicants, 'applications_count': applications_count})
  

    return render(request, "accounts/C-Gigs.html", {'gigs': gigs, 'applications':applications, 'applications_count': applications_count, 'shortlisted_applicants':shortlisted_applicants })



# ---------------AUXILIARY FUNCTIONS__-----------


# Search Bar functionality on Gigs Page
def search_gigs(request):
    if "q" in request.GET:
        q = request.GET["q"]
        gigs = Gig.objects.filter(title__icontains=q)
        multiple_q = Q(
            Q(title__icontains=q)
            | Q(location__icontains=q)
            | Q(status__icontains=q)
            | Q(budget__icontains=q)
            | Q(payment_policy__icontains=q)
        )
        gigs = Gig.objects.filter(multiple_q)
        # gigs_list = []
        # for gig in gigs:
        #     for genre in gig.genres.all():
        #         if genre.name.includes(q) and gig not in gigs_list:
        #             gigs_list.append(gig)
        return render(request, "accounts/M-Gigs.html", {"gigs": gigs})
    else:
        gigs = Gig.objects.all()

        context = {"gigs": gigs}

    return render(request, "accounts/M-Gigs.html", context)


# Search Bar functionality on Musicians Page
def search_musicians(request):
    if "mQ" in request.GET:
        q = request.GET["mQ"]
        # gigs = Gig.objects.filter(title__icontains=q)
        multiple_q = Q(
            Q(username__icontains=q)
            | Q(genre__icontains=q)
            | Q(fname__icontains=q)
            | Q(lname__icontains=q)
            | Q(skill_level__icontains=q)
            | Q(charge_rate__icontains=q)
            | Q(location__icontains=q)
        )
        musicians = Musician.objects.filter(multiple_q)
    else:
        gigs = Gig.objects.all()

    context = {"musicians": musicians}

    return render(request, "accounts/Musicianspage.html", context)


def services(request):
    cl = MpesaClient()
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    phone_number = '0702239686'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = 'https://api.darajambili.com/express-payment'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)   

def stk_push_callback():

    return HttpResponse("STK Push Callback")
    # return render(request, "accounts/ServicesPage(NC).html")


def job_count(request):
    jobs = Gig.objects.all()
    jobs_count = Gig.objects.count()
   
    return render(request, "accounts/M-Gigs.html",  {"job_count": job_count})


# PROBABLY MOVE THIS TO musiciansconnect app
def carousel_view(request):
    return render(request, 'CarouselSlider.html')

