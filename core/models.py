from django.db import models
import uuid
import datetime
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import os
from django.conf import settings


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    media_root = settings.MEDIA_ROOT
    file_path=os.path.join(
        media_root, instance.client_id, filename)
    return file_path


class ProjectDetails(models.Model):

    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    user = models.CharField(max_length=100)
    project_name = models.CharField(max_length=100)
    client_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    mobile = models.IntegerField()
    date = models.DateField(default=datetime.date.today)
    image_directory_path = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name


class Photo(models.Model):
    title = models.CharField(max_length=255, blank=True)
    file = models.ImageField(upload_to=user_directory_path)
    client_id = models.UUIDField(default=uuid.uuid4(), editable=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_file_selected = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.file = self.compress_image(self.file)
        super(Photo, self).save(*args, **kwargs)

    def compress_image(self, file):
        imageTemproary = Image.open(file)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((1920, 1080))
        imageTemproaryResized.save(outputIoStream,  format='JPEG', optimize=True, quality=60)
        outputIoStream.seek(0)
        uploaded_image = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % file.name.split('.')[0],
                                             'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploaded_image