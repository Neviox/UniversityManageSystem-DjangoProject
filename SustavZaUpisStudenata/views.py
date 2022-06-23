from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Korisnici, Predmeti, Upisi,Uloge
from .forms import LoginForm, RegisterForm, StudentCreate, SubjectCreate, SubjectView
from .decorators import profesor_or_admin, student
from collections import OrderedDict

# Create your views here.



def home(request):
    return render(request,"pages/index.html")

##LOGIN
def login_page(request):
    loggedUser = request.user
    if loggedUser.id:
        return redirect("/")

    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }

    if form.is_valid():
        username  = form.cleaned_data.get("Email")
        password  = form.cleaned_data.get("Password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            context["login_error"] = "Failed to login, wrong username and/or password!"
            print("Error")
    return render(request, "project/login.html", context)


##REGISTER
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    
    if form.is_valid():
        form.save()
        return redirect('/login')
    return render(request, "project/register.html", context)

##LOGOUT
@login_required(login_url='/login')
def logout_page(request):
    logout(request)
    return redirect('/login')

##STUDENTS----------------------------------------------------------------------------------------
@profesor_or_admin
def students_page(request):
    context = {}

    context['students'] = Korisnici.objects.filter(Roles_id=1)
    return render(request, "project/students.html", context)

##CREATE STUDENT
@profesor_or_admin
def create_student(request):
    uploadForm = StudentCreate()
    if request.method == 'POST':
        uploadForm = StudentCreate(request.POST)
        if uploadForm.is_valid():
            uploadForm.save()
            return redirect('/students')
        else:
            return HttpResponse("""Wrong form!""")
    else:
        return render(request, 'project/student_create.html', {'student_form':uploadForm})


#DELETE
@profesor_or_admin
def delete_student(request, student_id):
    student_id = int(student_id)
    try:
        student = Korisnici.objects.get(id = student_id)
    except Korisnici.DoesNotExist:
        return redirect('/students')
    student.delete()
    return redirect('/students')


#STUDENTPAGE
@login_required(login_url='/login')
def view_student(request, student_id):

    if request.user.id != student_id and request.user.Roles_id == 1:
        return redirect('/')

    context = {}
    student_id = int(student_id)
    student = Korisnici.objects.get(pk=student_id)    

    enrollments = Upisi.objects.filter(StudentID_id=student.id)
    enrolled_subject_ids = []
    passed_enrolled_subject_ids = []
    for enrolled in enrollments:
        enrolled_subject_ids.append(enrolled.PredmetID_id)
        if (enrolled.Status == "Polozen" or enrolled.Status == "Izgubio potpis"):
            passed_enrolled_subject_ids.append(enrolled.PredmetID_id)

    # enrolled subjects by semester
    enrolled_subjects_by_semester = {}
    enrolled_subjects = Predmeti.objects.filter(pk__in=enrolled_subject_ids)
    for enrolled_subject in enrolled_subjects:
        if student.Status == "Redovni":
            semester_number = enrolled_subject.Sem_redovni
        elif student.Status == "Izvanredni":
            semester_number = enrolled_subject.Sem_izvanredni            
        if semester_number in enrolled_subjects_by_semester:
            enrolled_subjects_by_semester[semester_number].append(enrolled_subject)
        else:
            enrolled_subjects_by_semester[semester_number] = [enrolled_subject]

    # not enrolled subjects
    not_enrolled_subjects = Predmeti.objects.filter().exclude(pk__in=enrolled_subject_ids)

    context["student"] = student
    context["enrolled_subjects_by_semester"] = OrderedDict(sorted(enrolled_subjects_by_semester.items()))
    context["not_enrolled_subjects"] = not_enrolled_subjects    
    context["passed_enrolled_subject_ids"] = passed_enrolled_subject_ids
    context["student_id"] = student_id
    
    return render(request, 'project/student_view.html', context)

##SUBJECT----------------------------------------------------------------------------------------------------------------------------
@profesor_or_admin
def subjects_page(request):
    context = {}
    context["subjects"] = Predmeti.objects.all()
    return render(request, "project/subjects.html", context)


##CREATE SUBJECT
@profesor_or_admin
def create_subject(request):
    uploadForm = SubjectCreate()
    if request.method == 'POST':
        uploadForm = SubjectCreate(request.POST)
        if uploadForm.is_valid():
            uploadForm.save()
            return redirect('/subjects')
        else:
            return HttpResponse("""Wrong form!""")
    else:
        return render(request, 'project/subject_create.html', {'subject_form':uploadForm})

##EDIT SUBJECT
@profesor_or_admin
def edit_subject(request, subject_id):
    subject_id = int(subject_id)
    try:
        subject = Predmeti.objects.get(id = subject_id)
    except Predmeti.DoesNotExist:
        return redirect('/subjects')
    subject_form = SubjectCreate(request.POST or None, instance = subject)
    if subject_form.is_valid():
       subject_form.save()
       return redirect('/subjects')
    return render(request, 'project/subject_edit.html', {'subject_form':subject_form,})

##DELETE SUBJECT
@profesor_or_admin
def delete_subject(request, subject_id):
    subject_id = int(subject_id)
    try:
        subject = Predmeti.objects.get(id = subject_id)
    except Predmeti.DoesNotExist:
        return redirect('/subjects')
    subject.delete()
    return redirect('/subjects')

##SUBJECT PAGE
@profesor_or_admin
def view_subject(request, subject_id):
    subject_id = int(subject_id)
    try:
        subject = Predmeti.objects.get(id = subject_id)
    except Predmeti.DoesNotExist:
        return redirect('/subjects')
    subject_form = SubjectView(request.POST or None, instance = subject)
    return render(request, 'project/subject_view.html', {'subject_form':subject_form})

##ENROLL SUBJECT
@student
def enroll_subject(request):
    student = Korisnici.objects.get(pk = int(request.POST.get("student_id", -1)))
    subject = Predmeti.objects.get(pk = int(request.POST.get("subject_id", -1)))
    Upisi.objects.create(StudentID_id = student.id, PredmetID_id = subject.id, Status = "Upisan")    
    return redirect('/student_view/'+str(student.id))

##DISENROLL SUBJECT
@student
def disenroll_subject(request):
    student = Korisnici.objects.get(pk = int(request.POST.get("student_id", -1)))
    subject = Predmeti.objects.get(pk = int(request.POST.get("subject_id", -1)))
    enrollment = Upisi.objects.filter(StudentID_id = student.id, PredmetID_id = subject.id)
    enrollment.delete()
    return redirect('/student_view/'+str(student.id))

##MARK AS PASSED
@profesor_or_admin
def mark_subject_as_passed(request):
    student = Korisnici.objects.get(pk = int(request.POST.get("student_id", -1)))
    subject = Predmeti.objects.get(pk = int(request.POST.get("subject_id", -1)))
    enrollment = Upisi.objects.filter(StudentID_id = student.id, PredmetID_id = subject.id)
    enrollment.update(Status="Polozen")
    return redirect('/student_view/'+str(student.id))

##MARK AS NOT PASSED
@profesor_or_admin
def mark_subject_as_not_passed(request):    
    student = Korisnici.objects.get(pk = int(request.POST.get("student_id", -1)))
    subject = Predmeti.objects.get(pk = int(request.POST.get("subject_id", -1)))
    enrollment = Upisi.objects.filter(StudentID_id = student.id, PredmetID_id = subject.id)
    enrollment.update(Status="Nije upisan")
    return redirect('/student_view/'+str(student.id))

##MARK AS LOST
@profesor_or_admin
def mark_subject_as_lost(request):    
    student = Korisnici.objects.get(pk = int(request.POST.get("student_id", -1)))
    subject = Predmeti.objects.get(pk = int(request.POST.get("subject_id", -1)))
    enrollment = Upisi.objects.filter(StudentID_id = student.id, PredmetID_id = subject.id)
    enrollment.update(Status="Izgubio potpis")
    return redirect('/student_view/'+str(student.id))

##STUDENT LIST BY SUBJECT
@profesor_or_admin
def student_list(request,subject_id):
    context = {}
    list=[]
    subject = Upisi.objects.filter(PredmetID_id = subject_id)
    students= Korisnici.objects.all()
    for s in students:
        for p in subject:
            if s.id == p.StudentID_id and p.Status=="Upisan":
                list.append(s)
    
    context["status"] = list
    context["subject"] = Predmeti.objects.filter(id=subject_id)
    return render(request, "project/student_list.html", context)
 
 ##CHANGE STATUS ------------------------------------------------->   
@profesor_or_admin
def lost_signature(request,subject_id):
    context = {}
    list=[]
    subject=Predmeti.objects.filter(id=subject_id)
    status=Upisi.objects.filter(Status="Izgubio potpis")
    for p in subject:
        for s in status:
            if p.id==s.PredmetID_id:
                list.append(s)
    
    context["upisi"] = list
    return render(request,"project/filterlist.html",context)


@profesor_or_admin
def enrolled(request,subject_id):
    context = {}
    list=[]
    subject=Predmeti.objects.filter(id=subject_id)
    status=Upisi.objects.filter(Status="Upisan")
    for p in subject:
        for s in status:
            if p.id==s.PredmetID_id:
                list.append(s)

    context["upisi"] = list
    return render(request,"project/filterlist.html",context)


@profesor_or_admin
def passed(request,subject_id):
    context = {}
    list=[]
    subject=Predmeti.objects.filter(id=subject_id)
    status=Upisi.objects.filter(Status="Polozen")
    for p in subject:
        for s in status:
            if p.id==s.PredmetID_id:
                list.append(s)
                
    context["upisi"] = list
    return render(request,"project/filterlist.html",context)

##PROFESOR PAGE -----------------------------------------------------------------------------------------------------------------
@profesor_or_admin
def profesor_page(request):
    context = {}
    context['students'] = Korisnici.objects.filter(Roles_id=2)
    return render(request, "project/students.html", context)

##EDIT USERS AS ADMIN ----------------------------------------------------------------------------
@profesor_or_admin
def edit_user(request, user_id):
    user_id = int(user_id)
    try:
        user = Korisnici.objects.get(id = user_id)
    except Korisnici.DoesNotExist:
        return redirect('/profesor')
    user_form = StudentCreate(request.POST or None, instance = user)
    if user_form.is_valid():
       user_form.save()
       return redirect('/profesors')
    return render(request, 'project/user_edit.html', {'user_form':user_form})

