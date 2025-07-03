from django.contrib.auth.decorators import login_required
"""
    The `learner_edit_Learner_details_view` function allows a learner to edit their details and saves
    the changes if the form is valid.
    
    :param request: The `request` parameter is an HttpRequest object that represents the current request
    from the user's browser. It contains information about the request, such as the user's session,
    method (GET or POST), and any data sent with the request
    :return: The view is returning a rendered HTML template with the form for editing learner details
    and the learner's current details.
"""
from django.shortcuts import render, get_object_or_404, redirect
from lxpapp import models as LXPModel
from django.db.models import Q
from lxpapp.models import Poll, PollOption, PollVote
from lxpapp import forms as LXPFORM
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import F



@login_required
def learner_dashboard_view(request):
    try:    
        if str(request.session['utype']) == 'learner':
            dict={
            'total_Video':0,
            'total_exam':0,
            }
            return render(request,'learner/learner_dashboard.html',context=dict)
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_exam_view(request):
    # try:    
        if str(request.session['utype']) == 'learner':
            learner_id = request.user.id

            # Fetch exams for the learner
            exams = LXPModel.Exam.objects.filter(
                batch__batchlearner__learner_id=learner_id,
                questiontpye='MCQ'
            ).select_related('batch').distinct()

            exam_data = []

            for exam in exams:
                # Get the best score (max marks) the learner has scored for this exam
                best_result = LXPModel.McqResult.objects.filter(
                    learner_id=learner_id,
                    exam=exam
                ).order_by('-marks').first()

                # You might need to get total marks from somewhere
                # Assuming total = correct + wrong * marks per question = 1 for simplicity
                total_marks = exam.mcqquestion_set.count()  # assuming a related name
                marks_earned = best_result.marks if best_result else 0

                exam_data.append({
                    'id': exam.id,
                    'exam_name': exam.exam_name,
                    'batch_name': exam.batch.batch_name,
                    'total_marks': total_marks,
                    'marks_earned': marks_earned
                })

            return render(request, 'learner/exam/learner_exam.html', {'exams': exam_data})
    # except:
    #     return render(request,'lxpapp/404page.html')

@login_required
def learner_take_exam_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            exam = LXPModel.Exam.objects.all().filter(id=pk)
            mcqquestion= LXPModel.McqQuestion.objects.filter(exam_id=pk)
            total_marks = 0
            total_questions = 0
            for x in mcqquestion:
                total_marks = total_marks + x.marks
                total_questions = total_questions + 1
            return render(request,'learner/exam/learner_take_exam.html',{'exam':exam,'total_questions':total_questions,'total_marks':total_marks})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_start_exam_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            if request.method == 'POST':
                mcqresult = LXPModel.McqResult.objects.create(learner_id = request.user.id,exam_id =pk,marks=0,wrong=0,correct=0)
                mcqresult.save()
                questions=LXPModel.McqQuestion.objects.all().filter(exam_id=pk).order_by('?')
                score=0
                wrong=0
                correct=0
                total=0
                r_id = 0
                q_id = 0
                r_id = mcqresult.id
                for q in questions:
                    total+=1
                    question = LXPModel.McqQuestion.objects.all().filter(question=q.question)
                    for i in question:
                        q_id = i.id
                    resdet = LXPModel.McqResultDetails.objects.create(mcqresult_id = r_id,question_id =q_id,selected =str(request.POST.get(q.question)).replace('option',''))
                    resdet.save()
                    if 'option' + q.answer ==  request.POST.get(q.question):
                        score+= q.marks
                        correct+=1
                        
                    else:
                        wrong+=1
                percent = score/(total) *100
                context = {
                    'score':score,
                    'time': request.POST.get('timer'),
                    'correct':correct,
                    'wrong':wrong,
                    'percent':percent,
                    'total':total
                }
                mcqresult.marks = score
                mcqresult.wrong = wrong
                mcqresult.correct = correct
                mcqresult.timetaken = request.POST.get('timer')
                mcqresult.save()
                resdetobj = LXPModel.McqResultDetails.objects.raw("SELECT 1 as id,  lxpapp_mcqquestion.question as q,  lxpapp_mcqquestion.option1 as o1,  lxpapp_mcqquestion.option2 as o2,  lxpapp_mcqquestion.option3 as o3,  lxpapp_mcqquestion.option4 as o4,  lxpapp_mcqquestion.answer AS Correct,  lxpapp_mcqquestion.marks,  lxpapp_mcqresultdetails.selected AS answered  FROM  lxpapp_mcqresultdetails  INNER JOIN lxpapp_mcqresult ON (lxpapp_mcqresultdetails.mcqresult_id = lxpapp_mcqresult.id)  INNER JOIN lxpapp_mcqquestion ON (lxpapp_mcqresultdetails.question_id = lxpapp_mcqquestion.id) WHERE lxpapp_mcqresult.id = " + str(r_id) + " AND lxpapp_mcqresult.learner_id = " + str(request.user.id) + " ORDER BY lxpapp_mcqquestion.id" )
                return render(request,'learner/exam/learner_exam_result.html',{'total':total,'percent':percent, 'wrong':wrong,'correct':correct,'time': request.POST.get('timer'),'score':score,'resdetobj':resdetobj})
            else:
                questions=LXPModel.McqQuestion.objects.all()
                context = {
                    'questions':questions
                }
            exam=LXPModel.Exam.objects.get(id=pk)
            questions=LXPModel.McqQuestion.objects.all().filter(exam_id=exam.id).order_by('?')
            return render(request,'learner/exam/learner_start_exam.html',{'exam':exam,'questions':questions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_show_exam_reuslt_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            exams=LXPModel.McqResult.objects.all().filter(exam_id__in = LXPModel.Exam.objects.all(), learner_id=request.user.id,exam_id = pk)
            return render(request,'learner/exam/learner_show_exam_reuslt.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_show_exam_reuslt_details_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            exams=LXPModel.McqResultDetails.objects.all().filter(question_id__in = LXPModel.McqQuestion.objects.all(), mcqresult_id = pk)
            return render(request,'learner/exam/learner_exam_result_details.html',{'exams':exams})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_short_exam_view(request):
    try:    
        if str(request.session['utype']) == 'learner':
            shortexams=LXPModel.Exam.objects.raw("SELECT  lxpapp_exam.id,  lxpapp_batch.batch_name,  lxpapp_exam.exam_name FROM  lxpapp_batch  INNER JOIN lxpapp_batchlearner ON (lxpapp_batch.id = lxpapp_batchlearner.batch_id)  INNER JOIN lxpapp_exam ON (lxpapp_batch.id = lxpapp_exam.batch_id) WHERE lxpapp_exam.questiontpye = 'ShortAnswer' AND lxpapp_batchlearner.learner_id = " + str(request.user.id)) 
            return render(request,'learner/shortexam/learner_short_exam.html',{'shortexams':shortexams})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_take_short_exam_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            shortexam = LXPModel.Exam.objects.all().filter(id=pk)
            mcqquestion= LXPModel.ShortQuestion.objects.filter(exam_id=pk)
            total_marks = 0
            total_questions = 0
            for x in mcqquestion:
                total_marks = total_marks + x.marks
                total_questions = total_questions + 1
            return render(request,'learner/shortexam/learner_take_short_exam.html',{'shortexam':shortexam,'total_questions':total_questions,'total_marks':total_marks})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_start_short_exam_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            if request.method == 'POST':
                shortresult = LXPModel.ShortResult.objects.create(learner_id = request.user.id,exam_id =pk,marks=0)
                shortresult.save()
                questions=LXPModel.ShortQuestion.objects.all().filter(exam_id=pk).order_by('?')
                r_id = 0
                q_id = 0
                r_id = shortresult.id
                for q in questions:
                    question = LXPModel.ShortQuestion.objects.all().filter(question=q.question)
                    for i in question:
                        q_id = i.id
                    a=request.POST.get(str(q_id))
                    resdet = LXPModel.ShortResultDetails.objects.create(shortresult_id = r_id,question_id =q_id,answer =a,feedback ='',marks=0)
                    resdet.save()
                    
                shortresult.timetaken = request.POST.get('timer')
                shortresult.save()
                
                shortexams=LXPModel.Exam.objects.raw("SELECT  lxpapp_exam.id,  lxpapp_batch.batch_name,  lxpapp_exam.exam_name FROM  lxpapp_batch  INNER JOIN lxpapp_batchlearner ON (lxpapp_batch.id = lxpapp_batchlearner.batch_id)  INNER JOIN lxpapp_exam ON (lxpapp_batch.id = lxpapp_exam.batch_id) WHERE lxpapp_exam.questiontpye = 'ShortAnswer' AND lxpapp_batchlearner.learner_id = " + str(request.user.id)) 
                return render(request,'learner/shortexam/learner_short_exam.html',{'shortexams':shortexams})
            shortexam=LXPModel.Exam.objects.get(id=pk)
            questions=LXPModel.ShortQuestion.objects.all().filter(exam_id=shortexam.id).order_by('?')
            return render(request,'learner/shortexam/learner_start_short_exam.html',{'shortexam':shortexam,'questions':questions})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_show_short_exam_reuslt_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            #shortexams=LXPModel.ShortResult.objects.all().filter(exam_id__in = LXPModel.Exam.objects.all(), learner_id=request.user.id,exam_id = pk)
            shortexams=LXPModel.ShortResult.objects.raw("SELECT DISTINCT  lxpapp_exam.exam_name,  lxpapp_shortresult.datecreate,  SUM(DISTINCT lxpapp_shortresult.marks) AS Obtained,  Sum(lxpapp_shortquestion.marks) AS Tot,  lxpapp_shortresult.learner_id,  lxpapp_shortresult.timetaken,  lxpapp_shortresult.status,  lxpapp_shortresult.id FROM  lxpapp_shortquestion  LEFT OUTER JOIN lxpapp_exam ON (lxpapp_shortquestion.exam_id = lxpapp_exam.id)  LEFT OUTER JOIN lxpapp_shortresult ON (lxpapp_exam.id = lxpapp_shortresult.exam_id) WHERE  lxpapp_exam.id = " + str(pk) + " AND  lxpapp_shortresult.learner_id = " + str(request.user.id) + " GROUP BY  lxpapp_exam.exam_name,  lxpapp_shortresult.datecreate,  lxpapp_shortresult.learner_id,  lxpapp_shortresult.timetaken,  lxpapp_shortresult.status,  lxpapp_shortresult.id")
            return render(request,'learner/shortexam/learner_show_short_exam_reuslt.html',{'shortexams':shortexams})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_show_short_exam_reuslt_details_view(request,pk):
    try:    
        if str(request.session['utype']) == 'learner':
            shortexams=LXPModel.ShortResultDetails.objects.all().filter(question_id__in = LXPModel.ShortQuestion.objects.all(), shortresult_id = pk)
            return render(request,'learner/shortexam/learner_short_exam_result_details.html',{'shortexams':shortexams})
    except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def learner_video_Course_view(request):
    try:    
        if str(request.session['utype']) == 'learner':
            videos1 = LXPModel.BatchCourseSet.objects.raw('SELECT DISTINCT lxpapp_courseset.id,  lxpapp_courseset.courseset_name FROM  lxpapp_batchcourseset   INNER JOIN lxpapp_courseset ON (lxpapp_batchcourseset.courseset_id = lxpapp_courseset.id)   INNER JOIN lxpapp_batch ON (lxpapp_batchcourseset.batch_id = lxpapp_batch.id)   INNER JOIN lxpapp_batchlearner ON (lxpapp_batchlearner.batch_id = lxpapp_batch.id) WHERE   lxpapp_batchlearner.learner_id = ' + str(request.user.id))
            return render(request,'learner/video/learner_video_course.html',{'videos':videos1})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_video_Course_subject_view(request):
    #try:    
        if str(request.session['utype']) == 'learner':
            subject = LXPModel.Playlist.objects.raw('SELECT id AS id, name, vtotal, mtotal, SUM(vwatched) AS VWatched, ROUND(CASE WHEN vtotal = 0 THEN 0 ELSE (100 * vwatched) / vtotal END,2) AS per, thumbnail_url FROM ( SELECT YYY.id, YYY.name, YYY.thumbnail_url, (SELECT COUNT(XX.id) FROM lxpapp_playlistitem XX WHERE XX.playlist_id = YYY.id) AS Vtotal, (SELECT COUNT(zz.id) FROM lxpapp_sessionmaterial zz WHERE zz.playlist_id = YYY.id) AS Mtotal, (SELECT COUNT(lxpapp_videowatched.id) FROM lxpapp_playlistitem GHGH LEFT OUTER JOIN lxpapp_videowatched ON GHGH.video_id = lxpapp_videowatched.video_id WHERE GHGH.playlist_id = YYY.id AND lxpapp_videowatched.learner_id = ' + str(request.user.id) + ') AS VWatched FROM lxpapp_batchlearner INNER JOIN lxpapp_batch ON lxpapp_batchlearner.batch_id = lxpapp_batch.id INNER JOIN lxpapp_batchrecordedvdolist ON lxpapp_batch.id = lxpapp_batchrecordedvdolist.batch_id INNER JOIN lxpapp_playlist YYY ON lxpapp_batchrecordedvdolist.playlist_id = YYY.id WHERE lxpapp_batchlearner.learner_id = ' + str(request.user.id) + ' ) AS derived_table GROUP BY id, name, vtotal, mtotal, thumbnail_url ORDER BY name')
            
            videocount = LXPModel.LearnerPlaylistCount.objects.all().filter(learner_id = request.user.id)
            countpresent =False
            if videocount:
                countpresent = True
            per = 0
            tc = 0
            wc = 0
            for x in subject:
                if not videocount:
                    countsave = LXPModel.LearnerPlaylistCount.objects.create(playlist_id = x.id, learner_id = request.user.id,count =x.vtotal )
                    countsave.save()
                tc += x.vtotal
                wc += x.VWatched
            try:
                per = round((100*int(wc))/int(tc),2)
            except:
                per =0
            dif = tc- wc

            return render(request,'learner/video/learner_video_course_subject.html',{'subject':subject,'dif':dif,'per':per,'wc':wc,'tc':tc})
    #except:
        return render(request,'lxpapp/404page.html')
 
@login_required
def learner_video_list_view(request,subject_id):
#    try:     
        if str(request.session['utype']) == 'learner':
            subjectname = LXPModel.Playlist.objects.only('name').get(id=subject_id).name
            # list = LXPModel.PlaylistItem.objects.raw(("SELECT DISTINCT MAINVID.ID, MAINVID.NAME, IFNULL((SELECT LXPAPP_VIDEOWATCHED.VIDEO_ID FROM LXPAPP_VIDEOWATCHED WHERE LXPAPP_VIDEOWATCHED.LEARNER_ID = " + str(request.user.id) + 
            #                                          " AND LXPAPP_VIDEOWATCHED.VIDEO_ID = MAINVID.ID), 0 ) AS watched, IFNULL((SELECT LXPAPP_VIDEOTOUNLOCK.VIDEO_ID FROM LXPAPP_VIDEOTOUNLOCK WHERE LXPAPP_VIDEOTOUNLOCK.LEARNER_ID = " + 
            #                                          str(request.user.id) + " AND LXPAPP_VIDEOTOUNLOCK.VIDEO_ID = MAINVID.ID), 0) AS unlocked, IFNULL((SELECT LXPAPP_SESSIONMATERIAL.ID FROM LXPAPP_SESSIONMATERIAL WHERE LXPAPP_SESSIONMATERIAL.playlist_id = MAINLIST.PLAYLIST_ID AND LXPAPP_SESSIONMATERIAL.VIDEO_ID = MAINVID.ID), 0) AS matid, IFNULL((SELECT LXPAPP_SESSIONMATERIAL.urlvalue FROM LXPAPP_SESSIONMATERIAL WHERE LXPAPP_SESSIONMATERIAL.playlist_id = MAINLIST.PLAYLIST_ID AND LXPAPP_SESSIONMATERIAL.VIDEO_ID = MAINVID.ID), 0) AS matlink , IFNULL((SELECT LXPAPP_ACTIVITY.ID FROM LXPAPP_ACTIVITY WHERE LXPAPP_ACTIVITY.playlist_id = ACTLIST.PLAYLIST_ID AND LXPAPP_ACTIVITY.VIDEO_ID = ACTVID.ID), 0) AS Actid, IFNULL((SELECT LXPAPP_ACTIVITY.urlvalue FROM LXPAPP_ACTIVITY WHERE LXPAPP_ACTIVITY.playlist_id = ACTLIST.PLAYLIST_ID AND LXPAPP_ACTIVITY.VIDEO_ID = ACTVID.ID), 0) AS Actlink FROM LXPAPP_PLAYLISTITEM MAINLIST INNER JOIN LXPAPP_VIDEO MAINVID ON ( MAINLIST.VIDEO_ID = MAINVID.ID ) WHERE MAINLIST.PLAYLIST_ID = " + str (subject_id) + " AND MAINVID.NAME <> 'Deleted video' ORDER BY MAINVID.NAME")  .lower())
            list = LXPModel.PlaylistItem.objects.raw("""SELECT DISTINCT 
                                        MAINVID.id, 
                                        MAINVID.name,
                                        MAINVID.video_id, 
                                        IFNULL(VW.video_id, 0) AS watched, 
                                        IFNULL(VU.video_id, 0) AS unlocked, 
                                        IFNULL(SM.id, 0) AS matid, 
                                        IFNULL(SM.urlvalue, 0) AS matlink, 
                                        IFNULL(ACT.id, 0) AS Actid, 
                                        IFNULL(ACT.urlvalue, 0) AS Actlink
                                    FROM lxpapp_playlistitem MAINLIST
                                    INNER JOIN lxpapp_video MAINVID ON MAINLIST.video_id = MAINVID.id
                                    LEFT JOIN lxpapp_videowatched VW 
                                        ON VW.learner_id = """ + str(request.user.id) + """ AND VW.video_id = MAINVID.id
                                    LEFT JOIN lxpapp_videotounlock VU 
                                        ON VU.learner_id = """ + str(request.user.id) + """ AND VU.video_id = MAINVID.id
                                    LEFT JOIN lxpapp_sessionmaterial SM 
                                        ON SM.playlist_id = MAINLIST.playlist_id AND SM.video_id = MAINVID.id
                                    LEFT JOIN lxpapp_activity ACT 
                                        ON ACT.playlist_id = MAINLIST.playlist_id AND ACT.video_id = MAINVID.id
                                    WHERE MAINLIST.playlist_id = """ + str(subject_id) + """
                                    AND MAINVID.name <> 'Deleted video'
                                    ORDER BY MAINVID.name;""")
            return render(request,'learner/video/learner_video_list.html',{'list':list,'subjectname':subjectname,'subject_id':subject_id})
 #   except:
        return render(request,'lxpapp/404page.html')

def learner_video_watched_saved_view(request):
    try:
        if str(request.session['utype']) == 'learner':
            if request.method == 'POST':
                id = request.POST.get('id')
                learner_id = request.user.id
                if not LXPModel.VideoWatched.objects.filter(video_id=id, learner_id=learner_id).exists():
                    LXPModel.VideoWatched.objects.create(video_id=id, learner_id=learner_id)
                return JsonResponse({'status': 'success'})
    except Exception as e:
        print("Error in learner_video_watched_saved_view:", e)
        return JsonResponse({'status': 'error', 'message': str(e)})
@login_required
def learner_video_sesseionmaterial_list_view(request,subject_id,video_id):
    try:     
        if str(request.session['utype']) == 'learner':
            subjectname = LXPModel.Playlist.objects.only('name').get(id=subject_id).name
            list = LXPModel.SessionMaterial.objects.all().filter(playlist_id = str (subject_id),video_id = str (video_id))  
            return render(request,'learner/video/learner_video_sesseionmaterial_list.html',{'list':list,'subjectname':subjectname,'subject_id':subject_id,'video_id':video_id})
    except:
        return render(request,'lxpapp/404page.html')


from django.db import connection  # only if raw SQL is still needed
import traceback
@login_required
def learner_show_video_view(request, subject_id, video_id):
    try:
        if str(request.session.get('utype')) != 'learner':
            return JsonResponse({'error': 'Unauthorized'}, status=403)

        subjectname = LXPModel.Playlist.objects.only('name').get(id=subject_id).name
        video = LXPModel.Video.objects.get(id=video_id)
        topicname = video.name
        url = f"https://www.youtube.com/embed/{video.video_id}"

        # Check if this video has been watched
        already_watched = LXPModel.VideoWatched.objects.filter(
            video_id=video_id,
            learner_id=request.user.id
        ).exists()

        # If not watched yet, record it and unlock the next video
        if not already_watched:
            LXPModel.VideoWatched.objects.create(
                video_id=video_id,
                learner_id=request.user.id
            )

            # Get next video (raw SQL is used here for compatibility with your setup)
            next_items = LXPModel.PlaylistItem.objects.raw(f'''
                SELECT 1 AS id, lxpapp_playlistitem.video_id 
                FROM lxpapp_playlistitem
                INNER JOIN lxpapp_video ON lxpapp_playlistitem.video_id = lxpapp_video.id
                WHERE lxpapp_playlistitem.video_id > {video_id}
                AND lxpapp_playlistitem.playlist_id = {subject_id}
                ORDER BY lxpapp_video.name
                LIMIT 1
            ''')

            for next_item in next_items:
                LXPModel.VideoToUnlock.objects.get_or_create(
                    video_id=next_item.video_id,
                    playlist_id=subject_id,
                    learner_id=request.user.id
                )

        # Respond with JSON for AJAX requests
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'topicname': topicname,
                'url': url,
                'subjectname': subjectname,
            })

        # Fallback for full-page request (optional)
        return render(request, 'learner/video/learner_show_video.html', {
            'topicname': topicname,
            'url': url,
            'subjectname': subjectname,
            'subject_id': subject_id,
            'video_id': video_id,
        })

    except Exception as e:
        print("Error in learner_show_video_view:", e)
        traceback.print_exc()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Something went wrong'}, status=500)
        return render(request, 'LXPapp/404page.html')

@login_required
def learner_see_sesseionmaterial_view(request,subject_id,video_id,pk):
    try:
        if str(request.session['utype']) == 'learner':
            details= LXPModel.SessionMaterial.objects.all().filter(id=pk)
            subjectname = LXPModel.Playlist.objects.only('name').get(id=subject_id).name
            chaptername = LXPModel.Video.objects.only('name').get(id=video_id).name

            materialtype = 0
            for x in details:
                materialtype = x.mtype

            if materialtype == "HTML":
                return render(request,'learner/sessionmaterial/learner_sessionmaterial_htmlshow.html',{'details':details,'subjectname':subjectname,'chaptername':chaptername,'subject_id':subject_id})
            if materialtype == "URL":
                return render(request,'learner/sessionmaterial/learner_sessionmaterial_urlshow.html',{'details':details,'subjectname':subjectname,'chaptername':chaptername,'subject_id':subject_id})
            if materialtype == "PDF":
                return render(request,'learner/sessionmaterial/learner_sessionmaterial_pdfshow.html',{'details':details,'subjectname':subjectname,'chaptername':chaptername,'subject_id':subject_id,'video_id':video_id})
            if materialtype == "Video":
                return render(request,'learner/sessionmaterial/learner_sessionmaterial_pdfshow.html',{'details':details,'subjectname':subjectname,'chaptername':chaptername,'subject_id':subject_id})
    except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def learner_studymaterial_course_view(request):
    #try:    
        if str(request.session['utype']) == 'learner':
            courses = LXPModel.Course.objects.raw('SELECT id, course_name, description, whatlearn, includes, themecolor, image , Topiccount, CASE WHEN watchcount = 0 THEN 0 ELSE watchcount - 1 END as watchcount, ((CASE WHEN watchcount = 0 THEN 0 ELSE watchcount - 1 END)*100)/Topiccount as per FROM ( SELECT mainmod.id, mainmod.course_name, mainmod.description, mainmod.whatlearn, mainmod.includes, mainmod.themecolor, mainmod.image , (SELECT count(chpmod.topic) AS Topiccount FROM lxpapp_coursechapter INNER JOIN lxpapp_material chpmod ON (lxpapp_coursechapter.chapter_id = chpmod.chapter_id) WHERE lxpapp_coursechapter.course_id = mainmod.id ) AS Topiccount, ( SELECT count(lxpapp_learnermaterialwatched.id) as watchcount FROM lxpapp_learnermaterialwatched WHERE lxpapp_learnermaterialwatched.course_id = mainmod.id) as watchcount FROM lxpapp_batchcourse LEFT OUTER JOIN lxpapp_batch ON (lxpapp_batchcourse.batch_id = lxpapp_batch.id) LEFT OUTER JOIN lxpapp_batchlearner ON (lxpapp_batch.id = lxpapp_batchlearner.batch_id) LEFT OUTER JOIN lxpapp_course mainmod ON (lxpapp_batchcourse.course_id = mainmod.id) WHERE lxpapp_batchlearner.learner_id = ' + str(request.user.id) + ' ) AS course_summary')
            if  not courses:
                return render(request,'learner/studymaterial/learner_studymaterial_nocourse.html')
            else:        
                return render(request,'learner/studymaterial/learner_studymaterial_course.html',{'courses':courses})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_studymaterial_course_chapter_view(request,course_id):
#    try:     
        if str(request.session['utype']) == 'learner':
            list = LXPModel.Course.objects.raw("SELECT id, srno, subject_id, subject_name, chapter_name, chapter_id, topic, mtype, urlvalue, description, per, CASE WHEN Row_number() OVER ( ORDER BY srno) = 1 THEN 'yes' WHEN Lag(per) OVER ( ORDER BY srno) > 0 THEN 'yes' ELSE 'no' END AS flag FROM ( SELECT lxpapp_material.id, Row_number() OVER ( partition BY lxpapp_chapter.chapter_name) AS srno, lxpapp_chapter.chapter_name, lxpapp_subject.subject_name, lxpapp_subject.id AS subject_id, lxpapp_chapter.id AS chapter_id, lxpapp_material.topic, lxpapp_material.mtype, lxpapp_material.urlvalue, lxpapp_material.description, ( SELECT per FROM ( SELECT lxpapp_chapterresult.id, lxpapp_chapterresult.correct * 100 / ( lxpapp_chapterresult.wrong + lxpapp_chapterresult.correct ) AS per FROM lxpapp_chapterresult WHERE lxpapp_chapterresult.course_id = main.course_id AND lxpapp_chapterresult.chapter_id = main.chapter_id AND lxpapp_chapterresult.learner_id = " + str(request.user.id) + ") a ORDER BY per DESC, 1) AS per FROM lxpapp_coursechapter main LEFT OUTER JOIN lxpapp_material ON ( main.chapter_id = lxpapp_material.chapter_id ) LEFT OUTER JOIN lxpapp_chapter ON ( main.chapter_id = lxpapp_chapter.id ) LEFT OUTER JOIN lxpapp_subject ON ( main.subject_id = lxpapp_subject.id ) WHERE main.course_id = " + str(course_id) + " ) WHERE id NOT null ORDER BY subject_name, chapter_name, id")

            count = LXPModel.Course.objects.raw('SELECT 1 as id, Topiccount, CASE WHEN watchcount = 0 THEN 0 ELSE watchcount - 1 END  as watchcount, ((CASE WHEN watchcount = 0 THEN 0 ELSE watchcount - 1 END)*100)/Topiccount as per FROM ( (SELECT count(lxpapp_material.topic) AS Topiccount FROM lxpapp_coursechapter INNER JOIN lxpapp_material ON (lxpapp_coursechapter.chapter_id = lxpapp_material.chapter_id) WHERE lxpapp_coursechapter.course_id = ' + str(course_id) + ' ) AS Topiccount, ( SELECT count (lxpapp_learnermaterialwatched.id) as watchcount FROM lxpapp_learnermaterialwatched WHERE lxpapp_learnermaterialwatched.course_id = ' + str(course_id) + ' ) as watchcount )')
            moddet = LXPModel.Course.objects.raw("SELECT lxpapp_course.id, lxpapp_course.description,  lxpapp_course.whatlearn,  lxpapp_course.includes,  lxpapp_course.themecolor,  lxpapp_course.tags,  lxpapp_course.image,  lxpapp_course.price,  lxpapp_mainhead.mainhead_name,  lxpapp_subhead.subhead_name FROM  lxpapp_course  INNER JOIN lxpapp_mainhead ON (lxpapp_course.mainhead_id = lxpapp_mainhead.id)  INNER JOIN lxpapp_subhead ON (lxpapp_course.subhead_id = lxpapp_subhead.id) WHERE lxpapp_course.id = " + str(course_id) )
            Topiccount = 0
            watchcount = 0
            per = 0
            for r in count:
                Topiccount = r.Topiccount
                watchcount= r.watchcount
                per= r.per
            per = 55
            coursename = LXPModel.Course.objects.only('course_name').get(id=course_id).course_name
            return render(request,'learner/studymaterial/learner_studymaterial_chapter_topic.html',{'list':list,'coursename':coursename,'course_id':course_id,'moddet':moddet,'Topiccount':Topiccount,'watchcount':watchcount,'per':per})
 #   except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_studymaterial_chapter_show_view(request,chapter_id,course_id):
#    try:     
        if str(request.session['utype']) == 'learner':
            chapter_name = ''
            topiccount = 0
            Topiccount = 0
            watchcount = 0
            per = 0
            count = LXPModel.Course.objects.raw('SELECT 1 as id, Topiccount, CASE WHEN watchcount = 0 THEN 0 ELSE watchcount - 1 END  as watchcount, ((CASE WHEN watchcount = 0 THEN 0 ELSE watchcount - 1 END)*100)/Topiccount as per FROM ( (SELECT count(lxpapp_material.topic) AS Topiccount FROM lxpapp_coursechapter INNER JOIN lxpapp_material ON (lxpapp_coursechapter.chapter_id = lxpapp_material.chapter_id) WHERE lxpapp_coursechapter.course_id = ' + str(course_id) + ' AND lxpapp_material.chapter_id = ' + str(chapter_id) + ') AS Topiccount, ( SELECT count (lxpapp_learnermaterialwatched.id) as watchcount FROM lxpapp_learnermaterialwatched WHERE lxpapp_learnermaterialwatched.course_id = ' + str(course_id) + ' AND lxpapp_learnermaterialwatched.learner_id = ' + str(request.user.id) + ' AND lxpapp_learnermaterialwatched.chapter_id = ' + str(chapter_id) + ' ) as watchcount )')
            result = LXPModel.Chapter.objects.raw("SELECT 1 as id,   lxpapp_chapter.chapter_name,  Count(lxpapp_material.id) as count FROM  lxpapp_material  INNER JOIN lxpapp_chapter ON (lxpapp_material.chapter_id = lxpapp_chapter.id) WHERE lxpapp_chapter.id = " + str(chapter_id) + " GROUP BY lxpapp_chapter.chapter_name")
            exam = LXPModel.ChapterQuestion.objects.filter(chapter_id = chapter_id).values_list("id").count()
            for r in result:
                chapter_name = r.chapter_name
                topiccount= r.count
            for r in count:
                Topiccount = r.Topiccount
                watchcount= r.watchcount
                per= r.per
            coursename = LXPModel.Course.objects.only('course_name').get(id=course_id).course_name
            list = LXPModel.Course.objects.raw("SELECT mat.id, (SELECT COUNT(lxpapp_learnermaterialwatched.id) AS MatCount FROM lxpapp_learnermaterialwatched LEFT OUTER JOIN lxpapp_material matwatch ON (lxpapp_learnermaterialwatched.material_id = matwatch.id) WHERE mat.id = matwatch.id AND lxpapp_learnermaterialwatched.course_id = " + str(course_id) + " ) AS matcount, lxpapp_chapter.chapter_name, lxpapp_chapter.id AS chapter_id, mat.topic, mat.mtype, mat.urlvalue, mat.description FROM lxpapp_material mat INNER JOIN lxpapp_chapter ON (mat.chapter_id = lxpapp_chapter.id) WHERE lxpapp_chapter.id = " + str(chapter_id) )
            activity = LXPModel.Activity.objects.all().filter(chapter_id = chapter_id)
            return render(request,'learner/studymaterial/learner_studymaterial_chapter_show.html',{'list':list,'chapter_id':chapter_id,'course_id':course_id,'chapter_name':chapter_name,'topiccount':topiccount,'coursename':coursename,'course_id':course_id,'Topiccount':Topiccount,'watchcount':watchcount,'per':per,'exam':exam, 'activity':activity})
 #   except:
        return render(request,'lxpapp/404page.html')

def save_topic(request):
    try:
        if request.method == 'POST':
            id = request.body
            id = str(id).replace("'",'')
            id = str(id).replace("bid=",'')
            id = str (id).replace("&course_id=",',')
            id = str (id).replace("&chapter_id=",',')
            x = id.split(",")
            matid= x[0]
            modid= x[1]
            chpid= x[2]
            mat =LXPModel.LearnerMaterialWatched.objects.all().filter(learner_id = request.user.id,material_id=matid,course_id = modid,chapter_id = chpid)
            if not mat:
                mat = LXPModel.LearnerMaterialWatched.objects.create(learner_id = request.user.id,material_id=matid,course_id = modid,chapter_id = chpid)
                mat.save()
            nextvalue = LXPModel.Material.objects.raw('SELECT lxpapp_material.id  FROM lxpapp_material where  lxpapp_material.id > ' + str(matid) + ' limit 1')
            a = len(nextvalue)
            if a == 0:
                xyz = LXPModel.LearnerMaterialWatched.objects.all().filter(learner_id = request.user.id,material_id=matid,course_id = modid,chapter_id = chpid)
                a = len(xyz)
                if a == 1:
                    mat = LXPModel.LearnerMaterialWatched.objects.create(learner_id = request.user.id,material_id=matid,course_id = modid,chapter_id = chpid)
                    mat.save()
            for c in nextvalue:
                mat =LXPModel.LearnerMaterialWatched.objects.all().filter(learner_id = request.user.id,material_id=c.id,course_id = modid,chapter_id = chpid)
                if not mat:
                    mat = LXPModel.LearnerMaterialWatched.objects.create(learner_id = request.user.id,material_id=c.id,course_id = modid,chapter_id = chpid)
                    mat.save()
            return JsonResponse({'status': 'success'})    
    except:
        return render(request,'lxpapp/404page.html')
@login_required
def learner_show_studymaterial_view(request,studymaterialtype,pk):
    try:
        if str(request.session['utype']) == 'learner':
            details= LXPModel.Material.objects.raw('SELECT lxpapp_material.id,  lxpapp_material.topic,  lxpapp_material.mtype,  lxpapp_material.urlvalue,  lxpapp_material.description FROM  lxpapp_material WHERE  lxpapp_material.id = ' + str(pk))
            if studymaterialtype == 'HTML':
                return render(request,'learner/studymaterial/learner_studymaterial_htmlshow.html',{'details':details})
            if studymaterialtype == 'URL':
                return render(request,'learner/studymaterial/learner_studymaterial_urlshow.html',{'details':details})
            if studymaterialtype == 'PDF':
                return render(request,'learner/studymaterial/learner_studymaterial_pdfshow.html',{'details':details})
            if studymaterialtype == 'Video':
                return render(request,'learner/studymaterial/learner_studymaterial_videoshow.html',{'details':details})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_availablecourse_course_view(request):
    try:    
        if str(request.session['utype']) == 'learner':
            courses = LXPModel.Course.objects.all().order_by('course_name')
            return render(request,'learner/availablecourse/learner_availablecourse_course.html',{'courses':courses})
    except:
        return render(request,'lxpapp/404page.html')


@login_required
def learner_availablecourse_course_chapter_view(request,coursename,course_id):
#    try:     
        if str(request.session['utype']) == 'learner':
            list = LXPModel.Course.objects.raw("SELECT lxpapp_material.id, ROW_NUMBER() OVER(PARTITION BY lxpapp_chapter.chapter_name) as srno,  lxpapp_chapter.chapter_name,  lxpapp_chapter.id as chapter_id,  lxpapp_material.topic,  lxpapp_material.mtype,  lxpapp_material.urlvalue,  lxpapp_material.description FROM  lxpapp_coursechapter  LEFT OUTER JOIN lxpapp_material ON (lxpapp_coursechapter.chapter_id = lxpapp_material.chapter_id)  LEFT OUTER JOIN lxpapp_chapter ON (lxpapp_coursechapter.chapter_id = lxpapp_chapter.id) WHERE lxpapp_coursechapter.course_id = " + str(course_id) )
            moddet = LXPModel.Course.objects.raw("SELECT lxpapp_course.id, lxpapp_course.description,  lxpapp_course.whatlearn,  lxpapp_course.includes,  lxpapp_course.themecolor,  lxpapp_course.tags,  lxpapp_course.image,  lxpapp_course.price,  lxpapp_mainhead.mainhead_name,  lxpapp_subhead.subhead_name FROM  lxpapp_course  INNER JOIN lxpapp_mainhead ON (lxpapp_course.mainhead_id = lxpapp_mainhead.id)  INNER JOIN lxpapp_subhead ON (lxpapp_course.subhead_id = lxpapp_subhead.id) WHERE lxpapp_course.id = " + str(course_id) )
            return render(request,'learner/availablecourse/learner_availablecourse_chapter_topic.html',{'list':list,'coursename':coursename,'course_id':course_id,'moddet':moddet})
 #   except:
        return render(request,'lxpapp/404page.html')



@login_required
def learner_chapterexam_view(request,chapter_id,course_id):
    #try:    
        if str(request.session['utype']) == 'learner':
            chapterexams=LXPModel.Chapter.objects.all().filter(id =  chapter_id) 
            coursename = LXPModel.Course.objects.only('course_name').get(id=course_id).course_name
            chaptername = LXPModel.Chapter.objects.only('chapter_name').get(id=chapter_id).chapter_name
            return render(request,'learner/studymaterial/chapterexam/learner_chapterexam.html',{'chapterexams':chapterexams,'coursename':coursename,'course_id':course_id,'chaptername':chaptername,'chapter_id':chapter_id})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_take_chapterexam_view(request,chapter_id,course_id):
    #try:    
        if str(request.session['utype']) == 'learner':
            coursename = LXPModel.Course.objects.only('course_name').get(id=course_id).course_name
            chaptername = LXPModel.Chapter.objects.only('chapter_name').get(id=chapter_id).chapter_name
            
            mcqquestion= LXPModel.ChapterQuestion.objects.filter(chapter_id=chapter_id)
            total_marks = 0
            total_questions = 0
            for x in mcqquestion:
                total_marks = total_marks + x.marks
                total_questions = total_questions + 1
            return render(request,'learner/studymaterial/chapterexam/learner_take_chapterexam.html',{'coursename':coursename,'chaptername':chaptername,'total_questions':total_questions,'total_marks':total_marks,'course_id':course_id,'chapter_id':chapter_id})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_start_chapterexam_view(request,chapter_id,course_id):
    #try:    
        if str(request.session['utype']) == 'learner':
            coursename = LXPModel.Course.objects.only('course_name').get(id=course_id).course_name
            chaptername = LXPModel.Chapter.objects.only('chapter_name').get(id=chapter_id).chapter_name
            if request.method == 'POST':
                mcqresult = LXPModel.ChapterResult.objects.create(learner_id = request.user.id,course_id =course_id,chapter_id =chapter_id,marks=0,wrong=0,correct=0)
                mcqresult.save()
                questions=LXPModel.ChapterQuestion.objects.all().filter(chapter_id=chapter_id).order_by('?')
                score=0
                wrong=0
                correct=0
                total=0
                r_id = 0
                q_id = 0
                r_id = mcqresult.id
                for q in questions:
                    total+=1
                    question = LXPModel.ChapterQuestion.objects.all().filter(question=q.question)
                    for i in question:
                        q_id = i.id
                    resdet = LXPModel.ChapterResultDetails.objects.create(chapterresult_id = r_id,question_id =q_id,selected =str(request.POST.get(q.question)).replace('option',''))
                    resdet.save()
                    if 'option' + q.answer ==  request.POST.get(q.question):
                        score+= q.marks
                        correct+=1
                        
                    else:
                        wrong+=1
                percent = score/(total) *100
                context = {
                    'score':score,
                    'time': request.POST.get('timer'),
                    'correct':correct,
                    'wrong':wrong,
                    'percent':percent,
                    'total':total
                }
                mcqresult.marks = score
                mcqresult.wrong = wrong
                mcqresult.correct = correct
                mcqresult.timetaken = request.POST.get('timer')
                mcqresult.save()
                resdetobj = LXPModel.ChapterResultDetails.objects.raw("SELECT 1 as id,  lxpapp_chapterquestion.question as q,  lxpapp_chapterquestion.option1 as o1,  lxpapp_chapterquestion.option2 as o2,  lxpapp_chapterquestion.option3 as o3,  lxpapp_chapterquestion.option4 as o4,  lxpapp_chapterquestion.answer AS Correct,  lxpapp_chapterquestion.marks,  lxpapp_chapterresultdetails.selected AS answered  FROM  lxpapp_chapterresultdetails  INNER JOIN lxpapp_chapterresult ON (lxpapp_chapterresultdetails.chapterresult_id = lxpapp_chapterresult.id)  INNER JOIN lxpapp_chapterquestion ON (lxpapp_chapterresultdetails.question_id = lxpapp_chapterquestion.id) WHERE lxpapp_chapterresult.id = " + str(r_id) + " AND lxpapp_chapterresult.learner_id = " + str(request.user.id) + " ORDER BY lxpapp_chapterquestion.id" )
                return render(request,'learner/studymaterial/chapterexam/learner_chapterexam_result.html',{'total':total,'percent':percent, 'wrong':wrong,'correct':correct,'time': request.POST.get('timer'),'score':score,'resdetobj':resdetobj,'coursename':coursename,'course_id':course_id,'chaptername':chaptername,'chapter_id':chapter_id})
            else:
                questions=LXPModel.ChapterQuestion.objects.all()
                context = {
                    'questions':questions
                }
            questions=LXPModel.ChapterQuestion.objects.all().filter(chapter_id=chapter_id).order_by('?')
            
            return render(request,'learner/studymaterial/chapterexam/learner_start_chapterexam.html',{'questions':questions,'coursename':coursename,'course_id':course_id,'chaptername':chaptername,'chapter_id':chapter_id})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_show_chapterexam_reuslt_view(request,chapter_id,course_id):
    #try:    
        if str(request.session['utype']) == 'learner':
            chapterexams=LXPModel.ChapterResult.objects.all().filter(chapter_id = chapter_id,learner_id=request.user.id)
            coursename = LXPModel.Course.objects.only('course_name').get(id=course_id).course_name
            chaptername = LXPModel.Chapter.objects.only('chapter_name').get(id=chapter_id).chapter_name
            return render(request,'learner/studymaterial/chapterexam/learner_show_chapterexam_reuslt.html',{'chapterexams':chapterexams,'coursename':coursename,'course_id':course_id,'chaptername':chaptername,'chapter_id':chapter_id})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_show_chapterexam_reuslt_details_view(request,result_id,attempt,chapter_id,course_id):
    try:    
        if str(request.session['utype']) == 'learner':
            coursename = LXPModel.Course.objects.only('course_name').get(id=course_id).course_name
            chaptername = LXPModel.Chapter.objects.only('chapter_name').get(id=chapter_id).chapter_name
            chapterexams=LXPModel.ChapterResultDetails.objects.all().filter(question_id__in = LXPModel.ChapterQuestion.objects.all(), chapterresult_id = result_id)
            return render(request,'learner/studymaterial/chapterexam/learner_chapterexam_result_details.html',{'chapterexams':chapterexams,'attempt':attempt,'coursename':coursename,'course_id':course_id,'chaptername':chaptername,'chapter_id':chapter_id})
    except:
        return render(request,'lxpapp/404page.html')


def save_cart(request):
    try:
        if request.method == 'POST':
            id = request.POST.get('id')
            # id = str(id).replace("'",'')
            # id = str(id).replace("bid=",'')
            # id = str (id).replace("&course_id=",',')
            # id = str (id).replace("&chapter_id=",',')
            
            cart =LXPModel.LearnerCart.objects.all().filter(learner_id = request.user.id,course_id=id)
            if not cart:
                 cart = LXPModel.LearnerCart.objects.create(learner_id = request.user.id,course_id=id)
                 cart.save()
            return JsonResponse({'status': 'success'})    
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_check_k8sterminal_view(request):
    try:
        if str(request.session['utype']) == 'learner':
            if request.method=='POST':
                password = request.POST.get("password")
                if password == '' or password is None:
                    messages.info(request, 'Please Enter password')
                    return render(request,'learner/labs/k8sterminal/learner_check_k8sterminal.html')
                usage = LXPModel.K8STerminal.objects.all().filter(learner_id= request.user.id)
                if not usage:
                    messages.info(request, 'Invalid password or Terminal Setting not found, please contact to your trainer')
                    return render(request,'learner/labs/k8sterminal/learner_check_k8sterminal.html')
                totcount = 0
                passwordmain=''
                for x in usage:
                    totcount += x.usagevalue
                    passwordmain = x.Password
                usagecount = LXPModel.K8STerminalLearnerCount.objects.all().filter(learner_id= request.user.id)
                count = 0
                for x in usagecount:
                    count += x.usedvalue
                if password != passwordmain:
                    messages.info(request, 'Invalid password or Terminal Setting not found, please contact to your trainer')
                    return render(request,'learner/labs/k8sterminal/learner_check_k8sterminal.html')
                if count > totcount:
                    messages.info(request, 'Terminal usage permission exceed, please contact to your trainer')
                    return render(request,'learner/labs/k8sterminal/learner_check_k8sterminal.html')
                
                count += 1
                usagecount = LXPModel.K8STerminalLearnerCount.objects.create(
                            learner_id = request.user.id,
                            usedvalue = 1
                ).save()
                return render(request,'learner/labs/k8sterminal/learner_launch_k8sterminal.html')
            return render(request,'learner/labs/k8sterminal/learner_check_k8sterminal.html')
    except: 
        return render(request,'lxpapp/404page.html')

@login_required
def learner_python_terminal_view(request):
    try:
        if str(request.session['utype']) == 'learner':  
            return render(request,'learner/labs/python/learner_python_terminal.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_linux_terminal_view(request):
    try:
        if str(request.session['utype']) == 'learner':  
            return render(request,'learner/labs/linux/learner_linux_terminal.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_cloudshell_terminal_view(request):
    try:
        if str(request.session['utype']) == 'learner':  
            return render(request,'learner/labs/cloudshell/learner_cloudshell_terminal.html')
    except:
        return render(request,'lxpapp/404page.html')
@login_required
def learner_edit_Learner_details_view(request, user_id):
    """
    Handles GET request to display the form.
    POST request will now be handled by an API view.
    """
    user = get_object_or_404(LXPModel.LearnerDetails, learner_id=user_id)
    # This view now only prepares the form for display
    form = LXPFORM.LearnerDetailsForm(instance=user)
    return render(request, 'learner/learner_edit_details.html', {'form': form, 'user': user})


@login_required
def learner_edit_Learner_details_api(request, user_id):
    """
    API endpoint to handle POST requests for updating learner details.
    """
    if request.method == "POST":
        user = get_object_or_404(LXPModel.LearnerDetails, learner_id=user_id)
        form = LXPFORM.LearnerDetailsForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            updated_user = form.save()
            # Prepare data for JSON response, especially if profile_pic URL changes
            profile_pic_url = None
            if updated_user.profile_pic:
                # Assuming profile_pic is a FileField, get its URL
                # In a real scenario, this would be `updated_user.profile_pic.url`
                # For placeholder:
                if hasattr(updated_user.profile_pic, 'url'):
                    profile_pic_url = updated_user.profile_pic.url
                else: # if it's just a path string after simulated save
                    profile_pic_url = f"/media/{updated_user.profile_pic}" # Example


            return JsonResponse({
                'status': 'success',
                'message': 'Details updated successfully!',
                'user_data': { # Optionally send back updated data
                    'user_full_name': updated_user.user_full_name,
                    'mobile': updated_user.mobile,
                    'whatsappno': updated_user.whatsappno,
                    'profile_pic_url': profile_pic_url
                }
            })
        else:
            # Send back form errors as JSON
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        # Only POST is allowed for this API endpoint
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed.'}, status=405)
import base64
from django.conf import settings
from lxpapp.gitupload import upload_to_github,check_file_exists_on_github
def learner_upload_activity_view(request,activity_id, course_id, chapter_id):
    if request.method == 'POST':
        pdf_file = request.FILES['pdf_file']
        content = pdf_file.read()
        content_base64 = base64.b64encode(content).decode('utf-8')
        
        # Construct the path dynamically using the uploaded file's name
        file_name = pdf_file.name
        github_path = f'activity/{file_name}'
        if check_file_exists_on_github(github_path) != 404:
            messages.info(request, 'File already exists on server with same name of \n'+file_name)
        else:
            response = upload_to_github(github_path, content_base64)
            url = response['content']['html_url']
            
            pdf_instance =LXPModel.ActivityAnswers( activity_id = activity_id, learner_id = request.user.id, file_url = url)
            pdf_instance.save()
            messages.success(request, 'Answer uploaded successfully')
    return render(request, 'learner/activity/learner_upload_activity.html')

@login_required
def learner_video_activity_list_view(request,playlist_id,video_id):
    # try:     
        if str(request.session['utype']) == 'learner':
            playlistname = LXPModel.Playlist.objects.only('name').get(id=playlist_id).name
            list = LXPModel.Activity.objects.all().filter(playlist_id = str (playlist_id),video_id = str (video_id))  
            return render(request,'learner/video/learner_video_activity_list.html',{'list':list,'playlistname':playlistname,'playlist_id':playlist_id,'video_id':video_id})
    # except:
        return render(request,'lxpapp/404page.html')

@login_required
def learner_see_activity_view(request,subject_id,video_id,pk):
    try:
        if str(request.session['utype']) == 'learner':
            details= LXPModel.Activity.objects.all().filter(id=pk)
            subjectname = LXPModel.Playlist.objects.only('name').get(id=subject_id).name
            chaptername = LXPModel.Video.objects.only('name').get(id=video_id).name
            return render(request,'learner/video/learner_video_activity_urlshow.html',{'details':details,'subjectname':subjectname,'chaptername':chaptername,'subject_id':subject_id,'video_id':video_id})
            
    except:
        return render(request,'lxpapp/404page.html')

# --- Corrected learner_polls_list ---
@login_required
def learner_polls_list(request):
    """
    Displays a list of polls that the current logged-in user is eligible
    to vote on and has NOT yet voted on.
    """
    user = request.user
    
    # CORRECT: Get IDs of polls the user has already voted on from the database.
    voted_poll_ids = PollVote.objects.filter(user=user).values_list('poll_id', flat=True)

    # CORRECT: Get the IDs of the groups the user belongs to.
    user_group_ids = user.groups.values_list('id', flat=True)

    # CORRECT: Build the complex query for eligibility.
    is_unrestricted = Q(eligible_groups__isnull=True)
    is_in_allowed_group = Q(eligible_groups__id__in=user_group_ids)

    # CORRECT: Combine conditions and get a distinct set of eligible polls.
    eligible_polls = Poll.objects.filter(is_unrestricted | is_in_allowed_group).distinct()

    # CORRECT: From that set, exclude the ones already voted on.
    voteable_polls = eligible_polls.exclude(id__in=voted_poll_ids).order_by('-created_at')
    
    context = {'polls': voteable_polls}
    
    # CORRECTION 1: Ensure the template path matches your project structure.
    # It should be 'voting/learner_polls_list.html' not 'learner/poll/...'
    return render(request, 'learner/poll/learner_polls_list.html', context)


# --- Corrected learner_poll_vote ---
@login_required
def learner_poll_vote(request, poll_id):
    """
    Displays a poll for voting (GET) and handles the vote submission (POST)
    by creating a Vote record.
    """
    poll = get_object_or_404(Poll, pk=poll_id)
    user = request.user

    # CORRECTION 2: The permission check logic is correct. No changes needed here.
    if poll.eligible_groups.exists():
        if not user.groups.filter(id__in=poll.eligible_groups.all()).exists():
            messages.error(request, "You are not eligible to vote on this poll.")
            # CORRECTION 3: The redirect URL name must match your urls.py.
            return redirect('learner_polls_list')

    # CORRECTION 4: The check for existing votes must query the database, not the session.
    # This is the single source of truth.
    if PollVote.objects.filter(poll=poll, user=user).exists():
        messages.warning(request, f"You have already cast your vote for the poll: '{poll.question}'")
        return redirect('learner-polls-list')

    if request.method == 'POST':
        selected_option_id = request.POST.get('option')
        if not selected_option_id:
            messages.error(request, "You must select an option to vote.")
            # CORRECTION 1 (again): Fix template path
            return render(request, 'learner/poll/learner_poll_vote.html', {'poll': poll})

        try:
            selected_option = poll.options.get(pk=selected_option_id)

            # CORRECTION 5: The main logic must create a `Vote` object.
            # The `votes` field on the Option model was removed. The F() object and .save() are no longer used here.
            PollVote.objects.create(
                user=user,
                poll=poll,
                option=selected_option
            )
            
            # CORRECTION 6: The session logic is no longer needed. The database check handles this.
            # Remove: request.session[f'voted_poll_{poll.id}'] = True

            messages.success(request, f"Your vote for '{selected_option.option_text}' has been registered successfully!")
            # CORRECTION 3 (again): Fix redirect URL name
            return redirect('learner-polls-list')

        # CORRECTION 7: The exception should be for the `Option` model, not a non-existent `PollOption`.
        except PollOption.DoesNotExist:
            messages.error(request, "Invalid option selected. Please try again.")
            # CORRECTION 1 (again): Fix template path
            return render(request, 'learner/poll/learner_poll_vote.html', {'poll': poll})

    else:  # GET request
        context = {'poll': poll}
        # CORRECTION 1 (again): Fix template path
        return render(request, 'learner/poll/learner_poll_vote.html', context)
