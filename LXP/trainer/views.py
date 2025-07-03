from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from lxpapp.models import *
from lxpapp import forms as LXPFORM
from lxpapp.forms import PollForm, PollOptionFormSet
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum,Count,Q
from django.urls import reverse
from social_django.models import UserSocialAuth
from django.db.models import Exists, OuterRef,Case, When, Value, IntegerField,F, Value, Q, Sum, Max
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
@login_required    
def trainer_dashboard_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            notification = TrainerNotification.objects.all().filter(trainer_id = request.user.id,status = False)
            mco = Exam.objects.filter(questiontpye='MCQ').count()
            short = Exam.objects.filter(questiontpye='ShortAnswer').count()
            mcqques= McqQuestion.objects.all().count()
            sques= ShortQuestion.objects.all().count()
            schedulers = Scheduler.objects.annotate(
                status_sum=Coalesce(Sum('schedulerstatus__status'), Value(0)),
                completion_date=Case(
                    When(status_sum__gte=100, then=Max('schedulerstatus__date')),
                    default=Value(None),
                )).filter(trainer_id = request.user.id, status_sum__lte=99)
            dict={
            'total_course':0,
            schedulers:schedulers,
            'total_exam':0,
            'total_shortExam':0, 
            'total_question':0,
            'total_short':0,
            'total_learner':0,
            'notifications':notification,
            }
            return render(request,'trainer/trainer_dashboard.html',{'schedulers':schedulers,'mcqques':mcqques,'sques':sques,'mco':mco,'short':short,'dict':dict})
        else:
            return render(request,'loginrelated/diffrentuser.html')
    #except:
        return render(request,'lxpapp/404page.html')
 
@login_required
def trainer_view_material_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            materials = Material.objects.all()
            return render(request,'trainer/material/trainer_view_material.html',{'materials':materials})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_show_material_view(request,materialtype,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            details= Material.objects.all().filter(id=pk)
            if materialtype == 'HTML':
                return render(request,'trainer/material/trainer_material_htmlshow.html',{'details':details})
            if materialtype == 'URL':
                return render(request,'trainer/material/trainer_material_urlshow.html',{'details':details})
            if materialtype == 'PDF':
                return render(request,'trainer/material/trainer_material_pdfshow.html',{'details':details})
            if materialtype == 'Video':
                return render(request,'trainer/material/trainer_material_videoshow.html',{'details':details})
    except:
        return render(request,'lxpapp/404page.html')


@login_required
def trainer_view_sessionmaterial_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            sessionmaterials = SessionMaterial.objects.all()
            return render(request,'trainer/sessionmaterial/trainer_view_sessionmaterial.html',{'sessionmaterials':sessionmaterials})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_show_sessionmaterial_view(request,sessionmaterialtype,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            details= SessionMaterial.objects.all().filter(id=pk)
            if sessionmaterialtype == 'HTML':
                return render(request,'trainer/sessionmaterial/trainer_sessionmaterial_htmlshow.html',{'details':details})
            if sessionmaterialtype == 'URL':
                return render(request,'trainer/sessionmaterial/trainer_sessionmaterial_urlshow.html',{'details':details})
            if sessionmaterialtype == 'PDF':
                return render(request,'trainer/sessionmaterial/trainer_sessionmaterial_pdfshow.html',{'details':details})
            if sessionmaterialtype == 'Video': 
                return render(request,'trainer/sessionmaterial/trainersessionmaterial_videoshow.html',{'details':details})
    except:
        return render(request,'lxpapp/404page.html')

def load_videos(request):
    try:
        playlist_id = request.GET.get('playlist')
        videos = PlaylistItem.objects.raw('SELECT  lxpapp_video.id as id,lxpapp_video.id as pk, lxpapp_video.name FROM  lxpapp_playlistitem  INNER JOIN lxpapp_video ON (lxpapp_playlistitem.video_id = lxpapp_video.id) WHERE  lxpapp_playlistitem.playlist_id = ' + str(playlist_id) + ' ORDER BY  lxpapp_video.name')
        context = {'videos': videos}
        return render(request, 'hr/video_dropdown_list_options.html', context)
    except:
        return render(request,'lxpapp/404page.html')

def trainer_create_poll(request):
    prefix = 'options'
    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        option_formset = PollOptionFormSet(request.POST, prefix=prefix)

        if poll_form.is_valid() and option_formset.is_valid():
            with transaction.atomic():
                poll_instance = poll_form.save()
                for option_form in option_formset:
                    option_text = option_form.cleaned_data.get('option_text')
                    if option_text:
                        PollOption.objects.create(poll=poll_instance, option_text=option_text)

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Poll created successfully!'})

            messages.success(request, f'Poll "{poll_instance.question}" created successfully!')
            return redirect('trainer-view-polls')

        # Return form errors as JSON if AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': {
                    'poll_form': poll_form.errors,
                    'option_formset': option_formset.non_form_errors()
                }
            }, status=400)

    else:
        poll_form = PollForm()
        option_formset = PollOptionFormSet(prefix=prefix)

    return render(request, 'trainer/polls/trainer_create_poll.html', {
        'poll_form': poll_form,
        'option_formset': option_formset
    })

@login_required
def trainer_edit_poll(request, poll_id):
    print("edit poll is called with id {}".format(poll_id))
    poll = get_object_or_404(Poll, pk=poll_id)
    prefix = 'options'

    if request.method == 'POST':
        # Populate the forms with submitted data AND the existing poll instance
        poll_form = PollForm(request.POST, instance=poll)
        option_formset = PollOptionFormSet(request.POST, prefix=prefix)

        if poll_form.is_valid() and option_formset.is_valid():
            # Use a transaction to ensure data integrity
            with transaction.atomic():
                # Save the updated poll question. Because we passed `instance=poll`,
                # .save() will perform an UPDATE, not a new INSERT.
                poll_form.save()

                # "Delete all and recreate" is the simplest robust strategy for editing formsets.
                # First, delete all existing options for this poll.
                poll.options.all().delete()

                # Then, create the new options from the formset data.
                for option_form in option_formset:
                    option_text = option_form.cleaned_data.get('option_text')
                    if option_text:
                        PollOption.objects.create(poll=poll, option_text=option_text)

            messages.success(request, f'Poll "{poll.question}" has been updated.')
            return redirect('trainer-view-polls')
        else:
            messages.error(request, 'Please correct the errors below.')

    else: # This is a GET request
        # Pre-populate the poll form with the existing poll's data
        poll_form = PollForm(instance=poll)
        
        # Pre-populate the option formset with existing options
        options_data = [{'option_text': opt.option_text} for opt in poll.options.all()]
        option_formset = PollOptionFormSet(initial=options_data, prefix=prefix)

    context = {
        'poll_form': poll_form,
        'option_formset': option_formset,
    }
    return render(request, 'trainer/polls/trainer_edit_poll.html', context)

@login_required
@require_POST # Ensures this view can only be accessed with a POST request
def trainer_delete_poll(request, poll_id):
    """
    Deletes a poll and its related options.
    """
    # get_object_or_404 is a common Django shortcut.
    # It tries to get the object, and if it doesn't exist, it automatically
    # returns a 404 Not Found page. This is cleaner than a try/except block.
    poll = get_object_or_404(Poll, pk=poll_id)

    # We store the question text before deleting to use in the flash message.
    poll_question = poll.question
    poll.delete()

        # Handle AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': f'Poll "{poll_question}" was deleted.'})

    # Handle regular request
    messages.success(request, f'Poll "{poll_question}" was successfully deleted.')
    return redirect('trainer-view-polls')
@login_required
def trainer_view_poll(request):
    """
    Displays all polls with their results for trainers.
    This version correctly calculates votes from the PollVote model.
    """
    # Get all Poll objects. We will attach all necessary data to them.
    polls_query = Poll.objects.annotate(
        # Create a 'total_votes' attribute on each poll object by counting
        # the number of related PollVote records.
        total_votes=Count('votes')  # 'votes' is the related_name from Poll to PollVote
    ).prefetch_related(
        # Prefetch the options to avoid N+1 queries. For each option,
        # also annotate it with its individual vote count.
        models.Prefetch(
            'options',
            queryset=PollOption.objects.annotate(
                vote_count=models.Count('votes') # 'votes' is related_name from PollOption to PollVote
            )
        ),
        # Also prefetch the user data for each vote to display who voted.
        'votes__user'
    ).order_by('-created_at')

    context = {
        # Pass the entire QuerySet of enhanced Poll objects to the template.
        # No need to build dictionaries manually.
        'polls_data': polls_query
    }
    return render(request, 'trainer/polls/trainer_view_poll.html', context)

@login_required
def trainer_exam_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/exam/trainer_exam.html')
    except:
        return render(request,'lxpapp/404page.html')


@login_required
def trainer_add_exam_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            form = LXPFORM.ExamForm(request.POST or None)
            breadcrumblink = []
            btrnr={}
            btrnr["head"]='Dashboard'
            btrnr["link"]='../../../../trainer/trainer-dashboard'
            breadcrumblink.append(btrnr)

            btrnr={}
            btrnr["head"]='View Exam'
            btrnr["link"]='../../../../trainer/trainer-view-exam'
            breadcrumblink.append(btrnr)
            
            btrnr={}
            btrnr["head"]='Active'
            btrnr["link"]='Add Exam'
            breadcrumblink.append(btrnr)
            
            context = {
                'form': form,
                'breadcrumbsetting':breadcrumblink,
                'page_title': 'Add Exam'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('exam_name')
                    exam = Exam.objects.all().filter(exam_name__iexact = name)
                    if exam:
                        messages.info(request, 'Exam Name Already Exist')
                        return redirect(reverse('trainer-add-exam'))
                    try:
                        qtype = form.cleaned_data.get('questiontpye')
                        batch = form.cleaned_data.get('batch').pk
                        exam = Exam.objects.create(
                                                    exam_name = name,questiontpye=qtype,batch_id=batch)
                        exam.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('trainer-add-exam'))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'trainer/exam/add_edit_exam.html', context)
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_update_exam_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            instance = get_object_or_404(Exam, id=pk)
            form = LXPFORM.ExamForm(request.POST or None, instance=instance)
            breadcrumblink = []
            btrnr={}
            btrnr["head"]='Dashboard'
            btrnr["link"]='../../../../trainer/trainer-dashboard'
            breadcrumblink.append(btrnr)
            
            btrnr={}
            btrnr["head"]='Add Exam'
            btrnr["link"]='../../../../trainer/trainer-add-exam'
            breadcrumblink.append(btrnr)
            
            btrnr={}
            btrnr["head"]='View Exam'
            btrnr["link"]='../../../../trainer/trainer-view-exam'
            breadcrumblink.append(btrnr)
            
            btrnr={}
            btrnr["head"]='Active'
            btrnr["link"]='Update Exam'
            breadcrumblink.append(btrnr)
            
            context = {
                'form': form,
                'exam_id': pk,
                'breadcrumbsetting':breadcrumblink,
                'page_title': 'Update Exam'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('exam_name')
                    batch = form.cleaned_data.get('batch').pk
                    qtype = form.cleaned_data.get('questiontpye')
                    exam = Exam.objects.all().filter(exam_name__iexact = name).exclude(id=pk)
                    if exam:
                        messages.info(request, 'Exam Name Already Exist')
                        return redirect(reverse('trainer-update-exam', args=[pk]))
                    try:
                        exam = Exam.objects.get(id=pk)
                        exam.exam_name = name
                        exam.batch_id = batch
                        exam.questiontpye = qtype
                        exam.save()
                        messages.success(request, "Successfully Updated")
                        exams = Exam.objects.all()
                        return render(request,'trainer/exam/trainer_view_exam.html',{'exams':exams})
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")

            return render(request, 'trainer/exam/add_edit_exam.html', context,{'a':'imran'})
    except:
        return render(request,'lxpapp/404page.html')
@login_required
def trainer_upload_exam_csv_view(request):
    if request.method=='POST':
        file=request.FILES["select_file"]
        examtext=request.POST.get('exam_name')
        batch=request.POST.get('batch')
        qtype=request.POST.get('examtype')
        exam = Exam.objects.all().filter(exam_name__iexact = examtext)
        if exam:
            messages.info(request, 'Exam Name Already Exist')
        else:
            if qtype=='0':
                qtype = 'MCQ'
            else:
                qtype = 'ShortAnswer'
            exam = Exam.objects.create(batch_id = batch,exam_name = examtext,questiontpye = qtype)
            exam.save()   
            csv_file = request.FILES["select_file"]
            file_data = csv_file.read().decode("utf-8")		
            lines = file_data.split("\n")
            no = 0
            for line in lines:						
                no = no + 1
                if no > 1:
                    fields = line.split(",")
                    if qtype == 'MCQ':
                        question = McqQuestion.objects.create(
                            question = fields[0],
                            option1 = fields[1],
                            option2 = fields[2],
                            option3 = fields[3],
                            option4 = fields[4],
                            answer = fields[5],
                            marks = fields[6],
                            exam_id = exam.id
                        )
                        question.save()
                    elif qtype == 'ShortAnswer':
                        question = ShortQuestion.objects.create(
                            question = fields[0],
                            marks = fields[1],
                            exam_id = exam.id
                        )
                        question.save()
            messages.info(request, 'Questions Added Successfully')
    batch = Batch.objects.all()
    context = {'batch': batch}
    return render(request,'trainer/exam/trainer_upload_exam_csv.html',context)

def upload_csv(request):
	data = {}
	if "GET" == request.method:
		return render(request, "myapp/upload_csv.html", data)
    # if not GET, then proceed
	try:
		csv_file = request.FILES["csv_file"]
		file_data = csv_file.read().decode("utf-8")		
		lines = file_data.split("\n")
		#loop over the lines and save them in db. If error , store as string and then display
		for line in lines:						
			fields = line.split(",")
			data_dict = {}
			data_dict["name"] = fields[0]
			data_dict["start_date_time"] = fields[1]
			data_dict["end_date_time"] = fields[2]
			data_dict["notes"] = fields[3]
			

	except Exception as e:
		messages.error(request,"Unable to upload file. "+repr(e))

@login_required
def trainer_view_exam_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            exams = Exam.objects.all().filter(batch_id__in = Batch.objects.all())
            return render(request,'trainer/exam/trainer_view_exam.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')

def trainer_view_filter_exam_view(request,type):
    try:
        if str(request.session['utype']) == 'trainer':
            exams = Exam.objects.all().filter(batch_id__in = Batch.objects.all(),questiontpye = type)
            return render(request,'trainer/exam/trainer_view_exam.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_delete_exam_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':  
            exam=Exam.objects.get(id=pk)
            exam.delete()
            return HttpResponseRedirect('/trainer/trainer-view-exam')
        exams = Exam.objects.all()
        return render(request,'trainer/exam/trainer_view_exam.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')
 
@login_required
def trainer_mcqquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/mcqquestion/trainer_mcqquestion.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_view_mcqquestion_exams_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            exams = Exam.objects.all().filter(questiontpye='MCQ')
            return render(request,'trainer/mcqquestion/trainer_view_mcqquestion_exams.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')
@login_required
def trainer_view_mcqquestion_view(request,examid):
    try:
        if str(request.session['utype']) == 'trainer':
            mcqquestions = McqQuestion.objects.all().filter(exam_id__in = Exam.objects.all().filter(id=examid))
            return render(request,'trainer/mcqquestion/trainer_view_mcqquestion.html',{'mcqquestions':mcqquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_shortquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/shortquestion/trainer_shortquestion.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_view_shortquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            shortquestions = ShortQuestion.objects.all().filter(exam_id__in = Exam.objects.all())
            return render(request,'trainer/shortquestion/trainer_view_shortquestion.html',{'shortquestions':shortquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_pending_short_exam_result_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            pending = ShortResult.objects.all().filter( learner_id__in = User.objects.all(),exam_id__in = Exam.objects.all(),status = False)
            return render(request,'trainer/shortexam/trainer_pending_short_exam_reuslt.html',{'pending':pending})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_update_short_question_result_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            resultdetails = ShortResultDetails.objects.all().filter( question_id__in = ShortQuestion.objects.all(),shortresult_id = pk)
            
            return render(request,'trainer/shortexam/trainer_update_short_question_result.html',{'resultdetails':resultdetails})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_save_short_question_result_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            if request.method=="POST":
                feedback=request.POST['newfeedback']
                marks=request.POST['newmarks']
                rid=request.POST['newid']
                qid=request.POST['newqid']
                answer=request.POST['newanswer']
                mainid=request.POST['newmainid']
                resupdate = ShortResultDetails.objects.all().filter(id=pk)
                resupdate.delete()
                resupdate = ShortResultDetails.objects.create(id=pk,marks=marks,feedback=feedback,question_id=qid,answer=answer,shortresult_id=mainid)
                resupdate.save()
                
                totmarks=ShortResultDetails.objects.all().filter(shortresult_id=mainid).aggregate(stars=Sum('marks'))['stars']
                maintbl=ShortResult.objects.get(id=mainid)
                tot=ShortResultDetails.objects.all().filter(shortresult_id=mainid).aggregate(stars=Count('marks'))['stars']
                totgiven=ShortResultDetails.objects.all().filter(shortresult_id=mainid,marks__gt=0).aggregate(stars=Count('marks'))['stars']
                if tot == totgiven:
                    maintbl.status=True
                maintbl.marks = totmarks
                maintbl.save()
                messages.info(request, 'Records saved successfully')
                if tot == totgiven:
                    resultdetails = ShortResultDetails.objects.all().filter( question_id__in = ShortQuestion.objects.all(),shortresult_id = pk)
                    return render(request,'trainer/shortexam/trainer_update_short_question_result.html',{'resultdetails':resultdetails})
                else:
                    resultdetails = ShortResultDetails.objects.all().filter( question_id__in = ShortQuestion.objects.all(),shortresult_id = mainid)
                    return render(request,'trainer/shortexam/trainer_update_short_question_result.html',{'resultdetails':resultdetails})
    except:
        return render(request,'lxpapp/404page.html') 

@login_required
def trainer_ytexamquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/ytexamquestion/trainer_ytexamquestion.html')
    except:
        return render(request,'lxpapp/404page.html')


@login_required
def trainer_view_ytexamquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            ytexamquestions = YTExamQuestion.objects.all().filter(playlist_id__in = Playlist.objects.all())
            return render(request,'trainer/ytexamquestion/trainer_view_ytexamquestion.html',{'ytexamquestions':ytexamquestions})
    except:
        return render(request,'lxpapp/404page.html')


@login_required
def trainer_view_learner_video_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            learner = UserSocialAuth.objects.raw('SELECT social_auth_usersocialauth.id, social_auth_usersocialauth.user_id, social_auth_usersocialauth.pic, auth_user.first_name, auth_user.last_name, GROUP_CONCAT(DISTINCT lxpapp_playlist.name) AS courseset_name, lxpapp_learnerdetails.mobile FROM social_auth_usersocialauth LEFT OUTER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id) LEFT OUTER JOIN lxpapp_batchlearner ON (auth_user.id = lxpapp_batchlearner.learner_id) LEFT OUTER JOIN lxpapp_batchrecordedvdolist ON (lxpapp_batchlearner.batch_id = lxpapp_batchrecordedvdolist.batch_id) LEFT OUTER JOIN lxpapp_playlist ON (lxpapp_batchrecordedvdolist.playlist_id = lxpapp_playlist.id) LEFT OUTER JOIN lxpapp_learnerdetails ON (auth_user.id = lxpapp_learnerdetails.learner_id) WHERE (social_auth_usersocialauth.utype = 0 OR social_auth_usersocialauth.utype = 2) AND social_auth_usersocialauth.status = 1 GROUP BY social_auth_usersocialauth.id, social_auth_usersocialauth.user_id, auth_user.first_name, auth_user.last_name, lxpapp_learnerdetails.mobile ')
            return render(request,'trainer/learnervideo/trainer_view_learner_video.html',{'learner':learner})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_learner_video_Course_view(request,user_id,userfirstname,userlastname):
#    try:    
        if str(request.session['utype']) == 'trainer':
            videos1 = BatchCourseSet.objects.raw('SELECT DISTINCT lxpapp_courseset.id,  lxpapp_courseset.courseset_name,lxpapp_batchcourseset.batch_id FROM  lxpapp_batchcourseset   INNER JOIN lxpapp_courseset ON (lxpapp_batchcourseset.courseset_id = lxpapp_courseset.id)   INNER JOIN lxpapp_batch ON (lxpapp_batchcourseset.batch_id = lxpapp_batch.id)   INNER JOIN lxpapp_batchlearner ON (lxpapp_batchlearner.batch_id = lxpapp_batch.id) WHERE   lxpapp_batchlearner.learner_id = ' + str(user_id))
            return render(request,'trainer/learnervideo/trainer_learner_video_course.html',{'videos':videos1,'userfirstname':userfirstname,'userlastname':userlastname,'user_id':user_id})
 #   except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_learner_video_Course_subject_view(request,user_id,userfirstname,userlastname):
#    try:    
        if str(request.session['utype']) == 'trainer':
            
            subject = Playlist.objects.raw('SELECT ID AS id, NAME, VTOTAL, Mtotal, SUM(VWATCHED) AS VWatched,((100*VWATCHED)/VTOTAL) as per, THUMBNAIL_URL FROM (SELECT YYY.ID, YYY.NAME, YYY.THUMBNAIL_URL, ( SELECT COUNT(XX.ID) FROM LXPAPP_PLAYLISTITEM XX WHERE XX.PLAYLIST_ID = YYY.ID ) AS Vtotal, ( SELECT COUNT(zz.ID) FROM LXPAPP_sessionmaterial zz WHERE zz.PLAYLIST_ID = YYY.ID ) AS Mtotal, (SELECT COUNT (LXPAPP_VIDEOWATCHED.ID) AS a FROM LXPAPP_PLAYLISTITEM GHGH LEFT OUTER JOIN LXPAPP_VIDEOWATCHED ON ( GHGH.VIDEO_ID = LXPAPP_VIDEOWATCHED.VIDEO_ID ) WHERE GHGH.PLAYLIST_ID = YYY.ID AND LXPAPP_VIDEOWATCHED.LEARNER_ID = ' + str( user_id) + ') AS VWatched FROM LXPAPP_BATCHLEARNER INNER JOIN LXPAPP_BATCH ON (LXPAPP_BATCHLEARNER.BATCH_ID = LXPAPP_BATCH.ID) INNER JOIN LXPAPP_BATCHRECORDEDVDOLIST ON (LXPAPP_BATCH.ID = LXPAPP_BATCHRECORDEDVDOLIST.BATCH_ID) INNER JOIN LXPAPP_PLAYLIST YYY ON (LXPAPP_BATCHRECORDEDVDOLIST.PLAYLIST_ID = YYY.ID) WHERE LXPAPP_BATCHLEARNER.LEARNER_ID = ' + str(user_id) + ') GROUP BY ID, NAME, VTOTAL ORDER BY NAME')
            videocount = LearnerPlaylistCount.objects.all().filter(learner_id = user_id)
            countpresent =False
            if videocount:
                countpresent = True
            per = 0
            tc = 0
            wc = 0
            for x in subject:
                if not videocount:
                    countsave = LearnerPlaylistCount.objects.create(playlist_id = x.id, learner_id = user_id,count =x.Vtotal )
                    countsave.save()
                tc += x.Vtotal
                wc += x.VWatched
            try:
                per = (100*int(wc))/int(tc)
            except:
                per =0
            dif = tc- wc
            return render(request,'trainer/learnervideo/trainer_learner_video_course_subject.html',{'user_id':user_id,'subject':subject,'userfirstname':userfirstname,'userlastname':userlastname,'dif':dif,'per':per,'wc':wc,'tc':tc})
 #   except:
        return render(request,'lxpapp/404page.html')
 
@login_required
def trainer_learner_video_list_view(request,subject_id,user_id):
    try:     
        if str(request.session['utype']) == 'trainer':
            subjectname = Playlist.objects.only('name').get(id=subject_id).name
            list = PlaylistItem.objects.raw('SELECT DISTINCT mainvid.id, mainvid.name, IFNULL((SELECT lxpapp_videowatched.video_id FROM lxpapp_videowatched WHERE lxpapp_videowatched.learner_id = ' + str(user_id) + ' AND lxpapp_videowatched.video_id = mainvid.id), 0) AS watched, IFNULL((SELECT lxpapp_videotounlock.video_id FROM lxpapp_videotounlock WHERE lxpapp_videotounlock.learner_id = ' + str(user_id) + ' AND lxpapp_videotounlock.video_id = mainvid.id), 0) AS unlocked FROM lxpapp_video mainvid INNER JOIN lxpapp_playlistitem ON (mainvid.id = lxpapp_playlistitem.video_id) WHERE lxpapp_playlistitem.playlist_id = ' + str (subject_id) + ' AND mainvid.name <> "Deleted video"')  
            return render(request,'trainer/learnervideo/trainer_learner_video_list.html',{'list':list,'subjectname':subjectname,'subject_id':subject_id,'user_id':user_id})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_learner_approve_video(request,pk,studid):
    try:
        if str(request.session['utype']) == 'trainer':
            unlock = VideoToUnlock.objects.create(learner_id=studid,video_id=pk)
            unlock.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    except:
        return render(request,'lxpapp/404page.html') 

@login_required
def trainer_learner_approveall_video(request,userid,subject_id):
    try:
        if str(request.session['utype']) == 'trainer':
            videos=Playlist.objects.raw('SELECT   lxpapp_video.id FROM  lxpapp_playlistitem  INNER JOIN lxpapp_video ON (lxpapp_playlistitem.video_id = lxpapp_video.id) where lxpapp_playlistitem.playlist_id = ' + str (subject_id))
            for x in videos:
                unlock = VideoToUnlock.objects.create(learner_id=userid,video_id=x.id)
                unlock.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_learner_show_video_view(request,subject_id,video_id):
    try:    
        if str(request.session['utype']) == 'trainer':
            subjectname = Playlist.objects.only('name').get(id=subject_id).name
            Videos=Video.objects.all().filter(id=video_id)
            topicname =''
            url=''
            for x in Videos:
                topicname =x.name
                url = "https://www.youtube.com/embed/" + x.video_id
            return render(request,'trainer/learnervideo/trainer_learner_show_video.html',{'topicname':topicname,'url':url,'subjectname':subjectname,'subject_id':subject_id})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_view_chapterquestion_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            chapterquestions = ChapterQuestion.objects.raw('SELECT DISTINCT  lxpapp_chapter.id,  lxpapp_subject.subject_name,  lxpapp_chapter.chapter_name FROM  lxpapp_chapterquestion  INNER JOIN lxpapp_chapter ON (lxpapp_chapterquestion.chapter_id = lxpapp_chapter.id)  INNER JOIN lxpapp_subject ON (lxpapp_chapterquestion.subject_id = lxpapp_subject.id)')
            return render(request,'trainer/chapterquestion/trainer_view_chapterquestion.html',{'chapterquestions':chapterquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_view_chapterquestion_chapter_view(request,chapter_id):
    try:
        if str(request.session['utype']) == 'trainer':
            chapterquestions = ChapterQuestion.objects.all().filter(chapter_id__in = Chapter.objects.all().filter(id=chapter_id))
            chapter_name = Chapter.objects.only('chapter_name').get(id=chapter_id).chapter_name

            return render(request,'trainer/chapterquestion/trainer_view_chapterquestion_chapter.html',{'chapterquestions':chapterquestions,'chapter_name':chapter_name})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_k8sterminal_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            return render(request,'trainer/labs/k8sterminal/trainer_k8sterminal.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_add_k8sterminal_view(request):
    try:
        if str(request.session['utype']) == 'trainer':
            if request.method=='POST':
                k8sterminalForm=LXPFORM.K8STerminalForm(request.POST)
                learner_id = request.POST['user_name']
                usagevalue = request.POST.get('usagevalue')
                password1 = request.POST.get("password")
                password2 = request.POST.get("confirmpassword")
                if password1 and password2 and password1 != password2:
                    messages.info(request, 'password_mismatch')
                else:
                    k8sterminal = K8STerminal.objects.create(
                        trainer_id = request.user.id,
                        learner_id = learner_id,
                        Password = password1,
                        usagevalue = usagevalue)
                    k8sterminal.save()
                    messages.info(request, 'Record Saved')
            k8sterminalForm=LXPFORM.K8STerminalForm()
            users = User.objects.raw('SELECT DISTINCT   auth_user.id,  auth_user.password,  auth_user.is_superuser,  auth_user.username,  auth_user.last_name,  auth_user.email,  auth_user.first_name,  social_auth_usersocialauth.utype,  social_auth_usersocialauth.status,  social_auth_usersocialauth.uid FROM  social_auth_usersocialauth  INNER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id) WHERE  social_auth_usersocialauth.status = 1 AND   (social_auth_usersocialauth.utype = 0 OR  social_auth_usersocialauth.utype = 2 ) ORDER BY auth_user.first_name, auth_user.last_name')
            return render(request,'trainer/labs/k8sterminal/trainer_add_k8sterminal.html',{'k8sterminalForm':k8sterminalForm,'users':users})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_update_k8sterminal_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':
            k8sterminal = K8STerminal.objects.get(id=pk)
            k8sterminalForm=LXPFORM.K8STerminalForm(request.POST,instance=k8sterminal)
            if request.method=='POST':
                if k8sterminalForm.is_valid(): 
                    k8sterminaltext = k8sterminalForm.cleaned_data["k8sterminal_name"]
                    chaptertext = k8sterminalForm.cleaned_data["chapterID"]
                    subjecttext = k8sterminalForm.cleaned_data["subjectID"]
                    k8sterminal = K8STerminal.objects.all().filter(k8sterminal_name__iexact = k8sterminaltext).exclude(id=pk)
                    if k8sterminal:
                        messages.info(request, 'K8STerminal Name Already Exist')
                    else:
                        chapter = Video.objects.get(chapter_name=chaptertext)
                        subject = Playlist.objects.get(subject_name=subjecttext)
                        k8sterminal = K8STerminal.objects.get(id=pk)
                        k8sterminal.k8sterminal_name = k8sterminaltext
                        k8sterminal.subject_id = subject.id
                        k8sterminal.chapter_id = chapter.id
                        k8sterminal.save()
                        c_list = K8STerminal.objects.filter(chapter_id__in=Video.objects.all())
                        return render(request,'trainer/labs/k8sterminal/trainer_view_k8sterminal.html',{'k8sterminals':c_list})
            k8sterminal_instance = get_object_or_404(K8STerminal, id=pk)
            k8sterminalForm = LXPFORM.K8STerminalForm(instance=k8sterminal_instance)
            return render(request,'trainer/labs/k8sterminal/trainer_update_k8sterminal.html',{'k8sterminalForm':k8sterminalForm,'sub':k8sterminal.k8sterminal_name})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_view_k8sterminal_view(request):
    #try:
        if str(request.session['utype']) == 'trainer':
            k8sterminals = K8STerminal.objects.all().filter(learner_id__in = User.objects.all().order_by('first_name').filter(id__in=UserSocialAuth.objects.all()))
            return render(request,'trainer/labs/k8sterminal/trainer_view_k8sterminal.html',{'k8sterminals':k8sterminals})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_delete_k8sterminal_view(request,pk):
    try:
        if str(request.session['utype']) == 'trainer':  
            k8sterminal=K8STerminal.objects.get(id=pk)
            k8sterminal.delete()
            return HttpResponseRedirect('/trainer/trainer-view-k8sterminal')
        k8sterminals = K8STerminal.objects.all()
        return render(request,'trainer/labs/k8sterminal/trainer_view_k8sterminal.html',{'k8sterminals':k8sterminals})
    except:
        return render(request,'lxpapp/404page.html')


@login_required
def trainer_python_terminal_view(request):
    try:
        if str(request.session['utype']) == 'trainer':  
            return render(request,'trainer/labs/python/trainer_python_terminal.html')
    except:
        return render(request,'lxpapp/404page.html')
    

@login_required
def trainer_linux_terminal_view(request):
    try:
        if str(request.session['utype']) == 'trainer':  
            return render(request,'trainer/labs/linux/trainer_linux_terminal.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_cloudshell_terminal_view(request):
    try:
        if str(request.session['utype']) == 'trainer':  
            return render(request,'trainer/labs/cloudshell/trainer_cloudshell_terminal.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def trainer_scheduler_calender(request):
    schedulers = Scheduler.objects.annotate(
        status_sum=Coalesce(Sum('schedulerstatus__status'), Value(0)),
        completion_date=Case(
            When(status_sum__gte=100, then=Max('schedulerstatus__date')),
            default=Value(None),
        )
    ).filter(trainer_id = request.user.id)
    return render(request, 'trainer/calender/trainer_calender.html', {'schedulers': schedulers})


@login_required
def trainer_calender(request):
    # Get schedulers for the logged-in trainer and use Coalesce to replace None with 0 for status_sum
    schedulers = Scheduler.objects.filter(
        trainer_id=request.user.id
    ).annotate(
        status_sum=Coalesce(Sum('schedulerstatus__status'), Value(0))
    )
    return render(request, 'trainer/scheduler/trainer_calender.html', {'schedulers': schedulers})

# Display list of schedulerstatus
@login_required
def trainer_schedulerstatus_list(request):
    if str(request.session['utype']) == 'trainer':
        schedulerstatus = SchedulerStatus.objects.all()
        return render(request, 'trainer/schedulerstatus/trainer_schedulerstatus_list.html', {'schedulerstatus': schedulerstatus})
    else:
        return render(request,'loginrelated/diffrentuser.html')

# Create a new schedulerstatus
@login_required
def schedulerstatus_create(request):
    if str(request.session['utype']) == 'trainer':
        if request.method == 'POST':
            scheduler = request.POST.get('scheduler')
            status = request.POST.get('status')
            tdate_str = request.POST.get('tdate')
            status_sum = SchedulerStatus.objects.filter(scheduler_id = scheduler).aggregate(Sum('status'))['status__sum']
            value = status
            if status_sum:
                if (float(status) < float(status_sum)) :
                    messages.warning(request, 'Scheduler Status count should be greater then Previous, total is ' + str(status_sum))
                    return redirect('trainer-schedulerstatus-create')
                value = float(status) - float(status_sum)
                if value > 100:
                    messages.warning(request, 'Scheduler Status count getting more then 100. Previous total is ' + str(status_sum))
                    return redirect('trainer-schedulerstatus-create') 
                if value == 0:
                    messages.warning(request, 'Scheduler Status count already marked as completed.' )
                    return redirect('trainer-schedulerstatus-create') 
            try:
                tdate = datetime.strptime(tdate_str, '%d-%m-%Y').date()
            except ValueError:
                return JsonResponse({"error": "Invalid date format"}, status=400)
           
            mode = SchedulerStatus.objects.create(scheduler_id=scheduler,
                                                           trainer_id = request.user.id,
                                                  status=value,
                                                  date = tdate
                                                  )
            mode.save()
            messages.success(request, 'Scheduler Status created successfully!')
            return redirect('trainer-schedulerstatus-create')
        schedulers = Scheduler.objects.filter(trainer_id = request.user.id)
        
        return render(request, 'trainer/schedulerstatus/trainer_schedulerstatus_create.html',{'schedulers':schedulers})
    else:
        return render(request,'loginrelated/diffrentuser.html')

@login_required
def get_scheduler_status_sum(request):
    # Check if the request is AJAX using the appropriate header
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        scheduler_id = request.GET.get("scheduler_id")
        
        # Get the sum of 'status' values for the given scheduler
        status_sum = SchedulerStatus.objects.filter(scheduler_id=scheduler_id).aggregate(Sum('status'))['status__sum']
        
        # If no statuses exist, set sum to 0
        if status_sum is None:
            status_sum = 0

        # Log the status_sum for debugging (you can remove this in production)
        print(f"Scheduler ID: {scheduler_id}, Status Sum: {status_sum}")  # Add print statement to check
        
        return JsonResponse({"status_sum": status_sum})

    return JsonResponse({"error": "Invalid request"}, status=400)
# Delete a schedulerstatus
@login_required
def schedulerstatus_delete(request, id):
    if str(request.session['utype']) == 'trainer':
        schedulerstatus = get_object_or_404(SchedulerStatus, id=id)
        # Now delete the schedulerstatus instance
        schedulerstatus.delete()
        
        return redirect('trainer-schedulerstatus-list')
    else:
        return render(request,'loginrelated/diffrentuser.html')

import json
from  datetime import datetime
@login_required
@csrf_exempt
def trainer_schedulerstatus_mark_done(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            status_id = int(data.get('id'))  # Convert ID to integer

            # Get sum of all status values for this scheduler
            total_status = SchedulerStatus.objects.filter(scheduler_id=status_id).aggregate(
                total=Sum('status')
            )['total'] or 0

            if total_status < 100:
                dif = 100 - total_status
                sch = SchedulerStatus.objects.create(
                    scheduler_id=status_id,
                    trainer_id=request.user.id,
                    status=dif,
                    date=datetime.now().date()
                )
                sch.save()
                
                return JsonResponse({'success': True, 'message': 'Status marked as done.'})
            else:
                return JsonResponse({'success': False, 'message': 'Status is already completed.'})
        
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Invalid ID format.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})
    
def trainer_activity_learner_list(request):
    if str(request.session['utype']) == 'trainer':
        activity_answers = User.objects.filter(
        batchlearner__batch__batchtrainer__trainer_id= request.user.id  # Traverse through BatchLearner, Batch, and BatchTrainer
    ).distinct().values('id','first_name', 'last_name')

        return render(request, 'trainer/learneractivity/trainer_activity_learner_list.html', {'activity_answers': activity_answers})
    else:
        return render(request,'loginrelated/diffrentuser.html')
    
def trainer_activity_learner_batch_list(request,learner_id):
    if str(request.session['utype']) == 'trainer':
        results = ActivityAnswers.objects.raw("""
                                                 SELECT DISTINCT 
                lxpapp_batch.batch_name,
                lxpapp_course.course_name,
                lxpapp_subject.subject_name,
                lxpapp_chapter.chapter_name,
                lxpapp_activity.description,
                lxpapp_activity.id,
                (SELECT anscount FROM (SELECT COUNT (lxpapp_activityanswers.id) as anscount  FROM lxpapp_activityanswers  WHERE lxpapp_activityanswers.course_ID = lxpapp_course.id
                AND lxpapp_activityanswers.id = ans.id
                AND lxpapp_activityanswers.learner_id = lxpapp_batchlearner.learner_id AND lxpapp_activityanswers.course_id = lxpapp_batchcourse.course_id) ) as anscount 
                FROM
                lxpapp_batchtrainer
                LEFT OUTER JOIN lxpapp_batch ON (lxpapp_batchtrainer.batch_id = lxpapp_batch.id)
                LEFT OUTER JOIN lxpapp_batchlearner ON (lxpapp_batch.id = lxpapp_batchlearner.batch_id)
                LEFT OUTER JOIN lxpapp_batchcourse ON (lxpapp_batch.id = lxpapp_batchcourse.batch_id)
                LEFT OUTER JOIN lxpapp_course ON (lxpapp_batchcourse.course_id = lxpapp_course.id)
                LEFT OUTER JOIN lxpapp_coursechapter ON (lxpapp_course.id = lxpapp_coursechapter.course_id)
                LEFT OUTER JOIN lxpapp_chapter ON (lxpapp_coursechapter.chapter_id = lxpapp_chapter.id)
                LEFT OUTER JOIN lxpapp_subject ON (lxpapp_chapter.subject_id = lxpapp_subject.id)
                LEFT OUTER JOIN lxpapp_activity ON (lxpapp_activity.chapter_id = lxpapp_chapter.id)
                LEFT OUTER JOIN lxpapp_activityanswers ans ON (ans.activity_id = lxpapp_activity.id)
                WHERE
                lxpapp_activity.id IS NOT NULL AND lxpapp_batchlearner.learner_id = %s AND lxpapp_batchtrainer.trainer_id = %s
                                              """ % (learner_id,request.user.id))
        
        return render(request, 'trainer/learneractivity/trainer_activity_learner_batch_list.html', {'results': results})
    else:
        return render(request,'loginrelated/diffrentuser.html')


def trainer_activity_learner_batch_activity(request,activity_id):
    if str(request.session['utype']) == 'trainer':
        activity = ActivityAnswers.objects.filter(activity_id=activity_id).select_related('activity').values(
            'activity__description',
            'id',
            'file_url',
            'marks',
            'remarks',
            'status',
            'submitted_on'
            )
        return render(request, 'trainer/learneractivity/trainer_activity_learner_batch_activity.html', {'activity': activity})
    else:
        return render(request,'loginrelated/diffrentuser.html')
    
@csrf_exempt  # To handle the POST request without CSRF token, optional if you're using AJAX with CSRF token
def trainer_activity_learner_batch_activity_update(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)

            # Extract data from the request
            activityanswer_id = data.get('id')
            marks = data.get('marks')
            status = data.get('status')
            remarks = data.get('remarks')

            # Ensure the required fields are provided
            if activityanswer_id is None or marks is None or remarks is None:
                return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)

            # Try to find the Answer object with the provided activityanswer_id
            answer = ActivityAnswers.objects.get(id=activityanswer_id)

            # Update the Answer fields with the new data
            answer.marks = marks
            answer.status = status
            answer.remarks = remarks

            # Save the changes
            answer.save() # imran Ali Khan

            # Return a success response
            return JsonResponse({'status': 'success', 'message': 'Answer updated successfully'})

        except ActivityAnswers.DoesNotExist:
            # Handle the case where the Answer with the provided ID does not exist
            return JsonResponse({'status': 'error', 'message': 'Answer not found'}, status=404)

        except json.JSONDecodeError:
            # Handle JSON decode errors
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)

        except Exception as e:
            # General error handling for unexpected issues
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    # Return an error response if the request is not a POST request
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def trainer_wheel(request):
    return render(request, 'trainer/wheel.html')
