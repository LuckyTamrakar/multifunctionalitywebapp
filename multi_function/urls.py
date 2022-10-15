from django.contrib import admin
from django.urls import path
from multi_function import views


urlpatterns = [
    path('', views.home),
    path('register/', views.UserRegistration.as_view()),
    path('login/', views.UserLogin.as_view()),
    path('user/', views.UserProfile.as_view()),
    path('changePassword/', views.ChangePassword.as_view()),
    path('send-reset-password-link/', views.SendPasswordResetMail.as_view()),
    path('reset-password/<uid>/<token>', views.UserPasswordReset.as_view()),
    path('contact/', views.ContactView.as_view()),
    path('quiz/', views.Quiz.as_view()),
    path('r/<str:topic>/',views.RandomQuestion.as_view()),
    path('q/<str:topic>/',views.QuizQuestion.as_view()),
    path('doctor-available/', views.DoctorView.as_view()),
    path('patients-available/<str:email>', views.PatientView.as_view()),
    path('patients-past/<str:email>', views.PastPatientDetail.as_view()),
    path('patients-appointment/', views.PatientAppointment.as_view()),
]
