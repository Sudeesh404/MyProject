from django.db import models
# from django.contrib.auth.models import User
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



