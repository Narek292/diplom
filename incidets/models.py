from django.db import models
from devices.models import Device
from wiki.models import Article
from users.models import User
from tinymce.models import HTMLField

class TicketStatus(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class TicketPriority(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    title = models.CharField(max_length=200)
    description = HTMLField()
    device = models.ForeignKey(Device, on_delete=models.SET_NULL, null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, blank=True, help_text='Связанная статья (решение)')
    status = models.ForeignKey(TicketStatus, on_delete=models.SET_NULL, null=True)
    priority = models.ForeignKey(TicketPriority, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_by')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_to')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.device.type.name}'

    def get_absolute_url(self):
        return f'/incidents/{self.id}'

class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Комментарий к {self.ticket.title}'

class TicketHistory(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='history')
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    field_name = models.CharField(max_length=100)
    old_value = models.CharField(max_length=255, blank=True, null=True)
    new_value = models.CharField(max_length=255, blank=True, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Изменение {self.field_name} в статье: {self.ticket.title}'