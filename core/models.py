
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    

        def __str__(self):
         return self.user.username

class Avatar(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.FileField(upload_to="media/avatares", null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.imagen}"
    



class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.TextField()
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def is_author(self, user):
        return self.user == user

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.created_at}'


from django.apps import AppConfig
from django.db.models.signals import post_migrate

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from django.contrib.auth.models import Group

        def create_groups(sender, **kwargs):
            Group.objects.get_or_create(name='Usuarios normales')
            Group.objects.get_or_create(name='Usuarios administradores')

        # Conéctate al evento post_migrate para garantizar que la base de datos esté lista
        post_migrate.connect(create_groups, sender=self)
