from .models import Ticket
from django.forms import ModelForm, Textarea, TextInput, Select
from tinymce.widgets import TinyMCE

class TicketForm(ModelForm):
    class Meta:

        model = Ticket
        fields = ['title','description','device','article','status','priority']

        widgets = {
            'title': TextInput(attrs={'class':'form-control',
                                    'placeholder':'Заголовок'}),
            'description': TinyMCE(attrs={'cols': 80, 'rows': 20}),
            'device': Select(attrs={'class':'form-select',
                                                 'placeholder':'Устройство'}),
            'article': Select(attrs={'class': 'form-select',
                                                 'placeholder': 'Статья решение'}),
            'status': Select(attrs={'class': 'form-select',
                                                 'placeholder': 'Статус'}),
            'priority': Select(attrs={'class': 'form-select',
                                                 'placeholder': 'Приоритет'})
        }