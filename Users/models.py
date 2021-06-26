from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("User must have an email address!")
        if not password:
            raise ValueError("User must set a password !")
        if not username:
            raise ValueError("You must provide a username Par force!")

        user = self.model(
            email = self.normalize_email(email),
            username = username

        )
        user.admin = is_admin
        user.staff = is_staff
        user.active = is_active
        user.set_password(password)
        user.save(using=self._db)

        return user
   

    #creating a staff user 
    def create_staffuser(self, email, username, password=None):
        user = self.create_user(
            email,
            username=username,
            password=password,
            is_staff=True    #allows the user to be a staff
        )
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            username=username,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user



class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)    
    active = models.BooleanField(default=True) #is able to login 
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    # working primarily with email and not username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def get_full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + self.last_name
        return self.username

    def get_short_name(self):
        return self.last_name if self.last_name else self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin



 