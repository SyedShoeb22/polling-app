from django.urls import path
from trainer import views
from django.contrib.auth.views import LoginView
from polls import views as poll_views


urlpatterns = [

    path('trainer-dashboard', views.trainer_dashboard_view,name='trainer-dashboard'),
    
    path("polls/save/", poll_views.save_selected_polls, name="save_selected_polls"),
    path("polls/generate/", poll_views.trainer_generate_polls, name="trainer-generate-polls"),
    
    path('trainer-view-material', views.trainer_view_material_view,name='trainer-view-material'),
    path('trainer-show-material/<materialtype>,/<int:pk>', views.trainer_show_material_view,name='trainer-show-material'),

    path('trainer-view-sessionmaterial', views.trainer_view_sessionmaterial_view,name='trainer-view-sessionmaterial'),
    path('trainer-show-sessionmaterial/<sessionmaterialtype>,/<int:pk>', views.trainer_show_sessionmaterial_view,name='trainer-show-sessionmaterial'),
    
    path('ajax/load-videos/', views.load_videos, name='ajax_load_videos'),
    
    path('trainer-create-poll', views.trainer_create_poll, name='trainer-create-poll'),
    path('trainer-view-polls', views.trainer_view_poll, name='trainer-view-polls'),
    path('trainer-delete-polls/<int:poll_id>', views.trainer_delete_poll, name='trainer-delete-polls'),
    path('trainer-edit-polls/<int:poll_id>', views.trainer_edit_poll, name='trainer-edit-polls'),

    path('trainer-exam', views.trainer_exam_view,name='trainer-exam'),
    path('trainer-add-exam', views.trainer_add_exam_view,name='trainer-add-exam'),
    path('trainer-update-exam/<int:pk>', views.trainer_update_exam_view,name='trainer-update-exam'),
    path('trainer-view-exam', views.trainer_view_exam_view,name='trainer-view-exam'),
    path('trainer-view-filter-exam/<type>', views.trainer_view_filter_exam_view,name='trainer-view-filter-exam'),
    path('trainer-delete-exam/<int:pk>', views.trainer_delete_exam_view,name='trainer-delete-exam'),
    path('trainer-upload-exam-csv', views.trainer_upload_exam_csv_view,name='trainer-upload-exam-csv'),
     
    path('trainer-mcqquestion', views.trainer_mcqquestion_view,name='trainer-mcqquestion'),
    path('trainer-view-mcqquestion-exams', views.trainer_view_mcqquestion_exams_view,name='trainer-view-mcqquestion-exams'),
    path('trainer-view-mcqquestion/<int:examid>', views.trainer_view_mcqquestion_view,name='trainer-view-mcqquestion'),

    path('trainer-shortquestion', views.trainer_shortquestion_view,name='trainer-shortquestion'),
    path('trainer-view-shortquestion', views.trainer_view_shortquestion_view,name='trainer-view-shortquestion'),
    
    path('trainer-pending-short-exam-reuslt', views.trainer_pending_short_exam_result_view,name='trainer-pending-short-exam-reuslt'),
    path('trainer-update-short-question-result/<int:pk>', views.trainer_update_short_question_result_view,name='trainer-update-short-question-result'),
    path('trainer-save-short-question-result/<int:pk>', views.trainer_save_short_question_result_view,name='trainer-save-short-question-result'),

    path('trainer-ytexamquestion', views.trainer_ytexamquestion_view,name='trainer-ytexamquestion'),
    path('trainer-view-ytexamquestion', views.trainer_view_ytexamquestion_view,name='trainer-view-ytexamquestion'),

    path('trainer-view-learner-video', views.trainer_view_learner_video_view,name='trainer-view-learner-video'),
    path('trainer-learner-video-course/<int:user_id>/<userfirstname>/<userlastname>', views.trainer_learner_video_Course_view,name='trainer-learner-video-course'),
    path('trainer-learner-video-course-subject/<int:user_id>/<userfirstname>/<userlastname>', views.trainer_learner_video_Course_subject_view,name='trainer-learner-video-course-subject'),
    path('trainer-learner-video-list/<int:subject_id>,/<int:user_id>', views.trainer_learner_video_list_view,name='trainer-learner-video-list'),
    path('trainer-learner-show-video/<int:subject_id>,/<int:video_id>', views.trainer_learner_show_video_view,name='trainer-learner-show-video'),
    path('trainer-learner-approve-video/<int:pk>/<int:studid>', views.trainer_learner_approve_video,name='trainer-learner-approve-video'),
    path('trainer-learner-approveall-video/<int:userid>/<subject_id>', views.trainer_learner_approveall_video,name='trainer-learner-approveall-video'),

    path('trainer-view-chapterquestion', views.trainer_view_chapterquestion_view,name='trainer-view-chapterquestion'),
    path('trainer-view-chapterquestion-chapter/<int:chapter_id>', views.trainer_view_chapterquestion_chapter_view,name='trainer-view-chapterquestion-chapter'),

    path('trainer-k8sterminal', views.trainer_k8sterminal_view,name='trainer-k8sterminal'),
    path('trainer-add-k8sterminal', views.trainer_add_k8sterminal_view,name='trainer-add-k8sterminal'),
    path('trainer-update-k8sterminal/<int:pk>', views.trainer_update_k8sterminal_view,name='trainer-update-k8sterminal'),
    path('trainer-view-k8sterminal', views.trainer_view_k8sterminal_view,name='trainer-view-k8sterminal'),
    path('trainer-delete-k8sterminal/<int:pk>', views.trainer_delete_k8sterminal_view,name='trainer-delete-k8sterminal'),
    
    path('trainer-pyton-terminal', views.trainer_python_terminal_view,name='trainer-pyton-terminal'),
    path('trainer-linux-terminal', views.trainer_linux_terminal_view,name='trainer-linux-terminal'),
    path('trainer-cloudshell-terminal', views.trainer_cloudshell_terminal_view,name='trainer-cloudshell-terminal'),
    
    path('trainer-schedulerstatus-list/', views.trainer_schedulerstatus_list, name='trainer-schedulerstatus-list'),
    path('trainer-schedulerstatus-create/', views.schedulerstatus_create, name='trainer-schedulerstatus-create'),
    path('trainer-schedulerstatus-delete/<int:id>/', views.schedulerstatus_delete, name='trainer-schedulerstatus-delete'),
    path('get-scheduler-status-sum/', views.get_scheduler_status_sum, name='get-scheduler-status-sum'),
    path('trainer-schedulerstatus-mark-done/', views.trainer_schedulerstatus_mark_done, name='trainer-schedulerstatus-mark-done'),
    path('trainer-scheduler-calender/', views.trainer_scheduler_calender, name='trainer-scheduler-calender'),

    path('trainer-activity-learner-list/', views.trainer_activity_learner_list, name='trainer-activity-learner-list'),
    path('trainer-activity-learner-batch-list/<int:learner_id>/', views.trainer_activity_learner_batch_list, name='trainer-activity-learner-batch-list'),
    path('trainer-activity-learner-batch-activity/<int:activity_id>/', views.trainer_activity_learner_batch_activity, name='trainer-activity-learner-batch-activity'),
    path('trainer-activity-learner-batch-activity-update/', views.trainer_activity_learner_batch_activity_update, name='trainer-activity-learner-batch-activity-update'),


    path('trainer-wheel/', views.trainer_wheel, name='trainer-wheel'),

]
