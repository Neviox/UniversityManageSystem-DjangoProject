from django.urls import path
from django.contrib import admin
from django.urls import include, path
from SustavZaUpisStudenata import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'project'
urlpatterns = [
    path('',views.home),
    path('admin/', admin.site.urls),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('students/', views.students_page, name='students'),
    path('student_delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('student_view/<int:student_id>/', views.view_student, name='view_student'),
    path('subjects/', views.subjects_page, name='subjects'),
    path('subject_create/', views.create_subject, name='create_subjects'),
    path('subject_edit/<int:subject_id>/', views.edit_subject, name='edit_subject'),
    path('subject_delete/<int:subject_id>/', views.delete_subject, name='delete_subject'),
    path('subject_view/<int:subject_id>/', views.view_subject, name='view_subject'),
    path('enroll_subject/', views.enroll_subject, name='enroll_subject'),
    path('disenroll_subject/', views.disenroll_subject, name='disenroll_subject'),
    path('student_list/<int:subject_id>',views.student_list,name='student list'),
    path('mark_subject_as_passed/', views.mark_subject_as_passed, name='mark_subject_as_passed'),    
    path('mark_subject_as_not_passed/', views.mark_subject_as_not_passed, name='mark_subject_as_not_passed'),
    path('mark_subject_as_lost/', views.mark_subject_as_lost, name='mark_subject_as_lost'),
    path('filterlist/izgubilipotpis/<int:subject_id>/',views.lost_signature,name='izgubilipotpis'),
    path('filterlist/upisani/<int:subject_id>/',views.enrolled,name='upisani'),
    path('filterlist/polozeni/<int:subject_id>/',views.passed,name='polozeni'),
    path('student_create/', views.create_student, name='create_student'),
    path('profesors/', views.profesor_page, name='profesors'),
    path('user_edit/<int:user_id>/', views.edit_user, name='edit_user'),
    
    
    
]