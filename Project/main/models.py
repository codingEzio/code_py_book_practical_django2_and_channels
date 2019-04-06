import logging

from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)

from django.core.validators import MinValueValidator

from . import exceptions

logger = logging.getLogger(__name__)


class ActiveManager(models.Manager):
    def active(self):
        return self.filter(active=True)


class ProductTagManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class ProductTag(models.Model):
    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=48)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    # tags = models.ManyToManyField(Product, blank=True)

    objects = ProductTagManager()

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.slug,)


class Product(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    slug = models.SlugField(max_length=48)
    active = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    date_updated = models.DateTimeField(auto_now=True)  # update each time

    tags = models.ManyToManyField(ProductTag, blank=True)

    objects = ActiveManager()

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """
    The field `image` requires an extra package.
        You can't even "migrated" because of it.
        Well, install it by `pipenv install Pillow` :)
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product-images")
    thumbnail = models.ImageField(upload_to="product-thumbnails", null=True)

    def __str__(self):
        return self.product.name


class UserManager(BaseUserManager):
    """
    Q & A
        is_staff            able to access the admin site
        is_superuser        able to do .. anything
        normalize_email     lowercasing the "domain" part
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password = None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have `is_stuff=True`.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have `is_superuser=True`.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Q & A
        USERNAME_FIELD      it could any fields (mostly 'CharField', 'EmailField', though)
        REQUIRED_FIELDS     prompted for when creating a user via the `createsuperuser` (huh)

        @.. is_employee     Flag stuff, modify data, check site performance
        @.. is_dispatcher   Flag stuff (less permissions than above)

            About the `@property`
            || Make the 'is_employee' simply returns True/False.
            || You're able to call it by 'INST.is_employee' without the brackets!
    """

    username = None
    email = models.EmailField("email address", unique=True)

    USERNAME_FIELD = "email"  # ↑ the `email` field above ↑
    REQUIRED_FIELDS = []

    objects = UserManager()  # override some of methods we needed

    @property
    def is_employee(self):
        return self.is_active and (
            self.is_superuser or self.is_staff
            and self.groups.filter(name="Employees").exists()
        )

    @property
    def is_dispatcher(self):
        return self.is_active and (
            self.is_superuser or self.is_staff
            and self.groups.filter(name="Dispatchers").exists()
        )


class Address(models.Model):
    """
    We'll need this info later when we build the 'checkout' system.
    """

    SUPPORTED_COUNTRIES = (
        ("uk", "United Kingdom"),
        ("us", "United States of America"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    address1 = models.CharField("Address line 1", max_length=60)
    address2 = models.CharField("Address line 2", max_length=60, blank=True)

    zip_code = models.CharField("ZIP / Postal code", max_length=12)
    city = models.CharField(max_length=60)
    country = models.CharField(max_length=3, choices=SUPPORTED_COUNTRIES)

    def __str__(self):
        return ", ".join([
            self.name,
            self.address1,
            self.address2,
            self.zip_code,
            self.city,
            self.country,
        ])


class Basket(models.Model):
    """
    A review of 'Basket' & 'BasketLine' model (which is very needed)

        #fields Basket
        || id           id          # internal & incremental
        || user         user_id     # whose basket (one user CAN have multiple baskets!!)
        || status       status      # basket status: STILL-BUYING, READY-TO-CHECKOUT

        #fields BasketLine
        || id           id          # internal & incremental
        || basket       basket_id   # link to 'Basket' model  (multiple to ONE in `Basket`)
        || product      product_id  # along with `quantity`   (each prod got its own records)
        || quantity     quantity    # along with `product_id` (each qutt got its own records)
    """

    OPEN = 10
    SUBMITTED = 20
    STATUSES = ((OPEN, "Open"), (SUBMITTED, "Submitted"))

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True
    )
    status = models.IntegerField(choices=STATUSES, default=OPEN)

    def is_empty(self):
        return self.basketline_set.all().count() == 0

    def count(self):
        return sum(i.quantity for i in self.basketline_set.all())

    def create_order(self, billing_address, shipping_address):
        """
        #TODO break down this method
        """

        # Being logged in is required
        if not self.user:
            raise exceptions.BasketException(
                "Cannot create order without user!"
            )

        logger.info(
            "Creating order for basket_id=%2d"
            ", shipping_address_id=%2d, billing_address_id=%2d",
            self.id,
            shipping_address.id,
            billing_address.id,
        )

        # Assigning values to the fields of 'Order' model
        #   what I'm really interested is the latter, `VARIABLE.ATTRIBUTE`.
        order_data = {
            "user": self.user,
            "billing_name": billing_address.name,
            "billing_address1": billing_address.address1,
            "billing_address2": billing_address.address2,
            "billing_zip_code": billing_address.zip_code,
            "billing_city": billing_address.city,
            "billing_country": billing_address.country,
            "shipping_name": shipping_address.name,
            "shipping_address1": shipping_address.address1,
            "shipping_address2": shipping_address.address2,
            "shipping_zip_code": shipping_address.zip_code,
            "shipping_city": shipping_address.city,
            "shipping_country": shipping_address.country,
        }

        # Nonetheless, the 'order' was created at this line
        order = Order.objects.create(**order_data)

        c = 0

        # All records of the `BasketLine' table
        for line in self.basketline_set.all():

            for item in range(line.quantity):

                # This line produces these
                # || order   info : {user, billing_info, shipping_info}
                # || product info : {product(id) -- looping outside by 'quantity'}
                order_line_data = {
                    "order": order,
                    "product": line.product,
                }

                # Creating `OrderLine` inst by {
                #   essential-ones          product-name/id  (quantity: outside loop)
                #   not-so-essential-ones   user, shipping/billing info
                # }
                order_line = OrderLine.objects.create(
                    **order_line_data
                )

                # Produces total num
                # e.g. (=> 4)
                #   2* prod-one
                #   1* prod-one
                #   1* prod-one-another-basket
                c += 1

        logger.info(
            "Created order with id=%2d and lines_count=%2d",
            order.id,
            c,
        )

        # Checkout (Basket => Submitted)
        self.status = Basket.SUBMITTED

        self.save()

        return order


class BasketLine(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )


class Order(models.Model):
    """
    About `xx_address` field
        It was meant to < make orders snapshots in time >
        & any subsequent change to a <users' addrs> won't affect existing orders.
    """

    NEW = 10
    PAID = 20
    DONE = 30
    STATUSES = ((NEW, "New"), (PAID, "Paid"), (DONE, "Done"),)

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # deletion related
    status = models.IntegerField(choices=STATUSES, default=NEW)

    # -------------------- Part One ---------- ----------

    billing_name = models.CharField(max_length=60)
    billing_address1 = models.CharField(max_length=60)
    billing_address2 = models.CharField(max_length=60, blank=True)

    billing_zip_code = models.CharField(max_length=12)
    billing_city = models.CharField(max_length=60)
    billing_country = models.CharField(max_length=3)

    # -------------------- Part Two ---------- ----------

    shipping_name = models.CharField(max_length=60)
    shipping_address1 = models.CharField(max_length=60)
    shipping_address2 = models.CharField(max_length=60, blank=True)

    shipping_zip_code = models.CharField(max_length=12)
    shipping_city = models.CharField(max_length=60)
    shipping_country = models.CharField(max_length=3)

    # -------------------- Part Three ---------- ----------

    date_updated = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)

    # -------------------- Part Four ---------- ----------

    last_spoken_to = models.ForeignKey(
        User,
        null=True,
        related_name="cs_chats",
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return "[Order] #" + repr(self.id)


class OrderLine(models.Model):
    """
    About `related_name`
        Example
            || OLD  --  order.orderline_set.all()
            || NEW  --  order.lines.all()
        Explanation
            1. We're doing "reverse related obj lookup" (which produces 'orderline').
    """

    NEW = 10
    PROCESSING = 20
    SENT = 30
    CANCELLED = 40
    STATUSES = (
        (NEW, "New"), (PROCESSING, "Processing"),
        (SENT, "Sent"), (CANCELLED, "Cancelled"),
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE, related_name="lines",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    status = models.IntegerField(choices=STATUSES, default=NEW)

    def __str__(self):
        return "[OrderLine] #" + repr(self.id)