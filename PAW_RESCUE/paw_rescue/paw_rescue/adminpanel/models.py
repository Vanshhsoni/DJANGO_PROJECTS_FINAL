from django.db import models

class Adoption(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='adoption/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
