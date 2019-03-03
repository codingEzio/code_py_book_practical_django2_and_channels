from io import BytesIO
import logging

from PIL import Image

from django.core.files.base import ContentFile
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import ProductImage


THUMBNAIL_SIZE = (300, 300)

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=ProductImage)
def generate_thumbnail(sender, instance, **kwargs):
    """
    For the sake of simplicity,
    I used the examples from the official documentation.
        https://pillow.readthedocs.io/en/stable/reference/Image.html#create-thumbnails
    
        OLD     image_inst = image_inst.convert("RGB")
                image_inst.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
                
        NEW     image_inst.thumbnail(THUMBNAIL_SIZE)
    """
    
    logger.info("Generating thumbnail for product %2d", instance.product.id)

    image_inst = Image.open(instance.image)
    image_inst.thumbnail(THUMBNAIL_SIZE)

    temp_thumb = BytesIO()
    image_inst.save(temp_thumb, "JPEG")

    temp_thumb.seek(0)

    instance.thumbnail.save(
        instance.image.name, ContentFile(temp_thumb.read()), save=False
    )

    temp_thumb.close()
