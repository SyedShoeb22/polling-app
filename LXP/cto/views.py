import os
import google_auth_oauthlib.flow
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from lxpapp import models as LXPModel
from lxpapp import forms as LXPFORM
from youtubemanager import PlaylistManager
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.urls import reverse
from django.conf import settings
from github import Github

@login_required    
def cto_dashboard_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            dict={
            'total_course':0,
            'total_exam':0,
            'total_shortCourse':0,
            'total_question':0,
            'total_learner':0,
            'final':'final'
            }
        return render(request,'cto/cto_dashboard.html',context=dict)
    except:
        return render(request,'lxpapp/404page.html')



@login_required
def cto_add_mainhead_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            form = LXPFORM.MainHeadForm(request.POST or None)
            context = {
                'form': form,
                'page_title': 'Add Main Head'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('mainhead_name')
                    mainhead = LXPModel.MainHead.objects.all().filter(mainhead_name__iexact = name)
                    if mainhead:
                        messages.info(request, 'Main Head Name Already Exist')
                        return redirect(reverse('cto-add-mainhead'))
                    try:
                        mainhead = LXPModel.MainHead.objects.create(
                                                    mainhead_name = name)
                        mainhead.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('cto-view-mainhead'))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/mainhead/add_edit_mainhead.html', context)
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_mainhead_view(request, pk):
    try:
        if str(request.session['utype']) == 'cto':
            instance = get_object_or_404(LXPModel.MainHead, id=pk)
            form = LXPFORM.MainHeadForm(request.POST or None, instance=instance)
            context = {
                'form': form,
                'mainhead_id': pk,
                'page_title': 'Edit Main Head'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('mainhead_name')
                    mainhead = LXPModel.MainHead.objects.all().filter(mainhead_name__iexact = name).exclude(id=pk)
                    if mainhead:
                        messages.info(request, 'Main Head Name Already Exist')
                        return redirect(reverse('cto-update-mainhead', args=[pk]))
                    try:
                        mainhead = LXPModel.MainHead.objects.get(id=pk)
                        mainhead.mainhead_name = name
                        mainhead.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('cto-view-mainhead', args=[pk]))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/mainhead/add_edit_mainhead.html', context)
    except:
        return render(request,'lxpapp/404page.html')


@login_required
def cto_view_mainhead_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            mainheads = LXPModel.MainHead.objects.all()
            return render(request,'cto/mainhead/cto_view_mainhead.html',{'mainheads':mainheads})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_mainhead_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            mainhead=LXPModel.MainHead.objects.get(id=pk)
            mainhead.delete()
            return HttpResponseRedirect('/cto/cto-view-mainhead')
        mainheads = LXPModel.MainHead.objects.all()
        return render(request,'cto/mainhead/cto_view_mainhead.html',{'mainheads':mainheads})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_add_subhead_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            form = LXPFORM.SubHeadForm(request.POST or None)
            context = {
                'form': form,
                'page_title': 'Add Sub Head'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('subhead_name')
                    mainid = form.cleaned_data.get('mainhead').pk
                    subhead = LXPModel.SubHead.objects.all().filter(subhead_name__iexact = name)
                    if subhead:
                        messages.info(request, 'Sub Head Name Already Exist')
                        return redirect(reverse('cto-add-subhead'))
                    try:
                        subhead = LXPModel.SubHead.objects.create(mainhead_id =mainid,
                                                    subhead_name = name)
                        subhead.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('cto-view-subhead'))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/subhead/add_edit_subhead.html', context)
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_subhead_view(request, pk):
    try:
        if str(request.session['utype']) == 'cto':
            instance = get_object_or_404(LXPModel.SubHead, id=pk)
            form = LXPFORM.SubHeadForm(request.POST or None, instance=instance)
            context = {
                'form': form,
                'subhead_id': pk,
                'page_title': 'Edit Sub Head'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('subhead_name')
                    mainid = form.cleaned_data.get('mainhead').pk
                    subhead = LXPModel.SubHead.objects.all().filter(subhead_name__iexact = name).exclude(id=pk)
                    if subhead:
                        messages.info(request, 'Sub Head Name Already Exist')
                        return redirect(reverse('cto-update-subhead', args=[pk]))
                    try:
                        subhead = LXPModel.SubHead.objects.get(id=pk)
                        subhead.mainhead_id = mainid
                        subhead.subhead_name = name
                        subhead.save()
                        messages.success(request, "Successfully Updated")
                        subheads = LXPModel.SubHead.objects.all()
                        return render(request,'cto/subhead/cto_view_subhead.html',{'subheads':subheads})
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/subhead/add_edit_subhead.html', context)
    except:
        return render(request,'lxpapp/404page.html')


@login_required
def cto_view_subhead_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            subheads = LXPModel.SubHead.objects.all()
            return render(request,'cto/subhead/cto_view_subhead.html',{'subheads':subheads})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_subhead_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            subhead=LXPModel.SubHead.objects.get(id=pk)
            subhead.delete()
            subheads = LXPModel.SubHead.objects.all()
            return render(request,'cto/subhead/cto_view_subhead.html',{'subheads':subheads})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_add_subject_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            form = LXPFORM.SubjectForm(request.POST or None)
            context = {
                'form': form,
                'page_title': 'Add Subject'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('subject_name')
                    subject = LXPModel.Subject.objects.all().filter(subject_name__iexact = name)
                    if subject:
                        messages.info(request, 'Subject Name Already Exist')
                        return redirect(reverse('cto-add-subject'))
                    try:
                        subject = LXPModel.Subject.objects.create(
                                                    subject_name = name)
                        subject.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('cto-view-subject'))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/subject/add_edit_subject.html', context)
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_subject_view(request, pk):
    try:
        if str(request.session['utype']) == 'cto':
            instance = get_object_or_404(LXPModel.Subject, id=pk)
            form = LXPFORM.SubjectForm(request.POST or None, instance=instance)
            context = {
                'form': form,
                'subject_id': pk,
                'page_title': 'Edit Subject'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('subject_name')
                    subject = LXPModel.Subject.objects.all().filter(subject_name__iexact = name).exclude(id=pk)
                    if subject:
                        messages.info(request, 'Subject Name Already Exist')
                        return redirect(reverse('cto-update-subject', args=[pk]))
                    try:
                        subject = LXPModel.Subject.objects.get(id=pk)
                        subject.subject_name = name
                        subject.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('cto-view-subject', args=[pk]))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/subject/add_edit_subject.html', context)
    except:
        return render(request,'lxpapp/404page.html')


@login_required
def cto_view_subject_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            subjects = LXPModel.Subject.objects.all()
            return render(request,'cto/subject/cto_view_subject.html',{'subjects':subjects})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_subject_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            subject=LXPModel.Subject.objects.get(id=pk)
            subject.delete()
            return HttpResponseRedirect('/cto/cto-view-subject')
        subjects = LXPModel.Subject.objects.all()
        return render(request,'cto/subject/cto_view_subject.html',{'subjects':subjects})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_upload_subject_details_csv_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                    file=request.FILES["select_file"]
                    csv_file = request.FILES["select_file"]
                    file_data = csv_file.read().decode("utf-8")		
                    lines = file_data.split("\n")
                    oldsub =''
                    oldchap=''
                    subid =0
                    chapid=0
                    oldtp=''
                    tpid =0
                    no = 0
                    for line in lines:						
                        no = no + 1
                        if no > 1:
                            fields = line.split(",")
                            if fields[0] != oldsub:
                                oldsub = fields[0]
                                sub = LXPModel.Subject.objects.all().filter(subject_name__exact = oldsub )
                                if not sub:
                                    sub = LXPModel.Subject.objects.create(subject_name = oldsub )
                                    sub.save()
                                    subid=sub.id
                                else:
                                    for x in sub:
                                        subid=x.id  
                            if fields[1] != oldchap:
                                oldchap = fields[1] 
                                chap = LXPModel.Chapter.objects.all().filter(chapter_name__exact = oldchap,subject_id=subid)
                                if not chap:
                                    chap = LXPModel.Chapter.objects.create(chapter_name = oldchap,subject_id=subid)
                                    chap.save()
                                    chapid=chap.id 
                                else:
                                    for x in chap:
                                        chapid=x.id 
                            if fields[2] != oldtp:
                                oldtp = fields[2] 
                                tp = LXPModel.Topic.objects.all().filter(topic_name__exact = oldtp,chapter_id=chapid)
                                if not tp:
                                    tp = LXPModel.Topic.objects.create(topic_name = oldtp,chapter_id=chapid)
                                    tp.save()
            return render(request,'cto/subject/cto_upload_subject_details_csv.html')
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_add_chapter_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            form = LXPFORM.ChapterForm(request.POST or None)
            context = {
                'form': form,
                'page_title': 'Add Chapter'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('chapter_name')
                    subject = form.cleaned_data.get('subject').pk
                    chapter = LXPModel.Chapter.objects.all().filter(chapter_name__iexact = name)
                    if chapter:
                        messages.info(request, 'Chapter Name Already Exist')
                        return redirect(reverse('cto-add-chapter'))
                    try:
                        chapter = LXPModel.Chapter.objects.create(
                                                    chapter_name = name,
                                                    subject_id = subject)
                        chapter.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('cto-view-chapter'))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/chapter/add_edit_chapter.html', context)
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_chapter_view(request, pk):
    try:
        if str(request.session['utype']) == 'cto':
            instance = get_object_or_404(LXPModel.Chapter, id=pk)
            form = LXPFORM.ChapterForm(request.POST or None, instance=instance)
            context = {
                'form': form,
                'chapter_id': pk,
                'page_title': 'Edit Chapter'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('chapter_name')
                    subject = form.cleaned_data.get('subject').pk
                    chapter = LXPModel.Chapter.objects.all().filter(chapter_name__iexact = name).exclude(id=pk)
                    if chapter:
                        messages.info(request, 'Chapter Name Already Exist')
                        return redirect(reverse('cto-update-chapter', args=[pk]))
                    try:
                        chapter = LXPModel.Chapter.objects.get(id=pk)
                        chapter.chapter_name = name
                        chapter.subject_id = subject
                        chapter.save()
                        messages.success(request, "Successfully Updated")
                        chapters = LXPModel.Chapter.objects.all()
                        return render(request,'cto/chapter/cto_view_chapter.html',{'chapters':chapters})
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/chapter/add_edit_chapter.html', context)
    except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def cto_view_chapter_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            c_list = LXPModel.Chapter.objects.all()
            return render(request,'cto/chapter/cto_view_chapter.html',{'chapters':c_list})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_chapter_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            chapter=LXPModel.Chapter.objects.get(id=pk)
            chapter.delete()
            chapters = LXPModel.Chapter.objects.all()
            return render(request,'cto/chapter/cto_view_chapter.html',{'chapters':chapters})
    except:
        return render(request,'lxpapp/404page.html')
    return render(request,'lxpapp/404page.html')
    

@login_required
def cto_add_course_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            form = LXPFORM.CourseForm(request.POST or None)
            clist = LXPModel.Subject.objects.raw('SELECT  Distinct  lxpapp_subject.id as id,  lxpapp_chapter.id as chapter_id, lxpapp_subject.subject_name,  lxpapp_chapter.chapter_name  FROM  lxpapp_chapter  INNER JOIN lxpapp_subject ON (lxpapp_chapter.subject_id = lxpapp_subject.id) ORDER BY  lxpapp_subject.subject_name,  lxpapp_chapter.chapter_name')
            sub = ''
            oldsub = ''
            js = '[{' 
            a = 1
            for x in clist:
                sub = x.subject_name
                if sub != oldsub:
                    if a != 1:
                        js = js[:len(js)-1]
                        js += ']},{'    
                    oldsub = sub
                    a = 2
                    js += 'id: "s___' + str(x.id) + '", text: "' + str(sub).replace('\r','') + '", expanded: false, items: ['
                
                js += ' { id: "c___' + str(x.chapter_id) + '", text: "' + str(x.chapter_name).replace('\r','') + '" },'
            js = js[:len(js)-1]
            js += ']}]' 
            bchapter = []

            context = {
                'form': form,
                'js': js,
                'page_title': 'Add Course',
                'chapterlistbyid' : bchapter
            }
            if request.method == 'POST':
                name = request.POST.get('course_name')
                course = LXPModel.Course.objects.all().filter(course_name__iexact = name)
                if course:
                    messages.info(request, 'Course Name Already Exist')
                    return redirect(reverse('cto-add-course'))
                try:
                    mainhead = request.POST.get('mainhead')
                    subhead = request.POST.get('subhead')
                    description = request.POST.get('description')
                    whatlearn = request.POST.get('whatlearn')
                    includes = request.POST.get('includes')
                    themecolor = request.POST.get('themecolor')
                    tags = request.POST.get('tag-output')
                    tags = str(tags).replace('<span class="close">x</span>','')
                    if ',' not in tags:
                        tags = tags + '<span class="close">x</span>'
                    image = request.POST.get ('image')
                    banner = request.POST.get ('banner')
                    price = request.POST.get ('price')
                    chapterlist = request.POST.get ('chapterlist')
                    course = LXPModel.Course.objects.create(
                                                course_name = name,
                                                mainhead_id = mainhead,
                                                subhead_id = subhead,
                                                description = description,
                                                whatlearn = whatlearn,
                                                themecolor = themecolor,
                                                includes = includes,
                                                image = image,
                                                banner = banner,
                                                price = price,
                                                tags = tags)
                    course.save()
                    fields = chapterlist.split(",")
                    for x in fields:
                        if x[0:4] != "s___":
                           ch = LXPModel.CourseChapter.objects.create(
                                    course_id = course.id,
                                    chapter_id = x[4:],
                                    subject_id = LXPModel.Chapter.objects.get(id=x[4:]).subject_id)
                           ch.save()
                    messages.success(request, "Successfully Updated")
                    return redirect(reverse('cto-view-course'))
                except Exception as e:
                    messages.error(request, "Could Not Add " + str(e))
            return render(request, 'cto/course/cto_add_course.html', context)
    #except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def cto_update_course_view(request, pk):
    #try:
        if str(request.session['utype']) == 'cto':
            course_name = ''
            description = ''
            whatlearn = ''
            includes = ''
            image = ''
            price = ''
            tags = ''
            banner = ''
            instance = get_object_or_404(LXPModel.Course, id=pk)
            modbyid = LXPModel.Course.objects.all().filter(id=pk)
            

            for x in modbyid:
                course_name = x.course_name
                description = x.description
                whatlearn = x.whatlearn
                includes = x.includes
                image = x.image
                price = x.price
                tags = x.tags
                banner = x.banner
            tags = tags.replace(', ','<span class="close">x</span>, ')
            tags += '<span class="close">x</span>'
            form = LXPFORM.CourseForm(request.POST or None, instance=instance)
            clist = LXPModel.Subject.objects.raw('SELECT    lxpapp_subject.id as id,  lxpapp_chapter.id as chapter_id, lxpapp_subject.subject_name,  lxpapp_chapter.chapter_name  FROM  lxpapp_chapter  INNER JOIN lxpapp_subject ON (lxpapp_chapter.subject_id = lxpapp_subject.id) ORDER BY  lxpapp_subject.subject_name,  lxpapp_chapter.chapter_name')
            chapbyid= list(LXPModel.CourseChapter.objects.raw('SELECT 1 as id,  lxpapp_chapter.chapter_name FROM  lxpapp_coursechapter  INNER JOIN lxpapp_chapter ON (lxpapp_coursechapter.chapter_id = lxpapp_chapter.id)  WHERE lxpapp_coursechapter.course_id = ' + str(pk)))

            bchapter = []
            for c in chapbyid:
                btrnr={}
                btrnr["name"]=str(c.chapter_name).replace('\r','')
                bchapter.append(btrnr)
            sub = ''
            oldsub = ''
            js = '[{' 
            a = 1
            for x in clist:
                sub = x.subject_name
                if sub != oldsub:
                    if a != 1:
                        js = js[:len(js)-1]
                        js += ']},{'    
                    oldsub = sub
                    a = 2
                    js += 'id: "s___' + str(x.id) + '", text: "' + str(sub).replace('\r','') + '", expanded: false, items: ['
                
                js += ' { id: "c___' + str(x.chapter_id) + '", text: "' + str(x.chapter_name).replace('\r','') + '" },'
            js = js[:len(js)-1]
            js += ']}]' 
            context = {
                'form': form,
                'js': js,
                'course_id': pk,
                'page_title': 'Edit Course',
                'chapterlistbyid' : bchapter,
                'mod_name' : course_name,
                'description' : description,
                'whatlearn' : whatlearn,
                'includes' : includes,
                'image' : image,
                'banner' : banner,
                'price' : price,
                'tags' : tags
            }
            if request.method == 'POST':
                name = request.POST.get('course_name')
                course = LXPModel.Course.objects.all().filter(course_name__iexact = name).exclude(id=pk)
                if course:
                    messages.info(request, 'Course Name Already Exist')
                    return redirect(reverse('cto-update-course', args=[pk]))
                try:
                    course = LXPModel.Course.objects.get(id=pk)
                    mainhead = request.POST.get('mainhead')
                    subhead = request.POST.get('subhead')
                    description = request.POST.get('description')
                    whatlearn = request.POST.get('whatlearn')
                    includes = request.POST.get('includes')
                    themecolor = request.POST.get('themecolor')
                    tags = request.POST.get('tag-output')
                    tags = str(tags).replace('<span class="close">x</span>','')
                    if ',' not in tags:
                        tags = tags + '<span class="close">x</span>'
                    image = request.POST.get ('image')
                    banner = request.POST.get ('banner')
                    price = request.POST.get ('price')
                    chapterlist = request.POST.get ('chapterlist')
                    course.course_name = name
                    course.mainhead_id = mainhead
                    course.subhead_id = subhead
                    course.description = description
                    course.whatlearn = whatlearn
                    course.themecolor = themecolor
                    course.includes = includes
                    course.image = image
                    course.banner = banner
                    course.price = price
                    course.tags = tags
                    course.save()
                    c_list = LXPModel.Course.objects.raw('SELECT    lxpapp_course.id,  lxpapp_course.course_name,  lxpapp_course.description,  lxpapp_course.whatlearn,  lxpapp_course.includes,  lxpapp_course.themecolor,  lxpapp_course.tags,  lxpapp_course.image,  lxpapp_course.price,  lxpapp_mainhead.mainhead_name,  lxpapp_subhead.subhead_name,  COunt(lxpapp_material.topic) AS lessons FROM  lxpapp_course  LEFT OUTER JOIN lxpapp_mainhead ON (lxpapp_course.mainhead_id = lxpapp_mainhead.id)  LEFT OUTER JOIN lxpapp_subhead ON (lxpapp_course.subhead_id = lxpapp_subhead.id)  LEFT OUTER JOIN lxpapp_coursechapter ON (lxpapp_course.id = lxpapp_coursechapter.course_id)  LEFT OUTER JOIN lxpapp_material ON (lxpapp_coursechapter.chapter_id = lxpapp_material.chapter_id) GROUP BY  lxpapp_course.id,  lxpapp_course.course_name,  lxpapp_course.description,  lxpapp_course.whatlearn,  lxpapp_course.includes,  lxpapp_course.themecolor,  lxpapp_course.tags,  lxpapp_course.image,  lxpapp_course.price,  lxpapp_mainhead.mainhead_name,  lxpapp_subhead.subhead_name')
                    return render(request,'cto/course/cto_view_course.html',{'courses':c_list})
                except Exception as e:
                    messages.error(request, "Could Not Add " + str(e))
            return render(request, 'cto/course/cto_update_course.html', context)
    #except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def cto_view_course_view(request):
    # try:
        if str(request.session['utype']) == 'cto':
            c_list = LXPModel.Course.objects.raw('SELECT    lxpapp_course.id,  lxpapp_course.course_name,  lxpapp_course.description,  lxpapp_course.whatlearn,  lxpapp_course.includes,  lxpapp_course.themecolor,  lxpapp_course.tags,  lxpapp_course.image,  lxpapp_course.price,  lxpapp_mainhead.mainhead_name,  lxpapp_subhead.subhead_name,  COunt(lxpapp_material.topic) AS lessons FROM  lxpapp_course  LEFT OUTER JOIN lxpapp_mainhead ON (lxpapp_course.mainhead_id = lxpapp_mainhead.id)  LEFT OUTER JOIN lxpapp_subhead ON (lxpapp_course.subhead_id = lxpapp_subhead.id)  LEFT OUTER JOIN lxpapp_coursechapter ON (lxpapp_course.id = lxpapp_coursechapter.course_id)  LEFT OUTER JOIN lxpapp_material ON (lxpapp_coursechapter.chapter_id = lxpapp_material.chapter_id) GROUP BY  lxpapp_course.id,  lxpapp_course.course_name,  lxpapp_course.description,  lxpapp_course.whatlearn,  lxpapp_course.includes,  lxpapp_course.themecolor,  lxpapp_course.tags,  lxpapp_course.image,  lxpapp_course.price,  lxpapp_mainhead.mainhead_name,  lxpapp_subhead.subhead_name')
            return render(request,'cto/course/cto_view_course.html',{'courses':c_list})
    #except:
        #return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_course_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            course=LXPModel.Course.objects.get(id=pk)
            course.delete()
        c_list = LXPModel.Course.objects.raw('SELECT    lxpapp_course.id,  lxpapp_course.course_name,  lxpapp_course.description,  lxpapp_course.whatlearn,  lxpapp_course.includes,  lxpapp_course.themecolor,  lxpapp_course.tags,  lxpapp_course.image,  lxpapp_course.price,  lxpapp_mainhead.mainhead_name,  lxpapp_subhead.subhead_name,  COunt(lxpapp_material.topic) AS lessons FROM  lxpapp_course  LEFT OUTER JOIN lxpapp_mainhead ON (lxpapp_course.mainhead_id = lxpapp_mainhead.id)  LEFT OUTER JOIN lxpapp_subhead ON (lxpapp_course.subhead_id = lxpapp_subhead.id)  LEFT OUTER JOIN lxpapp_coursechapter ON (lxpapp_course.id = lxpapp_coursechapter.course_id)  LEFT OUTER JOIN lxpapp_material ON (lxpapp_coursechapter.chapter_id = lxpapp_material.chapter_id) GROUP BY  lxpapp_course.id,  lxpapp_course.course_name,  lxpapp_course.description,  lxpapp_course.whatlearn,  lxpapp_course.includes,  lxpapp_course.themecolor,  lxpapp_course.tags,  lxpapp_course.image,  lxpapp_course.price,  lxpapp_mainhead.mainhead_name,  lxpapp_subhead.subhead_name')
        return render(request,'cto/course/cto_view_course.html',{'courses':c_list})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_upload_course_details_csv_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                coursetext=request.POST.get('course_name')
                course = LXPModel.Course.objects.all().filter(course_name__iexact = coursetext)
                if course:
                    messages.info(request, 'Course Name Already Exist')
                elif coursetext == '':
                    messages.info(request, 'Please enter Course Name')
                elif request.POST.get('select_file') == '':
                    messages.info(request, 'Please select CSV file for upload')
                else:
                    course = LXPModel.Course.objects.create(course_name = coursetext)
                    course.save()     
                    csv_file = request.FILES["select_file"]
                    file_data = csv_file.read().decode("utf-8")		
                    lines = file_data.split("\n")
                    oldsub =''
                    oldmod=''
                    oldchap=''
                    oldtop=''
                    subid =0
                    modid=0
                    chapid=0
                    topid=0
                    no = 0
                    for line in lines:						
                        no = no + 1
                        if no > 1:
                            fields = line.split(",")
                            if str(fields[0]).replace('///',',') != oldsub:
                                oldsub = str(fields[0]).replace('///',',')
                                sub = LXPModel.Subject.objects.all().filter(subject_name__exact = oldsub )
                                if not sub:
                                    sub = LXPModel.Subject.objects.create(subject_name = oldsub )
                                    sub.save()
                                    subid=sub.id
                                else:
                                    for x in sub:
                                        subid=x.id  
                            if str(fields[1]).replace('///',',') != oldmod:
                                oldmod = str(fields[1]).replace('///',',')
                                mod = LXPModel.Module.objects.all().filter(module_name__exact = oldmod,subject_id=subid)
                                if not mod:
                                    mod = LXPModel.Module.objects.create(module_name = oldmod,subject_id=subid)
                                    mod.save()
                                    modid=mod.id
                                else:
                                    for x in mod:
                                        modid=x.id 
                            if str(fields[2]).replace('///',',') != oldchap:
                                oldchap = str(fields[2]).replace('///',',')
                                chap = LXPModel.Chapter.objects.all().filter(chapter_name__exact = oldchap,module_id=modid)
                                if not chap:
                                    chap = LXPModel.Chapter.objects.create(chapter_name = oldchap,module_id=modid)
                                    chap.save()
                                    chapid=chap.id
                                else:
                                    for x in chap:
                                        chapid=x.id 
                            if str(fields[3]).replace('///',',') != oldtop:
                                oldtop = str(fields[3]).replace('///',',') 
                                top = LXPModel.Topic.objects.all().filter(topic_name__exact = oldtop,chapter_id=chapid)
                                if not top:
                                    top = LXPModel.Topic.objects.create(topic_name = oldtop,chapter_id=chapid)
                                    top.save()
                                    topid1=top.id 
                                else:
                                    for x in top:
                                        topid1=x.id 
                            coursedet = LXPModel.CourseDetails.objects.create(
                                        course_id =course.id,
                                        subject_id=subid,
                                        module_id=modid,
                                        chapter_id=chapid,
                                        topic_id=topid1
                                        )
                            coursedet.save()
            return render(request,'cto/course/cto_view_course.html')
    except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def cto_topic_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/topic/cto_topic.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_add_topic_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            form = LXPFORM.TopicForm(request.POST or None)
            context = {
                'form': form,
                'page_title': 'Add Topic'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('topic_name')
                    chapter = form.cleaned_data.get('chapter').pk
                    topic = LXPModel.Topic.objects.all().filter(topic_name__iexact = name)
                    if topic:
                        messages.info(request, 'Topic Name Already Exist')
                        return redirect(reverse('cto-add-topic'))
                    try:
                        topic = LXPModel.Topic.objects.create(
                                                    topic_name = name,
                                                    chapter_id = chapter)
                        topic.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('cto-view-topic'))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/topic/add_edit_topic.html', context)
    except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def cto_update_topic_view(request, pk):
    try:
        if str(request.session['utype']) == 'cto':
            instance = get_object_or_404(LXPModel.Topic, id=pk)
            form = LXPFORM.TopicForm(request.POST or None, instance=instance)
            context = {
                'form': form,
                'topic_id': pk,
                'page_title': 'Edit Topic'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('topic_name')
                    chapter = form.cleaned_data.get('chapter').pk
                    topic = LXPModel.Topic.objects.all().filter(topic_name__iexact = name).exclude(id=pk)
                    if topic:
                        messages.info(request, 'Topic Name Already Exist')
                        return redirect(reverse('cto-update-topic', args=[pk]))
                    try:
                        topic = LXPModel.Topic.objects.get(id=pk)
                        topic.topic_name = name
                        topic.chapter_id = chapter
                        topic.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('cto-view-topic'))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/topic/add_edit_topic.html', context)
    except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def cto_view_topic_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            c_list = LXPModel.Topic.objects.all()
            return render(request,'cto/topic/cto_view_topic.html',{'topics':c_list})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_topic_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            topic=LXPModel.Topic.objects.get(id=pk)
            topic.delete()
            return HttpResponseRedirect('/cto/cto-view-topic')
        topics = LXPModel.Topic.objects.all()
        return render(request,'cto/topic/cto_view_topic.html',{'topics':topics})
    except:
        return render(request,'lxpapp/404page.html')


def load_subheads(request):
    try:
        mainhead_id = request.GET.get('mainhead')
        subheads = LXPModel.SubHead.objects.filter(mainhead_id=mainhead_id).order_by('subhead_name')
        context = {'subheads': subheads}
        return render(request, 'hr/subhead_dropdown_list_options.html', context)
    except:
        return render(request,'lxpapp/404page.html')

def load_courses(request):
    try:
        subject_id = request.GET.get('subject')
        courses = LXPModel.Course.objects.filter(subject_id=subject_id).order_by('course_name')
        context = {'courses': courses}
        return render(request, 'hr/course_dropdown_list_options.html', context)
    except:
        return render(request,'lxpapp/404page.html')
    
def load_chapters(request):
    try:
        subject_id = request.GET.get('subject')
        chapters = LXPModel.Chapter.objects.filter(subject_id=subject_id).order_by('chapter_name')
        context = {'chapters': chapters}
        return render(request, 'hr/chapter_dropdown_list_options.html', context)
    except:
        return render(request,'lxpapp/404page.html')

def load_topics(request):
    try:
        chapter_id = request.GET.get('chapter')
        topics = LXPModel.Topic.objects.filter(chapter_id=chapter_id).order_by('topic_name')
        context = {'topics': topics}
        return render(request, 'hr/topic_dropdown_list_options.html', context)
    except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def getcredentials(request):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    client_secrets_file = "GoogleCredV1.json"

    # Get credentials and create an API client
    flow = None
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    flow.run_local_server()
    credentials = flow.credentials
    return credentials

@login_required
def cto_sync_youtube_view(request):
    try:
        if str(request.session['utype']) == 'cto':
    #pllist = LXPModel.IncludePlaylist.objects.all().filter(playlist_id__in =LXPModel.Playlist.objects.all().order_by('name'))
            pllist = LXPModel.Playlist.objects.all().order_by('name')
            return render(request,'cto/youtube/cto_sync_youtube.html',{'pllist':pllist})
    except:
        return render(request,'lxpapp/404page.html')
@login_required
def cto_sync_youtube_start_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                pm = PlaylistManager()
                credentials = getcredentials(request)
                
                alllist = pm.initializePlaylist(credentials)
                plcount = 1
                maxcount = alllist.__len__()
                for PL_ID in alllist:
                        PL_NAME = ''#LXPModel.Playlist.objects.values('name').filter(playlist_id = PL_ID)
                        print(str(plcount) + ' ' + PL_NAME)
                        pm.getAllVideosForPlaylist(PL_ID,credentials,maxcount,plcount,PL_NAME)
                        plcount = plcount + 1
                        HttpResponse(loader.get_template('cto/youtube/cto_sync_youtube.html').render(
                            {
                                "plname": PL_NAME,
                                "maxcount": maxcount,
                                "plcount": plcount
                            }
                            ))
                dict={
                'total_learner':0,
                'total_trainer':0,
                'total_exam':0,
                'total_question':0,
                }
                return render(request,'cto/cto_dashboard.html',context=dict)
            pllist = LXPModel.Playlist.objects.all().order_by('name')
            return render(request,'cto/youtube/cto_sync_youtube.html',{'pllist':pllist})    
    #except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def cto_sync_youtube_byselected_playlist_start_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                if 'dblist' in request.POST:
                    pllist = LXPModel.Playlist.objects.all().order_by('name')
                    return render(request,'cto/youtube/cto_sync_youtube.html',{'pllist':pllist})
                elif 'cloudlist' in request.POST:
                    pm = PlaylistManager()
                    credentials = getcredentials(request)
                    pl =  pm.initializePlaylist(credentials)
                    pllist = LXPModel.Playlist.objects.all().order_by('name')
                    return render(request,'cto/youtube/cto_sync_youtube.html',{'pllist':pllist})
                elif 'startselected' in request.POST:
                    pm = PlaylistManager()
                    selectedlist = request.POST.getlist('playlist[]')
                    maxcount = selectedlist.__len__()
                    plcount = 1
                    credentials = getcredentials(request)
                    for PL_NAME in selectedlist:
                        print(str(plcount) + ' of ' + str(maxcount))
                        _id = PL_NAME 
                        playlist = LXPModel.Playlist.objects.values_list('playlist_id', flat=True).get(id=PL_NAME)
                        pm.getAllVideosForPlaylist(playlist,credentials,maxcount,plcount,_id)
                        plcount= plcount + 1
            dict={
            'total_learner':0,
            'total_trainer':0,
            'total_exam':0,
            'total_question':0,
            }
            return render(request,'cto/cto_dashboard.html',context=dict)
    #except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def get_message_from_httperror(e):
    return e.error_details[0]['message']
######################################################################


@login_required
def cto_trainernotification_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            return render(request,'cto/trainernotification/cto_trainernotification.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_add_trainernotification_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            if request.method=='POST':
                trainernotificationForm=LXPFORM.TrainerNotificationForm(request.POST)
                if trainernotificationForm.is_valid(): 
                    trainernotificationtext = trainernotificationForm.cleaned_data["trainernotification_message"]
                    trainernotification = LXPModel.TrainerNotification.objects.all().filter(trainernotification_message__iexact = trainernotificationtext)
                    if trainernotification:
                        messages.info(request, 'TrainerNotification Name Already Exist')
                        trainernotificationForm=LXPFORM.TrainerNotificationForm()
                        return render(request,'cto/trainernotification/cto_add_trainernotification.html',{'trainernotificationForm':trainernotificationForm})                  
                    else:
                        trainernotification = LXPModel.TrainerNotification.objects.create(
                            trainer_id = trainernotificationForm.cleaned_data["trainerID"].user_id,
                            sender_id = request.user.id,
                            status = False,
                            trainernotification_message =trainernotificationtext
                        )
                        trainernotification.save()
                else:
                    print("form is invalid")
            trainernotificationForm=LXPFORM.TrainerNotificationForm()
            return render(request,'cto/trainernotification/cto_add_trainernotification.html',{'trainernotificationForm':trainernotificationForm})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_trainernotification_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':
            trainernotification = LXPModel.TrainerNotification.objects.get(id=pk)
            trainernotificationForm=LXPFORM.TrainerNotificationForm(request.POST,instance=trainernotification)
            if request.method=='POST':
                if trainernotificationForm.is_valid(): 
                    trainernotificationtext = trainernotificationForm.cleaned_data["trainernotification_message"]
                    trainernotification = LXPModel.TrainerNotification.objects.all().filter(trainernotification_message__iexact = trainernotificationtext).exclude(id=pk)
                    if trainernotification:
                        messages.info(request, 'TrainerNotification Name Already Exist')
                        return render(request,'cto/trainernotification/cto_update_trainernotification.html',{'trainernotificationForm':trainernotificationForm})
                    else:
                        trainernotificationForm.save()
                        trainernotifications = LXPModel.TrainerNotification.objects.all()
                        return render(request,'cto/trainernotification/cto_view_trainernotification.html',{'trainernotifications':trainernotifications})
            return render(request,'cto/trainernotification/cto_update_trainernotification.html',{'trainernotificationForm':trainernotificationForm,'sub':trainernotification.trainernotification_message})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_view_trainernotification_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            trainernotifications = LXPModel.TrainerNotification.objects.all()
            return render(request,'cto/trainernotification/cto_view_trainernotification.html',{'trainernotifications':trainernotifications})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_trainernotification_view(request,pk):
    try:
        if str(request.session['utype']) == 'cto':  
            trainernotification=LXPModel.TrainerNotification.objects.get(id=pk)
            trainernotification.delete()
        trainernotifications = LXPModel.TrainerNotification.objects.all()
        return render(request,'cto/trainernotification/cto_view_trainernotification.html',{'trainernotifications':trainernotifications})
    except:
        return render(request,'lxpapp/404page.html')
    
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


@login_required
def cto_lxp_upload_doc_file_view(request):
    if request.method == 'POST' and request.FILES['file']:
        emails = request.POST.get('emails-output')
        emails = str(emails).replace('<span class="close">x</span>','')
        fields = emails.split(",")
        
        
        import googleapiclient.discovery
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        from social_django.models import UserSocialAuth
        from apiclient.discovery import build
        from apiclient.errors import HttpError
        from apiclient.http import MediaFileUpload
        from oauth2client.client import flow_from_clientsecrets
        import datetime
        import pytz
        CLIENT_SECRETS_FILE = "GoogleCredV1.json"
        YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube"
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"

        playlistname = request.POST.get('playlist')  # Get the video ID from the form
        playlist_id = LXPModel.Playlist.objects.only('playlist_id').get(name=playlistname).playlist_id
        video_file = request.FILES.get('video')
        title = request.POST.get('title')
        description = request.POST.get('description')
        channel_id = request.POST.get('channel_id')
        channel_name = request.POST.get('channel_name')

        # youtube = build('youtube', 'v3', developerKey='AIzaSyBRlrfvqZLCXUU8oc19PO4Zg2-hB2QMBrI')
        # flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
        #                            scope=YOUTUBE_UPLOAD_SCOPE,
        #                            message="")

        # storage = CLIENT_SECRETS_FILE#os.path.abspath(os.path.join(os.path.dirname(__file__),
        #                             #CLIENT_SECRETS_FILE))
        
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, YOUTUBE_UPLOAD_SCOPE)
        flow.run_local_server()
        credentials = flow.credentials
        youtube = googleapiclient.discovery.build(
            YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)
        # Save the video file to a temporary location
        video_path = os.path.join(settings.MEDIA_ROOT, 'temp_video.mp4')
        with open(video_path, 'wb+') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)

        try:
            # Create a new video resource
            videos_insert_response = youtube.videos().insert(
                part='snippet,status',
                body={
                    'snippet': {
                        'title': title,
                        'description': description,
                    },
                    'status': {
                        'privacyStatus': 'private'  # Set video privacy as public
                    }
                },
                media_body=MediaFileUpload(video_path, chunksize=-1, resumable=True)
            ).execute()

            video_id = videos_insert_response['id']
            video_url = f'https://www.youtube.com/watch?v={video_id}'

            # Add the video to a playlist
            youtube.playlistItems().insert(
                part='snippet',
                body={
                    'snippet': {
                        'playlistId': playlist_id,
                        'resourceId': {
                            'kind': 'youtube#video',
                            'videoId': video_id
                        }
                    }
                }
            ).execute()

            # Optionally, you can delete the temporary video file
            os.remove(video_path)

        except Exception as e:
            # Handle API errors or display an error message
            error_message = str(e)
            return render(request,'lxpapp/404page.html')

        file = request.FILES['file']
        # Connect to the GitHub API
        access_token = settings.GITHUB_ACCESS_TOKEN
        github = Github(access_token)
        # Get the repository
        repo_owner = settings.GITHUB_REPO_OWNER
        repo_name = settings.GITHUB_REPO_NAME
        repo = github.get_repo(f'{repo_owner}/{repo_name}')
        # Create a new file in the repository
        new_file = repo.create_file(
            path=file.name,
            message='Upload file',
            content=file.read(),
            branch='main'  # Replace with your desired branch name
        )
        file_url = new_file['content'].download_url
        file_url = file_url.replace('raw.githubusercontent','github')
        file_url = file_url.replace('/main/','/blob/main/')
        # Get the URL of the newly created file
        #file_url = 'https://raw.githubusercontent.com/' + settings.GITHUB_REPO_OWNER +  '/' + settings.GITHUB_REPO_NAME +  '/main/' + file.name + '?token=A76LNERAQFQXBYUZ77XVTBDEQHWBO'

        video = LXPModel.Video.objects.create(
                            video_id=video_id,
                            published_at=datetime.datetime.now(pytz.utc),
                            name=title,
                            description=description,
                            thumbnail_url = '',
                            channel_id= channel_id,
                            channel_name=channel_name
                        )
        video.save()
        videocount = LXPModel.Playlist.objects.all().count()
        PL_id = LXPModel.Playlist.objects.only('id').get(name=playlistname).id
        plylistitems = LXPModel.PlaylistItem.objects.create(
            playlist_item_id = '',
            video_position = videocount,
            published_at = datetime.datetime.now(pytz.utc),
            channel_id= channel_id,
            channel_name=channel_name,
            is_duplicate = False,
            is_marked_as_watched = False,
            num_of_accesses = 0,
            playlist_id = PL_id,
            video_id = video.id
        )
        plylistitems.save()
        material = LXPModel.SessionMaterial.objects.create(
                mtype = 'PDF',
                urlvalue = file_url,
                description = description,
                playlist_id = PL_id,
                video_id = video.id
        )
        material.save()
        return render(request, 'cto/lxpdocgitupload/success.html', {'file_url': file_url})
    playlist = LXPModel.Playlist.objects.all().order_by('name')
    return render(request, 'cto/lxpdocgitupload/upload_recorded_video_material.html',{'playlist': playlist})


@login_required
def cto_add_playlist_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            form = LXPFORM.PlayListForm(request.POST or None)
            context = {
                'form': form,
                'page_title': 'Add Play List'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('name')
                    playlist = LXPModel.Playlist.objects.all().filter(name__iexact = name)
                    if playlist:
                        messages.info(request, 'PlayList Name Already Exist')
                        return redirect(reverse('cto-add-playlist'))
                    try:
                        channel_id = form.cleaned_data.get('channel_id')
                        channel_name = form.cleaned_data.get('channel_name')
                        playlist_id = form.cleaned_data.get('playlist_id')
                        playlist = LXPModel.Playlist.objects.create(
                                                    name = name,
                                                    channel_id = channel_id,
                                                    channel_name = channel_name,
                                                    playlist_id = playlist_id)
                        playlist.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('cto-add-playlist'))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/playlist/add_edit_playlist.html', context)
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_playlist_view(request, pk):
    #try:
        if str(request.session['utype']) == 'cto':
            instance = get_object_or_404(LXPModel.Playlist, id=pk)
            form = LXPFORM.PlayListForm(request.POST or None, instance=instance)
            context = {
                'form': form,
                'playlist_id': pk,
                'page_title': 'Edit Play List'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('name')
                    playlist = LXPModel.Playlist.objects.all().filter(name__iexact = name).exclude(id=pk)
                    if playlist:
                        messages.info(request, 'PlayList Name Already Exist')
                        return redirect(reverse('cto-update-playlist', args=[pk]))
                    try:
                        playlist = LXPModel.Playlist.objects.get(id=pk)
                        name = form.cleaned_data.get('name')
                        channel_id = form.cleaned_data.get('channel_id')
                        channel_name = form.cleaned_data.get('channel_name')
                        playlist_id = form.cleaned_data.get('playlist_id')

                        playlist.name = name
                        playlist.channel_id = channel_id
                        playlist.channel_name = channel_name
                        playlist.playlist_id = playlist_id
                        playlist.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('cto-view-playlist', args=[pk]))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/playlist/add_edit_playlist.html', context)
    #except:
        return render(request,'lxpapp/404page.html')


@login_required
def cto_view_playlist_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            playlists = LXPModel.Playlist.objects.all()
            return render(request,'cto/playlist/cto_view_playlist.html',{'playlists':playlists})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_delete_playlist_view(request,pk):
    #try:
        if str(request.session['utype']) == 'cto':  
            playlist=LXPModel.Playlist.objects.get(id=pk)
            playlist.delete()
        playlists = LXPModel.Playlist.objects.all()
        return render(request,'cto/playlist/cto_view_playlist.html',{'playlists':playlists})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_view_video_list_view(request):
    #try:
        if str(request.session['utype']) == 'cto':
            c_list = LXPModel.PlaylistItem.objects.raw(' SELECT DISTINCT  lxpapp_playlist.id as id, lxpapp_playlistitem.id as item_id, lxpapp_playlist.name as Pl_Name , lxpapp_video.id as vid_id,  lxpapp_video.name as vid_Name FROM  lxpapp_playlistitem  INNER JOIN lxpapp_playlist ON (lxpapp_playlistitem.playlist_id = lxpapp_playlist.id)  INNER JOIN lxpapp_video ON (lxpapp_playlistitem.video_id = lxpapp_video.id) ORDER BY  lxpapp_playlist.name,  lxpapp_video.name')
            return render(request,'cto/youtube/cto_view_video_list.html',{'videos':c_list})
    #except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def cto_delete_video_view(request,pk,pl_id,vid_id):
    #try:
        if str(request.session['utype']) == 'cto':  
            delobj = LXPModel.PlaylistItem.objects.all().filter(id = pk).delete()
            delobj = LXPModel.Video.objects.all().filter(id = vid_id).delete()
        c_list = LXPModel.PlaylistItem.objects.raw(' SELECT DISTINCT  lxpapp_playlist.id as id, lxpapp_playlistitem.id as item_id, lxpapp_playlist.name as Pl_Name , lxpapp_video.id as vid_id,  lxpapp_video.name as vid_Name FROM  lxpapp_playlistitem  INNER JOIN lxpapp_playlist ON (lxpapp_playlistitem.playlist_id = lxpapp_playlist.id)  INNER JOIN lxpapp_video ON (lxpapp_playlistitem.video_id = lxpapp_video.id) ORDER BY  lxpapp_playlist.name,  lxpapp_video.name')
        return render(request,'cto/youtube/cto_view_video_list.html',{'videos':c_list})
    #except:
        return render(request,'lxpapp/404page.html')

from datetime import datetime
API_KEY = 'AIzaSyDBSnyGaMAoCEpFyh_WPj7E3pQV7GJivJA'  # Replace with your API Key
CHANNEL_ID = 'UCxdhwzsgcGldYghv6u3nrXw'  # Replace with your Channel ID

youtube = build('youtube', 'v3', developerKey=API_KEY)

def sync_playlists_and_videos():
    # Fetch playlists from the channel
    request = youtube.playlists().list(
        part='snippet,contentDetails',
        channelId=CHANNEL_ID,
        maxResults=50
    )
    response = request.execute()

    for playlist_data in response['items']:
        playlist, created = LXPModel.Playlist.objects.get_or_create(
            playlist_id=playlist_data['id'],
            defaults={
                'title': playlist_data['snippet']['title'],
                'description': playlist_data['snippet'].get('description', ''),
                'published_at': datetime.strptime(
                    playlist_data['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%S.%fZ'
                )
            }
        )

        # Fetch videos in the playlist
        sync_videos(playlist)

def sync_videos(playlist):
    request = youtube.playlistItems().list(
        part='snippet,contentDetails',
        playlistId=playlist.playlist_id,
        maxResults=50
    )
    response = request.execute()

    for video_data in response['items']:
        LXPModel.Video.objects.get_or_create(
            video_id=video_data['contentDetails']['videoId'],
            defaults={
                'playlist': playlist,
                'title': video_data['snippet']['title'],
                'description': video_data['snippet'].get('description', ''),
                'published_at': datetime.strptime(
                    video_data['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%S.%fZ'
                )
            }
        )


@login_required
def cto_add_zaid_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            form = LXPFORM.ZaidForm(request.POST or None)
            context = {
                'form': form,
                'page_title': 'Add Zaid'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('zaid_name')
                    zaid = LXPModel.Zaid.objects.all().filter(zaid_name__iexact = name)
                    if zaid:
                        messages.info(request, 'Zaid Name Already Exist')
                        return redirect(reverse('cto-add-zaid'))
                    try:
                        zaid = LXPModel.Zaid.objects.create(
                                                    zaid_name = name)
                        zaid.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('cto-add-zaid'))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/zaid/add_edit_zaid.html', context)
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def cto_update_zaid_view(request, pk):
    try:
        if str(request.session['utype']) == 'cto':
            instance = get_object_or_404(LXPModel.Zaid, id=pk)
            form = LXPFORM.ZaidForm(request.POST or None, instance=instance)
            context = {
                'form': form,
                'zaid_id': pk,
                'page_title': 'Edit Zaid'
            }
            if request.method == 'POST':
                if form.is_valid():
                    name = form.cleaned_data.get('zaid_name')
                    zaid = LXPModel.Zaid.objects.all().filter(zaid_name__iexact = name).exclude(id=pk)
                    if zaid:
                        messages.info(request, 'Zaid Name Already Exist')
                        return redirect(reverse('cto-update-zaid', args=[pk]))
                    try:
                        zaid = LXPModel.Zaid.objects.get(id=pk)
                        zaid.zaid_name = name
                        zaid.save()
                        messages.success(request, "Successfully Updated")
                        return redirect(reverse('cto-update-zaid', args=[pk]))
                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                    messages.error(request, "Fill Form Properly")
            return render(request, 'cto/zaid/add_edit_zaid.html', context)
    except:
        return render(request,'lxpapp/404page.html')


@login_required
def cto_view_zaid_view(request):
    try:
        if str(request.session['utype']) == 'cto':
            zaids = LXPModel.Zaid.objects.all()
            return render(request,'cto/zaid/cto_view_zaid.html',{'zaids':zaids})
    except:
        return render(request,'lxpapp/404page.html')