from django.db import models


class DeviceType(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class DeviceStatus(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Location(models.Model):

    building = models.CharField(max_length=100, blank=True, null=True)
    floor = models.CharField(max_length=100)
    room = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.building} {self.floor}/{self.room}'

class Device(models.Model):

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    inventory_number = models.CharField(max_length=100, blank=True, null=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    type = models.ForeignKey(DeviceType, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(DeviceStatus, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.type.name}-{self.status.name}'

    def get_absolute_url(self):
        return f'/devices/{self.id}'

class DeviceLog(models.Model):

    ACTIONS = (
        ('create', 'Создание'),
        ('update', 'Редактирование'),
        ('delete', 'Удаление')
    )
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='logs')
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device}-{self.action}"