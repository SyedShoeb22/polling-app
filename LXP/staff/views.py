from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from lxpapp import models as LXPModel
from lxpapp import forms as LXPFORM
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
def staff_dashboard_view(request):
    #try:
        if str(request.session['utype']) == 'staff':
            mco = LXPModel.Exam.objects.filter(questiontpye='MCQ').count()
            short = LXPModel.Exam.objects.filter(questiontpye='ShortAnswer').count()
            mcqques= LXPModel.McqQuestion.objects.all().count()
            sques= LXPModel.ShortQuestion.objects.all().count()
            dict={
            'total_course':0,
            'total_exam':0,
            'total_shortExam':0, 
            'total_question':0,
            'total_short':0,
            'total_learner':0,
            }
            return render(request,'staff/staff_dashboard.html',{'mcqques':mcqques,'sques':sques,'mco':mco,'short':short,'dict':dict})
        else:
            return render(request,'loginrelated/diffrentuser.html')
    #except:
        return render(request,'lxpapp/404page.html')
 
@login_required
def staff_add_material_view(request):
    try:
        if str(request.session['utype']) == 'staff':
            if request.method=='POST':
                materialForm=LXPFORM.MaterialForm(request.POST)
                subject = request.POST.get('subject')
                chapter = request.POST.get('chapter')
                mtype = request.POST.get('mtype')
                topic = name = request.POST.get('topic')
                urlvalue = request.POST.get('urlvalue')
                description = request.POST.get('description')
                material = LXPModel.Material.objects.create(subject_id = subject,chapter_id = chapter,topic = topic,mtype = mtype,urlvalue = urlvalue,description = description)
                topic = LXPModel.Topic.objects.all().filter(topic_name__iexact = name)
                if not topic:
                    topic = LXPModel.Topic.objects.create(
                                                topic_name = name,
                                                chapter_id = chapter)
                    topic.save()
                material.save()
                
            materialForm=LXPFORM.MaterialForm()
            return render(request,'staff/material/staff_add_material.html',{'materialForm':materialForm})
    except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def staff_update_material_view(request,pk):
    try:
        if str(request.session['utype']) == 'staff':
            materialForm=LXPFORM.MaterialForm(request.POST)
            if request.method=='POST':
                subject = request.POST.get('subject')
                chapter = request.POST.get('chapter')
                mtype = request.POST.get('mtype')
                topic = request.POST.get('topic')
                urlvalue = request.POST.get('urlvalue')
                description = request.POST.get('description')
                
                material = LXPModel.Material.objects.get(id=pk)
                material.subject_id = subject
                material.chapter_id = chapter
                material.topic = topic
                material.mtype = mtype
                material.urlvalue = urlvalue
                material.description = description
                material.save()
                materials = LXPModel.Material.objects.all()
                return render(request,'staff/material/staff_view_material.html',{'materials':materials})
            material_instance = get_object_or_404(LXPModel.Material, id=pk)
            materialForm = LXPFORM.MaterialForm(instance=material_instance)
            return render(request,'staff/material/staff_update_material.html',{'materialForm':materialForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_view_material_view(request):
    #try:
        if str(request.session['utype']) == 'staff':
            materials = LXPModel.Material.objects.all()
            return render(request,'staff/material/staff_view_material.html',{'materials':materials})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_delete_material_view(request,pk):
    try:
        if str(request.session['utype']) == 'staff':  
            material=LXPModel.Material.objects.get(id=pk)
            material.delete()
            materials = LXPModel.Material.objects.all()
            return render(request,'staff/material/staff_view_material.html',{'materials':materials})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_show_material_view(request,materialtype,pk):
    try:
        if str(request.session['utype']) == 'staff':
            details= LXPModel.Material.objects.all().filter(id=pk)
            if materialtype == 'HTML':
                return render(request,'staff/material/staff_material_htmlshow.html',{'details':details})
            if materialtype == 'URL':
                return render(request,'staff/material/staff_material_urlshow.html',{'details':details})
            if materialtype == 'PDF':
                return render(request,'staff/material/staff_material_pdfshow.html',{'details':details})
            if materialtype == 'Video':
                return render(request,'staff/material/staff_material_videoshow.html',{'details':details})
    except:
        return render(request,'lxpapp/404page.html')
@login_required
def staff_upload_material_details_csv_view(request):
    if request.method=='POST':
        if request.POST.get('select_file') == '':
            messages.info(request, 'Please select CSV file for upload')
        else:
            csv_file = request.FILES["select_file"]
            file_data = csv_file.read().decode("utf-8")		
            lines = file_data.split("\n")
            mat_type =''
            mat_url =''
            mat_desc =''
            oldsub =''
            oldchap=''
            top=''
            subid =0
            chapid=0
            topid=0
            tochk=''
            no = 0
            for line in lines:						
                no = no + 1
                if no > 1:
                    fields = line.split(",")
                    mat_type = str(fields[3]).replace('///',',').replace('\r','')
                    mat_url = str(fields[4]).replace('///',',').replace('\r','')
                    mat_desc = str(fields[5]).replace('///',',').replace('\r','')
                    tochk = str(fields[0]).replace('///',',').replace('\r','')
                    if tochk != oldsub:
                        oldsub = tochk
                        sub = LXPModel.Subject.objects.all().filter(subject_name__exact = oldsub )
                        if not sub:
                            sub = LXPModel.Subject.objects.create(subject_name = oldsub )
                            sub.save()
                            subid=sub.id
                        else:
                            for x in sub:
                                subid=x.id  
                    tochk = str(fields[1]).replace('///',',').replace('\r','')
                    if tochk != oldchap:
                        oldchap = tochk
                        chap = LXPModel.Chapter.objects.all().filter(chapter_name__exact = oldchap,subject_id=subid)
                        if not chap:
                            chap = LXPModel.Chapter.objects.create(chapter_name = oldchap,subject_id=subid)
                            chap.save()
                            chapid=chap.id
                        else:
                            for x in chap:
                                chapid=x.id 
                    top = str(fields[2]).replace('///',',').replace('\r','')
                    t = LXPModel.Topic.objects.all().filter(topic_name__exact = top,chapter_id=chapid)
                    if not t:
                        t = LXPModel.Topic.objects.create(topic_name = top,chapter_id=chapid)
                        t.save()
                    mat = LXPModel.Material.objects.create(
                                subject_id=subid,
                                chapter_id=chapid,
                                topic =top,
                                mtype = mat_type,
                                urlvalue = mat_url,
                                description = mat_desc
                                )
                    mat.save()
    return render(request,'staff/material/staff_upload_material_details_csv.html')

@login_required
def staff_sessionmaterial_view(request):
    try:
        if str(request.session['utype']) == 'staff':
            return render(request,'staff/sessionmaterial/staff_sessionmaterial.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_add_sessionmaterial_view(request):
    try:
        if str(request.session['utype']) == 'staff':
            if request.method=='POST':
                sessionmaterialForm=LXPFORM.SessionMaterialForm(request.POST)
                playlist = request.POST.get('playlist')
                video = request.POST.get('video')
                mtype = request.POST.get('mtype')
                urlvalue = request.POST.get('urlvalue')
                description = request.POST.get('description')
                sessionmaterial = LXPModel.SessionMaterial.objects.create(playlist_id = playlist,video_id = video,mtype = mtype,urlvalue = urlvalue,description = description)
                sessionmaterial.save()
                
            sessionmaterialForm=LXPFORM.SessionMaterialForm()
            return render(request,'staff/sessionmaterial/staff_add_sessionmaterial.html',{'sessionmaterialForm':sessionmaterialForm})
    except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def staff_update_sessionmaterial_view(request,pk):
    try:
        if str(request.session['utype']) == 'staff':
            sessionmaterialForm=LXPFORM.SessionMaterialForm(request.POST)
            if request.method=='POST':
                playlist = request.POST.get('playlist')
                video = request.POST.get('video')
                mtype = request.POST.get('mtype')
                urlvalue = request.POST.get('urlvalue')
                description = request.POST.get('description')
                
                sessionmaterial = LXPModel.SessionMaterial.objects.get(id=pk)
                sessionmaterial.playlist_id = playlist
                sessionmaterial.video_id = video
                sessionmaterial.mtype = mtype
                sessionmaterial.urlvalue = urlvalue
                sessionmaterial.description = description
                sessionmaterial.save()
                sessionmaterials = LXPModel.SessionMaterial.objects.all()
                return render(request,'staff/sessionmaterial/staff_view_sessionmaterial.html',{'sessionmaterials':sessionmaterials})
            sessionmaterial_instance = get_object_or_404(LXPModel.SessionMaterial, id=pk)
            sessionmaterialForm = LXPFORM.SessionMaterialForm(instance=sessionmaterial_instance)
            return render(request,'staff/sessionmaterial/staff_update_sessionmaterial.html',{'sessionmaterialForm':sessionmaterialForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_view_sessionmaterial_view(request):
    try:
        if str(request.session['utype']) == 'staff':
            sessionmaterials = LXPModel.SessionMaterial.objects.all()
            return render(request,'staff/sessionmaterial/staff_view_sessionmaterial.html',{'sessionmaterials':sessionmaterials})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_delete_sessionmaterial_view(request,pk):
    try:
        if str(request.session['utype']) == 'staff':  
            sessionmaterial=LXPModel.SessionMaterial.objects.get(id=pk)
            sessionmaterial.delete()
            sessionmaterials = LXPModel.SessionMaterial.objects.all()
            return render(request,'staff/sessionmaterial/staff_view_sessionmaterial.html',{'sessionmaterials':sessionmaterials})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_show_sessionmaterial_view(request,sessionmaterialtype,pk):
    try:
        if str(request.session['utype']) == 'staff':
            details= LXPModel.SessionMaterial.objects.all().filter(id=pk)
            if sessionmaterialtype == 'HTML':
                return render(request,'staff/sessionmaterial/staff_sessionmaterial_htmlshow.html',{'details':details})
            if sessionmaterialtype == 'URL':
                return render(request,'staff/sessionmaterial/staff_sessionmaterial_urlshow.html',{'details':details})
            if sessionmaterialtype == 'PDF':
                return render(request,'staff/sessionmaterial/staff_sessionmaterial_pdfshow.html',{'details':details})
            if sessionmaterialtype == 'Video': 
                return render(request,'staff/sessionmaterial/staffsessionmaterial_videoshow.html',{'details':details})
    except:
        return render(request,'lxpapp/404page.html')

def load_videos(request):
    try:
        playlist_id = request.GET.get('playlist')
        videos = LXPModel.PlaylistItem.objects.raw('SELECT  lxpapp_video.id as id,lxpapp_video.id as pk, lxpapp_video.name FROM  lxpapp_playlistitem  INNER JOIN lxpapp_video ON (lxpapp_playlistitem.video_id = lxpapp_video.id) WHERE  lxpapp_playlistitem.playlist_id = ' + str(playlist_id) + ' ORDER BY  lxpapp_video.name')
        context = {'videos': videos}
        return render(request, 'hr/video_dropdown_list_options.html', context)
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_exam_view(request):
    try:
        if str(request.session['utype']) == 'staff':
            return render(request,'staff/exam/staff_exam.html')
    except:
        return render(request,'lxpapp/404page.html')


@login_required
def staff_add_exam_view(request):
    try:
        if str(request.session['utype']) == 'staff':
            form = LXPFORM.ExamForm(request.POST or None)
            breadcrumblink = []
            btrnr={}
            btrnr["head"]='Dashboard'
            btrnr["link"]='../../../../staff/staff-dashboard'
            breadcrumblink.append(btrnr)

            btrnr={}
            btrnr["head"]='View Exam'
            btrnr["link"]='../../../../staff/staff-view-exam'
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
                    exam = LXPModel.Exam.objects.all().filter(exam_name__iexact = name)
                    if exam:
                        messages.info(request, 'Exam Name Already Exist')
                        return redirect(reverse('staff-add-exam'))
                    try:
                        qtype = form.cleaned_data.get('questiontpye')
                        batch = form.cleaned_data.get('batch').pk
                        exam = LXPModel.Exam.objects.create(
                                                    exam_name = name,questiontpye=qtype,batch_id=batch)
                        exam.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('staff-add-exam'))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'staff/exam/add_edit_exam.html', context)
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_update_exam_view(request,pk):
    try:
        if str(request.session['utype']) == 'staff':
            instance = get_object_or_404(LXPModel.Exam, id=pk)
            form = LXPFORM.ExamForm(request.POST or None, instance=instance)
            breadcrumblink = []
            btrnr={}
            btrnr["head"]='Dashboard'
            btrnr["link"]='../../../../staff/staff-dashboard'
            breadcrumblink.append(btrnr)
            
            btrnr={}
            btrnr["head"]='Add Exam'
            btrnr["link"]='../../../../staff/staff-add-exam'
            breadcrumblink.append(btrnr)
            
            btrnr={}
            btrnr["head"]='View Exam'
            btrnr["link"]='../../../../staff/staff-view-exam'
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
                    exam = LXPModel.Exam.objects.all().filter(exam_name__iexact = name).exclude(id=pk)
                    if exam:
                        messages.info(request, 'Exam Name Already Exist')
                        return redirect(reverse('staff-update-exam', args=[pk]))
                    try:
                        exam = LXPModel.Exam.objects.get(id=pk)
                        exam.exam_name = name
                        exam.batch_id = batch
                        exam.questiontpye = qtype
                        exam.save()
                        messages.success(request, "Successfully Updated")
                        exams = LXPModel.Exam.objects.all()
                        return render(request,'staff/exam/staff_view_exam.html',{'exams':exams})
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")

            return render(request, 'staff/exam/add_edit_exam.html', context,{'a':'imran'})
    except:
        return render(request,'lxpapp/404page.html')
@login_required
def staff_upload_exam_csv_view(request):
    if request.method=='POST':
        file=request.FILES["select_file"]
        examtext=request.POST.get('exam_name')
        batch=request.POST.get('batch')
        qtype=request.POST.get('examtype')
        exam = LXPModel.Exam.objects.all().filter(exam_name__iexact = examtext)
        if exam:
            messages.info(request, 'Exam Name Already Exist')
        else:
            if qtype=='0':
                qtype = 'MCQ'
            else:
                qtype = 'ShortAnswer'
            exam = LXPModel.Exam.objects.create(batch_id = batch,exam_name = examtext,questiontpye = qtype)
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
                        question = LXPModel.McqQuestion.objects.create(
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
                        question = LXPModel.ShortQuestion.objects.create(
                            question = fields[0],
                            marks = fields[1],
                            exam_id = exam.id
                        )
                        question.save()
    batch = LXPModel.Batch.objects.all()
    context = {'batch': batch}
    return render(request,'staff/exam/staff_upload_exam_csv.html',context)

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
def staff_view_exam_view(request):
    try:
        if str(request.session['utype']) == 'staff':
            exams = LXPModel.Exam.objects.all().filter(batch_id__in = LXPModel.Batch.objects.all())
            return render(request,'staff/exam/staff_view_exam.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')

def staff_view_filter_exam_view(request,type):
    try:
        if str(request.session['utype']) == 'staff':
            exams = LXPModel.Exam.objects.all().filter(batch_id__in = LXPModel.Batch.objects.all(),questiontpye = type)
            return render(request,'staff/exam/staff_view_exam.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_delete_exam_view(request,pk):
    try:
        if str(request.session['utype']) == 'staff':  
            exam=LXPModel.Exam.objects.get(id=pk)
            exam.delete()
            return HttpResponseRedirect('/staff/staff-view-exam')
        exams = LXPModel.Exam.objects.all()
        return render(request,'staff/exam/staff_view_exam.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')
 
@login_required
def staff_mcqquestion_view(request):
    try:
        if str(request.session['utype']) == 'staff':
            return render(request,'staff/mcqquestion/staff_mcqquestion.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_add_mcqquestion_view(request):
    try:
        if str(request.session['utype']) == 'staff':
            storage = messages.get_messages(request)
            storage.used = True
            if request.method=='POST':
                mcqquestionForm=LXPFORM.McqQuestionForm(request.POST)
                if mcqquestionForm.is_valid(): 
                    questiontext = mcqquestionForm.cleaned_data["question"]
                    mcqquestion = LXPModel.McqQuestion.objects.all().filter(question__iexact = questiontext)
                    if mcqquestion:
                        messages.info(request, 'Mcq Question Name Already Exist')
                        mcqquestionForm=LXPFORM.McqQuestionForm()
                        return render(request,'staff/mcqquestion/staff_add_mcqquestion.html',{'mcqquestionForm':mcqquestionForm})                  
                    else:
                        exam=LXPModel.Exam.objects.get(id=request.POST.get('examID'))
                        mcqquestion = LXPModel.McqQuestion.objects.create(exam_id = exam.id,question = questiontext,option1=request.POST.get('option1'),option2=request.POST.get('option2'),option3=request.POST.get('option3'),option4=request.POST.get('option4'),answer=request.POST.get('answer'),marks=request.POST.get('marks'))
                        mcqquestion.save()
                        messages.info(request, 'Mcq Question added')
                else:
                    print("form is invalid")
            mcqquestionForm=LXPFORM.McqQuestionForm()
            return render(request,'staff/mcqquestion/staff_add_mcqquestion.html',{'mcqquestionForm':mcqquestionForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_update_mcqquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'staff':
            mcqquestion = LXPModel.McqQuestion.objects.get(id=pk)
            mcqquestionForm=LXPFORM.McqQuestionForm(request.POST,instance=mcqquestion)
            if request.method=='POST':
                if mcqquestionForm.is_valid(): 
                    mcqquestiontext = mcqquestionForm.cleaned_data["mcqquestion_name"]
                    mcqquestion = LXPModel.McqQuestion.objects.all().filter(mcqquestion_name__iexact = mcqquestiontext).exclude(id=pk)
                    if mcqquestion:
                        messages.info(request, 'McqQuestion Name Already Exist')
                        return render(request,'staff/mcqquestion/staff_update_mcqquestion.html',{'mcqquestionForm':mcqquestionForm})
                    else:
                        mcqquestionForm.save()
                        mcqquestions = LXPModel.McqQuestion.objects.all()
                        return render(request,'staff/mcqquestion/staff_view_mcqquestion.html',{'mcqquestions':mcqquestions})
            mcqquestion_instance = get_object_or_404(LXPModel.McqQuestion, id=pk)
            mcqquestionForm = LXPFORM.McqQuestionForm(instance=mcqquestion_instance)
            return render(request,'staff/mcqquestion/staff_update_mcqquestion.html',{'mcqquestionForm':mcqquestionForm,'ex':mcqquestion.mcqquestion_name,'sub':mcqquestion.questiontpye})
    except:
        return render(request,'lxpapp/404page.html')
@login_required
def staff_view_mcqquestion_exams_view(request):
    try:
        if str(request.session['utype']) == 'staff':
            exams = LXPModel.Exam.objects.all().filter(questiontpye='MCQ')
            return render(request,'staff/mcqquestion/staff_view_mcqquestion_exams.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')
@login_required
def staff_view_mcqquestion_view(request,examid):
    try:
        if str(request.session['utype']) == 'staff':
            mcqquestions = LXPModel.McqQuestion.objects.all().filter(exam_id__in = LXPModel.Exam.objects.all().filter(id=examid))
            return render(request,'staff/mcqquestion/staff_view_mcqquestion.html',{'mcqquestions':mcqquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_delete_mcqquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'staff':  
            mcqquestion=LXPModel.McqQuestion.objects.get(id=pk)
            mcqquestion.delete()
            return HttpResponseRedirect('/staff/staff-view-mcqquestion')
        mcqquestions = LXPModel.McqQuestion.objects.all()
        return render(request,'staff/mcqquestion/staff_view_mcqquestion.html',{'mcqquestions':mcqquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_shortquestion_view(request):
    try:
        if str(request.session['utype']) == 'staff':
            return render(request,'staff/shortquestion/staff_shortquestion.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_add_shortquestion_view(request):
    try:
        if str(request.session['utype']) == 'staff':
            if request.method=='POST':
                shortquestionForm=LXPFORM.ShortQuestionForm(request.POST)
                if shortquestionForm.is_valid(): 
                    questiontext = shortquestionForm.cleaned_data["question"]
                    shortquestion = LXPModel.ShortQuestion.objects.all().filter(question__iexact = questiontext)
                    if shortquestion:
                        messages.info(request, 'Short Question Already Exist')
                        shortquestionForm=LXPFORM.ShortQuestionForm()
                        return render(request,'staff/shortquestion/staff_add_shortquestion.html',{'shortquestionForm':shortquestionForm})                  
                    else:
                        exam=LXPModel.Exam.objects.get(id=request.POST.get('examID'))
                        shortquestion = LXPModel.ShortQuestion.objects.create(exam_id = exam.id,question = questiontext,marks=request.POST.get('marks'))
                        shortquestion.save()
                else:
                    print("form is invalid")
            shortquestionForm=LXPFORM.ShortQuestionForm()
            return render(request,'staff/shortquestion/staff_add_shortquestion.html',{'shortquestionForm':shortquestionForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_update_shortquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'staff':
            shortquestion = LXPModel.ShortQuestion.objects.get(id=pk)
            shortquestionForm=LXPFORM.ShortQuestionForm(request.POST,instance=shortquestion)
            if request.method=='POST':
                if shortquestionForm.is_valid(): 
                    shortquestiontext = shortquestionForm.cleaned_data["question"]
                    shortquestion = LXPModel.ShortQuestion.objects.all().filter(question__iexact = shortquestiontext).exclude(id=pk)
                    if shortquestion:
                        messages.info(request, 'ShortQuestion Name Already Exist')
                    else:
                        examid = LXPModel.Exam.objects.all().filter(id=request.POST['examID'])
                        shortquestionForm.examID=examid
                        shortquestionForm.save()
                        shortquestions = LXPModel.ShortQuestion.objects.all()
                        return render(request,'staff/shortquestion/staff_view_shortquestion.html',{'shortquestions':shortquestions})
            shortquestion_instance = get_object_or_404(LXPModel.ShortQuestion, id=pk)
            shortquestionForm = LXPFORM.ShortQuestionForm(instance=shortquestion_instance)
            return render(request,'staff/shortquestion/staff_update_shortquestion.html',{'shortquestionForm':shortquestionForm,'ex':shortquestion.question})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_view_shortquestion_view(request):
    try:
        if str(request.session['utype']) == 'staff':
            shortquestions = LXPModel.ShortQuestion.objects.all().filter(exam_id__in = LXPModel.Exam.objects.all())
            return render(request,'staff/shortquestion/staff_view_shortquestion.html',{'shortquestions':shortquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_delete_shortquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'staff':  
            shortquestion=LXPModel.ShortQuestion.objects.get(id=pk)
            shortquestion.delete()
            return HttpResponseRedirect('/staff/staff-view-shortquestion')
        shortquestions = LXPModel.ShortQuestion.objects.all()
        return render(request,'staff/shortquestion/staff_view_shortquestion.html',{'shortquestions':shortquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_pending_short_exam_result_view(request):
    try:
        if str(request.session['utype']) == 'staff':
            pending = LXPModel.ShortResult.objects.all().filter( learner_id__in = User.objects.all(),exam_id__in = LXPModel.Exam.objects.all(),status = False)
            return render(request,'staff/shortexam/staff_pending_short_exam_reuslt.html',{'pending':pending})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_update_short_question_result_view(request,pk):
    try:
        if str(request.session['utype']) == 'staff':
            resultdetails = LXPModel.ShortResultDetails.objects.all().filter( question_id__in = LXPModel.ShortQuestion.objects.all(),shortresult_id = pk)
            
            return render(request,'staff/shortexam/staff_update_short_question_result.html',{'resultdetails':resultdetails})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_save_short_question_result_view(request,pk):
    try:
        if str(request.session['utype']) == 'staff':
            if request.method=="POST":
                feedback=request.POST['newfeedback']
                marks=request.POST['newmarks']
                rid=request.POST['newid']
                qid=request.POST['newqid']
                answer=request.POST['newanswer']
                mainid=request.POST['newmainid']
                resupdate = LXPModel.ShortResultDetails.objects.all().filter(id=pk)
                resupdate.delete()
                resupdate = LXPModel.ShortResultDetails.objects.create(id=pk,marks=marks,feedback=feedback,question_id=qid,answer=answer,shortresult_id=mainid)
                resupdate.save()
                
                totmarks=LXPModel.ShortResultDetails.objects.all().filter(shortresult_id=mainid).aggregate(stars=Sum('marks'))['stars']
                maintbl=LXPModel.ShortResult.objects.get(id=mainid)
                tot=LXPModel.ShortResultDetails.objects.all().filter(shortresult_id=mainid).aggregate(stars=Count('marks'))['stars']
                totgiven=LXPModel.ShortResultDetails.objects.all().filter(shortresult_id=mainid,marks__gt=0).aggregate(stars=Count('marks'))['stars']
                if tot == totgiven:
                    maintbl.status=True
                maintbl.marks = totmarks
                maintbl.save()
                if tot == totgiven:
                    resultdetails = LXPModel.ShortResultDetails.objects.all().filter( question_id__in = LXPModel.ShortQuestion.objects.all(),shortresult_id = pk)
                    return render(request,'staff/shortexam/staff_update_short_question_result.html',{'resultdetails':resultdetails})
                else:
                    resultdetails = LXPModel.ShortResultDetails.objects.all().filter( question_id__in = LXPModel.ShortQuestion.objects.all(),shortresult_id = mainid)
                    return render(request,'staff/shortexam/staff_update_short_question_result.html',{'resultdetails':resultdetails})
    except:
        return render(request,'lxpapp/404page.html') 

@login_required
def staff_ytexamquestion_view(request):
    try:
        if str(request.session['utype']) == 'staff':
            return render(request,'staff/ytexamquestion/staff_ytexamquestion.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_add_ytexamquestion_view(request):
    try:
        if str(request.session['utype']) == 'staff':
            if request.method=='POST':
                ytexamquestionForm=LXPFORM.YTExamQuestionForm(request.POST)
                if ytexamquestionForm.is_valid(): 
                    questiontext = ytexamquestionForm.cleaned_data["question"]
                    ytexamquestion = LXPModel.YTExamQuestion.objects.all().filter(question__iexact = questiontext)
                    if ytexamquestion:
                        messages.info(request, 'Mcq Question Name Already Exist')
                        ytexamquestionForm=LXPFORM.YTExamQuestionForm()
                        return render(request,'staff/ytexamquestion/staff_add_ytexamquestion.html',{'ytexamquestionForm':ytexamquestionForm})                  
                    else:
                        playlist=LXPModel.Playlist.objects.get(id=ytexamquestionForm.cleaned_data["playlistID"].pk)
                        video=LXPModel.Video.objects.get(id=ytexamquestionForm.cleaned_data["videoID"].pk)
                        ytexamquestion = LXPModel.YTExamQuestion.objects.create(
                            playlist_id = playlist.id,
                            video_id = video.id,
                            question = questiontext,
                            option1=request.POST.get('option1'),
                            option2=request.POST.get('option2'),
                            option3=request.POST.get('option3'),
                            option4=request.POST.get('option4'),
                            answer=request.POST.get('answer'),
                            marks=request.POST.get('marks'))
                        ytexamquestion.save()
                else:
                    print("form is invalid")
            ytexamquestionForm=LXPFORM.YTExamQuestionForm()
            return render(request,'staff/ytexamquestion/staff_add_ytexamquestion.html',{'ytexamquestionForm':ytexamquestionForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_update_ytexamquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'staff':
            ytexamquestion = LXPModel.YTExamQuestion.objects.get(id=pk)
            ytexamquestionForm=LXPFORM.YTExamQuestionForm(request.POST,instance=ytexamquestion)
            if request.method=='POST':
                if ytexamquestionForm.is_valid(): 
                    ytexamquestiontext = ytexamquestionForm.cleaned_data["ytexamquestion_name"]
                    ytexamquestion = LXPModel.YTExamQuestion.objects.all().filter(ytexamquestion_name__iexact = ytexamquestiontext).exclude(id=pk)
                    if ytexamquestion:
                        messages.info(request, 'Question Already Exist')
                    else:
                        ytexamquestionForm.save()
                        ytexamquestions = LXPModel.YTExamQuestion.objects.all()
                        return render(request,'staff/ytexamquestion/staff_view_ytexamquestion.html',{'ytexamquestions':ytexamquestions})
            ytexamquestion_instance = get_object_or_404(LXPModel.YTExamQuestion, id=pk)
            ytexamquestionForm = LXPFORM.YTExamQuestionForm(instance=ytexamquestion_instance)
            return render(request,'staff/ytexamquestion/staff_update_ytexamquestion.html',{'ytexamquestionForm':ytexamquestionForm,'ex':ytexamquestion.ytexamquestion_name,'sub':ytexamquestion.questiontpye})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_view_ytexamquestion_view(request):
    try:
        if str(request.session['utype']) == 'staff':
            ytexamquestions = LXPModel.YTExamQuestion.objects.all().filter(playlist_id__in = LXPModel.Playlist.objects.all())
            return render(request,'staff/ytexamquestion/staff_view_ytexamquestion.html',{'ytexamquestions':ytexamquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_delete_ytexamquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'staff':  
            ytexamquestion=LXPModel.YTExamQuestion.objects.get(id=pk)
            ytexamquestion.delete()
            return HttpResponseRedirect('/staff/staff-view-ytexamquestion')
        ytexamquestions = LXPModel.YTExamQuestion.objects.all()
        return render(request,'staff/ytexamquestion/staff_view_ytexamquestion.html',{'ytexamquestions':ytexamquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_view_learner_video_view(request):
    #try:
        if str(request.session['utype']) == 'staff':
            learner = UserSocialAuth.objects.raw('SELECT social_auth_usersocialauth.id, social_auth_usersocialauth.user_id, social_auth_usersocialauth.pic, auth_user.first_name, auth_user.last_name, GROUP_CONCAT(DISTINCT lxpapp_playlist.name) AS courseset_name, lxpapp_learnerdetails.mobile FROM social_auth_usersocialauth LEFT OUTER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id) LEFT OUTER JOIN lxpapp_batchlearner ON (auth_user.id = lxpapp_batchlearner.learner_id) LEFT OUTER JOIN lxpapp_batchrecordedvdolist ON (lxpapp_batchlearner.batch_id = lxpapp_batchrecordedvdolist.batch_id) LEFT OUTER JOIN lxpapp_playlist ON (lxpapp_batchrecordedvdolist.playlist_id = lxpapp_playlist.id) LEFT OUTER JOIN lxpapp_learnerdetails ON (auth_user.id = lxpapp_learnerdetails.learner_id) WHERE (social_auth_usersocialauth.utype = 0 OR social_auth_usersocialauth.utype = 2) AND social_auth_usersocialauth.status = 1 GROUP BY social_auth_usersocialauth.id, social_auth_usersocialauth.user_id, auth_user.first_name, auth_user.last_name, lxpapp_learnerdetails.mobile ')
            return render(request,'staff/learnervideo/staff_view_learner_video.html',{'learner':learner})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_learner_video_Course_view(request,user_id,userfirstname,userlastname):
#    try:    
        if str(request.session['utype']) == 'staff':
            videos1 = LXPModel.BatchCourseSet.objects.raw('SELECT DISTINCT lxpapp_courseset.id,  lxpapp_courseset.courseset_name,lxpapp_batchcourseset.batch_id FROM  lxpapp_batchcourseset   INNER JOIN lxpapp_courseset ON (lxpapp_batchcourseset.courseset_id = lxpapp_courseset.id)   INNER JOIN lxpapp_batch ON (lxpapp_batchcourseset.batch_id = lxpapp_batch.id)   INNER JOIN lxpapp_batchlearner ON (lxpapp_batchlearner.batch_id = lxpapp_batch.id) WHERE   lxpapp_batchlearner.learner_id = ' + str(user_id))
            return render(request,'staff/learnervideo/staff_learner_video_course.html',{'videos':videos1,'userfirstname':userfirstname,'userlastname':userlastname,'user_id':user_id})
 #   except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_learner_video_Course_subject_view(request,user_id,userfirstname,userlastname):
#    try:    
        if str(request.session['utype']) == 'staff':
            
            subject = LXPModel.Playlist.objects.raw('SELECT ID AS id, NAME, VTOTAL, Mtotal, SUM(VWATCHED) AS VWatched,((100*VWATCHED)/VTOTAL) as per, THUMBNAIL_URL FROM (SELECT YYY.ID, YYY.NAME, YYY.THUMBNAIL_URL, ( SELECT COUNT(XX.ID) FROM LXPAPP_PLAYLISTITEM XX WHERE XX.PLAYLIST_ID = YYY.ID ) AS Vtotal, ( SELECT COUNT(zz.ID) FROM LXPAPP_sessionmaterial zz WHERE zz.PLAYLIST_ID = YYY.ID ) AS Mtotal, (SELECT COUNT (LXPAPP_VIDEOWATCHED.ID) AS a FROM LXPAPP_PLAYLISTITEM GHGH LEFT OUTER JOIN LXPAPP_VIDEOWATCHED ON ( GHGH.VIDEO_ID = LXPAPP_VIDEOWATCHED.VIDEO_ID ) WHERE GHGH.PLAYLIST_ID = YYY.ID AND LXPAPP_VIDEOWATCHED.LEARNER_ID = ' + str( user_id) + ') AS VWatched FROM LXPAPP_BATCHLEARNER INNER JOIN LXPAPP_BATCH ON (LXPAPP_BATCHLEARNER.BATCH_ID = LXPAPP_BATCH.ID) INNER JOIN LXPAPP_BATCHRECORDEDVDOLIST ON (LXPAPP_BATCH.ID = LXPAPP_BATCHRECORDEDVDOLIST.BATCH_ID) INNER JOIN LXPAPP_PLAYLIST YYY ON (LXPAPP_BATCHRECORDEDVDOLIST.PLAYLIST_ID = YYY.ID) WHERE LXPAPP_BATCHLEARNER.LEARNER_ID = ' + str(user_id) + ') GROUP BY ID, NAME, VTOTAL ORDER BY NAME')
            videocount = LXPModel.LearnerPlaylistCount.objects.all().filter(learner_id = user_id)
            countpresent =False
            if videocount:
                countpresent = True
            per = 0
            tc = 0
            wc = 0
            for x in subject:
                if not videocount:
                    countsave = LXPModel.LearnerPlaylistCount.objects.create(playlist_id = x.id, learner_id = user_id,count =x.Vtotal )
                    countsave.save()
                tc += x.Vtotal
                wc += x.VWatched
            try:
                per = (100*int(wc))/int(tc)
            except:
                per =0
            dif = tc- wc
            return render(request,'staff/learnervideo/staff_learner_video_course_subject.html',{'user_id':user_id,'subject':subject,'userfirstname':userfirstname,'userlastname':userlastname,'dif':dif,'per':per,'wc':wc,'tc':tc})
 #   except:
        return render(request,'lxpapp/404page.html')
 
@login_required
def staff_learner_video_list_view(request,subject_id,user_id):
    try:     
        if str(request.session['utype']) == 'staff':
            subjectname = LXPModel.Playlist.objects.only('name').get(id=subject_id).name
            list = LXPModel.PlaylistItem.objects.raw('SELECT DISTINCT mainvid.id, mainvid.name, IFNULL((SELECT lxpapp_videowatched.video_id FROM lxpapp_videowatched WHERE lxpapp_videowatched.learner_id = ' + str(user_id) + ' AND lxpapp_videowatched.video_id = mainvid.id), 0) AS watched, IFNULL((SELECT lxpapp_videotounlock.video_id FROM lxpapp_videotounlock WHERE lxpapp_videotounlock.learner_id = ' + str(user_id) + ' AND lxpapp_videotounlock.video_id = mainvid.id), 0) AS unlocked FROM lxpapp_video mainvid INNER JOIN lxpapp_playlistitem ON (mainvid.id = lxpapp_playlistitem.video_id) WHERE lxpapp_playlistitem.playlist_id = ' + str (subject_id) + ' AND mainvid.name <> "Deleted video"')  
            return render(request,'staff/learnervideo/staff_learner_video_list.html',{'list':list,'subjectname':subjectname,'subject_id':subject_id,'user_id':user_id})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_learner_approve_video(request,pk,studid):
    try:
        if str(request.session['utype']) == 'staff':
            unlock = LXPModel.VideoToUnlock.objects.create(learner_id=studid,video_id=pk)
            unlock.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    except:
        return render(request,'lxpapp/404page.html') 

@login_required
def staff_learner_approveall_video(request,userid,subject_id):
    try:
        if str(request.session['utype']) == 'staff':
            videos=LXPModel.Playlist.objects.raw('SELECT   lxpapp_video.id FROM  lxpapp_playlistitem  INNER JOIN lxpapp_video ON (lxpapp_playlistitem.video_id = lxpapp_video.id) where lxpapp_playlistitem.playlist_id = ' + str (subject_id))
            for x in videos:
                unlock = LXPModel.VideoToUnlock.objects.create(learner_id=userid,video_id=x.id)
                unlock.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_learner_show_video_view(request,subject_id,video_id):
    try:    
        if str(request.session['utype']) == 'staff':
            subjectname = LXPModel.Playlist.objects.only('name').get(id=subject_id).name
            Videos=LXPModel.Video.objects.all().filter(id=video_id)
            topicname =''
            url=''
            for x in Videos:
                topicname =x.name
                url = "https://www.youtube.com/embed/" + x.video_id
            return render(request,'staff/learnervideo/staff_learner_show_video.html',{'topicname':topicname,'url':url,'subjectname':subjectname,'subject_id':subject_id})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_add_chapterquestion_view(request):
    try:
        if str(request.session['utype']) == 'staff':
            storage = messages.get_messages(request)
            storage.used = True
            if request.method=='POST':
                chapterquestionForm=LXPFORM.ChapterQuestionForm(request.POST)
                if chapterquestionForm.is_valid(): 
                    questiontext = chapterquestionForm.cleaned_data["question"]
                    chapterquestion = LXPModel.ChapterQuestion.objects.all().filter(question__iexact = questiontext)
                    if chapterquestion:
                        messages.info(request, 'Chapter Question Name Already Exist')
                        chapterquestionForm=LXPFORM.ChapterQuestionForm()
                        return render(request,'staff/chapterquestion/staff_add_chapterquestion.html',{'chapterquestionForm':chapterquestionForm})                  
                    else:
                        chapterquestion = LXPModel.ChapterQuestion.objects.create(subject_id = chapterquestionForm.cleaned_data["subject"].pk,chapter_id = chapterquestionForm.cleaned_data["chapter"].pk,question = questiontext,option1=request.POST.get('option1'),option2=request.POST.get('option2'),option3=request.POST.get('option3'),option4=request.POST.get('option4'),answer=request.POST.get('answer'),marks=request.POST.get('marks'))
                        chapterquestion.save()
                        messages.info(request, 'Chapter  Question added')
                else:
                    print("form is invalid")
            chapterquestionForm=LXPFORM.ChapterQuestionForm()
            return render(request,'staff/chapterquestion/staff_add_chapterquestion.html',{'chapterquestionForm':chapterquestionForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_update_chapterquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'staff':
            chapterquestion = LXPModel.ChapterQuestion.objects.get(id=pk)
            chapterquestionForm=LXPFORM.ChapterQuestionForm(request.POST,instance=chapterquestion)
            if request.method=='POST':
                if chapterquestionForm.is_valid(): 
                    chapterquestiontext = chapterquestionForm.cleaned_data["chapterquestion_name"]
                    chapterquestion = LXPModel.ChapterQuestion.objects.all().filter(chapterquestion_name__iexact = chapterquestiontext).exclude(id=pk)
                    if chapterquestion:
                        messages.info(request, 'ChapterQuestion Name Already Exist')
                    else:
                        chapterquestionForm.save()
                        chapterquestions = LXPModel.ChapterQuestion.objects.all()
                        return render(request,'staff/chapterquestion/staff_view_chapterquestion.html',{'chapterquestions':chapterquestions})
            chapterquestion_instance = get_object_or_404(LXPModel.ChapterQuestion, id=pk)
            chapterquestionForm = LXPFORM.ChapterQuestionForm(instance=chapterquestion_instance)
            return render(request,'staff/chapterquestion/staff_update_chapterquestion.html',{'chapterquestionForm':chapterquestionForm,'ex':chapterquestion.chapterquestion_name,'sub':chapterquestion.questiontpye})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_view_chapterquestion_view(request):
    try:
        if str(request.session['utype']) == 'staff':
            chapterquestions = LXPModel.ChapterQuestion.objects.raw('SELECT DISTINCT  lxpapp_chapter.id,  lxpapp_subject.subject_name,  lxpapp_chapter.chapter_name FROM  lxpapp_chapterquestion  INNER JOIN lxpapp_chapter ON (lxpapp_chapterquestion.chapter_id = lxpapp_chapter.id)  INNER JOIN lxpapp_subject ON (lxpapp_chapterquestion.subject_id = lxpapp_subject.id)')
            return render(request,'staff/chapterquestion/staff_view_chapterquestion.html',{'chapterquestions':chapterquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_view_chapterquestion_chapter_view(request,chapter_id):
    try:
        if str(request.session['utype']) == 'staff':
            chapterquestions = LXPModel.ChapterQuestion.objects.all().filter(chapter_id__in = LXPModel.Chapter.objects.all().filter(id=chapter_id))
            chapter_name = LXPModel.Chapter.objects.only('chapter_name').get(id=chapter_id).chapter_name

            return render(request,'staff/chapterquestion/staff_view_chapterquestion_chapter.html',{'chapterquestions':chapterquestions,'chapter_name':chapter_name})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_delete_chapterquestion_view(request,pk):
    try:
        if str(request.session['utype']) == 'staff':  
            chapterquestion=LXPModel.ChapterQuestion.objects.get(id=pk)
            chapterquestion.delete()
            return HttpResponseRedirect('/staff/staff-view-chapterquestion')
        chapterquestions = LXPModel.ChapterQuestion.objects.all()
        return render(request,'staff/chapterquestion/staff_view_chapterquestion.html',{'chapterquestions':chapterquestions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_k8sterminal_view(request):
    try:
        if str(request.session['utype']) == 'staff':
            return render(request,'staff/labs/k8sterminal/staff_k8sterminal.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_add_k8sterminal_view(request):
    try:
        if str(request.session['utype']) == 'staff':
            if request.method=='POST':
                k8sterminalForm=LXPFORM.K8STerminalForm(request.POST)
                learner_id = request.POST['user_name']
                usagevalue = request.POST.get('usagevalue')
                password1 = request.POST.get("password")
                password2 = request.POST.get("confirmpassword")
                if password1 and password2 and password1 != password2:
                    messages.info(request, 'password_mismatch')
                else:
                    k8sterminal = LXPModel.K8STerminal.objects.create(
                        staff_id = request.user.id,
                        learner_id = learner_id,
                        Password = password1,
                        usagevalue = usagevalue)
                    k8sterminal.save()
                    messages.info(request, 'Record Saved')
            k8sterminalForm=LXPFORM.K8STerminalForm()
            users = User.objects.raw('SELECT DISTINCT   auth_user.id,  auth_user.password,  auth_user.is_superuser,  auth_user.username,  auth_user.last_name,  auth_user.email,  auth_user.first_name,  social_auth_usersocialauth.utype,  social_auth_usersocialauth.status,  social_auth_usersocialauth.uid FROM  social_auth_usersocialauth  INNER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id) WHERE  social_auth_usersocialauth.status = 1 AND   (social_auth_usersocialauth.utype = 0 OR  social_auth_usersocialauth.utype = 2 ) ORDER BY auth_user.first_name, auth_user.last_name')
            return render(request,'staff/labs/k8sterminal/staff_add_k8sterminal.html',{'k8sterminalForm':k8sterminalForm,'users':users})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_update_k8sterminal_view(request,pk):
    try:
        if str(request.session['utype']) == 'staff':
            k8sterminal = LXPModel.K8STerminal.objects.get(id=pk)
            k8sterminalForm=LXPFORM.K8STerminalForm(request.POST,instance=k8sterminal)
            if request.method=='POST':
                if k8sterminalForm.is_valid(): 
                    k8sterminaltext = k8sterminalForm.cleaned_data["k8sterminal_name"]
                    chaptertext = k8sterminalForm.cleaned_data["chapterID"]
                    subjecttext = k8sterminalForm.cleaned_data["subjectID"]
                    k8sterminal = LXPModel.K8STerminal.objects.all().filter(k8sterminal_name__iexact = k8sterminaltext).exclude(id=pk)
                    if k8sterminal:
                        messages.info(request, 'K8STerminal Name Already Exist')
                    else:
                        chapter = LXPModel.Video.objects.get(chapter_name=chaptertext)
                        subject = LXPModel.Playlist.objects.get(subject_name=subjecttext)
                        k8sterminal = LXPModel.K8STerminal.objects.get(id=pk)
                        k8sterminal.k8sterminal_name = k8sterminaltext
                        k8sterminal.subject_id = subject.id
                        k8sterminal.chapter_id = chapter.id
                        k8sterminal.save()
                        c_list = LXPModel.K8STerminal.objects.filter(chapter_id__in=LXPModel.Video.objects.all())
                        return render(request,'staff/labs/k8sterminal/staff_view_k8sterminal.html',{'k8sterminals':c_list})
            k8sterminal_instance = get_object_or_404(LXPModel.K8STerminal, id=pk)
            k8sterminalForm = LXPFORM.K8STerminalForm(instance=k8sterminal_instance)
            return render(request,'staff/labs/k8sterminal/staff_update_k8sterminal.html',{'k8sterminalForm':k8sterminalForm,'sub':k8sterminal.k8sterminal_name})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_view_k8sterminal_view(request):
    #try:
        if str(request.session['utype']) == 'staff':
            k8sterminals = LXPModel.K8STerminal.objects.all().filter(learner_id__in = User.objects.all().order_by('first_name').filter(id__in=UserSocialAuth.objects.all()))
            return render(request,'staff/labs/k8sterminal/staff_view_k8sterminal.html',{'k8sterminals':k8sterminals})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_delete_k8sterminal_view(request,pk):
    try:
        if str(request.session['utype']) == 'staff':  
            k8sterminal=LXPModel.K8STerminal.objects.get(id=pk)
            k8sterminal.delete()
            return HttpResponseRedirect('/staff/staff-view-k8sterminal')
        k8sterminals = LXPModel.K8STerminal.objects.all()
        return render(request,'staff/labs/k8sterminal/staff_view_k8sterminal.html',{'k8sterminals':k8sterminals})
    except:
        return render(request,'lxpapp/404page.html')


@login_required
def staff_python_terminal_view(request):
    #try:
        if str(request.session['utype']) == 'staff':  
            return render(request,'staff/labs/python/staff_python_terminal.html')
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_linux_terminal_view(request):
    try:
        if str(request.session['utype']) == 'staff':  
            return render(request,'staff/labs/linux/staff_linux_terminal.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_cloudshell_terminal_view(request):
    try:
        if str(request.session['utype']) == 'staff':  
            return render(request,'staff/labs/cloudshell/staff_cloudshell_terminal.html')
    except:
        return render(request,'lxpapp/404page.html')


@login_required
def staff_add_activity_view(request):
    #try:
        if str(request.session['utype']) == 'staff':
            if request.method=='POST':
                activityForm=LXPFORM.ActivityForm(request.POST)
                playlist = request.POST.get('playlist')
                video = request.POST.get('video')
                urlvalue = request.POST.get('urlvalue')
                description = request.POST.get('description')
                activity = LXPModel.Activity.objects.create(playlist_id = playlist,video_id = video,urlvalue = urlvalue,description = description)
                activity.save()
                
            activityForm=LXPFORM.ActivityForm()
            return render(request,'staff/activity/staff_add_activity.html',{'activityForm':activityForm})
    #except:
        return render(request,'lxpapp/404page.html')
    
@login_required 
def staff_update_activity_view(request,pk):
    try:
        if str(request.session['utype']) == 'staff':
            activityForm=LXPFORM.ActivityForm(request.POST)
            if request.method=='POST':
                playlist = request.POST.get('playlist')
                video = request.POST.get('video')
                urlvalue = request.POST.get('urlvalue')
                description = request.POST.get('description')
                
                activity = LXPModel.Activity.objects.get(id=pk)
                activity.playlist_id = playlist
                activity.video_id = video
                activity.urlvalue = urlvalue
                activity.description = description
                activity.save()
                activitys = LXPModel.Activity.objects.all()
                return render(request,'staff/activity/staff_view_activity.html',{'activitys':activitys})
            activity_instance = get_object_or_404(LXPModel.Activity, id=pk)
            activityForm = LXPFORM.ActivityForm(instance=activity_instance)
            return render(request,'staff/activity/staff_update_activity.html',{'activityForm':activityForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_view_activity_view(request):
    #try:
        if str(request.session['utype']) == 'staff':
            activitys = LXPModel.Activity.objects.all()
            return render(request,'staff/activity/staff_view_activity.html',{'activitys':activitys})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_delete_activity_view(request,pk):
    try:
        if str(request.session['utype']) == 'staff':  
            activity=LXPModel.Activity.objects.get(id=pk)
            activity.delete()
            activitys = LXPModel.Activity.objects.all()
            return render(request,'staff/activity/staff_view_activity.html',{'activitys':activitys})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def staff_show_activity_view(request,pk):
    try:
        if str(request.session['utype']) == 'staff':
            details= LXPModel.Activity.objects.all().filter(id=pk)
            return render(request,'staff/activity/staff_activity_urlshow.html',{'details':details})
    except:
        return render(request,'lxpapp/404page.html')
@login_required
def staff_upload_activity_details_csv_view(request):
    if request.method=='POST':
        if request.POST.get('select_file') == '':
            messages.info(request, 'Please select CSV file for upload')
        else:
            csv_file = request.FILES["select_file"]
            file_data = csv_file.read().decode("utf-8")		
            lines = file_data.split("\n")
            mat_type =''
            mat_url =''
            mat_desc =''
            oldsub =''
            oldchap=''
            top=''
            subid =0
            chapid=0
            topid=0
            tochk=''
            no = 0
            for line in lines:						
                no = no + 1
                if no > 1:
                    fields = line.split(",")
                    mat_type = str(fields[3]).replace('///',',').replace('\r','')
                    mat_url = str(fields[4]).replace('///',',').replace('\r','')
                    mat_desc = str(fields[5]).replace('///',',').replace('\r','')
                    tochk = str(fields[0]).replace('///',',').replace('\r','')
                    if tochk != oldsub:
                        oldsub = tochk
                        sub = LXPModel.Playlist.objects.all().filter(playlist_name__exact = oldsub )
                        if not sub:
                            sub = LXPModel.Playlist.objects.create(playlist_name = oldsub )
                            sub.save()
                            subid=sub.id
                        else:
                            for x in sub:
                                subid=x.id  
                    tochk = str(fields[1]).replace('///',',').replace('\r','')
                    if tochk != oldchap:
                        oldchap = tochk
                        chap = LXPModel.Video.objects.all().filter(video_name__exact = oldchap,playlist_id=subid)
                        if not chap:
                            chap = LXPModel.Video.objects.create(video_name = oldchap,playlist_id=subid)
                            chap.save()
                            chapid=chap.id
                        else:
                            for x in chap:
                                chapid=x.id 
                    top = str(fields[2]).replace('///',',').replace('\r','')
                    
                    mat = LXPModel.Activity.objects.create(
                                playlist_id=subid,
                                video_id=chapid,
                                topic =top,
                                mtype = mat_type,
                                urlvalue = mat_url,
                                description = mat_desc
                                )
                    mat.save()
    return render(request,'staff/activity/staff_upload_activity_details_csv.html')

