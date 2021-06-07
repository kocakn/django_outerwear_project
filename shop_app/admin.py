from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm, ValidationError
from PIL import Image

from .models import *


class OuterwearAdminForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = 'Загрузите изображение товара. Разрешение должно быть больше {}x{}'.format(
            *Product.MIN_RESOLUTION
        )
    
    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_height, min_width = Product.MIN_RESOLUTION
        max_height, max_width = Product.MAX_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError('Размер изображения не должен превышать 3 Мб')
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Разрешение изображения меньше минимального')
        if img.height > max_height or img.width > max_width:
            raise ValidationError('Слишком большое изображение')
        return image


class MenOuterwearAdmin(admin.ModelAdmin):
    form = OuterwearAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='men'))  # Slug категории задается при ее добавлении
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



class WomenOuterwearAdmin(admin.ModelAdmin):
    form = OuterwearAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='women'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class GirlsOuterwearAdmin(admin.ModelAdmin):
    form = OuterwearAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='girls'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class BoysOuterwearAdmin(admin.ModelAdmin):
    form = OuterwearAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='boys'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(MenOuterwear, MenOuterwearAdmin)
admin.site.register(WomenOuterwear, WomenOuterwearAdmin)
admin.site.register(GirlsOuterwear, GirlsOuterwearAdmin)
admin.site.register(BoysOuterwear, BoysOuterwearAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)