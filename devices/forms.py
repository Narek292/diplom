from .models import Device
from django.forms import ModelForm, Textarea, TextInput, Select

class DeviceForm(ModelForm):
    class Meta:

        model = Device
        fields = ['type','ip_address','inventory_number','serial_number','status','location','notes']

        widgets = {
            'type': Select(attrs={'class':'form-select',
                                    'placeholder':'Тип устройства'}),
            'ip_address': TextInput(attrs={'class':'form-control',
                                           'placeholder':'ip адрес'}),
            'inventory_number': TextInput(attrs={'class':'form-control',
                                                 'placeholder':'Инвентарный номер'}),
            'serial_number': TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'Серийний номер'}),
            'status': Select(attrs={'class': 'form-select',
                                                 'placeholder': 'Инвентарный номер'}),
            'location': Select(attrs={'class': 'form-select',
                                                 'placeholder': 'Местоположение'}),
            'notes': Textarea(attrs={'class': 'form-control',
                                                 'placeholder': 'Примечания'})
        }