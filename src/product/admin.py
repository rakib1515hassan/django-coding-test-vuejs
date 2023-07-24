from django.contrib import admin
from product.models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Variant)
admin.site.register(ProductVariant)
admin.site.register(ProductImage)
admin.site.register(ProductVariantPrice)


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ( "product", "file_path" )
    


# @admin.register(Variant)
# class VariantAdmin(admin.ModelAdmin):
#     list_display = ( "title", "description", "active" )



# @admin.register(ProductImage)
# class VariantAdmin(admin.ModelAdmin):
#     list_display = ( "product", "file_path" )


# @admin.register(ProductVariant)
# class VariantAdmin(admin.ModelAdmin):
#     list_display = ("variant_title", "variant", "product" )



# @admin.register(ProductVariantPrice)
# class VariantAdmin(admin.ModelAdmin):
#     list_display = ("product_variant_one", "product_variant_two", "product_variant_three", "price", "stock", "product" )