from django.db import models
from django.utils import timezone
import hashlib
import random
import string
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone number must be set")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = PhoneNumberField(unique=True)
    invite_code = models.CharField(max_length=6, unique=True)
    verification_code_hash = models.CharField(max_length=128, blank=True, null=True)
    code_sent_time = models.DateTimeField(null=True, blank=True)
    referrer = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='invited_users')

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.id and not self.invite_code:
            self.invite_code = "".join(
                random.choices(string.ascii_letters + string.digits, k=6)
            )
        super(User, self).save(*args, **kwargs)

    def set_verification_code(self, code):
        self.verification_code_hash = hashlib.sha256(code.encode()).hexdigest()

    @staticmethod
    def check_verification_code(code, hash):
        return hashlib.sha256(code.encode()).hexdigest() == hash
