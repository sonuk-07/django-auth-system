from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class CustomUserManager(models.Manager):
    """
    Why do we need this?
    - Django needs to know HOW to create users
    - We're changing from username to email
    - Manager handles create_user() and create_superuser()
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save regular user
        """
        if not email:
            raise ValueError('Email is required')
        # Normalize email (lowercase domain part)
        email = self.normalize_email(email)
        
        # Create user instance (not saved yet)
        user = self.model(email=email, **extra_fields)
        
        # Hash the password (NEVER store plain password)
        user.set_password(password)
        
        # Save to database
        user.save(using=self._db)
        return user
    

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create superuser for admin panel 
        """

        # Set required fields for superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        
        return self.create_user(email, password, **extra_fields)
    

#Create Custom User Model

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Why AbstractBaseUser and not AbstractUser?
    - AbstractUser: Keeps username field (we don't want it)
    - AbstractBaseUser: Minimal, we build from scratch
    
    PermissionsMixin: Adds permission-related fields
    - is_superuser, groups, user_permissions
    """

    #CORE FIELDS
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    # Status fields
    is_active = models.BooleanField(default=True)  # Can login?
    is_staff = models.BooleanField(default=False)  # Can access admin?
    is_verified = models.BooleanField(default=False)  # Email verified?

    date_joined = models.DateTimeField(default=timezone.now)


    # tell django: use email for login, not username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # email is already required by username_field

    #connect our custom manager
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    