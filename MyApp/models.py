from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Group, Permission
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        USER = "USER", "User"
        OFFICER = "OFFICER", "Officer"

    role = models.CharField(
        max_length=50,
        choices=Role.choices,
        default=Role.USER,
    )
    
    # Add a related_name for groups
    groups = models.ManyToManyField(
        Group,
        verbose_name="Groups",
        blank=True,
        related_name="myapp_user_set",
        related_query_name="user",
    )

    # Add a related_name for user_permissions
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="User Permissions",
        blank=True,
        related_name="myapp_user_set",
        related_query_name="user",
    )

      
class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=122)
    place = models.CharField(max_length=122)
    Description= models.CharField(max_length=122)
    PhysicalEvidence= models.CharField(max_length=122)
    fileUpload = models.ImageField(upload_to='evidence', blank=True)


    def __str__(self):
        return self.name + ": " + str(self.fileUpload)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15,blank=True)
    address = models.TextField(max_length=100)

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username} at {self.created_at}"

from django.db import models

class Criminal(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='criminal_photos/')
    description = models.TextField()

    def __str__(self):
        return self.name
    
class MissingPerson(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    description = models.TextField()
    photo = models.ImageField(upload_to='missing_persons/')
    status = models.CharField(max_length=20, choices=[('reported', 'Reported'),('searching', 'Searching'), ('found', 'Found')], default='reported')

    def __str__(self):
        return self.name
    
class PoliceStation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    station_id = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    branch = models.CharField(max_length=100)
    

    def __str__(self):
        return f"{self.branch} - {self.station_id}"


