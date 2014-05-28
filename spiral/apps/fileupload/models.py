# encoding: utf-8
from django.db import models
from re import search
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from apps.sp.models.Model import Model
from django.conf import settings

class Picture(models.Model):

    file = models.ImageField(
        upload_to="pictures"
    )
    slug = models.SlugField(
        max_length=80,
        blank=True,
        null=True
    )
    content_type = models.ForeignKey(
        ContentType,
        null=True
    )
    object_id = models.PositiveIntegerField(
        null=True
    )
    content_object = generic.GenericForeignKey(
        'content_type', 'content_object'
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    modified = models.DateTimeField(
        auto_now=True
    )

    def __unicode__(self):
        return self.file.name

    @models.permalink
    def get_absolute_url(self):
        return ('upload-new', )

    def save(self, *args, **kwargs):
        self.slug = self.file.name
        for field in self._meta.fields:
            if field.name == 'file':
                if self.content_type.name == 'model':
                    model = Model.objects.get(pk=self.object_id)
                    field.upload_to = 'pictures/model/%s' % str(model.model_code)
        super(Picture, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """delete -- Remove to leave file."""
        self.file.delete(False)
        super(Picture, self).delete(*args, **kwargs)

    def get_file_name_with_extension(self):
        from re import search
        file_name = self.file.name
        match = search("/(.+)", file_name)
        if match:
            real_file_name_with_extension = match.group(1)
            return real_file_name_with_extension

    def get_all_thumbnail(self):
        data = []
        thumbnails = self.picture_thumbnail_set.all()
        for thumbnail in thumbnails:
            data.append({
                'id': thumbnail.id,
                'type': thumbnail.get_type_display(),
                'url': thumbnail.file.name
            })
        return data


class PictureThumbnail(models.Model):
    # Thumbnail sizes.
    SMALL = {'key': 1, 'size': (160, 160), 'quality': 100, 'text': 'small', 'crop': False}
    MEDIUM = {'key': 2, 'size': (300, 300), 'quality': 100, 'text': 'medium', 'crop': False}
    LARGE = {'key': 3, 'size': (450, 450), 'quality': 100, 'text': 'large', 'crop': False}
    THUMBS = [SMALL, MEDIUM, LARGE]
    CHOICE_THUMBNAIL = (
        (SMALL.get('key'), 'Small'),
        (MEDIUM.get('key'), 'Medium'),
        (LARGE.get('key'), 'Large')
    )

    file = models.ImageField(
        upload_to="pictures"
    )

    type = models.SmallIntegerField(
        choices=CHOICE_THUMBNAIL,
        default=SMALL.get('key')
    )

    picture = models.ForeignKey(
        'Picture',
        verbose_name='Picture',
        related_name='picture_thumbnail_set',
    )

    @classmethod
    def save_all_thumbnails(self, picture):
        thumbnails = {}
        from easy_thumbnails.files import get_thumbnailer
        real_file_name_with_extension = picture.get_file_name_with_extension()

        file_url = settings.MEDIA_URL + "pictures/" + real_file_name_with_extension
        file_path = settings.ROOT_PATH + file_url
        file_name = picture.file.name

        try:
            _picture = open(file_path)
            thumbnailer = get_thumbnailer(_picture, relative_name=file_name)
            for thumb_options in self.THUMBS:
                thumb = thumbnailer.get_thumbnail(thumb_options)
                thumbnail = self.save_thumbnail(picture, thumb, thumb_options)
                if thumbnail.type == PictureThumbnail.SMALL.get('key'):
                    thumbnails.update({
                        'file': settings.MEDIA_URL + thumbnail.file.name
                    })
            return thumbnails
        except IOError:
            return None
        except Exception, e:
            return None

    @classmethod
    def save_thumbnail(self, picture, thumb, thumb_options):
        s = search('media\/(.+)', thumb._get_path())
        try:
            # thumb_file_path = u'pictures/heroku.png.100x100_q100.jpg'
            thumb_file_path = s.group(1)
            picture_thumbnail = PictureThumbnail()
            picture_thumbnail.picture = picture
            picture_thumbnail.file = thumb_file_path
            picture_thumbnail.type = thumb_options.get('key')
            picture_thumbnail.save()
            return picture_thumbnail
        except IndexError:
            # could not get the photo path
            return None
        except AttributeError:
            # error assigning attributes
            return None