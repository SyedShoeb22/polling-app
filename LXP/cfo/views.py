from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from lxpapp import models as LXPModel
from lxpapp import forms as LXPFORM
from django.shortcuts import render, redirect
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from social_django.models import UserSocialAuth
import json
from django.db.models import Exists, OuterRef,Case, When, Value, IntegerField,F, Value, Q, Sum, Max
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from urllib.parse import quote_plus
from django.conf import settings
@login_required    
def cfo_dashboard_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            dict={
            'total_course':0,
            'total_exam':0,
            'total_shortExam':0,
            'total_question':0,
            'total_learner':0
            }
        return render(request,'cfo/cfo_dashboard.html',context=dict)
    except:
        return render(request,'lxpapp/404page.html')
 

@login_required
def cfo_add_coursetype_view(request):
    form = LXPFORM.CourseTypeForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Course Type'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('coursetype_name')
            coursetype = LXPModel.CourseType.objects.all().filter(coursetype_name__iexact = name)
            if coursetype:
                messages.info(request, 'Course Type Name Already Exist')
                return redirect(reverse('cfo-add-coursetype'))
            try:
                coursetype = LXPModel.CourseType.objects.create(
                                            coursetype_name = name)
                coursetype.save()
                messages.success(request, "Successfully Updated")
                return HttpResponseRedirect('/cfo/cfo-view-coursetype')
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'cfo/coursetype/add_edit_coursetype.html', context)

@login_required
def cfo_update_coursetype_view(request, pk):
    instance = get_object_or_404(LXPModel.CourseType, id=pk)
    form = LXPFORM.CourseTypeForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'coursetype_id': pk,
        'page_title': 'Edit CourseType'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('coursetype_name')
            coursetype = LXPModel.CourseType.objects.all().filter(coursetype_name__iexact = name).exclude(id=pk)
            if coursetype:
                messages.info(request, 'Course Type Name Already Exist')
                return redirect(reverse('cfo-update-coursetype', args=[pk]))
            try:
                coursetype = LXPModel.CourseType.objects.get(id=pk)
                coursetype.coursetype_name = name
                coursetype.save()
                messages.success(request, "Successfully Updated")
                return HttpResponseRedirect('/cfo/cfo-view-coursetype')
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'cfo/coursetype/add_edit_coursetype.html', context)


@login_required
def cfo_view_coursetype_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            coursetypes = LXPModel.CourseType.objects.all()
            return render(request,'cfo/coursetype/cfo_view_coursetype.html',{'coursetypes':coursetypes})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_delete_coursetype_view(request,pk):
    try:
        if str(request.session['utype']) == 'cfo':  
            coursetype=LXPModel.CourseType.objects.get(id=pk)
            coursetype.delete()
            return HttpResponseRedirect('/cfo/cfo-view-coursetype')
        coursetypes = LXPModel.CourseType.objects.all()
        return render(request,'cfo/coursetype/cfo_view_coursetype.html',{'coursetypes':coursetypes})
    except:
        return render(request,'lxpapp/404page.html')
    
from django.db import transaction
@login_required
def cfo_add_batch_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            if request.method=='POST':
                batchForm=LXPFORM.BatchForm(request.POST)
                batchtext = batchForm.data["batch_name"]
                batch = LXPModel.Batch.objects.all().filter(batch_name__iexact = batchtext)
                if batch:
                    messages.info(request, 'Batch Name Already Exist')
                    batchForm=LXPFORM.BatchForm()
                    return render(request,'cfo/batch/cfo_add_batch.html',{'batchForm':batchForm})                  
                else:
                    coursetypeid = batchForm.data["coursetypeID"]
                    batchtable = LXPModel.Batch.objects.create(batch_name=batchtext,stdate=batchForm.data["stdate"],enddate=batchForm.data["enddate"],coursetype_id=coursetypeid)
                    batchtable.save()
                    selectedlist = request.POST.getlist('listbox1')
                    for x in selectedlist:
                        trainerid = str(x)
                        batchtrainertable = LXPModel.BatchTrainer.objects.create(batch_id=batchtable.id,trainer_id=trainerid)
                        batchtrainertable.save()
                    import json
                    json_data = json.loads(request.POST.get('myvalue'))
                    for cx in json_data:
                        a=json_data[cx]['id']
                        b=json_data[cx]['fee']
                        batchlearnertable = LXPModel.Batchlearner.objects.create(batch_id=batchtable.id,learner_id=a,fee=b)
                        batchlearnertable.save()
                    selectedlist = request.POST.getlist('listbox3')
                    for x in selectedlist:
                        modid = str(x)
                        batchmodtable = LXPModel.BatchCourse.objects.create(batch_id=batchtable.id,course_id=modid)
                        batchmodtable.save()
                    selectedlist = request.POST.getlist('vdolist')
                    for x in selectedlist:
                        PLid = str(x)
                        batchvdotable = LXPModel.BatchRecordedVDOList.objects.create(batch_id=batchtable.id,playlist_id=PLid)
                        batchvdotable.save()
                    messages.success(request, 'Batch Added Successfully')
                    return render(request,'cfo/batch/cfo_view_batch.html')
            batchForm=LXPFORM.BatchForm()
            trainers =  User.objects.raw('SELECT   auth_user.id,  auth_user.username,  auth_user.first_name,  auth_user.last_name,  auth_user.email FROM  social_auth_usersocialauth  INNER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id) WHERE  social_auth_usersocialauth.utype = 1 AND  social_auth_usersocialauth.status = true')
            learners =  list(User.objects.raw('SELECT   auth_user.id,  auth_user.username,  auth_user.first_name,  auth_user.last_name,  auth_user.email FROM  social_auth_usersocialauth  INNER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id) WHERE  social_auth_usersocialauth.utype = 2 AND  social_auth_usersocialauth.status = true ORDER BY auth_user.first_name, auth_user.last_name'))
            courses =  LXPModel.Course.objects.all()
            PList =  LXPModel.Playlist.objects.all().order_by('name')
            return render(request,'cfo/batch/cfo_add_batch.html',{'batchForm':batchForm,'trainers':trainers,'learners':learners,'courses':courses,'PList':PList})
    except:
        return render(request,'lxpapp/404page.html')
import json
@login_required
def cfo_update_batch_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cfo':
            batch = LXPModel.Batch.objects.get(id=pk)
            batchForm=LXPFORM.BatchForm(request.POST,instance=batch)
            if request.method=='POST':
                if batchForm.is_valid(): 
                    batchtext = batchForm.cleaned_data["batch_name"]
                    batch = LXPModel.Batch.objects.all().filter(batch_name__iexact = batchtext).exclude(id=pk)
                    if batch:
                        messages.info(request, 'Batch Name Already Exist')
                        return render(request,'cfo/batch/cfo_update_batch.html',{'batchForm':batchForm})
                    else:
                        batchForm.save()
                        selectedlist = request.POST.getlist('listbox1')
                        det = LXPModel.BatchTrainer.objects.all().filter(batch_id=pk)
                        det.delete()
                        for x in selectedlist:
                            trainerid = str(x)
                            batchtrainertable = LXPModel.BatchTrainer.objects.create(batch_id=pk,trainer_id=trainerid)
                            batchtrainertable.save()
                        det = LXPModel.Batchlearner.objects.all().filter(batch_id=pk)
                        det.delete()
                        json_data = json.loads(request.POST.get('myvalue'))
                        for cx in json_data:
                            a=json_data[cx]['id']
                            b=json_data[cx]['fee']
                            batchlearnertable = LXPModel.Batchlearner.objects.create(batch_id=pk,learner_id=a,fee=b)
                            batchlearnertable.save()
                        selectedlist = request.POST.getlist('listbox3')
                        det = LXPModel.BatchCourse.objects.all().filter(batch_id=pk)
                        det.delete()
                        for x in selectedlist:
                            courseid = str(x)
                            batchcoursetable = LXPModel.BatchCourse.objects.create(batch_id=pk,course_id=courseid)
                            batchcoursetable.save()
                        det = LXPModel.BatchRecordedVDOList.objects.all().filter(batch_id=pk)
                        det.delete()
                        selectedlist = request.POST.getlist('vdolist')
                        for x in selectedlist:
                            PLid = str(x)
                            batchvdotable = LXPModel.BatchRecordedVDOList.objects.create(batch_id=pk,playlist_id=PLid)
                            batchvdotable.save()
                        batchs = LXPModel.Batch.objects.all()
                        messages.success(request, 'Batch Updated Successfully')
                        return render(request,'cfo/batch/cfo_view_batch.html',{'batchs':batchs})
            trainers =  list(User.objects.raw('SELECT   auth_user.id,  auth_user.username,  auth_user.first_name,  auth_user.last_name,  auth_user.email FROM  social_auth_usersocialauth  INNER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id) WHERE  social_auth_usersocialauth.utype = 1 AND  social_auth_usersocialauth.status = true'))
            learners =  list(User.objects.raw('SELECT   auth_user.id,  auth_user.username,  auth_user.first_name,  auth_user.last_name,  auth_user.email FROM  social_auth_usersocialauth  INNER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id) WHERE  social_auth_usersocialauth.utype = 2 AND  social_auth_usersocialauth.status = true ORDER BY auth_user.first_name, auth_user.last_name'))
            batchtrainers =  list(User.objects.raw('SELECT DISTINCT   auth_user.id,  auth_user.first_name , auth_user.last_name ,  auth_user.email FROM  lxpapp_batchtrainer  INNER JOIN auth_user ON (lxpapp_batchtrainer.trainer_id = auth_user.id)   WHERE lxpapp_batchtrainer.batch_id = ' + str (pk)))
            PList =  list(LXPModel.Playlist.objects.all().order_by('name'))

            bPList = []
            for c in PList:
                btrnr={}
                btrnr["id"]=c.id
                btrnr["name"]=c.name
                bPList.append(btrnr)
            bPList = json.dumps(bPList)
            
            btrainer = []
            for c in batchtrainers:
                btrnr={}
                btrnr["id"]=c.id
                btrnr["first_name"]=c.first_name
                btrnr["last_name"]=c.last_name
                btrnr["email"]=c.email
                btrainer.append(btrnr)
            btrainer = json.dumps(btrainer)
            batchlearners =  list(User.objects.raw('SELECT DISTINCT   auth_user.id,  auth_user.first_name , auth_user.last_name ,  auth_user.email,lxpapp_batchlearner.fee FROM  lxpapp_batchlearner  INNER JOIN auth_user ON (lxpapp_batchlearner.learner_id = auth_user.id)   WHERE lxpapp_batchlearner.batch_id = ' + str (pk)))
            blearner = []
            for c in batchlearners:
                btrnr={}
                btrnr["id"]=c.id
                btrnr["first_name"]=c.first_name
                btrnr["last_name"]=c.last_name
                btrnr["email"]=c.email
                btrnr["fee"]=c.fee
                blearner.append(btrnr)
            blearner = json.dumps(blearner)
            courses = LXPModel.BatchCourse.objects.filter(batch_id=pk).select_related('course').values('course__course_name','course__id', 'batch_id')
            course = []
            for c in courses:
                btrnr={}
                btrnr["id"]=c['course__id']
                btrnr["course_name"]=c['course__course_name']
                course.append(btrnr)
            course = json.dumps(course)
            courses  = LXPModel.Course.objects.all()
            query = LXPModel.Batch.objects.get(id=pk)
            stdate = (query.stdate).strftime('%Y-%m-%d')
            enddate = (query.enddate).strftime('%Y-%m-%d')
            coursetype = query.coursetype
            dict={
            'batchForm':batchForm,
            'sub':batch.batch_name,
            'trainers':trainers,
            'learners':learners,
            'batchtrainers':batchtrainers,
            'batchlearners':batchlearners,
            'btrainer':btrainer,
            'blearner':blearner,
            'stdate':stdate,
            'enddate':enddate,
            'coursetype':coursetype,
            'bPList':bPList,
            'PList':PList,
            'courses':courses,
            'selectedcourse':course}
            return render(request,'cfo/batch/cfo_update_batch.html',context=dict)
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_view_batch_view(request):
    try:
        if str(request.session['utype']) == 'cfo':
            batchs = LXPModel.Batch.objects.all()
            return render(request,'cfo/batch/cfo_view_batch.html',{'batchs':batchs})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_view_batch_details_view(request,batchname,pk):
    try:
        if str(request.session['utype']) == 'cfo':
            batchs = LXPModel.Batch.objects.raw("SELECT lxpapp_batch.id, GROUP_CONCAT(DISTINCT lxpapp_course.course_name) AS course_name, GROUP_CONCAT(DISTINCT lxpapp_playlist.name) AS video_name, lxpapp_batch.stdate, lxpapp_batch.enddate, GROUP_CONCAT(DISTINCT trainer.first_name || ' ' || trainer.last_name) AS trainer_name, GROUP_CONCAT(DISTINCT learner.first_name || ' ' || learner.last_name) AS learner_name FROM lxpapp_batch LEFT OUTER JOIN lxpapp_batchcourse ON (lxpapp_batchcourse.batch_id = lxpapp_batch.id) LEFT OUTER JOIN lxpapp_batchrecordedvdolist ON (lxpapp_batchrecordedvdolist.batch_id = lxpapp_batch.id) LEFT OUTER JOIN lxpapp_playlist ON (lxpapp_batchrecordedvdolist.playlist_id = lxpapp_playlist.id) LEFT OUTER JOIN lxpapp_batchlearner ON (lxpapp_batch.id = lxpapp_batchlearner.batch_id) LEFT OUTER JOIN lxpapp_batchtrainer ON (lxpapp_batch.id = lxpapp_batchtrainer.batch_id) LEFT OUTER JOIN auth_user trainer ON (lxpapp_batchtrainer.trainer_id = trainer.id) LEFT OUTER JOIN lxpapp_course ON (lxpapp_batchcourse.course_id = lxpapp_course.id) LEFT OUTER JOIN auth_user learner ON (lxpapp_batchlearner.learner_id = learner.id) WHERE lxpapp_batch.id = " + str(pk))
            return render(request,'cfo/batch/cfo_view_batch_details.html',{'batchs':batchs,'batchname':batchname})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cfo_delete_batch_view(request,pk):
    try:
        if str(request.session['utype']) == 'cfo':  
            batch=LXPModel.Batch.objects.get(id=pk)
            batch.delete()
        batchs = LXPModel.Batch.objects.all()
        return render(request,'cfo/batch/cfo_view_batch.html',{'batchs':batchs})
    except:
        return render(request,'lxpapp/404page.html')

# Create Scheduler
@login_required
def generate_meeting_link(request,meeting_type):
    type ={'1':'Session',
           '2':'Interview',
           '3':'Client Requirment',
           '4':'Lab Call',
           '5':'Meeting',
           '6':'Others'}
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S") + f"{now.microsecond // 1000:03d}"
    base_url = settings.MEET_BASE_URL  # Replace with your actual meeting service URL
    meeting_type = type[meeting_type]
    base_url = f"{base_url}{quote_plus(meeting_type)}-{timestamp}"
    print(base_url)
    return f"{base_url}"

def cfo_create_scheduler(request):
    if str(request.session['utype']) != 'cfo':
        return render(request, 'lxpapp/404page.html')
    
    if request.method == 'POST':
        trainer = request.POST.get('trainer')
        type = request.POST.get('type')
        subject = request.POST.get('subject')
        chapter = request.POST.get('chapter')
        topic = request.POST.get('topic')
        start = request.POST.get('start')
        end = request.POST.get('end')
        eventdetails = request.POST.get('eventdetail')

        trainer = LXPModel.User.objects.get(id=trainer)
        subject = LXPModel.Subject.objects.get(id=subject) if type == '1' else None
        chapter = LXPModel.Chapter.objects.get(id=chapter) if type == '1' else None
        topic = LXPModel.Topic.objects.get(id=topic) if type == '1' else None

        scheduler = LXPModel.Scheduler(
            subject=subject,
            trainer=trainer,
            chapter=chapter,
            topic=topic,
            start=start,
            end=end,
            type=type,
            eventdetails=eventdetails,
        )
        scheduler.save()

        # Automatically generate a meeting link using scheduler id
        scheduler.meeting_link = generate_meeting_link(request,type)
        scheduler.save()

        return redirect('cfo-scheduler-list')

    subjects = LXPModel.Subject.objects.all()
    trainers = UserSocialAuth.objects.select_related('user').order_by('user__first_name', 'user__last_name').values(
        'id', 
        'user_id', 
        'user__first_name', 
        'user__last_name', 
        'utype'
    ).filter(utype=1)
    
    return render(request, 'cfo/scheduler/create_scheduler.html', {'trainers': trainers, 'subjects': subjects})

@login_required
def cfo_update_scheduler(request, scheduler_id):
    if str(request.session['utype']) != 'cfo':
        return render(request,'lxpapp/404page.html')
    # Get the Scheduler object to be updated
    scheduler = get_object_or_404(LXPModel.Scheduler, id=scheduler_id)
    
    if request.method == "POST":
        trainer = request.POST.get('trainer')
        type = request.POST.get('type')
        subject = request.POST.get('subject')
        chapter = request.POST.get('chapter')
        topic = request.POST.get('topic')
        start = request.POST.get('start')
        end = request.POST.get('end')
        eventdetails = request.POST.get('eventdetail')
        trainer=LXPModel.User.objects.get(id=trainer)
        if  type == '1':
            subject=LXPModel.Subject.objects.get(id=subject)
            chapter=LXPModel.Chapter.objects.get(id=chapter)
            topic=LXPModel.Topic.objects.get(id=topic)    
            eventdetails = None
        else:
            subject=None
            chapter=None
            topic=None
        
        # Update the scheduler instance
        scheduler.type = type
        scheduler.subject = subject
        scheduler.trainer = trainer
        scheduler.chapter = chapter
        scheduler.topic = topic
        scheduler.start = start
        scheduler.end = end if end else None
        scheduler.eventdetails = eventdetails
        scheduler.save()
        
        messages.success(request, 'Scheduler updated successfully!')
        return redirect('cfo-scheduler-list')  # Redirect to the scheduler list or another page as needed

    else:
        subjects = LXPModel.Subject.objects.all()
        trainers = UserSocialAuth.objects.select_related('user').order_by('user__first_name', 'user__last_name').values(
                    'id', 
                    'user_id', 
                    'user__first_name', 
                    'user__last_name', 
                    'utype'
                ).filter(utype=1)
        topics = LXPModel.Scheduler.objects.select_related('topic').values(
                    'id', 
                    'topic__id', 
                    'topic__topic_name'
                ).filter(id=scheduler_id)
        chapters = LXPModel.Scheduler.objects.select_related('chapter').values(
                    'id', 
                    'chapter__id', 
                    'chapter__chapter_name'
                ).filter(id=scheduler_id)
        # Return the form with current scheduler data
        context = {
            'scheduler': scheduler,
            'subjects': subjects,
            'chapters': chapters,
            'topics': topics,
            'trainers': trainers
        }
        return render(request, 'cfo/scheduler/update_scheduler.html', context)
    
# List all Schedulers
@login_required
def cfo_scheduler_list(request):
    if str(request.session['utype']) != 'cfo':
        return render(request,'lxpapp/404page.html')
    schedulers = LXPModel.Scheduler.objects.all()
    return render(request, 'cfo/scheduler/scheduler_list.html', {'schedulers': schedulers})


# List scheduler_calender
@login_required
def cfo_scheduler_calender(request):
    if str(request.session['utype']) != 'cfo':
        return render(request,'lxpapp/404page.html')
    schedulers = LXPModel.Scheduler.objects.annotate(
        status_sum=Coalesce(Sum('schedulerstatus__status'), Value(0)),
        completion_date=Case(
            When(status_sum__gte=100, then=Max('schedulerstatus__date')),
            default=Value(None),
        )
    )
    return render(request, 'cfo/scheduler/scheduler_calender.html', {'schedulers': schedulers})

def get_meetings(request):
    meetings = LXPModel.Scheduler.objects.all()
    events = [
        {
            "title": f"{meeting.subject.name if meeting.subject else meeting.eventdetails}",
            "start": meeting.start.isoformat(),
            "end": meeting.end.isoformat(),
            "meeting_link": meeting.meeting_link,  # Include meeting link
        }
        for meeting in meetings
    ]
    return JsonResponse(events, safe=False)
# Delete Scheduler
@login_required
def cfo_delete_scheduler(request, scheduler_id):
    if str(request.session['utype']) != 'cfo':
        return render(request,'lxpapp/404page.html')
    scheduler = get_object_or_404(LXPModel.Scheduler, id=scheduler_id)
    scheduler.delete()
    return redirect('scheduler_list')    


@login_required
def get_chapters(request, subject_id):
    chapters = LXPModel.Chapter.objects.all().filter(subject_id = subject_id)  # Adjust logic if needed
    return JsonResponse([{'id': chapter.id, 'name': chapter.chapter_name} for chapter in chapters], safe=False)

@login_required
def get_topics(request, chapter_id):
    topics = LXPModel.Topic.objects.all().filter(chapter_id = chapter_id)
    return JsonResponse([{'id': topic.id, 'name': topic.topic_name} for topic in topics], safe=False)


import jwt
import datetime
import uuid
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

JITSI_SECRET = "a5f9c73e4d85e0c9f25b2d4394b6d24d5c00f27aaebef34f97f13a9f6f1c9ec7"
JITSI_SERVER = "https://34.235.128.110"  # Replace with your Jitsi Meet server IP

def generate_jitsi_token(username, meeting_id, is_host):
    payload = {
        "context": {
            "user": {
                "name": username,
                "id": username
            }
        },
        "aud": "my_django_app",
        "iss": "my_django_app",
        "sub": "your-jitsi-domain",
        "room": meeting_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "moderator": is_host
    }
    token = jwt.encode(payload, JITSI_SECRET, algorithm='HS256')
    return token