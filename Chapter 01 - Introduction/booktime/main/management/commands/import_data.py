import csv
import os.path
from collections import Counter

from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify

from main import models


class Command(BaseCommand):
    help = "Import product in BookTime"

    def add_arguments(self, parser):
        """
        Well, this is basically what we'll implement.
        The test files should be put in the right place before testing.
        """

        parser.add_argument("csvfile", type=open)
        parser.add_argument("image_basedir", type=str)

    def handle(self, *args, **options):
        """ The logic code will be put in here.
        
        How to use this management command?
        >> ./manage.py import_data YOUR_CSV_FILE_PATH YOUR_IMAGES_FILE_PATH
        """

        self.stdout.write("Importing products")

        # Load the data
        c = Counter()
        reader = csv.DictReader(options.pop("csvfile"))

        for row in reader:

            # Generate data :: Product
            product, created = models.Product.objects.get_or_create(
                name=row["name"], price=row["price"]
            )

            product.description = row["description"]
            product.slug = slugify(row["name"])

            # Parse multiple tags if there is
            # that means the "delim" depends on the data (may not '|')
            for import_tag in row["tags"].split("|"):

                # Generate data :: ProductTag
                tag, tag_created = models.ProductTag.objects.get_or_create(
                    name=import_tag
                )

                product.tags.add(tag)

                c["tags"] += 1
                if tag_created:
                    c["tag_created"] += 1

            with open(
                os.path.join(options["image_basedir"], row["image_filename"]),
                "rb"
            ) as fi:

                # Generate data :: ProductImage
                image = models.ProductImage(
                    product=product,
                    image=ImageFile(fi, name=row["image_filename"])
                )

                image.save()
                c["images"] += 1

            product.save()
            c["products"] += 1

            if created:
                c["products_created"] += 1

        self.stdout.write(
            "Products processed=%d (created=%d)"
            % (c["products"], c["products_created"])
        )

        # self.stdout.write(
        #     "Tags processed=%d (created=%d)"
        #     % (c["tags"], c["tags_created"])
        # )

        self.stdout.write(
            "Images processed=%d" % (c["images"])
        )
