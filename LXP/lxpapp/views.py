from django.shortcuts import render,redirect,get_object_or_404
from lxpapp import forms,models
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import connection
from social_django.models import UserSocialAuth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from datetime import datetime
login_time = datetime.now()
logout_time  = datetime.now()
from django.http import HttpResponse
from django.contrib.auth import logout
from django.urls import reverse
from lxpapp.models import UserProfile, Playlist, Video, PlaylistItem
from django.contrib import messages
from django.core.files.storage import default_storage
from django.contrib.auth.views import LoginView
from django.db.models import Exists, OuterRef,Case, When, Value, IntegerField,F, Value, Q, Sum, Max
from django.db.models.functions import Coalesce
from lxpapp import models as LXPModel

import os
from django.utils import timezone
from googleapiclient.discovery import build


# Replace with your actual API key
YOUTUBE_API_KEY = 'AIzaSyBRlrfvqZLCXUU8oc19PO4Zg2-hB2QMBrI'

def sync_youtube(channel_id):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    # Fetch all playlists from the channel
    playlists = []
    next_page_token = None
    while True:
        playlist_response = youtube.playlists().list(
            part='id,snippet',
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        playlists.extend(playlist_response['items'])
        next_page_token = playlist_response.get('nextPageToken')
        if not next_page_token:
            break

    for pl in playlists:
        playlist_id = pl['id']
        playlist_title = pl['snippet']['title']
        playlist_description = pl['snippet'].get('description', '')
        playlist_published_at = pl['snippet']['publishedAt']

        # Update or create the Playlist object
        playlist_obj, created = Playlist.objects.update_or_create(
            playlist_id=playlist_id,
            defaults={
                'name': playlist_title,
                'description': playlist_description,
                'published_at': playlist_published_at,
                'last_accessed_on': timezone.now(),
                'is_in_db': True,
            }
        )

        # Fetch all videos in the playlist
        videos = []
        next_video_page_token = None
        while True:
            playlist_items_response = youtube.playlistItems().list(
                part='snippet,contentDetails',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_video_page_token
            ).execute()

            videos.extend(playlist_items_response['items'])
            next_video_page_token = playlist_items_response.get('nextPageToken')
            if not next_video_page_token:
                break

        existing_video_ids = set(playlist_obj.videos.values_list('video_id', flat=True))
        current_video_ids = set()

        for item in videos:
            video_id = item['contentDetails']['videoId']
            current_video_ids.add(video_id)
            video_title = item['snippet']['title']
            video_description = item['snippet'].get('description', '')
            video_published_at = item['snippet'].get('publishedAt', None)
            channel_title = item['snippet']['channelTitle']
            channel_id = item['snippet']['channelId']
            # thumbnail_url = item['snippet']['thumbnails']['default']['url']

            # Update or create the Video object
            video_obj, created = Video.objects.update_or_create(
                video_id=video_id,
                defaults={
                    'name': video_title,
                    'description': video_description,
                    'published_at': video_published_at,
                    'channel_name': channel_title,
                    'channel_id': channel_id,
                    'thumbnail_url': '',
                }
            )

            # Add video to playlist if not already added
            if not playlist_obj.videos.filter(video_id=video_id).exists():
                playlist_obj.videos.add(video_obj)

        # Remove videos that are no longer in the playlist
        videos_to_remove = existing_video_ids - current_video_ids
        if videos_to_remove:
            videos_to_remove_objs = Video.objects.filter(video_id__in=videos_to_remove)
            playlist_obj.videos.remove(*videos_to_remove_objs)

        # Update video count
        playlist_obj.video_count = playlist_obj.videos.count()
        playlist_obj.save()
class CustomLoginView(LoginView):
    template_name = 'loginrelated/userlogin.html'  # Your login template path
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('indexpage')  # Replace 'indexpage' with your indexpage URL name
        return super().get(request, *args, **kwargs)
    
    
@login_required
def switch_user_view(request):
    logout(request)
    google_auth_url = reverse('social:begin', args=['google-oauth2'])
    redirect_uri = request.build_absolute_uri(reverse('social:complete', args=['google-oauth2']))
    authorize_url = reverse('social:begin', args=['google-oauth2'])
    return redirect('/social-auth/login/google-oauth2/')

def signup(request):
        if request.method=="POST":
            first_name = str(request.POST['first_name']).strip()
            last_name = str(request.POST['last_name']).strip()
            import datetime
            username = first_name.replace(' ','_')+ '_' + last_name.replace(' ','_') + '_' + str( User.objects.all().values_list('id', flat=True).order_by('-id').first())
            password = request.POST['password']
            email = request.POST['email']
            newuser = User.objects.create_user(
                first_name=first_name, 
                last_name=last_name,
                username=username,
                password=password,
                email=email
            )
            try:
                newuser.save()
            except:
                return HttpResponse("Something went wrong.")
        else:
            form = forms.UserRegistrationForm()
        form1 = forms.UserRegistrationForm()
        return render(request, 'loginrelated/signup.html', {'form':form1})


def session_expire_view(request):
    A = models.LastUserLogin.objects.all()
    if A:
        for x in A:
            id = x.id
            logout_time = datetime.now()
            dur = str( logout_time - login_time).split(".")[0]
            userlog = models.UserLog.objects.create(
                    user_id = id,
                    login = login_time,
                    logout = logout_time,
                    dur = dur
                    )
            userlog.save()
    models.LastUserLogin.objects.all().delete()
    return render(request, 'loginrelated/user_session_expire.html')

def login(request):
    
    return render(request, 'loginrelated/userlogin.html')

@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    if not user.is_staff:
        pic = UserSocialAuth.objects.only('pic').get(user_id=user.id).pic
    login_time = datetime.now()

@receiver(user_logged_out)
def post_logout(sender, user, request, **kwargs):
    logout_time = datetime.now()
    dur = str( logout_time - login_time).split(".")[0]
    userlog = models.UserLog.objects.create(
              user = user,
              login = login_time,
              logout = logout_time,
              dur = dur
            )
    userlog.save()
    models.LastUserLogin.objects.all().delete()

@login_required
def user_change_password_view(request):
    try:    
        sub = forms.ContactusForm()
        if request.method == 'POST':
            u = request.user
            u.set_password(request.POST['passid'])
            u.save() # Add this line
            logout()
        return render(request, 'loginrelated/changepassword.html')
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def home(request):
    
    if request.user.is_authenticated:
        # user = User.objects.raw('SELECT   auth_user.id,  auth_user.password,  auth_user.last_login,  auth_user.is_superuser,  auth_user.username,  auth_user.first_name,  auth_user.email,  auth_user.is_staff,  auth_user.is_active,  auth_user.date_joined,  auth_user.last_name,  social_auth_usersocialauth.provider,  social_auth_usersocialauth.uid,  social_auth_usersocialauth.extra_data,  social_auth_usersocialauth.user_id,  social_auth_usersocialauth.utype,  social_auth_usersocialauth.status,  social_auth_usersocialauth.modified,  social_auth_usersocialauth.pic,  social_auth_usersocialauth.usercode,  social_auth_usersocialauth.created FROM  social_auth_usersocialauth  INNER JOIN auth_user ON (social_auth_usersocialauth.user_id = auth_user.id)')
        # update_session_auth_hash(request, user)
        return HttpResponseRedirect(reverse('indexpage'))
    return render(request,'lxpapp/404page.html')


def afterlogin_view(request):
    # sync_youtube('UCxdhwzsgcGldYghv6u3nrXw')
    user = UserSocialAuth.objects.all().filter(user_id = request.user.id)
    
    if not user:
        request.session['utype'] = 'admin'
        import requests
        # response = requests.get('http://127.0.0.1:5566/login/')
        return redirect('admin-view-user-list')
    elif user:

        for xx in user:
            if not xx.status:
                return render(request,'loginrelated/wait_for_approval.html')
            if xx.utype == 1:
                request.session['utype'] = 'trainer'
                notification = models.TrainerNotification.objects.all().filter(trainer_id = request.user.id,status = False)
                mco = models.Exam.objects.filter(questiontpye='MCQ').count()
                short = models.Exam.objects.filter(questiontpye='ShortAnswer').count()
                mcqques= models.McqQuestion.objects.all().count()
                sques= models.ShortQuestion.objects.all().count()
                schedulers = models.Scheduler.objects.annotate(
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
            elif xx.utype == 2  or xx.utype == 0 :
                request.session.set_expiry(2400)
                request.session['utype'] = 'learner'
                # return render(request,'learner/learner_dashboard.html')
                learnerdetails = models.LearnerDetails.objects.all().filter(learner_id = request.user.id)
                if learnerdetails:
                    request.session['utype'] = 'learner'
                    setcookies = get_object_or_404(LXPModel.LearnerDetails, learner_id=request.user.id)
                    print("done printing")
                    response =  render(request,'learner/learner_dashboard.html')    
                    response.set_cookie('learnerdetails',{setcookies.user_full_name,setcookies.profile_pic})
                    return response 
                else:
                    if request.method=='POST':
                        profile_pic = request.FILES.get('profile_pic')
                        user_full_name = request.POST["user_full_name"]
                        mobile = request.POST["mobile"]
                        whatsappno = request.POST["whatsappno"]
                        learnerdetails = models.LearnerDetails.objects.create(learner_id=request.user.id,
                                                                            user_full_name= user_full_name,
                                                                            mobile=mobile,
                                                                            whatsappno=whatsappno,profile_pic=profile_pic)
                        learnerdetails.save()
                        logout(request)
                        return HttpResponseRedirect('/')  
#                                send_mail('New User Login / Pending User Login Notification', 'Please check following user is registered or relogin before approval\n' + 'E-mail : ' + str (request.user.email) + '\nFirst Name : ' + str (request.user.first_name) + '\nLast Name : '+ str (request.user.last_name), 'info@nubeera.com', ['info@nubeera.com'])
                        
                    user =  User.objects.all().filter(id = request.user.id)
                    username=''
                    for u in user:
                        username = u.first_name + ' ' + u.last_name
                    return render(request,'loginrelated/add_learnerdetails.html',{'username':username})
            elif xx.utype == 3:
                request.session['utype'] = 'cto'
                return render(request,'cto/cto_dashboard.html')
            elif xx.utype == 4:
                request.session['utype'] = 'cfo'
                return render(request,'cfo/cfo_dashboard.html')
            elif xx.utype == 5:
                request.session['utype'] = 'mentor'
                return render(request,'mentor/mentor_dashboard.html')
            elif xx.utype == 6:
                request.session['utype'] = 'staff'
                return render(request,'staff/staff_dashboard.html')


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('indexpage')
    return HttpResponseRedirect('userlogin')

@login_required
def admin_dashboard_view(request):
    #try:
        if str(request.session['utype']) == 'admin':
            dict={
            'total_learner':0,
            'total_trainer':0,
            'total_exam':0,
            'total_question':0,
            }
            return render(request,'lxpapp/admin_dashboard.html',context=dict)
    #except:
        return render(request,'lxpapp/404page.html')
def aboutus_view(request):
    return render(request,'lxpapp/aboutus.html')

def contactus_view(request):
    try:    
        if str(request.session['utype']) == 'admin':
            sub = forms.ContactusForm()
            if request.method == 'POST':
                sub = forms.ContactusForm(request.POST)
                if sub.is_valid():
                    email = sub.cleaned_data['Email']
                    name=sub.cleaned_data['Name']
                    message = sub.cleaned_data['Message']
                    send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
                    return render(request, 'lxpapp/contactussuccess.html')
            return render(request, 'lxpapp/contactus.html', {'form':sub})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def getUserTable(request):
    users = UserSocialAuth.objects.raw('SELECT   SOCIAL_AUTH_USERSOCIALAUTH.ID,  SOCIAL_AUTH_USERSOCIALAUTH.USER_ID,  AUTH_USER.FIRST_NAME,  AUTH_USER.LAST_NAME,  LXPAPP_LEARNERDETAILS.MOBILE FROM  SOCIAL_AUTH_USERSOCIALAUTH  LEFT OUTER JOIN AUTH_USER ON (SOCIAL_AUTH_USERSOCIALAUTH.USER_ID = AUTH_USER.ID)  LEFT OUTER JOIN LXPAPP_LEARNERDETAILS ON (AUTH_USER.ID = LXPAPP_LEARNERDETAILS.LEARNER_ID) ORDER BY  AUTH_USER.FIRST_NAME,  AUTH_USER.LAST_NAME'.lower())
    # users = UserSocialAuth.objects.select_related('user') \
    # .prefetch_related('user__learnerdetails') \
    # .filter(user__is_superuser=False) \
    # .values(
    #     'id',
    #     'user_id',
    #     'user__first_name',
    #     'user__last_name',
    #     'user__learnerdetails__mobile'
    # ).order_by('user__first_name', 'user__last_name')
    return users


@login_required
def getUserTableWithAdmin(request):
    users = UserSocialAuth.objects.raw('SELECT   SOCIAL_AUTH_USERSOCIALAUTH.ID,  SOCIAL_AUTH_USERSOCIALAUTH.USER_ID,  AUTH_USER.FIRST_NAME,  AUTH_USER.LAST_NAME,  LXPAPP_LEARNERDETAILS.MOBILE FROM  SOCIAL_AUTH_USERSOCIALAUTH  LEFT OUTER JOIN AUTH_USER ON (SOCIAL_AUTH_USERSOCIALAUTH.USER_ID = AUTH_USER.ID)  LEFT OUTER JOIN LXPAPP_LEARNERDETAILS ON (AUTH_USER.ID = LXPAPP_LEARNERDETAILS.LEARNER_ID) ORDER BY  AUTH_USER.FIRST_NAME,  AUTH_USER.LAST_NAME')
    return users
@login_required
def admin_view_user_list_view(request):
    # try:    
        if str(request.session['utype']) == 'admin':
            users = getUserTable(request)
            return render(request,'lxpapp/users/admin_view_user_list.html',{'users':users})
    # except:
        return render(request,'lxpapp/404page.html')

    
@login_required
def admin_view_user_grid_view(request):
    try:    
        if str(request.session['utype']) == 'admin':
            users = getUserTable(request)
            return render(request,'lxpapp/users/admin_view_user_grid.html',{'users':users})
    except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def admin_view_user_log_details_view(request,user_id):
    try:    
        if str(request.session['utype']) == 'admin':
            users = models.UserLog.objects.all().filter(user_id = user_id)
            return render(request,'lxpapp/users/admin_view_user_log_details.html',{'users':users})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def admin_view_user_activity_details_view(request,user_id):
    #try:    
        if str(request.session['utype']) == 'admin':
            users = models.UserActivity.objects.all().filter(user_id = user_id)
            return render(request,'lxpapp/users/admin_view_user_activity_details.html',{'users':users})
    #except:
        return render(request,'lxpapp/404page.html')

@login_required
def update_user_view(request,userfirstname,userlastname,userid,pk):
    try:    
        if str(request.session['utype']) == 'admin':
            if request.method == 'POST':
                course = request.POST.getlist('courses[]')
                active = request.POST.get('active')
                usertype = request.POST.getlist('utype[]')
                users = UserSocialAuth.objects.get(id=pk)
                if active:
                    users.status = True
                else:
                    users.status = False
                users.utype = usertype[0]
                users.save()
                users = getUserTable(request)
                return HttpResponseRedirect('/admin-view-user-list',{'users':users})
            learnercourses = ''
            users = UserSocialAuth.objects.all().filter(id=pk)
            userdetails = models.LearnerDetails.objects.all().filter(learner_id=userid)
            username = userfirstname + ' ' + userlastname
            return render(request,'lxpapp/users/admin_update_user.html',{'users':users,'learnercourses':learnercourses,'username':username,'userdetails':userdetails})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def active_user_view(request,userid,pk):
    try:    
        if str(request.session['utype']) == 'admin':
            cursor = connection.cursor()
            cursor.execute("UPDATE social_auth_usersocialauth SET status = 1, utype = CASE WHEN utype = 0 THEN 2 ELSE utype END WHERE id = " + str(pk))
            users = models.User.objects.raw("SELECT * FROM social_auth_usersocialauth where user_id = " + str(pk))
            isfirstlogin =models.IsFirstLogIn.objects.all().filter(user_id = userid)
            if not isfirstlogin:
                isfirstlogin =models.IsFirstLogIn.objects.create(user_id = userid)
                isfirstlogin.save()
            return HttpResponseRedirect('/admin-view-user-list',{'users':users})
    except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def admin_user_reset_password_view(request,pk):
    try:    
        if str(request.session['utype']) == 'admin':

            u = request.user
            usertochange = models.User.objects.all().filter(id = pk)
            usertochange.set_password('Nubeera@123')
            usertochange.save() # Add this line
            update_session_auth_hash(request, u)
            users = getUserTable(request)
            return HttpResponseRedirect('/admin-view-user-list',{'users':users})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def inactive_user_view(request,pk):
    try:    
        if str(request.session['utype']) == 'admin':
            cursor = connection.cursor()
            cursor.execute("UPDATE social_auth_usersocialauth SET status = 0 WHERE id = " + str(pk))
            users = models.User.objects.raw("SELECT * FROM social_auth_usersocialauth where user_id = " + str(request.user.id))
            return HttpResponseRedirect('/admin-view-user-list',{'users':users})
    except:
        return render(request,'lxpapp/404page.html')

@login_required
def delete_user_view(request,userid,pk):
    try:    
        if str(request.session['utype']) == 'admin':
            # cursor = connection.cursor()
            # cursor.execute("DELETE FROM lxpapp_BatchTrainer WHERE trainer_id = " + str(pk))
            # cursor.execute("DELETE FROM lxpapp_UserPics WHERE user_id = " + str(userid))
            # cursor.execute("DELETE FROM lxpapp_UserCourse WHERE user_id = " + str(userid))
            # cursor.execute("DELETE FROM lxpapp_LearnerDetails WHERE learner_id = " + str(userid))
            # cursor.execute("DELETE FROM lxpapp_IsFirstLogIn WHERE user_id = " + str(userid))
            # cursor.execute("DELETE FROM lxpapp_McqResult WHERE learner_id = " + str(userid))
            # cursor.execute("DELETE FROM lxpapp_ShortResult WHERE learner_id = " + str(userid))
            # cursor.execute("DELETE FROM lxpapp_VideoToUnlock WHERE learner_id = " + str(userid))
            # cursor.execute("DELETE FROM lxpapp_VideoWatched WHERE learner_id = " + str(userid))
            # cursor.execute("DELETE FROM lxpapp_WaringMail WHERE learner_id = " + str(userid))
            # cursor.execute("DELETE FROM lxpapp_K8STerminal WHERE learner_id = " + str(userid))
            # cursor.execute("DELETE FROM lxpapp_K8STerminalLearnerCount WHERE learner_id = " + str(userid))
            # cursor.execute("DELETE FROM social_auth_usersocialauth WHERE id = " + str(pk))
            # cursor.execute("DELETE FROM auth_user WHERE id = " + str(userid))
            users = models.User.objects.raw("SELECT * FROM social_auth_usersocialauth where user_id = " + str(request.user.id))
            return HttpResponseRedirect('/admin-view-user-list',{'users':users})
    except:
        return render(request,'lxpapp/404page.html')
    
@login_required
def user_profile_view(request):
    userdetails = User.objects.prefetch_related(
                        'social_auth',  
                        'userprofile_set'   
                    ).all().filter(id = request.user.id).first()
    
    base_template = 'base.html'  # Default base template
    if userdetails:
        if userdetails.social_auth.first().utype == 1:
            base_template = 'trainer/trainerbase.html'
        elif userdetails.social_auth.first().utype == 3:
            base_template = 'cto/ctobase.html'
        elif userdetails.social_auth.first().utype == 4:
            base_template = 'cfo/cfobase.html'
        elif userdetails.social_auth.first().utype == 5:
            base_template = 'mentor/mentorbase.html'
        elif userdetails.social_auth.first().utype == 6:
            base_template = 'staff/staffbase.html'
    return render(request,'lxpapp/users/user_profile.html',{'userdetails':userdetails,'base_template': base_template})

@login_required
def user_profile_update_view(request):
    if request.method == 'POST':
        userdetails = models.UserProfile.objects.all().filter(user_id = request.user.id).first()
        if not userdetails:
            userdetails = models.UserProfile.objects.create(user_id=request.user.id)
        userdetails.regdate = request.POST['regdate']
        userdetails.contactno = request.POST['contactno']
        userdetails.skills = request.POST['skills']
        userdetails.bio = request.POST['bio']
        userdetails.save()
        profile_img = request.FILES.get('profile_img')
        
        # If a profile picture was uploaded
        if profile_img:
            # Generate the custom file name: username_userid.extension
            file_extension = os.path.splitext(profile_img.name)[1]  # Get the file extension
            new_file_name = f"{userdetails.user.first_name}_{userdetails.user.id}{file_extension}"
            
            # Define the path where the file will be saved
            file_path = userdetails.profile_img.storage.path(new_file_name)
            
            # Check if a file with the same name exists and delete it
            if default_storage.exists(new_file_name):
                default_storage.delete(new_file_name)

            # Save the new profile pic with the new file name
            userdetails.profile_img.save(new_file_name, profile_img)
        userdetails.save
        messages.info(request, 'Record Updated Successfully')
        return HttpResponseRedirect('user-profile')
    userdetails = User.objects.prefetch_related(
                        'social_auth',  
                        'userprofile_set'   
                    ).all().filter(id = request.user.id).first()
    
    base_template = 'base.html'  # Default base template
    if userdetails:
        if userdetails.social_auth.first().utype == 1:
            base_template = 'trainer/trainerbase.html'
        elif userdetails.social_auth.first().utype == 3:
            base_template = 'cto/ctobase.html'
        elif userdetails.social_auth.first().utype == 4:
            base_template = 'cfo/cfobase.html'
        elif userdetails.social_auth.first().utype == 5:
            base_template = 'mentor/mentorbase.html'
        elif userdetails.social_auth.first().utype == 6:
            base_template = 'staff/staffbase.html'
    return render(request,'lxpapp/users/user_profile_update.html',{'userdetails':userdetails,'base_template': base_template})

