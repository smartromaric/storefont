from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class TaggedItemManager(models.Manager):
    def get_tag_for(self, obj_type, obj_id):
        prod = ContentType.objects.get_for_model(obj_type)  # takin product table raw from content_type
        return Tagged_Item.objects.select_related("tag") \
            .filter(
            content_type=prod,
            object_id=obj_id,
        )


# Create your models here.
class Tag(models.Model):
    label = models.CharField(max_length=255)


class Tagged_Item(models.Model):
    objects = TaggedItemManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
