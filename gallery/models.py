from django.db import models
from auth_app.models import User

class Image(models.Model):

    title = models.CharField(verbose_name='Image title', max_length=256)
    image = models.ImageField(verbose_name='Image url', upload_to='images')
    update_at = models.DateTimeField(verbose_name='Date of update', auto_now=True)
    created_date = models.DateTimeField(verbose_name='Date of create', auto_now_add=True )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
