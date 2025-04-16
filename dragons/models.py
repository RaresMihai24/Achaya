from django.db import models

class Dragon(models.Model):
    name = models.CharField(max_length=100, unique=True)
    race = models.CharField(max_length=100)
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
    res = models.FloatField(default=0)
    vit = models.FloatField(default=0)
    dre = models.FloatField(default=0)
    gal = models.FloatField(default=0)
    sar = models.FloatField(default=0)
    tra = models.FloatField(default=0)
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

    class Meta:
        db_table = "dragons"  # Use your existing table name

    def __str__(self):
        return self.name
