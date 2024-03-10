from datetime import timedelta, timezone
from django.db import models 
from django.contrib.auth.models import User


class Client(models.Model):
    
    
    CLIENT_TYPE_CHOICES = [
        ('Business', 'Business'),
        ('Individual', 'Individual'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    description = models.TextField()
    client_type = models.CharField(max_length=20, blank=True, choices=CLIENT_TYPE_CHOICES)
    phone = models.CharField(max_length=20)
    genres = models.ManyToManyField('Genre', related_name='clients')#ondelete set null/ do nothing.
    dob = models.DateField(blank=False)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_images', blank=True)


    def __str__(self):
        return f"{self.user}"


class Musician(models.Model):
    MUSICIAN_SKILL_LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Pro', 'Pro'),
        ('Maestro', 'Maestro'),
    ]
    
    CHARGE_RATE_CHOICES = [
        ('hour', 'Per Hour'),
        ('session', 'Per Session'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    genres = models.ManyToManyField('Genre', related_name='musicians')
    phone_number = models.CharField(max_length=15)
    location = models.CharField(max_length=100)
    skill_level = models.CharField(max_length=20, choices=MUSICIAN_SKILL_LEVEL_CHOICES)
    charge_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0.0)#implement null functionality
    charge_rate_type = models.CharField(max_length=10, choices=CHARGE_RATE_CHOICES)
    dob = models.DateField(blank=False)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_images', blank=True)
    bio = models.CharField(max_length=255, blank=True)
    available = models.BooleanField(default=True)
   
    def __str__(self):
        return self.user.username


class Gig(models.Model):

    dry_run_choices = [
    ('', 'Select one'),  
    ('Yes', 'Yes (Paid Separate)'),
    ('No', 'Yes (No payment)'),
    ('Full-after-job', 'NO'),
    ('Negotiable', 'To Be Determined'),
    ]

    PAYMENT_POLICY_CHOICES=[
    ('', 'Select one'),
    ('Full-before-job', '100%: Before Job'),
    ('Half-before-after', '50%: Before and After'),
    ('Full-after-job', '100%: After Job'),
    ('Negotiable', 'Negotiable')

    ]

    PROFESSION_CHOICES = [
    ('', 'Select one'),
    ('singer', 'Singer'),
    ('songwriter', 'Songwriter'),
    ('producer', 'Producer'),
    ('vocalist', 'Vocalist'),
    ('band', 'Band'),
    ('instrumentalist', 'Instrumentalist'),
    ('sound-engineer', 'Sound Engineer'),
    ('music-educator', 'Music Educator'),
    ('folk-traditional', 'Folk and Traditional'),
    ('dj', 'DJ'),
    ('cover-band', 'Cover Band')
    ]

    STATUS_CHOICES =[
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Pending', 'Pending'),
    ]
   
    
    title = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='gigs', )
    genres = models.ManyToManyField('Genre', related_name='gigs')
    description = models.TextField()
    email = models.EmailField()
    location = models.CharField(max_length=100, null=True)
    date_created = models.DateField(auto_now_add=True, auto_created=True)
    expiry_date = models.DateField(auto_now_add=False, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Open")
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Profession_category = models.CharField(max_length=25, choices=PROFESSION_CHOICES,  null=True)
    dry_run = models.CharField(max_length=20, choices = dry_run_choices,  null=True)
    payment_policy = models.CharField(max_length=20, choices= PAYMENT_POLICY_CHOICES,  null=True)
    event_date = models.DateField(auto_now_add=False, null=True)  
    

    def __str__(self):
        return self.title
    
    def snippet(self):
        return self.description[:50]+'...'



class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
#In the Process.... (^_^)
class Application(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT) #Will probably raise integrity issues, How to handle them?
    musician = models.ForeignKey(Musician, on_delete=models.PROTECT) #Will probably raise integrity issues, How to handle them?
    date_applied = models.DateTimeField(auto_now_add=True)
    gig =  models.ForeignKey(Gig, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=(("Submitted", "Submitted"), ("Pending", "Pending"), ("Accepted", "Accepted"), ("Rejected", "Rejected")), default="Submitted")
    
    
    class Meta:
        unique_together = (("gig", "musician"),)

    def __str__(self):
        return f"Job by - {self.client} - {self.musician} applied for {self.gig.title} on {self.date_applied}"
  

#Not Complete!
class Message(models.Model):
    sender = models.OneToOneField(User, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.OneToOneField(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} to {self.recipient.username}"

#Not Complete!
class Notification(models.Model):
    recipient = models.OneToOneField(User, on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient.username}"

#Not Complete!
class Review(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="given_reviews")
    musician = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_reviews")
    gig = models.OneToOneField(Gig, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(choices=[(1, "1 Star"), (2, "2 Stars"), (3, "3 Stars"), (4, "4 Stars"), (5, "5 Stars")])
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.username} on {self.musician.username}"
