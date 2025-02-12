from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

# Custom Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, full_name, password=None):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        if not full_name:
            raise ValueError("Full name is required")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, full_name, password=None):
        user = self.create_user(email, username, full_name, password)
        user.is_superuser = True  # Required for Django admin (if needed later)
        user.save(using=self._db)
        return user

# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    # User authentication settings
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)  # 🚨 Admin Flag

    # Define custom manager
    objects = CustomUserManager()

    # Set email as the unique identifier instead of username
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "full_name"]

    def __str__(self):
        return self.username

@property
def is_staff(self):
    return self.is_admin  # Admins are considered staff
