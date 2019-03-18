import logging
from io import BytesIO

from django.core.files.base import ContentFile
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in

from PIL import Image

from .models import ProductImage, Basket
from .models import OrderLine, Order

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


@receiver(user_logged_in)
def merge_baskets_if_found(sender, user, request, **kwargs):
    """
    About the `receiver`
        `user_logged_in`    Sent when a user logs in successfully.

    About the 'merge' here
        It means that 'merging products in the basket to the current user'.

    I havn't cleaned up my mind about this method (merging baskets).
    """

    # See if there's a basket being stored before
    anonymous_basket = getattr(request, "basket", None)

    # This big chunk of code won't run unless it gets stuff in the `request` object
    if anonymous_basket:
        try:
            # Assign the current user to a new 'basket' object
            loggedin_basket = Basket.objects.get(
                user=user, status=Basket.OPEN
            )

            # About the `basketline_set`
            #   It was called 'reverse related object lookup'.
            #   Simply put, from [fk.being_fked](fked) to [being_fked.fk_set](fk_set)
            for line in anonymous_basket.basketline_set.all():

                # Merging the basket with the current user's
                line.basket = loggedin_basket
                line.save()

            # Delete the one in the ?cache
            anonymous_basket.delete()

            # Assign the basket for 'views, templates' to use
            request.basket = loggedin_basket

            logger.info(
                "Merged basket to id %d", loggedin_basket.id
            )

        except Basket.DoesNotExist:

            # Assign a blank basket to the user?
            anonymous_basket.user = user
            anonymous_basket.save()

            logger.info(
                "Assigned user to basket id %d", anonymous_basket.id
            )


@receiver(post_save, sender=OrderLine)
def orderline_to_order_status(sender, instance, **kwargs):
    """
    Quite a complex `if` statement!
    || In short, it produces <NOT [any NEW/PROCESSING]> exists
    || that is, all the "order lines" have been exec_ed (aka. 'SENT').
    """

    if not instance.order.lines \
        .filter(status__lt=OrderLine.SENT) \
        .exists():

        # If all 'sent', tell us that it was all 'sent'.
        logger.info(
            "All lines for order [%2d] have been processed. Marking as done.",
            instance.order.id
        )

        # Mark the order as finished, done!
        instance.order.status = Order.DONE

        instance.order.save()
