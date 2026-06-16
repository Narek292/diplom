from django.forms import ModelForm, Textarea, TextInput, Select, ModelMultipleChoiceField, SelectMultiple
from .models import Article, ArticleTag
from tinymce.widgets import TinyMCE

class ArticleForm(ModelForm):
    tags = ModelMultipleChoiceField(queryset=ArticleTag.objects.all(),
                                    required=False,
                                    widget=SelectMultiple(attrs={'class':'form-control'}))
    class Meta:

        model = Article
        fields = ['title','category','tags','content']

        widgets = {
            'title': TextInput(attrs={'class':'form-control',
                                      'placeholder':'Заголовок'}),
            'category': Select(attrs={'class':'form-control'}),
            'content': TinyMCE(attrs={'cols': 80, 'rows': 20}),
        }
