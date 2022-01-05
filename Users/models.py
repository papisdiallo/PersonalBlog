from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import pre_save
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        username,
        password=None,
        active=True,
        is_staff=False,
        is_admin=False,
    ):
        if not email:
            raise ValueError("User must have an email address!")
        if not password:
            raise ValueError("User must set a password !")
        if not username:
            raise ValueError("You must provide a username!")

        user = self.model(email=self.normalize_email(email), username=username)
        user.admin = is_admin
        user.staff = is_staff
        user.is_active = active
        user.set_password(password)
        user.save(using=self._db)

        return user

    # creating a staff user
    def create_staffuser(self, email, username, password=None):
        user = self.create_user(
            email,
            username=username,
            password=password,
            is_staff=True,  # allows the user to be a staff
        )
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email, username=username, password=password, is_staff=True, is_admin=True
        )
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)  # is able to login
    staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_developer_account = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    # working primarily with email and not username
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

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
    def tokens(self):
        tokens = RefreshToken.for_user(self)
        return {
            "refresh": tokens,
            "access_token": tokens.access_token,
        }

    @property
    def active(self):
        return self.is_active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin


class Profile(models.Model):
    choices = (
        ("Developer", "developer"),
        ("Software Engineer", "Software engineer"),
        ("Data Analyst", "Data Analyst"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        default="/media/default.jpg", upload_to="media/profile_pics"
    )
    city = models.CharField(max_length=100, blank=True, null=True)
    profession = models.CharField(max_length=40, choices=choices, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
