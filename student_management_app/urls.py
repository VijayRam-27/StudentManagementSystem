from django.urls import path
from . import views, HodView, StudentView, StaffView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.show_login, name=''),
    path('show_login', views.show_login, name='show_login'),
    path('do_login', views.do_login, name='do_login'),
    path('do_logout', views.do_logout, name='do_logout'),
    path('admin_home', HodView.admin_home, name='admin_home'),
    path('add_staff', HodView.add_staff, name='add_staff'),
    path('add_staff_save', HodView.add_staff_save, name='add_staff_save'),
    path('add_course', HodView.add_course, name='add_course'),
    path('add_course_save', HodView.add_course_save, name='add_course_save'),
    path('add_student', HodView.add_student, name='add_student'),
    path('add_student_save', HodView.add_student_save, name='add_student_save'),
    path('add_subject', HodView.add_subject, name='add_subject'),
    path('add_subject_save', HodView.add_subject_save, name='add_subject_save'),
    path('manage_staff', HodView.manage_staff, name='manage_staff'),
    path('manage_student', HodView.manage_student, name='manage_student'),
    path('manage_course', HodView.manage_course, name='manage_course'),
    path('manage_subject', HodView.manage_subject, name='manage_subject'),
    path('edit_student/<str:id>', HodView.edit_student, name='edit_student'),
    path('edit_staff/<str:id>', HodView.edit_staff, name='edit_staff'),
    path('edit_staff_save', HodView.edit_staff_save, name='edit_staff_save'),
    path('edit_student_save', HodView.edit_student_save, name='edit_student_save'),
    path('edit_course/<str:id>', HodView.edit_course, name='edit_course'),
    path('edit_course_save', HodView.edit_course_save, name='edit_course_save'),
    path('edit_subject/<int:id>', HodView.edit_subject, name='edit_subject'),
    path('edit_subject_save', HodView.edit_subject_save, name='edit_subject_save'),
    path('manage_session', HodView.manage_session, name='manage_session'),
    path('add_manage_session', HodView.add_manage_session, name='add_manage_session'),
    #Staff, Student Url
    path('staff_home_view', StaffView.staff_home_view, name='staff_home_view'),
    path('student_home_view', StudentView.student_home_view, name='student_home_view'),
    path('staff_take_attendance', StaffView.staff_take_attendance, name='staff_take_attendance'),
    path('get_student', StaffView.get_student, name='get_student'),
    path('save_student_attendance', StaffView.save_student_attendance, name='save_student_attendance'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)