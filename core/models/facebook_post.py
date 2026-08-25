from django.db import models

class FacebookPost(models.Model):
    campaign = models.ForeignKey('Campaign', on_delete=models.CASCADE, related_name='posts')
    topic = models.CharField(max_length=255)
    caption = models.TextField()
    hashtags = models.JSONField(default=list)
    call_to_action = models.CharField(max_length=255, blank=True)
    image_prompt = models.TextField()
    raw_report = models.JSONField(default=dict, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post for {self.campaign.title} - {self.topic}"