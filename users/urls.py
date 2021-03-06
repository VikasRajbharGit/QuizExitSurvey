"""Quizzes_Surveys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import RegisterStudentView, RegisterTeacherView, StudentQuizListView, LoginView, TeacherSubjectListView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/student/', view=RegisterStudentView.as_view(), name='register-student'),
    path('register/teacher/', view=RegisterTeacherView.as_view(), name='register-teacher'),
    path('login/', view=LoginView.as_view(), name='login'),
    path('logout/', view=auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('student/<int:pk>/home/', view=StudentQuizListView.as_view(), name='student-home'),
    path('teacher/<int:pk>/home/', view=TeacherSubjectListView.as_view(), name='teacher-home')
]
