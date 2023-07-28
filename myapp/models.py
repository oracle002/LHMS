from django.db import models
from datetime import date
import calendar
cat=(
    ('normal','normal'),
    ('mixed','mixed'),
)
sex=(
    ('male','male'),
    ('female','female'),
    ('both','both'),
)
STATUS_CHOICES = (
        (False, 'Pending'),
        (True, 'Approved'),
    )
DOSE_CHOICES = (
    (0, 'Pending dose'),
    (1, 'First dose'),
    (2, 'Second dose'),
    (3, 'Yearly dose'),
    (4, 'Pending yearly dose'),
)


# Create your models here.
class Vaccines(models.Model):
    vaccine=models.CharField(max_length=28)
    catagory=models.CharField(max_length=28,choices=cat)
    manfacture=models.CharField(max_length=28,blank=True)
    def __str__(self):
        return self.vaccine



class Disease(models.Model):
    disease=models.CharField(max_length=40)
    vaccine=models.ForeignKey(Vaccines,blank=True, null=True, on_delete=models.CASCADE)
    firstdose=models.IntegerField()
    boosterdose=models.IntegerField()
    subsequentdose=models.IntegerField(default=12,null=True)
    def __str__(self):
        return self.disease

class Farmer(models.Model):
    firstname = models.CharField(max_length=28)
    lastname = models.CharField(max_length=28)
    email = models.CharField(max_length=28, unique=True)
    phonenumber = models.CharField(max_length=28)
    addressline1 = models.CharField(max_length=28)
    addressline2 = models.CharField(max_length=28)
    place = models.CharField(max_length=28)
    pin = models.CharField(max_length=28)
    password = models.CharField(max_length=28)

    def __str__(self):
        return self.firstname + " " + self.lastname







class Cattle(models.Model):
    tagno = models.CharField(max_length=12, unique=True)
    breed = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    dob = models.DateField(default=date.today)
    age = models.IntegerField(default=0)
    age_years = models.IntegerField(default=0)
    weight = models.IntegerField()
    color = models.CharField(max_length=50)
    owner = models.ForeignKey(Farmer, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.dob:
            # Update age and age_years based on dob
            today = date.today()
            age_in_months = (today.year - self.dob.year) * 12 + (today.month - self.dob.month)
            self.age = age_in_months
            self.age_years = age_in_months // 12

        elif self.age:
            # Update dob and age_years based on age
            today = date.today()
            dob_year = today.year - self.age_years
            dob_month = today.month - (self.age % 12)
            if dob_month <= 0:
                dob_year -= 1
                dob_month += 12
            self.dob = date(dob_year, dob_month, 1)

        elif self.age_years:
            # Update dob and age based on age_years
            today = date.today()
            dob_year = today.year - self.age_years
            dob_month = today.month
            self.dob = date(dob_year, dob_month, 1)
            age_in_months = (today.year - dob_year) * 12 + (today.month - dob_month)
            self.age = age_in_months

        super(Cattle, self).save(*args, **kwargs)


    def __str__(self):
        return self.tagno


class Vaccination_Reg(models.Model):
    cattleid = models.ForeignKey(Cattle, on_delete=models.CASCADE)
    cattletagno = models.CharField(max_length=15)
    farmerid = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    farmer_name = models.CharField(max_length=255)
    diseaseid = models.ForeignKey(Disease, on_delete=models.CASCADE)
    disease = models.CharField(max_length=40)
    vaccine = models.CharField(max_length=28)
    date_requested = models.DateField()
    date_approved = models.DateField(blank=True, null=True)
    dose = models.PositiveSmallIntegerField(choices=DOSE_CHOICES, default=0)
    status = models.BooleanField(choices=STATUS_CHOICES, default=False)


    def __str__(self):
        return f"{self.cattletagno} - {self.disease} - {self.status}"

class Vaccination_S(models.Model):
    cattleid = models.ForeignKey(Cattle, on_delete=models.CASCADE)
    diseaseid = models.ForeignKey(Disease, on_delete=models.CASCADE)
    firstdose_status = models.BooleanField(default=False)
    seconddose_status = models.BooleanField(default=False)
    eligibility_yd = models.BooleanField(default=False)
    fdate_approved = models.DateField(blank=True, null=True)
    sdate_approved = models.DateField(blank=True, null=True)
    ldate_approved = models.DateField(blank=True, null=True)


from django.utils import timezone

class Bull(models.Model):
    bull_id = models.CharField(max_length=28,)
    bull_name = models.CharField(max_length=28)
    breed = models.CharField(max_length=28,blank=True)

    def __str__(self):
        return self.bull_name

class ArtificialInsemination(models.Model):
    STATUS_AI = [
        (True, 'Pregnant'),
        (False, 'Not Pregnant'),
        (None, 'Pending Pregnancy'),
    ]

    cattleid = models.ForeignKey(Cattle, on_delete=models.CASCADE)
    farmerid = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    date_requested = models.DateField()
    date_approved = models.DateField(blank=True, null=True)
    status = models.BooleanField(default=False)
    bull = models.ForeignKey(Bull,blank=True, null=True, on_delete=models.CASCADE)
    pregnant_status = models.BooleanField(choices=STATUS_AI, default=None, null=True,blank=True)






