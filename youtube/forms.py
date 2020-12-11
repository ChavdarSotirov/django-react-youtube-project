from django import forms

from youtube.models import Video


class VideoCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for (_, field) in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Video
        fields = '__all__'


class CommentForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control rounded-2', }
        )
    )
