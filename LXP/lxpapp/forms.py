from django import forms
from social_django.models import UserSocialAuth
from django.contrib.auth.models import User
from django.db.models import Q
from . import models
from .models import Poll

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
                'username', 
                'password', 
                'email', 
                'first_name', 
                'last_name'
        ]

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class SubjectForm(forms.ModelForm):
    subject_name = forms.CharField(
        max_length=90000,
        #  forms ↓
        widget=forms.TextInput(attrs={'autofocus': True , 'class': 'form-control '})
    )
    class Meta:
        model=models.Subject
        fields=['subject_name']
        
class ChapterForm(forms.ModelForm):
    def _init_(self, *args, **kwargs):
        super(ChapterForm, self)._init_(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control mb-3'})  # Add a Bootstrap class or your custom class

    class Meta:
        model = models.Chapter
        fields = ['subject', 'chapter_name']
        widgets = {
    'subject': forms.Select(attrs={
        'class': 'form-control mb-3',
        'placeholder': 'Enter the subject',
    }),
    'chapter_name': forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter the chapter name',
    }),
}
        


class MainHeadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MainHeadForm, self).__init__(*args, **kwargs)
        self.fields['mainhead_name'].label = 'Main Head Name'
    

    mainhead_name = forms.CharField(
        max_length=90000,
        #  forms ↓
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'})
    )
    class Meta:
        model=models.MainHead
        
        fields=['mainhead_name']

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'poll_type', 'eligible_groups']
        widgets = {
            'question': forms.TextInput(attrs={
                'class': 'lxp-input', 'size': '50', 'placeholder': 'Enter your poll question...'
            }),
            'poll_type': forms.Select(attrs={
                'class': 'large-select', 'onchange': 'onPollTypeChange()'
            }),
            # This widget renders the ManyToManyField as a box of checkboxes.
            # It's generally more user-friendly than a standard multi-select box.
            'eligible_groups': forms.CheckboxSelectMultiple,
        }
        labels = {
            'question': 'Question',
            'poll_type': 'Poll Type',
            'eligible_groups': 'Who can vote on this poll?',
        }

class PollOptionForm(forms.Form):
    option_text = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',  # Replaced lxp-input with GetSkills style
        })
    )

PollOptionFormSet = forms.formset_factory(
    PollOptionForm,
    extra=0,
    min_num=2,
    validate_min=True
)

YesNoOptionFormSet = forms.formset_factory(
    PollOptionForm,
    extra=0,
    min_num=2,
    max_num=2,
    validate_min=True
)

class SubHeadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubHeadForm, self).__init__(*args, **kwargs)
        self.fields['mainhead'].label = 'Main Head Name'
        self.fields['subhead_name'].label = 'Sub Head Name'
        
        # Add form-control class to mainhead dropdown
        self.fields['mainhead'].widget.attrs['class'] = 'form-control mb-5'
    
    subhead_name = forms.CharField(
        max_length=90000,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'})
    )
    
    class Meta:
        model = models.SubHead
        fields = ['mainhead', 'subhead_name']


        
class TopicForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control mb-3'  # Add Bootstrap class and margin
            })

    class Meta:
        model = models.Topic
        fields = ['topic_name', 'chapter']
        widgets = {
            'topic_name': forms.TextInput(attrs={
                'class': 'form-control mb-3',  # Add styling and spacing
                'placeholder': 'Enter the topic name',
            }),
            'chapter': forms.Select(attrs={
                'class': 'form-control mb-3',  # Add styling and spacing
            }),
        }        

class LearnerDetailsForm(forms.ModelForm):
    user_full_name = forms.CharField(
        max_length=90000,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}),
        required=True  # Explicitly required
    )
    mobile = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True  # Explicitly required
    )
    whatsappno = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True  # Explicitly required
    )
    profile_pic = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=True  # Explicitly required (to ensure file is uploaded)
    )

    class Meta:
        model = models.LearnerDetails
        fields = ['user_full_name', 'mobile', 'whatsappno', 'profile_pic']
        
class CourseForm(forms.ModelForm):
    class Meta:
        model=models.Course 
        fields=['mainhead','subhead','themecolor']
    def _init_(self, *args, **kwargs):
        super(CourseForm, self)._init_(*args, **kwargs)



class TrainerNotificationForm(forms.ModelForm):
    trainerID=forms.ModelChoiceField(queryset=UserSocialAuth.objects.all().filter(utype = '1',user_id__in=models.User.objects.all().order_by('first_name')),empty_label="Trainer Name", to_field_name="id")
    trainernotification_message = forms.CharField(
        max_length=255,
        #  forms ↓
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    class Meta:
        model=models.TrainerNotification
        fields=['trainernotification_message']        

class MaterialForm(forms.ModelForm):
    class Meta:
        model = models.Material
        fields = ('subject', 'chapter','topic','mtype','urlvalue','description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CourseTypeForm(forms.ModelForm):
    coursetype_name = forms.CharField(
        max_length=90000,
        #  forms ↓
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'})
    )
    class Meta:
        model=models.CourseType
        fields=['coursetype_name']

class BatchForm(forms.ModelForm):
    coursetypeID=forms.ModelChoiceField(queryset=models.CourseType.objects.all(),empty_label="Course Type Name", to_field_name="id")
    batch_name = forms.CharField(
        max_length=255,
        #  forms ↓
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    class Meta:
        model=models.Batch
        fields=['batch_name','stdate','enddate']
        widgets = {
            'stdate': forms.DateInput(format='%d/%m/%Y'),
            'enddate': forms.DateInput(format='%d/%m/%Y')
        }

class ExamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        self.fields['questiontpye'].label = 'Question Type'
    class Meta:
        model=models.Exam
        fields=['exam_name','questiontpye','batch']

class McqQuestionForm(forms.ModelForm):
    examID=forms.ModelChoiceField(queryset=models.Exam.objects.all().filter(questiontpye='MCQ'),empty_label="Exam Name", to_field_name="id")
    class Meta:
        model=models.McqQuestion
        fields=['marks','question','option1','option2','option3','option4','answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50,'autofocus': True})
        }

class ShortQuestionForm(forms.ModelForm):
    examID=forms.ModelChoiceField(queryset=models.Exam.objects.all().filter(questiontpye='ShortAnswer'),empty_label="Exam Name", to_field_name="id")
    class Meta:
        model=models.McqQuestion
        fields=['marks','question']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50, 'autofocus': True})
        }

class YTExamQuestionForm(forms.ModelForm):
    playlistID=forms.ModelChoiceField(queryset=models.Playlist.objects.all(),empty_label="Play List Name", to_field_name="id")
    videoID=forms.ModelChoiceField(queryset=models.Video.objects.all(),empty_label="Video Name", to_field_name="id")
    class Meta:
        model=models.YTExamQuestion
        fields=['marks','question','option1','option2','option3','option4','answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50,'autofocus': True})
        }


class SessionMaterialForm(forms.ModelForm):
    class Meta:
        model = models.SessionMaterial
        fields = ('playlist', 'video','mtype','urlvalue','description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['video'].queryset = models.Video.objects.none()

        if 'playlist' in self.data:
            try:
                playlist_id = int(self.data.get('playlist'))
                self.fields['video'].queryset = models.PlaylistItem.objects.all().distinct().filter (video_id__in = models.Video.objects.all().distinct(),playlist_id = playlist_id).distinct()
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['video'].queryset = self.instance.playlist.video_set.order_by('name')

class ChapterQuestionForm(forms.ModelForm):
    class Meta:
        model=models.ChapterQuestion
        fields=['subject', 'chapter','marks','question','option1','option2','option3','option4','answer']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50,'autofocus': True})
        }

class K8STerminalForm(forms.ModelForm):
    learnerID=forms.ModelChoiceField(queryset= User.objects.all().filter(id__in = UserSocialAuth.objects.all().filter(Q(utype=0) | Q(utype=2),status = 1)),empty_label="Learner Name", to_field_name="id")
    
    class Meta:
        model=models.K8STerminal
        fields=['Password','usagevalue']


class PlayListForm(forms.ModelForm):
    name = forms.CharField(
        max_length=90000,
        #  forms ↓
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    channel_id = forms.CharField(
        max_length=90000,
        #  forms ↓
        widget=forms.TextInput(attrs={'value': 'UCxdhwzsgcGldYghv6u3nrXw'})
    )
    channel_name = forms.CharField(
        max_length=90000,
        #  forms ↓
        widget=forms.TextInput(attrs={'value': 'Team NubeEra'})
    )
    playlist_id = forms.CharField(
        max_length=90000,
        #  forms ↓
        widget=forms.TextInput()
    )
    class Meta:
        model=models.Playlist
        fields=['channel_id','channel_name','playlist_id','name']

class ActivityForm(forms.ModelForm):
    class Meta:
        model = models.Activity
        fields = ['playlist', 'video', 'urlvalue', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        