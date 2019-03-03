from django.contrib import admin
from django.utils.html import format_html

from . import models


class ProductAdmin(admin.ModelAdmin):
    """
    Just in case you don't know it
    
    The simpler ones
        list_display    what to show
        list_filter     filtering by what
    
    A bit more interesting ones
        list_editable   you could "edit" it on-the-fly (& "save" it, btn exists)
        search_fields   kinda the 'keyword' you're searching for (e.g. "By Title")
        
    Also, about `search_fields`
        it could use the QuerySet as well (based on the examples),
        since we often need cross-table queries (which is reasonable!).
        
        e.g.
            search_fields = ("product__name",)
    """
    
    list_display = ("name", "slug", "in_stock", "price")
    list_filter = ("active", "in_stock", "date_updated")
    list_editable = ("in_stock",)
    search_fields = ("name",)


admin.site.register(models.Product, ProductAdmin)


class ProductTagAdmin(admin.ModelAdmin):
    """
    Just in case you don't know it :D
    
    prepopulated_fields     auto generating based on other fields
    autocomplete_fields     kinda like dropdown-list (based on ur "products")
    """
    
    list_display = ("name", "slug")
    list_filter = ("active",)
    search_fields = ("name",)
    prepopulated_fields = { "slug": ("name",) }
    autocomplete_fields = ("products",)


admin.site.register(models.ProductTag, ProductTagAdmin)


class ProductImageAdmin(admin.ModelAdmin):
    """
    Just in case you don't know it :D
        readonly_fields     you can't modify it ('autogen-thumb' for our cases)
    
    The generated thumbnails still NOT displaying (on admin site).
    You'll need to edit 'booktime/urls.py'
        append something like `settings.MEDIA_URL` to the `urlpatterns`.
    """
    
    list_display = ("thumbnail_tag", "product_name")
    readonly_fields = ("thumbnail",)
    search_fields = ("product__name",)
    
    def thumbnail_tag(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="%s"' % obj.thumbnail.url
            )
        return "-"
    
    # The title which is displayed
    #   on the 'localhost:8000/admin/main/productimage/'
    thumbnail_tag.short_description = "Thumbnail"
    
    def product_name(self, obj):
        return obj.product.name  # might be cross-table-querying related??


admin.site.register(models.ProductImage, ProductImageAdmin)