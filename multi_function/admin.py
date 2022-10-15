from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
'''@admin.register(Users, My)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','stuname','email']'''

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id','email','tc','phone', 'name', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name','tc','phone')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name','tc','phone' 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email','id')
    filter_horizontal = ()
# Now register the new UserAdmin...
admin.site.register(models.MyUser, UserAdmin)
admin.site.register(models.Contact)
admin.site.register(models.PastPatient)
@admin.register(models.Category)
class CatAdmin(admin.ModelAdmin):
    list_display=['name',]
@admin.register(models.Quizzes)
class QuizAdmin(admin.ModelAdmin):
    list_display=['id','title',]
class AnswerInlineModel(admin.TabularInline):
    model=models.Answer
    fields= ['answer_text','is_right']
@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    fields=['title','quiz']
    list_display=['title','quiz','date_updated']
    inlines=[AnswerInlineModel,]
@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display=['answer_text','is_right','question']
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
@admin.register(models.Doctor1)
class DoctorAdmin(admin.ModelAdmin):
    list_filter=['department']
    list_display=['department','name']
@admin.register(models.Patients)
class PatientAdmin(admin.ModelAdmin):
    list_filter=['dtr_id']
    list_display=['id','dtr_id','name',]
admin.site.register(models.DoctorCategory)