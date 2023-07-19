from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # a admin user; non super-user

    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.last_name

    def __str__(self):
        return self.email


class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company")
    name = models.CharField(max_length=100)
    leaves = models.IntegerField(default=20)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, )
    position = models.ForeignKey("CompanyPosition", on_delete=models.SET_NULL, null=True)
    leave_count = models.FloatField()
    time_shift = models.ForeignKey("EmployeeShift", on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('user', 'company')]

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class EmployeeShift(models.Model):
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE, related_name='shifts')
    name = models.CharField(max_length=200, null=True, blank=True)
    from_shift = models.TimeField()
    to_shift = models.TimeField()

    def __str__(self):
        return str(self.id)


class CompanyPosition(models.Model):
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE, related_name='positions')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
