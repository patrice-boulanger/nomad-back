from django.db import models
from django.utils.translation import gettext_lazy as _
from .user import User

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
import os
from django.conf import settings


class Files(models.Model):

    def group_based_upload_to(instance, filename):
        return f"files/{instance.user.last_name}/{filename}"

    files = models.FileField(upload_to=group_based_upload_to, blank=True, verbose_name=_(
        'files required'))

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="files")

    class Meta:
        ordering = ("user",)
        verbose_name = _("Files required")
        verbose_name_plural = _("Files required")


@receiver(post_delete, sender=Files)
def my_handler(sender, **kwargs):
    path = os.path.join(settings.BASE_DIR, 'nomad/media/',
                        str(kwargs['instance'].files))
    try:
        os.remove(path)
        print("Successfuly removed")

    except:
        print("Error file not found")
