from django import forms
from .models import UserProfile,Badge

class UserProfileForm(forms.ModelForm):
    avatar_choice = forms.ChoiceField(required=False, help_text='Or select an existing avatar.')

    class Meta:
        model = UserProfile
        fields = ['avatar', 'biography']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        
        # Dynamically set avatar choices based on user level
        if user:
            self.fields['avatar_choice'].choices = self.get_unlocked_avatars(user.profile.level)
    
    @staticmethod
    def get_unlocked_avatars(level):
        AVATAR_CHOICES = [
            ('default_avatars/avatar1.png', 'Avatar 1', 5),
            ('default_avatars/avatar2.png', 'Avatar 2', 10),
            ('default_avatars/avatar3.png', 'Avatar 3', 15),
            # Extend as needed
        ]
        
        return [(choice[0], choice[1]) for choice in AVATAR_CHOICES if level >= choice[2]]

class BadgeForm(forms.ModelForm):
    class Meta:
        model = Badge
        fields = ['label', 'description', 'image']

class ReminderForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['reading_reminder_time', 'reading_reminder_frequency']
        widgets = {'reading_reminder_time': forms.TimeInput(attrs={'type': 'time'})}