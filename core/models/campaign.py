from django.db import models

class Campaign(models.Model):
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, related_name='campings')
    title = models.CharField(max_length=255)
    objective = models.TextField()
    target_audience = models.CharField(max_length=255)
    tone = models.CharField(max_length=100, blank=True, default="")
    Keywords = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title