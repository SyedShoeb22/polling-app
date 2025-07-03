from django.urls import path
from mentor import views
from django.contrib.auth.views import LoginView

urlpatterns = [

    path('mentor-dashboard', views.mentor_dashboard_view,name='mentor-dashboard'),

    path('mentor-add-material', views.mentor_add_material_view,name='mentor-add-material'),
    path('mentor-update-material/<int:pk>', views.mentor_update_material_view,name='mentor-update-material'),
    path('mentor-view-material', views.mentor_view_material_view,name='mentor-view-material'),
    path('mentor-delete-material/<int:pk>', views.mentor_delete_material_view,name='mentor-delete-material'),
    path('mentor-show-material/<materialtype>,/<int:pk>', views.mentor_show_material_view,name='mentor-show-material'),
    path('mentor-upload-material-details-csv', views.mentor_upload_material_details_csv_view,name='mentor-upload-material-details-csv'),

    path('mentor-sessionmaterial', views.mentor_sessionmaterial_view,name='mentor-sessionmaterial'),
    path('mentor-add-sessionmaterial', views.mentor_add_sessionmaterial_view,name='mentor-add-sessionmaterial'),
    path('mentor-update-sessionmaterial/<int:pk>', views.mentor_update_sessionmaterial_view,name='mentor-update-sessionmaterial'),
    path('mentor-view-sessionmaterial', views.mentor_view_sessionmaterial_view,name='mentor-view-sessionmaterial'),
    path('mentor-delete-sessionmaterial/<int:pk>', views.mentor_delete_sessionmaterial_view,name='mentor-delete-sessionmaterial'),
    path('mentor-show-sessionmaterial/<sessionmaterialtype>,/<int:pk>', views.mentor_show_sessionmaterial_view,name='mentor-show-sessionmaterial'),
    
    path('ajax/load-videos/', views.load_videos, name='ajax_load_videos'),
    
    path('mentor-exam', views.mentor_exam_view,name='mentor-exam'),
    path('mentor-add-exam', views.mentor_add_exam_view,name='mentor-add-exam'),
    path('mentor-update-exam/<int:pk>', views.mentor_update_exam_view,name='mentor-update-exam'),
    path('mentor-view-exam', views.mentor_view_exam_view,name='mentor-view-exam'),
    path('mentor-view-filter-exam/<type>', views.mentor_view_filter_exam_view,name='mentor-view-filter-exam'),
    path('mentor-delete-exam/<int:pk>', views.mentor_delete_exam_view,name='mentor-delete-exam'),
    path('mentor-upload-exam-csv', views.mentor_upload_exam_csv_view,name='mentor-upload-exam-csv'),
     
    path('mentor-mcqquestion', views.mentor_mcqquestion_view,name='mentor-mcqquestion'),
    path('mentor-add-mcqquestion', views.mentor_add_mcqquestion_view,name='mentor-add-mcqquestion'),
    path('mentor-update-mcqquestion/<int:pk>', views.mentor_update_mcqquestion_view,name='mentor-update-mcqquestion'),
    path('mentor-view-mcqquestion-exams', views.mentor_view_mcqquestion_exams_view,name='mentor-view-mcqquestion-exams'),
    path('mentor-view-mcqquestion/<int:examid>', views.mentor_view_mcqquestion_view,name='mentor-view-mcqquestion'),
    path('mentor-delete-mcqquestion/<int:pk>', views.mentor_delete_mcqquestion_view,name='mentor-delete-mcqquestion'),

    path('mentor-shortquestion', views.mentor_shortquestion_view,name='mentor-shortquestion'),
    path('mentor-add-shortquestion', views.mentor_add_shortquestion_view,name='mentor-add-shortquestion'),
    path('mentor-update-shortquestion/<int:pk>', views.mentor_update_shortquestion_view,name='mentor-update-shortquestion'),
    path('mentor-view-shortquestion', views.mentor_view_shortquestion_view,name='mentor-view-shortquestion'),
    path('mentor-delete-shortquestion/<int:pk>', views.mentor_delete_shortquestion_view,name='mentor-delete-shortquestion'),
    
    path('mentor-pending-short-exam-reuslt', views.mentor_pending_short_exam_result_view,name='mentor-pending-short-exam-reuslt'),
    path('mentor-update-short-question-result/<int:pk>', views.mentor_update_short_question_result_view,name='mentor-update-short-question-result'),
    path('mentor-save-short-question-result/<int:pk>', views.mentor_save_short_question_result_view,name='mentor-save-short-question-result'),

    path('mentor-ytexamquestion', views.mentor_ytexamquestion_view,name='mentor-ytexamquestion'),
    path('mentor-add-ytexamquestion', views.mentor_add_ytexamquestion_view,name='mentor-add-ytexamquestion'),
    path('mentor-update-ytexamquestion/<int:pk>', views.mentor_update_ytexamquestion_view,name='mentor-update-ytexamquestion'),
    path('mentor-view-ytexamquestion', views.mentor_view_ytexamquestion_view,name='mentor-view-ytexamquestion'),
    path('mentor-delete-ytexamquestion/<int:pk>', views.mentor_delete_ytexamquestion_view,name='mentor-delete-ytexamquestion'),

    path('mentor-view-learner-video', views.mentor_view_learner_video_view,name='mentor-view-learner-video'),
    path('mentor-learner-video-course/<int:user_id>/<userfirstname>/<userlastname>', views.mentor_learner_video_Course_view,name='mentor-learner-video-course'),
    path('mentor-learner-video-course-subject/<int:user_id>/<userfirstname>/<userlastname>', views.mentor_learner_video_Course_subject_view,name='mentor-learner-video-course-subject'),
    path('mentor-learner-video-list/<int:subject_id>,/<int:user_id>', views.mentor_learner_video_list_view,name='mentor-learner-video-list'),
    path('mentor-learner-show-video/<int:subject_id>,/<int:video_id>', views.mentor_learner_show_video_view,name='mentor-learner-show-video'),
    path('mentor-learner-approve-video/<int:pk>/<int:studid>', views.mentor_learner_approve_video,name='mentor-learner-approve-video'),
    path('mentor-learner-approveall-video/<int:userid>/<subject_id>', views.mentor_learner_approveall_video,name='mentor-learner-approveall-video'),

    path('mentor-add-chapterquestion', views.mentor_add_chapterquestion_view,name='mentor-add-chapterquestion'),
    path('mentor-update-chapterquestion/<int:pk>', views.mentor_update_chapterquestion_view,name='mentor-update-chapterquestion'),
    path('mentor-view-chapterquestion', views.mentor_view_chapterquestion_view,name='mentor-view-chapterquestion'),
    path('mentor-view-chapterquestion-chapter/<int:chapter_id>', views.mentor_view_chapterquestion_chapter_view,name='mentor-view-chapterquestion-chapter'),
    path('mentor-delete-chapterquestion/<int:pk>', views.mentor_delete_chapterquestion_view,name='mentor-delete-chapterquestion'),


    path('mentor-k8sterminal', views.mentor_k8sterminal_view,name='mentor-k8sterminal'),
    path('mentor-add-k8sterminal', views.mentor_add_k8sterminal_view,name='mentor-add-k8sterminal'),
    path('mentor-update-k8sterminal/<int:pk>', views.mentor_update_k8sterminal_view,name='mentor-update-k8sterminal'),
    path('mentor-view-k8sterminal', views.mentor_view_k8sterminal_view,name='mentor-view-k8sterminal'),
    path('mentor-delete-k8sterminal/<int:pk>', views.mentor_delete_k8sterminal_view,name='mentor-delete-k8sterminal'),
    
    path('mentor-pyton-terminal', views.mentor_python_terminal_view,name='mentor-pyton-terminal'),
    path('mentor-linux-terminal', views.mentor_linux_terminal_view,name='mentor-linux-terminal'),
    path('mentor-cloudshell-terminal', views.mentor_cloudshell_terminal_view,name='mentor-cloudshell-terminal'),
    
    path('mentor-schedulerstatus-list/', views.mentor_schedulerstatus_list, name='mentor-schedulerstatus-list'),
    path('mentor-schedulerstatus-create/', views.schedulerstatus_create, name='mentor-schedulerstatus-create'),
    path('mentor-schedulerstatus-delete/<int:id>/', views.schedulerstatus_delete, name='mentor-schedulerstatus-delete'),
    path('get-scheduler-status-sum/', views.get_scheduler_status_sum, name='get-scheduler-status-sum'),
    path('mentor-schedulerstatus-mark-done/', views.mentor_schedulerstatus_mark_done, name='mentor-schedulerstatus-mark-done'),
    path('mentor-scheduler-calender/', views.mentor_scheduler_calender, name='mentor-scheduler-calender'),
    
    path('mentor-add-activity', views.mentor_add_activity_view,name='mentor-add-activity'),
    path('mentor-update-activity/<int:pk>', views.mentor_update_activity_view,name='mentor-update-activity'),
    path('mentor-view-activity', views.mentor_view_activity_view,name='mentor-view-activity'),
    path('mentor-delete-activity/<int:pk>', views.mentor_delete_activity_view,name='mentor-delete-activity'),
    path('mentor-show-activity/<activitytype>,/<int:pk>', views.mentor_show_activity_view,name='mentor-show-activity'),
    path('mentor-upload-activity-details-csv', views.mentor_upload_activity_details_csv_view,name='mentor-upload-activity-details-csv'),
    

    
]
