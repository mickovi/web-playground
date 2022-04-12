from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'profiles/' + filename

# Create your models here.
class Profile(models.Model):
    # Relación uno a uno (user-profile)
    user = models.OneToOneField(User, verbose_name='Usuario', on_delete=models.CASCADE)
    # Instalar Pillow para servir archivos media (pip install Pillow)
    avatar = models.ImageField(upload_to=custom_upload_to, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    link = models.URLField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['user__username']

@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    # created en False indica que se ejecuta cuando se crea por primera vez y no cuando se modifica
    if kwargs.get('created', False):
        # Creamos el perfil
        Profile.objects.get_or_create(user=instance)
        # print('Se ha creado el usuario y su perfil')