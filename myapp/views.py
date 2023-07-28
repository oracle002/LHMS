from django.contrib.auth import logout
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Farmer, Cattle,Disease, Vaccines,Vaccination_Reg,Vaccination_S,ArtificialInsemination
from datetime import date, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import date, timedelta
from django.db.models.signals import post_save

# Create your views here.
def index(request):
    num_users = Farmer.objects.count()
    num_cattles = Cattle.objects.count()
    num_reg = Vaccination_Reg.objects.count()
    # Pass the num_users variable to your template context
    context = {'num_users': num_users, 'num_cattles': num_cattles, 'num_reg': num_reg}
    return render(request,"index.html", context)

def about(request):
    num_users = Farmer.objects.count()
    num_cattles=Cattle.objects.count()
    num_reg=Vaccination_Reg.objects.count()
    # Pass the num_users variable to your template context
    context = {'num_users': num_users,'num_cattles': num_cattles,'num_reg':num_reg}
    return render(request, 'about.html', context)


def reg(request):
    if request.method == "POST":
        a = request.POST.get('firstname')
        b = request.POST.get('lastname')
        c = request.POST.get('email')
        d = request.POST.get('phonenumber')
        e = request.POST.get('addressline1')
        f = request.POST.get('addressline2')
        g = request.POST.get('place')
        h = request.POST.get('pin')
        i = request.POST.get('password')

        # check if user already exists based on email
        if Farmer.objects.filter(email=c).exists():
            error_msg = "This email address is already registered"
            return render(request, "reg.html", {'error_msg': error_msg})

        # create new user
        sa = Farmer(firstname=a, lastname=b, email=c, phonenumber=d, addressline1=e, addressline2=f, place=g, pin=h,
                    password=i)
        sa.save()

        # redirect to login page
        return render(request, "signin.html")

    return render(request, "reg.html")

def sign(request):
    if request.method == "POST":
        userid = request.POST.get('username')
        pswd = request.POST.get('pass')
        urec = Farmer.objects.filter(email=userid,password=pswd)
        if urec.exists():
            for j in urec:
               id=j.id
               f=j.firstname
               p=j.phonenumber
            request.session['id']=id
            request.session['username']=userid
            request.session['password']=pswd
            request.session['firstname']=f
            request.session['phno'] = p
            return render(request, "service.html")
        else:
            error_msg = "Invalid username or password."
            return render(request, "signin.html", {'error_msg': error_msg})

    return render(request, "signin.html")


def service(request):
    return render(request,"service.html")

def cattlereg(request):
    username = request.session.get('username')
    if not username:
        messages.error(request, 'You must be logged in to access this page.')
        return redirect('/signin/')
    if request.method == "POST":
        tagno = request.POST.get('tagno')
        breed = request.POST.get('breed')
        gender = request.POST.get('gender')
        dob_str = request.POST.get('dob')
        weight = request.POST.get('weight')
        color = request.POST.get('color')
        age_months = request.POST.get('age_months')
        age_years = request.POST.get('age_years')

        # Validate date of birth
        try:
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
            if dob >= datetime.now().date():
                raise ValidationError("Date of birth cannot be in the future.")
        except ValueError:
            messages.error(request, 'Invalid date of birth format. Please use YYYY-MM-DD.')
            return render(request, "4042.html")
        except ValidationError as e:
            messages.error(request, str(e))
            return render(request, "4042.html")

        # Get the current session username and firstname
        firstname = request.session.get('firstname')

        # Retrieve the matching Farmer object
        owner = Farmer.objects.get(email=username)

        # Create and save the Cattle object with the retrieved Farmer object as the owner
        cattle = Cattle(tagno=tagno, breed=breed, gender=gender, dob=dob, weight=weight, color=color, owner=owner, age=age_months, age_years=age_years)
        if Cattle.objects.filter(tagno=tagno).exists():
            messages.error(request, 'Cattle tag number already exists.')
            return render(request, "4042.html")
        cattle.save()

        messages.success(request, 'Cattle registration successful.')
        return render(request, "4042.html")
    return render(request, "4042.html")


def test(request):
    return render(request, "404.html")
def profile(request):
    username = request.session.get('username')
    if not username:
        messages.error(request, 'You must be logged in to access this page.')
        return redirect('/signin/')
    farmer_id = request.session.get('id')
    farmer = Farmer.objects.get(id=farmer_id)
    cattles = Cattle.objects.filter(owner=farmer)

    return render(request, "profile.html", {'farmer': farmer, 'cattles': cattles})
def logout_view(request):
    logout(request)
    return redirect('index')
def vaccinate(request):
    username = request.session.get('username')
    if not username:
        messages.error(request, 'You must be logged in to access this page.')
        return redirect('/signin/')
    username = request.session.get('id')
    cattles = Cattle.objects.filter(owner=username)
    vaccines = Vaccines.objects.all()
    diseases = Disease.objects.all()
    context = {'cattles': cattles, 'diseases': diseases, 'vaccines': vaccines}
    return render(request, 'vaccinate.html', context)

def view_vaccine(request, id):
    username = request.session.get('username')
    if not username:
        messages.error(request, 'You must be logged in to access this page.')
        return redirect('/signin/')
    # Get the cattle object for the given id
    cattle = Cattle.objects.get(id=id)

    # Store the cattle's id in the session
    request.session['cattleid'] = cattle.id

    # Get the cattle's age
    age = cattle.age
    tagno=cattle.tagno

    # Get all the vaccination registrations for the cattle
    vaccination_registrations = Vaccination_Reg.objects.filter(cattleid=cattle)

    # Get a list of diseases for which the cattle has already been vaccinated
    vaccinated_diseases = [vr.diseaseid for vr in vaccination_registrations]

    # Get the vaccination status for each disease for the cattle
    vaccination_statuses = {}
    vaccination_statuses_query = Vaccination_S.objects.filter(cattleid=cattle)
    for vs in vaccination_statuses_query:
        disease_id = vs.diseaseid.id
        if vs.firstdose_status and vs.seconddose_status:
            vaccination_statuses[disease_id] = 2
        elif vs.firstdose_status:
            vaccination_statuses[disease_id] = 1
        else:
            vaccination_statuses[disease_id] = 0

    # Get a list of diseases for which the cattle is eligible for the first dose
    eligible_for_first_dose = Disease.objects.filter(firstdose__lte=age).exclude(disease__in=vaccinated_diseases)

    # Get a list of diseases for which the cattle is eligible for the second dose
    eligible_for_second_dose = []
    for disease in vaccinated_diseases:
        if disease.id in vaccination_statuses and vaccination_statuses[disease.id] == 1:
            eligible_for_second_dose_query = Disease.objects.filter(id=disease.id, boosterdose__gte=age)
            if eligible_for_second_dose_query.exists():
                # Check if the cattle has already received the second dose or if it has already been requested
                if Vaccination_Reg.objects.filter(cattleid=cattle, diseaseid=disease, dose=2).exists() or \
                        Vaccination_Reg.objects.filter(cattleid=cattle, diseaseid=disease, dose=1,
                                                       status=False).exists():
                    continue
                eligible_for_second_dose.append(eligible_for_second_dose_query.first())

    # Get a list of cattle eligible for yearly dose
    eligible_for_yearly_dose = []
    fourth_dose_diseases = [vr.diseaseid for vr in vaccination_registrations if vr.dose == 4]
    vaccination_statuses_query = Vaccination_S.objects.filter(cattleid=cattle)
    for vs in vaccination_statuses_query:
        if vs.eligibility_yd and vs.ldate_approved is not None:
            today = date.today()
            if today >= vs.ldate_approved + timedelta(days=365):
                if vs.diseaseid not in fourth_dose_diseases:
                    eligible_for_yearly_dose.append({
                        'id': vs.diseaseid.id,
                        'disease': vs.diseaseid.disease,
                        'vaccine': vs.diseaseid.vaccine,
                        'last_vaccination_date': vs.ldate_approved,
                    })

    # Get all the available vaccines
    vaccines = Vaccines.objects.all()


    context = {
        'cattle': cattle,
        'tagno': tagno,
        'eligible_for_first_dose': eligible_for_first_dose,
        'eligible_for_second_dose': eligible_for_second_dose,
        'vaccination_statuses': vaccination_statuses,
        'eligible_for_yearly_dose': eligible_for_yearly_dose,
        'vaccines': vaccines,
    }


    # Pass the relevant data to the template for rendering
    return render(request, 'vaccinate1.html', context)

def booking(request, disease_id):
    disease = Disease.objects.get(id=disease_id)
    dis = disease.disease
    vac = disease.vaccine
    farmer_id = request.session.get('id')
    farmer = Farmer.objects.filter(id=farmer_id).first()
    farmer_name = f"{farmer.firstname} {farmer.lastname}"
    cattle = Cattle.objects.get(id=request.session.get('cattleid'))
    tagno = cattle.tagno

    # Check if booking for first or second dose
    vaccination_registrations = Vaccination_Reg.objects.filter(cattleid=cattle, diseaseid=disease)
    if vaccination_registrations.exists():
        # Already registered for the first dose
        dose = 2 if vaccination_registrations.first().dose == 1 else 1

        # Check if eligible for second dose
        first_dose_date_approved = vaccination_registrations.first().date_approved
        six_months_from_first_dose = first_dose_date_approved + timedelta(days=180)
        if dose == 2 and date.today() < six_months_from_first_dose:
            # Not eligible for second dose yet
            messages.error(request, 'Not Eligible for Second Dose Yet.')
            return HttpResponseRedirect(f'/viewv/{cattle.id}/')
    else:
        # First time registration for the disease, set dose as 0
        dose = 0

    # Create a new Vaccination_Reg object
    sa = Vaccination_Reg(cattleid=cattle, cattletagno=tagno, farmerid=farmer, farmer_name=farmer_name,
                                      diseaseid=disease, disease=dis, vaccine=vac, date_requested=date.today(),
                                      dose=dose, status=False)
    sa.save()

    cattles = Cattle.objects.filter(owner=farmer_id)
    vaccines = Vaccines.objects.all()
    diseases = Disease.objects.all()
    context = {'cattles': cattles, 'diseases': diseases, 'vaccines': vaccines}
    return HttpResponseRedirect(f'/viewv/{cattle.id}/')



def booking2(request, disease_id):
    disease = Disease.objects.get(id=disease_id)
    dis = disease.disease
    vac = disease.vaccine
    farmer_id = request.session.get('id')
    farmer = Farmer.objects.filter(id=farmer_id).first()
    farmer_name = f"{farmer.firstname} {farmer.lastname}"
    cattle = Cattle.objects.get(id=request.session.get('cattleid'))
    tagno = cattle.tagno
    dose = 4

    # Create a new Vaccination_Reg object
    sa = Vaccination_Reg(cattleid=cattle, cattletagno=tagno, farmerid=farmer, farmer_name=farmer_name,
                                      diseaseid=disease, disease=dis, vaccine=vac, date_requested=date.today(),
                                      dose=dose, status=False)
    sa.save()

    cattles = Cattle.objects.filter(owner=farmer_id)
    vaccines = Vaccines.objects.all()
    diseases = Disease.objects.all()
    context = {'cattles': cattles, 'diseases': diseases, 'vaccines': vaccines}
    return HttpResponseRedirect(f'/viewv/{cattle.id}/')



def vaccination_history(request):
    username = request.session.get('username')
    if not username:
        messages.error(request, 'You must be logged in to access this page.')
        return redirect('/signin/')
    farmer_id = request.session.get('id')
    farmer = Farmer.objects.get(id=farmer_id)
    cattles = Cattle.objects.filter(owner=farmer_id)
    vaccination_data = []
    ai_data = []
    for cattle in cattles:
        cattle_vaccinations = Vaccination_Reg.objects.filter(cattleid=cattle)
        vaccination_data.append({'cattle': cattle, 'vaccinations': cattle_vaccinations})
    for cattle in cattles:
        cattle_ai = ArtificialInsemination.objects.filter(cattleid=cattle)
        ai_data.append({'cattle': cattle, 'artificialinsemination': cattle_ai})
    return render(request, 'History.html', {'vaccination_data': vaccination_data, 'ai_data': ai_data, 'farmer': farmer})



def changepassword(request):
    if request.method == "POST":
        email = request.POST.get("email")
        newpass = request.POST.get("t2")
        confrmpass = request.POST.get("t3")

        try:
            farmer = Farmer.objects.get(email=email)
        except Farmer.DoesNotExist:
            return render(request, "chpswd.html")

        if newpass == confrmpass:
            farmer.password = newpass
            farmer.save()
            return render(request, 'index.html')
        else:
            return render(request, "chpswd.html")

    return render(request, "chpswd.html")






from datetime import date, timedelta

def ai(request):
    username = request.session.get('username')
    if not username:
        messages.error(request, 'You must be logged in to access this page.')
        return redirect('/signin/')
    username = request.session.get('id')
    cattles = Cattle.objects.filter(owner=username, gender='Female', age__gte=12)
    vaccines = Vaccines.objects.all()
    diseases = Disease.objects.all()

    # filter cattles by pregnant_status and time since date_approved
    filtered_cattles = []
    for cattle in cattles:
        ai_records = ArtificialInsemination.objects.filter(cattleid=cattle)
        if ai_records:
            last_ai_record = ai_records.latest('date_approved')
            if last_ai_record.pregnant_status is False:
                filtered_cattles.append(cattle)
            elif last_ai_record.pregnant_status is True and last_ai_record.date_approved + timedelta(days=365) <= date.today():
                filtered_cattles.append(cattle)
        else:
            filtered_cattles.append(cattle)

    context = {'cattles': filtered_cattles, 'diseases': diseases, 'vaccines': vaccines}
    return render(request, 'ai.html', context)


def book_ai(request, cattle_id):
    farmer_id = request.session.get('id')
    ai = ArtificialInsemination.objects.create(
        cattleid_id=cattle_id,
        farmerid_id=farmer_id,
        date_requested=date.today(),
    )
    ai.save()
    return HttpResponseRedirect('/ai/')

def update_pregnancy_status(request, ai_id):
    ai = ArtificialInsemination.objects.get(id=ai_id)
    if request.method == 'POST' and ai.pregnant_status is None:
        pregnancy_status = request.POST.get('pregnancy_status')
        if pregnancy_status == 'True':
            ai.pregnant_status = True
        elif pregnancy_status == 'False':
            ai.pregnant_status = False
        ai.save()
    return redirect('/vaccination-history/')

def delete_cattle(request, cattle_id):
    cattle = get_object_or_404(Cattle, id=cattle_id)
    if request.method == 'POST':
        cattle.delete()
        return redirect('/profile/')





@receiver(post_save, sender=Vaccination_Reg)
def create_or_update_vaccination_s(sender, instance, created, **kwargs):
    # Check if the instance was just created or updated
    if created:
        # Check if a record with the same cattleid and diseaseid already exists in Vaccination_S
        existing_vaccination_s = Vaccination_S.objects.filter(cattleid=instance.cattleid, diseaseid=instance.diseaseid).first()
        if existing_vaccination_s:
            # Record already exists, don't create a new one
            return
        # Create a new Vaccination_S object
        new_vaccination_s = Vaccination_S(
            cattleid=instance.cattleid,
            diseaseid=instance.diseaseid,
            firstdose_status=(instance.dose == 1),
            seconddose_status=(instance.dose == 2),
            eligibility_yd=False,
        )
        new_vaccination_s.save()
    else:
        # The instance was updated, find the corresponding Vaccination_S object and update it
        vaccination_s = Vaccination_S.objects.filter(cattleid=instance.cattleid, diseaseid=instance.diseaseid).first()
        if vaccination_s:
            vaccination_s.firstdose_status = (instance.dose == 1)
            vaccination_s.seconddose_status = (instance.dose == 2)
            vaccination_s.save()

@receiver(post_save, sender=Vaccination_Reg)
def update_vaccination_s(sender, instance, **kwargs):
    # Check if a corresponding Vaccination_S record exists
    vaccination_s = Vaccination_S.objects.filter(cattleid=instance.cattleid, diseaseid=instance.diseaseid).first()
    if vaccination_s:
        # Update the appropriate fields based on the dose status
        if instance.dose == 1 and instance.status:
            vaccination_s.firstdose_status = True
            vaccination_s.fdate_approved = instance.date_approved
        elif instance.dose == 2 and instance.status:
            vaccination_s.sdate_approved = instance.date_approved
            vaccination_s.seconddose_status = True
            if vaccination_s.firstdose_status:
                vaccination_s.eligibility_yd = True
            vaccination_s.firstdose_status = True
            vaccination_s.ldate_approved = instance.date_approved
        elif instance.dose == 3 and instance.status:
            vaccination_s.seconddose_status = True
            if vaccination_s.firstdose_status:
                vaccination_s.eligibility_yd = True
            vaccination_s.firstdose_status = True
            vaccination_s.ldate_approved = instance.date_approved
        vaccination_s.save()









#@receiver(post_save, sender=Vaccination_Reg)
#def update_vaccination_s(sender, instance, **kwargs):
    # Check if a corresponding Vaccination_S record exists
    #vaccination_s = Vaccination_S.objects.filter(cattleid=instance.cattleid, diseaseid=instance.diseaseid).first()
    #if vaccination_s:
        # Update the appropriate field based on the dose status
       # if instance.dose == 1:
         #   vaccination_s.fdate_approved = instance.date_approved
      #  elif instance.dose == 2 and not vaccination_s.seconddose_status:
       #     vaccination_s.sdate_approved = instance.date_approved
       #     vaccination_s.firstdose_status=True
        #    if instance.status:
          #      vaccination_s.ldate_approved = instance.date_approved
       # vaccination_s.save()