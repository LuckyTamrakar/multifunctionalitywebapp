import email
from multiprocessing import context
from pyclbr import Class
from django.shortcuts import render
from django.urls import is_valid_path
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from .models import MyUser, PastPatient, Quizzes,Question,Patients,Doctor1
from .serializers import PastPatientDetailSerial, PatientPastDetailSerial, PatientPastSerialView, UserRegisterationSerial, UserLoginSerial, UserProfileSerial, ChangePasswordSeial, SendPasswordResetMailSerial,UserPasswordResetSerial, ContactSerial,QuestionSerial,RandomQuestionSerial,QuizSerial,PatientAppointmentSerial,DoctorSerial,PatientSerialView, VerifyEmailOtp
from rest_framework.generics import ListAPIView
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from.utils import Util
from django.http import HttpResponse
import random


# Create your views here.
'''class UserList(ListAPIView):
    queryset=Users.objects.all()
    serializer_class=UserSerializers'''
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

        
class UserRegistration(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=UserRegisterationSerial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({'token':token, 'msg':'Registration Success'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class ContactView(APIView):
    def post(self,request,format=None):
        serializer=ContactSerial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            contact=serializer.save()
            return Response({'msg':"Contact Saved, Our Team contact you very shortly"}, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class UserLogin(APIView):
    def post(self,request,format=None):
        serializer=UserLoginSerial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password = serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                body='Account Login Successfully, Team MFW'
                data={'subject':'Account Login successfully, Team MFW','body':body,'to_email':email}
                Util.sendEmail(data)
                return Response({'token':token,'msg':'Login Success'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'Non_field_errors' : ['Email or Password is not valid or your account is not verify']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserProfile(APIView):
    #renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        serializer=UserProfileSerial(request.user)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChangePassword(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer=ChangePasswordSeial(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            
            return Response({'msg':'Change Password Success'}, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class SendPasswordResetMail(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=SendPasswordResetMailSerial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset Link is Sent Successful in your mail'}, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserPasswordReset(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,uid,token,format=None):
        serializer=UserPasswordResetSerial(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset Successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Quiz(ListAPIView):
        serializer_class=QuizSerial
        queryset=Quizzes.objects.all()
class RandomQuestion(APIView):
    def get(self,request,format=None,**kwargs):
        question=Question.objects.filter(quiz__title=kwargs['topic']).order_by('?')[:1]
        serializer=RandomQuestionSerial(question,many=True)
        return Response(serializer.data)
class QuizQuestion(APIView):
    def get(self,request,format=None,**kwargs):
        question=Question.objects.filter(quiz__title=kwargs['topic'])
        serializer=QuestionSerial(question,many=True)
        return Response(serializer.data)

class DoctorView(APIView):
    
    def get(self,request,format=None):
        datas=Doctor1.objects.all()
        serializer=DoctorSerial(datas,many=True)
        return Response(serializer.datas, status=status.HTTP_200_OK)

class PatientView(APIView):
    def get(self,request,format=None,**kwargs):
        data=Patients.objects.filter(email=kwargs['email'])
        serializer=PatientSerialView(data,many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    def delete(self,request,email,format=None,**kwargs):
        
        data=Patients.objects.get(email=email)
       
        data.delete()
        return Response({'msg':'Successfully Deleted'},status=status.HTTP_200_OK)
    def post(self,request,email,*args,**kwargs):
        task=Patients.objects.get(email=email)
        
        time=random.randint(8,20)
        serializer=PatientSerialView(instance=task,data=request.data)
        serializer1=PatientPastSerialView(instance=task,data=request.data)
        if serializer.is_valid(raise_exception=True) and serializer1.is_valid(raise_exception=True):
            date=serializer.validated_data.get('date')
            name=serializer.validated_data.get('name')
            desc=serializer.validated_data.get('desc')
            serializer1.save()
            
            if time<=11:
                body=f'Your Appointment is done for the {date} at {time}am for the {desc},  Regards team MFW.'
                datas={'subject':f'Appointment is successful for the patient','body':body,'to_email':email}
                Util.sendEmail(datas)
            else:
                body=f'Your Appointment is done for the {date} at {time}pm for the {desc}, Regards team MFW.'
                datas={'subject':f'Appointment is successful for the patient {name}','body':body,'to_email':email}
                Util.sendEmail(datas)
            
            serializer.save()
            
            
           
            return Response(serializer.data)
class PatientAppointment(APIView):
    def post(self,request,format=None):
        serializer=PatientAppointmentSerial(data=request.data)
        serializer1=PatientPastDetailSerial(data=request.data)
        if serializer.is_valid(raise_exception=True) and serializer1.is_valid(raise_exception=True):
            serializer.save()
            serializer1.save()
            return Response({'msg':"Appointment Successfully, Please check your mail, if any query please contact us"}, status=status.HTTP_200_OK)
       
        
            
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

def home(request):
    # request is handled using HttpResponse object
    return HttpResponse("<h1>Hello</h1>")

class PastPatientDetail(APIView):
    def get(self,request,format=None,**kwargs):
        
        data=PastPatient.objects.filter(email=kwargs['email'])
        serializer=PastPatientDetailSerial(data,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class VerifyOtpView(APIView):
    def post(self,request,format=None):
        serializerl=VerifyEmailOtp(data=request.data)
        
        if serializerl.is_valid(raise_exception=True):
            email=serializerl.data.get('email')
            otp=serializerl.data.get('otp')
           
            if MyUser.objects.filter(email=email).exists():
                user=MyUser.objects.get(email=email)
                u_otp=user.otp
                
                if int(u_otp)==int(otp):
                    user.is_active=True
                    body='Account has been activated Successfully Team MFW'
                    data={'subject':f'Account activation successfully via MFW','body':body,'to_email':email}
                    Util.sendEmail(data)
                    user.save()
                   
                    return Response({'msg':"Hello"})
                else:
                    return Response("Invalid Otp",status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Email not exists",status=status.HTTP_400_BAD_REQUEST)
        return Response(serializerl.errors,status=status.HTTP_400_BAD_REQUEST)