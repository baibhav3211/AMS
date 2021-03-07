from django.shortcuts import render,redirect
from .models import student,attendanceclass,subject,time
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime
from .forms import AttendanceForm
# Create your views here.
dateg = datetime.date.today() - datetime.timedelta(days=1)
print("dekh")
print(dateg)
@login_required
def index(request):
    return render(request, 'home/index.html',{
        "students":student.objects.order_by('roll')
    })

@login_required
def class_date(request):
    n = timezone.now()
    k = datetime.datetime.now()
    global dateg
    print(dateg)
    status = 0
    date = datetime.date.today()
    time = k.strftime("%H%M")
    datec = datetime.date.today() - datetime.timedelta(days=1)
    if time >= "0001" and dateg == datec:
        if(date.weekday()==1 or date.weekday==3):
            status=1
        else:
            status=0
        dateg = date
        reg = attendanceclass(date = date , status = status)
        reg.save()
    ob = attendanceclass.objects.all()
    #base = datetime.datetime.today()
    #numdays=31
    #date_list = [base - datetime.timedelta(days=x) for x in range(numdays)]
    return render(request, 'home/t_class_date.html',{
        "status":ob
    })

@login_required
def sub(request):
    sub=subject.objects.order_by('sub')
    return render(request, 'home/t_clas.html',{
        "sub":sub
    })

@login_required
def a_form(request):
    form = AttendanceForm()
    if request.method == "POST":
        form=AttendanceForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            form.save()
            #messages.success(request,"Your Attendance is recorded.")
            return redirect('attend')
    return render(request,"home/attendance_form.html",{'form':form})

@login_required
def attend(request):
    name=request.user.get_full_name()
    firstname=request.user.get_short_name()
    return render(request, 'home/t_attendance.html',{
        "name":name,"firstname":firstname
    })

@login_required
def load_sub(request):
    sub_id=request.GET.get('sub_id')
    print(sub_id)
    times = time.objects.filter(sub_id=sub_id)
    return render(request, "home/sub_dropdown.html",{
        "times":times
    })
