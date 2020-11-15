from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    published = models.DateTimeField()
    image = models.ImageField(upload_to='media/') #mediaに画像ファイルを置く
    body = models.TextField()

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:100]
