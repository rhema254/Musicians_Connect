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
# from .filters import ApplicationFilter


import re
from django.core.exceptions import ObjectDoesNotExist


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

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the form data
            # Here you can access form.cleaned_data to get the validated data
            # For example:
            title = form.cleaned_data['title']
            bio = form.cleaned_data['bio']
            location = form.cleaned_data['location']
            instagram = form.cleaned_data['instagram']
            facebook = form.cleaned_data['facebook']
            youtube = form.cleaned_data['youtube']
            genres = form.cleaned_data['genres']
            profession = form.cleaned_data['profession']
            skill_level = form.cleaned_data['skill_level']
            charge_rate = form.cleaned_data['charge_rate']
            charge_rate_type = form.cleaned_data['charge_rate_type']
            samples = form.cleaned_data['samples']
            experience = form.cleaned_data['experience']
            certifications = form.cleaned_data['certifications']
            
            # Process the data further, such as saving to the database
            # Example:
            # new_musician = Musician(title=title, bio=bio, ...)
            musician = Musician.objects.get_or_create(
                
                title = title,
                bio = bio,
                location = location,
                instagram = instagram,
                facebook = facebook,
                youtube = youtube,
                genres = genres ,
                profession = profession,
                skill_level = skill_level,
                charge_rate = charge_rate,
                charge_rate_type = charge_rate_type,
                samples = samples,
                experience = experience,
                certifications = certifications,
                )
            
            return HttpResponse('Form submitted successfully!')

    return render(request, "accounts/EditProfiles.html")

@login_required(login_url="login")
def view_profile(request, musician_id):
    musician = Musician.objects.get(id=musician_id)
    
    if request.user.is_authenticated:
        user = request.user

    # I don't know what this does, I'll be back
    musicians = Musician.objects.all()

    return render(request, "accounts/ViewProfile.html", {'musician': musician, 'musicians':musicians})

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

          

             # Validate the password
            if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            # Password does not meet the requirements
                error_message = "Password must be at least 8 characters long /n contain at least one uppercase letter /n none lowercase letter, /n one digit, and one special character."
                return render(request, 'registration.html', {'error_message': error_message})

            user = User.objects.create_user(username, email, password , first_name=fname, last_name=lname)

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

        cleaned_email = email.strip()
        cleaned_fname = fname.strip()
        cleaned_lname = lname.strip()
        cleaned_password = password.strip()

    # Validate the password
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
        # Password does not meet the requirements
            error_message = "Password must be at least 8 characters long /n contain at least one uppercase letter /n none lowercase letter, /n one digit, and one special character."
            return render(request, 'registration.html', {'error_message': error_message})
     
        new_user = User.objects.create_user(username, email = cleaned_email, password =cleaned_password, first_name=cleaned_fname, last_name=cleaned_lname)  
        Client.objects.create(user=new_user, dob=dob)
        
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
         # Check if age is less than 13
        if age < 13:
            messages.error(request, "You should be over 13years.")
            return redirect('landingpage')
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
        

        if request.method == 'POST':

            application_id = request.POST.get('applicationId')
            withdraw = request.POST.get('withdraw_application')
            
            if withdraw == 'True':
                application = Application.objects.get(id=application_id)
                application.delete()

            if applications.count() == 0:
                messages.info(request, "You have no application Yet.")

        
       
        accepted_applications = applications.filter(status='Accepted').order_by('date_applied')
        musician = request.user.musician
        
        # Access the musician on individual instances within the accepted_applications queryset
        for application in accepted_applications:
            musician = application.musician
            client = application.client.id
            gig = application.gig
            status = application.status

            
            #Ongoing  GIgs
        if request.method == 'POST' and request.POST.get('final_decision'):
            
            final_decision = request.POST.get('final_decision')
            application_Id = request.POST.get('applicationId')
            application = Application.objects.get(id=application_Id)


            if final_decision == 'TRUE':
                successful_hire = SuccessfulHire.objects.get_or_create(application=application, musician=musician, client=client, completion_status= 'Completed')
                  
                application.status = 'Done'
                application.save()


        successful_hires = SuccessfulHire.objects.filter(musician = musician)
        
        if request.method == 'POST' and request.POST.get('mark_complete'):
                
                mark_complete = request.POST.get('mark_complete')
                successful_hireId = request.POST.get('successful_hireId')
                successful_hire = successful_hires.get(id = successful_hireId)
                print(successful_hire)
                if mark_complete == 'True':        
                    successful_hire.completion_status = 'Done'
                    successful_hire.save()
                    return redirect('servicespage') 

        completed_gigs = SuccessfulHire.objects.filter(musician=musician, completion_status= 'Done')
        completed_gigs_count = completed_gigs.count()

        return render(request, "accounts/Dashboard.html", {"applications": applications, 'accepted_applications': accepted_applications, 'successful_hires': successful_hires, 'completed_gigs_count':completed_gigs_count, 'completed_gigs':completed_gigs} )

# @musician_required
# def trial_dashboard(request):
#     applications = Application.objects.filter(musician=request.user.musician).order_by('-date_applied')
    

#     if applications.count() == 0:
#         messages.info(request, "No applications found.")


#     return render(request, "accounts/TrialDashboard.html", {"applications": applications})

@client_required
def application_review(request):
    applications = Application.objects.filter(client=request.user.client).order_by('-date_applied')
    gig_ids = [application.gig.id for application in applications]
    print(gig_ids)
    no_of_applications = Application.objects.filter().count()
    if applications.count() == 0:
        messages.info(request, "No applications found.")


    return render(request, "accounts/ApplicationReview.html", {"applications": applications, 'no_of_applications': no_of_applications})
# #

@client_required
def trial_application_review(request):
    applications = Application.objects.filter(client=request.user.client).order_by('-date_applied')
    
    if request.user.is_authenticated:
        client = request.user.client
        genres_list =  list(client.genres.values_list('name', flat=True))
        print(genres_list)

    if request.user.is_authenticated:
        client = request.user.client
        total_gigs = client.gigs.count()
        gigs_list = Gig.objects.filter(client=client)


    if applications.count() == 0:
        messages.info(request, "No applications found.")


    return render(request, "accounts/TrialApplicationReview.html", {"applications": applications, 'genres_list':genres_list, 'total_gigs':total_gigs, 'gigs_list':gigs_list })

@musician_required
def gigs(request):
    
    sum_gigs = Gig.objects.all().count()
    today = datetime.today()
    gigs = Gig.objects.filter(expiry_date__gte=today, status = 'Open')
    
    gig_count = gigs.count()
    if gig_count == 0:
        gig_count = '0'
    closed_gigs_count = sum_gigs - gig_count

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

    return render(request, "accounts/M-Gigs.html", {"gigs": gigs , "gig_count": gig_count, 'sum_gigs': sum_gigs, 'closed_gigs_count':closed_gigs_count})



@client_required
def cGigs(request):
        
        ####### Creating A Gig code: Receive inputs from FrontEnd, Process and Save.  
    
        if request.method == "POST":
            
            try:
                # Retrieve data from the request
                title = request.POST.get("title")
                description = request.POST.get("description")
                genre_names = request.POST.getlist("genres") # Use getlist() to retrieve multiple values
                location = request.POST.get("location")
                budget = request.POST.get("budget")
                Profession_category = request.POST.get("Profession_category")
                dry_run = request.POST.get("dry-run-requirement")
                payment_policy = request.POST.get("payment_policy")
                event_date = request.POST.get("event_date")
                expiry_date = request.POST.get("deadline")

                client = Client.objects.get(user=request.user)    
                genres = Genre.objects.filter(name__in=genre_names)  # Retrieve the Genre objects by their names 
                genre_ids = [genre.id for genre in genres]


                # Create a new Gig object
                new_gig = Gig.objects.create(client=client,title=title,description=description,location=location,status="Open",budget=budget,Profession_category=Profession_category,dry_run=dry_run,payment_policy=payment_policy,event_date=event_date,expiry_date=expiry_date)
                print(new_gig)
                new_gig.genres.set(genre_ids),
                new_gig.save()  # Save the new Gig object

                return redirect("gigspage")  # Redirect to a success page
            except:
                print("error")
                

        ## NEW SECTION ####
        # This code retrieves a queryset of objects that are associated with request.user. Present all gigs of a client.
        gigs = Gig.objects.filter(client=request.user.client)

        gig_id = [gig.id for gig in gigs]
        
        applications = Application.objects.filter(client=request.user.client, status = 'Submitted', gig__in=gig_id)
        
        applications_count = applications.count()

        # Display the list of applicant who have been shortlisted...After shortlisting submitted-->pending. 
        gig_ids = [application.gig.id for application in applications]
        shortlisted_applicants = Application.objects.filter(status='Pending', client=request.user.client)
        shortlisted_app_count =shortlisted_applicants.count()
        
        if shortlisted_applicants.count() == 0:
            messages.info(request, 'You have not selected a job. <br>Select a job and Shortlist your choice Musician.')
                
             #debug code 
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
            
        ###When you click one gig on My pending Gigs, whether to reject application or shortlist it
        if request.method == 'POST' and 'Accept_application' in request.POST:
            decision = request.POST.get('Accept_application')
            application_id = request.POST.get('applicationId')
            print(application_id)
            try:    
                application = Application.objects.get(id=application_id)

                if decision == 'True':
                    application.status = 'Pending'     
                    application.save()
                    
                elif decision == 'False':
                    application.status = 'Rejected'
                    application.save()
                    
                else:
                    messages.info('Invalid decision')    

            except Application.DoesNotExist:
                print('Application not found')
            
            return redirect('clientgigs')

        ########## Code For short listed applicants 
        if request.method == 'POST' and 'final_decision' in request.POST:
            final_decision = request.POST.get('final_decision')
            application_id = request.POST.get('applicationId')
            application = Application.objects.get(id=application_id)

            if final_decision == 'True':
                application.status = 'Accepted'     
                application.save()
                    
            if final_decision == 'False':
                application.status = 'Rejected'
                application.save()
                    
            else:
                print('Ata mimi sijui niweke nini hapa')        
        
        accepted_applications = Application.objects.filter(client=request.user.client, status='Accepted')
        Accepted_applications_no = accepted_applications.count()

        if request.method == 'POST' and 'cancel_gig' in request.POST:
            cancel_gig = request.POST.get('cancel_gig')
            application_id = request.POST.get('applicationId')
            application = Application.objects.get(id=application_id)

            if cancel_gig == 'True':
                application.status = 'Rejected'   
                messages.success(request, f'You have successfully rejected application by {application.musician.user.username} for job: {application.gig.title}d')  
                application.save()
        
        print(Accepted_applications_no)
        #  return render(request, "accounts/C-Gigs.html", {'gigs': gigs, 'applications':applications, 'shortlisted_applicants':shortlisted_applicants, 'applications_count': applications_count})


        return render(request, "accounts/C-Gigs.html", {'gigs': gigs, 'applications':applications, 'applications_count': applications_count, 'shortlisted_applicants':shortlisted_applicants, 'shortlisted_app_count': shortlisted_app_count, 'accepted_applications': accepted_applications, 'Accepted_applications_no': Accepted_applications_no })


@client_required
def finalise_agreement(request, shortlisted_applicant_id):
    
    application = Application.objects.get(id=shortlisted_applicant_id)
    hire = request.POST.get('hire')
    
    
    if request.method == 'POST' and 'hire' in request.POST:
        
            signature = request.POST.get('signature')
            # application_id = request.POST.get('application_id')
            application = Application.objects.get(id=application.id)
            gig = Gig.objects.get(id=application.gig.id)
            musician= Musician.objects.get(id=application.musician.id)   
            client = Client.objects.get(id=request.user.client.id)
            clientId = client.id
            gig_id = application.gig.id

            if hire == 'True' and signature:
                if signature == f"{request.user.first_name} {request.user.last_name}":
                    try:

                        application.status = 'Accepted'
                        application.save()
                        successfulhire = SuccessfulHire.objects.create(client_id=clientId, musician=musician, gig=gig, application=application, completion_status = 'Ongoing')
                        
                    
                    except IntegrityError:
                        messages.error(request, "This gig is already ongoing!")

                    return redirect('clientgigs')    
                else:
                    messages.error(request, " Error ")   
            else:
                messages.info(request, "Enter the Full Names that you signed up with")  

    clientId = Client.objects.get(id=request.user.client.id)
    ongoing_hires = SuccessfulHire.objects.all()
    hires_count = ongoing_hires.count()  
    print(hires_count)
    print(ongoing_hires)

    return render(request, 'accounts/FinaliseAgreement.html', {'messages': messages, 'application':application, 'ongoing_hires': ongoing_hires, 'hires_count': hires_count} )



# ---------------AUXILIARY FUNCTIONS__-----------


# Search Bar functionality on Gigs Page
def search_gigs(request):

    today = datetime.today()
    
    if "q" in request.GET:
        q = request.GET["q"]
        
        gigs = Gig.objects.filter(title__icontains=q,  expiry_date__gte=today)
        multiple_q = Q(
            Q(title__icontains=q)
            | Q(location__icontains=q)
            | Q(status__icontains=q)
            | Q(budget__icontains=q)
            | Q(payment_policy__icontains=q)
        )
       
        # gigs = Gig.objects.filter(multiple_q,  today = datetime.today())
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

    phone_number = request.POST.get('phone')
    
    # if request.method == 'POST': 
    #     cl = MpesaClient()
    #     # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    #     phone_number = phone_number
    #     amount = 1
    #     account_reference = 'reference'
    #     transaction_desc = 'Description'
    #     callback_url = 'https://api.darajambili.com/express-payment'
    #     response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    #     print(response)
    #     return HttpResponse(response)




    


    return render(request, 'accounts/ServicesPage.html')

def stk_push_callback(request):
    # data = request.body


    
    return HttpResponse("STK Push Callback")
    # return render(request, "accounts/ServicesPage(NC).html")


def job_count(request):
    jobs = Gig.objects.all()
    jobs_count = Gig.objects.count()
   
    return render(request, "accounts/M-Gigs.html",  {"job_count": job_count})


# PROBABLY MOVE THIS TO musiciansconnect app
def carousel_view(request):
    return render(request, 'CarouselSlider.html')



def payment(request):
    return render(request, 'accounts/PaymentPage.html')




