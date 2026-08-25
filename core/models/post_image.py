from django.db import models

class PostImage(models.Model):
    post = models.ForeignKey('FacebookPost', on_delete=models.CASCADE, related_name='images')
    prompt_used = models.TextField()
    image_file = models.ImageField(upload_to='post_images/')
    provider = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    generated_at = models.DateTimeField(auto_now_add=True)

