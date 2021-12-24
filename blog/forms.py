from django.forms import Form, ChoiceField, CharField
from django import forms

from blog.models import Post, Category, Comment

class FilterForm(Form):
    '''
    A filter form for searching bar
    '''
    FILTER_CHOICES = (
        ('all', 'All'),
        ('author', 'Author'),
        ('title', 'Title'),
        ('content', 'Content'),
    )
    

    search = forms.CharField(
        label=("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control mr-sm-2', 
                                        'type': 'search',
                                        'placeholder': "What Post Do You Want To See",
        }))
    filter_field = ChoiceField(choices=FILTER_CHOICES, widget=forms.Select(attrs={'class':'form-control mr-sm-2'}))
    # choices = Category.objects.all().values_list('name', 'name') # grab name as tuple pairs
    # category = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=choices)
    
    
class CreateForm(forms.ModelForm):
    class Meta:
        choices = Category.objects.all().values_list('name', 'name') # grab name as tuple pairs
        model = Post
        fields = ('title', 'category', 'content')
        widgets = {
            'title': forms.TextInput(),
            'category': forms.Select(choices = choices),
            'content': forms.Textarea(),
        }
        

class UpdateForm(forms.ModelForm):
    class Meta:
        choices = Category.objects.all().values_list('name', 'name') # grab name as tuple pairs
        model = Post
        fields = ('title', 'category', 'content')
        widgets = {
            'title': forms.TextInput(),
            'category': forms.Select(choices = choices),
            'content': forms.Textarea(),
        }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(),
        }