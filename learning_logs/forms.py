from django import forms

from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}

        # A widget is an HTML form element, such as:
        #  a single-line text box,
        #  multi-line text area, or
        #  drop-down list
        # By including the widgets attribute you can override
        # Django’s default widget choices. Telling Django to use
        # a forms.Textarea element, we’re customizing the input
        # widget for the field 'text' so the text area will be 80
        # columns wide instead of the default 40.
        # This will give users enough room to write a meaningful entry.
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}

class DeleteEntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = []
        labels = {'text': ''}

class DeleteTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = []
        labels = {'text': ''}
