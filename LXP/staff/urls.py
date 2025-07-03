from django.urls import path
from staff import views
from django.contrib.auth.views import LoginView

urlpatterns = [

    path('staff-dashboard', views.staff_dashboard_view,name='staff-dashboard'),

    path('staff-add-material', views.staff_add_material_view,name='staff-add-material'),
    path('staff-update-material/<int:pk>', views.staff_update_material_view,name='staff-update-material'),
    path('staff-view-material', views.staff_view_material_view,name='staff-view-material'),
    path('staff-delete-material/<int:pk>', views.staff_delete_material_view,name='staff-delete-material'),
    path('staff-show-material/<materialtype>,/<int:pk>', views.staff_show_material_view,name='staff-show-material'),
    path('staff-upload-material-details-csv', views.staff_upload_material_details_csv_view,name='staff-upload-material-details-csv'),

    path('staff-sessionmaterial', views.staff_sessionmaterial_view,name='staff-sessionmaterial'),
    path('staff-add-sessionmaterial', views.staff_add_sessionmaterial_view,name='staff-add-sessionmaterial'),
    path('staff-update-sessionmaterial/<int:pk>', views.staff_update_sessionmaterial_view,name='staff-update-sessionmaterial'),
    path('staff-view-sessionmaterial', views.staff_view_sessionmaterial_view,name='staff-view-sessionmaterial'),
    path('staff-delete-sessionmaterial/<int:pk>', views.staff_delete_sessionmaterial_view,name='staff-delete-sessionmaterial'),
    path('staff-show-sessionmaterial/<sessionmaterialtype>,/<int:pk>', views.staff_show_sessionmaterial_view,name='staff-show-sessionmaterial'),
    
    path('ajax/load-videos/', views.load_videos, name='ajax_load_videos'),
    
    path('staff-exam', views.staff_exam_view,name='staff-exam'),
    path('staff-add-exam', views.staff_add_exam_view,name='staff-add-exam'),
    path('staff-update-exam/<int:pk>', views.staff_update_exam_view,name='staff-update-exam'),
    path('staff-view-exam', views.staff_view_exam_view,name='staff-view-exam'),
    path('staff-view-filter-exam/<type>', views.staff_view_filter_exam_view,name='staff-view-filter-exam'),
    path('staff-delete-exam/<int:pk>', views.staff_delete_exam_view,name='staff-delete-exam'),
    path('staff-upload-exam-csv', views.staff_upload_exam_csv_view,name='staff-upload-exam-csv'),
     
    path('staff-mcqquestion', views.staff_mcqquestion_view,name='staff-mcqquestion'),
    path('staff-add-mcqquestion', views.staff_add_mcqquestion_view,name='staff-add-mcqquestion'),
    path('staff-update-mcqquestion/<int:pk>', views.staff_update_mcqquestion_view,name='staff-update-mcqquestion'),
    path('staff-view-mcqquestion-exams', views.staff_view_mcqquestion_exams_view,name='staff-view-mcqquestion-exams'),
    path('staff-view-mcqquestion/<int:examid>', views.staff_view_mcqquestion_view,name='staff-view-mcqquestion'),
    path('staff-delete-mcqquestion/<int:pk>', views.staff_delete_mcqquestion_view,name='staff-delete-mcqquestion'),

    path('staff-shortquestion', views.staff_shortquestion_view,name='staff-shortquestion'),
    path('staff-add-shortquestion', views.staff_add_shortquestion_view,name='staff-add-shortquestion'),
    path('staff-update-shortquestion/<int:pk>', views.staff_update_shortquestion_view,name='staff-update-shortquestion'),
    path('staff-view-shortquestion', views.staff_view_shortquestion_view,name='staff-view-shortquestion'),
    path('staff-delete-shortquestion/<int:pk>', views.staff_delete_shortquestion_view,name='staff-delete-shortquestion'),
    
    path('staff-pending-short-exam-reuslt', views.staff_pending_short_exam_result_view,name='staff-pending-short-exam-reuslt'),
    path('staff-update-short-question-result/<int:pk>', views.staff_update_short_question_result_view,name='staff-update-short-question-result'),
    path('staff-save-short-question-result/<int:pk>', views.staff_save_short_question_result_view,name='staff-save-short-question-result'),

    path('staff-ytexamquestion', views.staff_ytexamquestion_view,name='staff-ytexamquestion'),
    path('staff-add-ytexamquestion', views.staff_add_ytexamquestion_view,name='staff-add-ytexamquestion'),
    path('staff-update-ytexamquestion/<int:pk>', views.staff_update_ytexamquestion_view,name='staff-update-ytexamquestion'),
    path('staff-view-ytexamquestion', views.staff_view_ytexamquestion_view,name='staff-view-ytexamquestion'),
    path('staff-delete-ytexamquestion/<int:pk>', views.staff_delete_ytexamquestion_view,name='staff-delete-ytexamquestion'),

    path('staff-view-learner-video', views.staff_view_learner_video_view,name='staff-view-learner-video'),
    path('staff-learner-video-course/<int:user_id>/<userfirstname>/<userlastname>', views.staff_learner_video_Course_view,name='staff-learner-video-course'),
    path('staff-learner-video-course-subject/<int:user_id>/<userfirstname>/<userlastname>', views.staff_learner_video_Course_subject_view,name='staff-learner-video-course-subject'),
    path('staff-learner-video-list/<int:subject_id>,/<int:user_id>', views.staff_learner_video_list_view,name='staff-learner-video-list'),
    path('staff-learner-show-video/<int:subject_id>,/<int:video_id>', views.staff_learner_show_video_view,name='staff-learner-show-video'),
    path('staff-learner-approve-video/<int:pk>/<int:studid>', views.staff_learner_approve_video,name='staff-learner-approve-video'),
    path('staff-learner-approveall-video/<int:userid>/<subject_id>', views.staff_learner_approveall_video,name='staff-learner-approveall-video'),

    path('staff-add-chapterquestion', views.staff_add_chapterquestion_view,name='staff-add-chapterquestion'),
    path('staff-update-chapterquestion/<int:pk>', views.staff_update_chapterquestion_view,name='staff-update-chapterquestion'),
    path('staff-view-chapterquestion', views.staff_view_chapterquestion_view,name='staff-view-chapterquestion'),
    path('staff-view-chapterquestion-chapter/<int:chapter_id>', views.staff_view_chapterquestion_chapter_view,name='staff-view-chapterquestion-chapter'),
    path('staff-delete-chapterquestion/<int:pk>', views.staff_delete_chapterquestion_view,name='staff-delete-chapterquestion'),


    path('staff-k8sterminal', views.staff_k8sterminal_view,name='staff-k8sterminal'),
    path('staff-add-k8sterminal', views.staff_add_k8sterminal_view,name='staff-add-k8sterminal'),
    path('staff-update-k8sterminal/<int:pk>', views.staff_update_k8sterminal_view,name='staff-update-k8sterminal'),
    path('staff-view-k8sterminal', views.staff_view_k8sterminal_view,name='staff-view-k8sterminal'),
    path('staff-delete-k8sterminal/<int:pk>', views.staff_delete_k8sterminal_view,name='staff-delete-k8sterminal'),
    
    path('staff-pyton-terminal', views.staff_python_terminal_view,name='staff-pyton-terminal'),
    path('staff-linux-terminal', views.staff_linux_terminal_view,name='staff-linux-terminal'),
    path('staff-cloudshell-terminal', views.staff_cloudshell_terminal_view,name='staff-cloudshell-terminal'),

    path('staff-add-activity', views.staff_add_activity_view,name='staff-add-activity'),
    path('staff-update-activity/<int:pk>', views.staff_update_activity_view,name='staff-update-activity'),
    path('staff-view-activity', views.staff_view_activity_view,name='staff-view-activity'),
    path('staff-delete-activity/<int:pk>', views.staff_delete_activity_view,name='staff-delete-activity'),
    path('staff-show-activity/<int:pk>', views.staff_show_activity_view,name='staff-show-activity'),
    path('staff-upload-activity-details-csv', views.staff_upload_activity_details_csv_view,name='staff-upload-activity-details-csv'),
      
]





