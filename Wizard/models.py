from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    birthday = models.DateTimeField(null=True, blank=False)
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.username}"

class LogFiles(models.Model):
    logname = models.CharField(max_length=100, blank=False)
    logtype = models.CharField(max_length=100, blank=False)
    size = models.IntegerField(blank=False)

    def __str__(self):
        return f"{self.logname} ({self.logtype}, {self.size} bytes)"

class Logs(models.Model):
    name = models.CharField(max_length=100, blank=False)
    time = models.DateTimeField()
    priority = models.CharField(max_length=50, blank=False)
    code = models.IntegerField(blank=False)
    OS = models.CharField(max_length=50, blank=False, default=None)
    browser = models.CharField(max_length=50, blank=False, default=None)
    log_file = models.ForeignKey(LogFiles, related_name="logs", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.name} - {self.code} ({self.priority})"

class Notifications(models.Model):
    message = models.TextField(blank=False)
    user = models.ForeignKey(User, related_name="notifications", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}..."
