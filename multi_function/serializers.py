from ast import Try
from dataclasses import fields
from pyexpat import model
import random
from unittest.util import _MAX_LENGTH
from xml.dom import ValidationErr
from rest_framework import serializers
from .models import MyUser, Contact, PastPatient, Question,Quizzes,Answer,Patients,Doctor1
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util
'''class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id','stuname','email']'''

class UserRegisterationSerial(serializers.ModelSerializer):
    #password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=MyUser
        fields=['email','name','phone','password','tc']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def validate(self,attrs):
        password=attrs.get('password')
        #password2=attrs.get('password2')
        email=attrs.get('email')
        
        phone=attrs.get('phone')
        if len(phone)!=10:
            raise serializers.ValidationError("Mobile number is not valid")
        if len(password) <= 10:
            if not any(char.isdigit() for char in password):
                raise serializers.ValidationError("Password have one digit")
        
    # check for letter
            if not any(char.isalpha() for char in password):
                raise serializers.ValidationError("Password have one alphabet")
            raise serializers.ValidationError("Minimum password have 10 length")
        
       
        
        return attrs
    def create(self,validated_data):
        user = super(UserRegisterationSerial, self).create(validated_data)
        user.set_password(validated_data['password'])

        
        email=user.email
        otp = random.randint(10000,99999)
        user.otp = otp
        body='Account has been created Successfully please verify http://localhost:3000/otp Team MFW'
        data={'subject':f'Account creation successfully via MFW Your Otp is {otp}','body':body,'to_email':email}
        Util.sendEmail(data)
        
        user.save()
        return user
class ContactSerial(serializers.ModelSerializer):
    class Meta:
        model=Contact
        fields=['name','email','phone','address','city','state','desc']

class UserLoginSerial(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=MyUser
        fields=['email','password']
class UserProfileSerial(serializers.ModelSerializer):
    class Meta:
        model=MyUser
        fields=['id','email','name','password','doctordiag']
class ChangePasswordSeial(serializers.Serializer):
    password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True) 
      
    class Meta:
        model=MyUser
        fields=['password','password2']
    def validate(self,attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        user=self.context.get('user') 
        if password!=password2:
            raise serializers.ValidationError("password and Confirm password Does not match")
        user.set_password(password)
        user.save()
        return attrs
class SendPasswordResetMailSerial(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']
    def validate(self, attrs):
        email=attrs.get('email')
        if MyUser.objects.filter(email=email).exists():
            user=MyUser.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)
            link='http://localhost:3000/reset-password/'+uid+'/'+token
            print(link)
            body='Click Following Link to reset Password : '+link
            data={'subject':'Reset Password Link via MFW','body':body,'to_email':user.email}
            Util.sendEmail(data)


            return attrs
        else:
            raise serializers.ValidationError('You are not registered User')

class UserPasswordResetSerial(serializers.Serializer):
    password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True) 
      
    class Meta:
        model=MyUser
        fields=['password','password2']
    def validate(self,attrs):
       try:
        password=attrs.get('password')
        password2=attrs.get('password2')
        uid=self.context.get('uid') 
        token=self.context.get('token') 
        if password!=password2:
            raise serializers.ValidationError("password and Confirm password Does not match")
        id = urlsafe_base64_decode(uid)
        user=MyUser.objects.get(id=id)
        #use_email=MyUser.objects.get(email=email)
        if not PasswordResetTokenGenerator().check_token(user,token):
            raise ValidationErr('Token is not Valid or Expired')
        user.set_password(password)
        user.save()
        
        return attrs
       except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationErr('Token is not Valid or Expired')

class QuizSerial(serializers.ModelSerializer):
    class Meta:
        model=Quizzes
        fields=['title']            
class AnswerSerial(serializers.ModelSerializer):
    class Meta:
        model=Answer
        fields=['id','answer_text','is_right']
class RandomQuestionSerial(serializers.ModelSerializer):
    answer=AnswerSerial(many=True,read_only=True)
    class Meta:
        model=Question
        fields=['quiz','title','answer']
class QuestionSerial(serializers.ModelSerializer):
    answer=AnswerSerial(many=True,read_only=True)
    quiz=QuizSerial(read_only=True)
    class Meta:
        model=Question
        fields=['quiz','title','answer',]           

class DoctorSerial(serializers.ModelSerializer):
    class Meta:
        model=Doctor1
        fields=['email','name']

class PatientSerialView(serializers.ModelSerializer):
    name=serializers.CharField(max_length=250)
    date=serializers.DateField()
    desc=serializers.CharField(max_length=2000)
    
    class Meta:
        model=Patients
        fields=['id','name','email','phone','dtr_id','desc','date','time']
class PatientPastSerialView(serializers.ModelSerializer):
    name=serializers.CharField(max_length=250)
    date=serializers.DateField()
    desc=serializers.CharField(max_length=2000)
    
    class Meta:
        model=PastPatient
        fields=['name','email','phone','dtr_id','desc','date']
class PatientAppointmentSerial(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    
    
    class Meta:
        model=Patients
        fields=['dtr_id','email','name','phone','address','city','state','date','desc','time']
    def validate(self, attrs):
        email=attrs.get('email')
        name=attrs.get('name')
        date=attrs.get('date')
        doctor=attrs.get('dtr_id')
        desc=attrs.get('desc')
        time=random.randint(8, 20)
        
        
        '''times=attrs.get('time')
        
        timeslot=Patients.objects.values('dtr_id')
        slot=timeslot
        print(slot)'''
        
        if Patients.objects.filter(email=email).exists():
            raise serializers.ValidationError('One time only one patients can be appointed with one email id')
                
        elif MyUser.objects.filter(email=email).exists():
            
                
            
            return attrs
        else:
            raise serializers.ValidationError('You are not registered User')
    def create(self,validated_data):
        user = super(PatientAppointmentSerial, self).create(validated_data)
        time=random.randint(8, 20)
        
        name=user.name
        date=user.date
        doctor=user.dtr_id
        desc=user.desc
        if time<=11:
                body=f'Your Appointment is done for the {date} at {time}am of {doctor} for the {desc}, Regards team MFW.'
                data={'subject':f'Appointment is successful for the patient {name}','body':body,'to_email':user.email}
                Util.sendEmail(data)
                
        else:
                body=f'Your Appointment is done for the {date} at {time}pm of {doctor} for the {desc}, Regards team MFW.'
                data={'subject':f'Appointment is successful for the patient {name}','body':body,'to_email':user.email}
                Util.sendEmail(data)
        user.time=time
        user.save()
        return user
class PatientPastDetailSerial(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=PastPatient
        fields=['dtr_id','email','name','phone','address','city','state','date','desc','time']
class PastPatientDetailSerial(serializers.ModelSerializer):
    names = serializers.CharField(source='name')
    doctor = serializers.CharField(source='dtr_id')
    class Meta:
        model=PastPatient
        fields=['names','doctor','doctordiag','email']

class VerifyEmailOtp(serializers.ModelSerializer):
    class Meta:
        model=MyUser
        fields=['email','otp']
    email=serializers.EmailField(max_length=255)   
    otp=serializers.CharField(max_length=10)