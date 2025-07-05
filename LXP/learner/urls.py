from django.urls import path
from learner import views
from polls.views import poll_detail
from django.contrib import admin  # ✅ This line fixes the NameError
from django.urls import path, include

urlpatterns = [
    path('learner-dashboard', views.learner_dashboard_view,name='learner-dashboard'),
    path('learner-edit-Learner-details/<int:user_id>', views.learner_edit_Learner_details_view,name='learner-edit-Learner-details'),
    path('api/learner/<int:user_id>/edit/', views.learner_edit_Learner_details_api, name='learner-edit-Learner-details-api'),
    path('learner-exam', views.learner_exam_view,name='learner-exam'),
    path('learner-take-exam/<int:pk>', views.learner_take_exam_view,name='learner-take-exam'),
    path('learner-start-exam/<int:pk>', views.learner_start_exam_view,name='learner-start-exam'),
    path('learner-show-exam-reuslt/<int:pk>', views.learner_show_exam_reuslt_view,name='learner-show-exam-reuslt'),
    path('learner-show-exam-reuslt-details/<int:pk>', views.learner_show_exam_reuslt_details_view,name='learner-show-exam-reuslt-details'),
    path('poll/<int:poll_id>/', poll_detail, name='poll_detail'),
    path('admin/', admin.site.urls),
    path('trainer/polls/', include('polls.urls')),   

    path('learner-short-exam', views.learner_short_exam_view,name='learner-short-exam'),
    path('learner-take-short-exam/<int:pk>', views.learner_take_short_exam_view,name='learner-take-short-exam'),
    path('learner-start-short-exam/<int:pk>', views.learner_start_short_exam_view,name='learner-start-short-exam'),
    path('learner-show-short-exam-reuslt/<int:pk>', views.learner_show_short_exam_reuslt_view,name='learner-show-short-exam-reuslt'),
    path('learner-show-short-exam-reuslt-details/<int:pk>', views.learner_show_short_exam_reuslt_details_view,name='learner-show-short-exam-reuslt-details'),
    path('learner-video-course', views.learner_video_Course_view,name='learner-video-course'),
    path('learner-video-course-subject', views.learner_video_Course_subject_view,name='learner-video-course-subject'),
    path('learner-video-list/<int:subject_id>', views.learner_video_list_view,name='learner-video-list'),
    path('learner-show-video/<int:subject_id>,/<int:video_id>', views.learner_show_video_view,name='learner-show-video'),
    path('learner-video-sesseionmaterial-list/<subject_id>/<video_id>', views.learner_video_sesseionmaterial_list_view,name='learner-video-sesseionmaterial-list'),
    path('learner-see-sesseionmaterial/<subject_id>/<video_id>/<int:pk>', views.learner_see_sesseionmaterial_view,name='learner-see-sesseionmaterial'),
    path('learner-video-watched-saved-view', views.learner_video_watched_saved_view, name='learner-video-watched-saved-view'),
    
    path('learner-video-activity-list/<playlist_id>/<video_id>', views.learner_video_activity_list_view,name='learner-video-activity-list'),
    path('learner-see-activity/<subject_id>/<video_id>/<int:pk>', views.learner_see_activity_view,name='learner-see-activity'),
    path('learner-upload-activity/<int:activity_id>/<int:course_id>/<int:chapter_id>', views.learner_upload_activity_view,name='learner-upload-activity'),
    
    
    path('learner-studymaterial-course', views.learner_studymaterial_course_view,name='learner-studymaterial-course'),
    path('learner-studymaterial-course-chapter/<int:course_id>', views.learner_studymaterial_course_chapter_view,name='learner-studymaterial-course-chapter'),
    path('learner-studymaterial-chapter-show/<int:chapter_id>/<int:course_id>', views.learner_studymaterial_chapter_show_view,name='learner-studymaterial-chapter-show'),
    path('learner-studymaterial-show/<studymaterialtype>/<int:pk>', views.learner_show_studymaterial_view,name='learner-studymaterial-show'),
    path('ajax/save-topic/', views.save_topic, name='ajax_save_topic'),

    path('learner-available-course', views.learner_availablecourse_course_view,name='learner-available-course'),
    path('learner-available-course-chapter/<coursename>/<int:course_id>', views.learner_availablecourse_course_chapter_view,name='learner-available-course-chapter'),
    
    path('learner-chapterexam/<int:chapter_id>/<int:course_id>', views.learner_chapterexam_view,name='learner-chapterexam'),
    path('learner-take-chapterexam/<int:chapter_id>/<int:course_id>', views.learner_take_chapterexam_view,name='learner-take-chapterexam'),
    path('learner-start-chapterexam/<int:chapter_id>/<int:course_id>', views.learner_start_chapterexam_view,name='learner-start-chapterexam'),
    path('learner-show-chapterexam-reuslt/<int:chapter_id>/<int:course_id>', views.learner_show_chapterexam_reuslt_view,name='learner-show-chapterexam-reuslt'),
    path('learner-show-chapterexam-reuslt-details/<int:result_id>/<int:attempt>/<int:chapter_id>/<int:course_id>', views.learner_show_chapterexam_reuslt_details_view,name='learner-show-chapterexam-reuslt-details'),

    path('learner-check-k8sterminal', views.learner_check_k8sterminal_view,name='learner-check-k8sterminal'),
    path('learner-pyton-terminal', views.learner_python_terminal_view,name='learner-pyton-terminal'),
    path('learner-linux-terminal', views.learner_linux_terminal_view,name='learner-linux-terminal'),
    path('learner-cloudshell-terminal', views.learner_cloudshell_terminal_view,name='learner-cloudshell-terminal'),

    path('ajax/save-cart/', views.save_cart, name='ajax_save_cart'),

    path('learner-vote-polls/<int:poll_id>/', views.learner_poll_vote, name='learner-poll-vote'),  
    path('learner-vote-polls/', views.learner_polls_list, name='learner-polls-list'),


]
#<a href="{% url 'learner-studymaterial-subject-chapter' coursename t.subject_name t.id courseset_id %}">Preview</a>