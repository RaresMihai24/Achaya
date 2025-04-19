from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)

class Race(models.Model):
    name       = models.CharField(max_length=50, unique=True)
    base_res   = models.FloatField(default=0)
    base_vit   = models.FloatField(default=0)
    base_dre   = models.FloatField(default=0)
    base_gal   = models.FloatField(default=0)
    base_sar   = models.FloatField(default=0)
    base_tra   = models.FloatField(default=0)
    image      = models.ImageField(
        upload_to='race_images/',
        blank=True,
        null=True,
        help_text="Upload a representative image for this race"
    )

    def __str__(self):
        return self.name

class Dragon(models.Model):
    name = models.CharField(max_length=100, unique=True)
    race  = models.ForeignKey(Race, on_delete=models.PROTECT, related_name="dragons")
    specie = models.CharField(max_length=100)
    height = models.IntegerField()
    sex = models.CharField(max_length=10)
    age = models.CharField(max_length=50)  # or models.IntegerField(), adjust as needed
    weight = models.FloatField()
    born_on = models.DateField()
    energy = models.FloatField(default=100)
    moral = models.FloatField(default=100)
    health = models.FloatField(default=100)
    # Genetic stats
    res   = models.FloatField()
    vit   = models.FloatField()
    dre   = models.FloatField()
    gal   = models.FloatField()
    sar   = models.FloatField()
    tra   = models.FloatField()
    # Calculated ability stats
    ac_res = models.FloatField(default=0)
    ac_vit = models.FloatField(default=0)
    ac_dre = models.FloatField(default=0)
    ac_gal = models.FloatField(default=0)
    ac_sar = models.FloatField(default=0)
    ac_tra = models.FloatField(default=0)

    GP = models.FloatField(default=0)
    BLUP = models.FloatField(default=0)
    mother = models.CharField(max_length=100, blank=True, null=True)
    father = models.CharField(max_length=100, blank=True, null=True)
    producer = models.CharField(max_length=100, blank=True, null=True)
    sleep = models.BooleanField(default=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # or 'users.User' if you’re using a custom user model
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='dragons',
    )

    def save(self, *args, **kwargs):
        if not self.pk:  # only on first creation
            self.res = self.race.base_res
            self.vit = self.race.base_vit
            self.dre = self.race.base_dre
            self.gal = self.race.base_gal
            self.sar = self.race.base_sar
            self.tra = self.race.base_tra
        super().save(*args, **kwargs)

    class Meta:
        db_table = "dragons"  # Use your existing table name

    def __str__(self):
        return self.name

class PlayerManager(BaseUserManager):
    def create_user(self, mail, name, password=None):
        if not mail:
            raise ValueError("Users must have an email address")
        user = self.model(
            mail=self.normalize_email(mail),
            name=name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mail, name, password):
        user = self.create_user(mail, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Player(AbstractBaseUser, PermissionsMixin):
    mail = models.EmailField(unique=True, default='')
    name = models.CharField(max_length=255, default='')
    pwd = models.CharField(max_length=128, default='', blank=True)
    # … any other fields you need …
    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)

    USERNAME_FIELD  = 'mail'
    REQUIRED_FIELDS = ['name']

    objects = PlayerManager()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.mail
		