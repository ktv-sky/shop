from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

User = get_user_model()

def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]

def get_product_url(obj, viewname, *model_name):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug':obj.slug})

class MinResolutionErrorException(Exception):
    pass

class MaxResolutionErrorException(Exception):
    pass


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_redpect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_product = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_product)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products,
                        key=lambda x:__class__.__meta.model_name.startswith(
                            with_respect_to,
                            reverse=True))
        return products


class LatestProducts:
    objects = LatestProductsManager()


class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        'Ноутбуки': 'notebook__count',
        'Смартфоны': 'smartphone__count',
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_left_sidebar(self):
        models = get_models_for_count('notebook', 'smartphone')
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(
                name=c.name,
                url=c.get_absolute_url(),
                count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]
        return data



class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='имя категории')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):

    category = models.ForeignKey(
        Category, verbose_name='категория', on_delete=models.CASCADE
        )
    title = models.CharField(max_length=255, verbose_name='наименование')
    slug = models.SlugField(unique=True, verbose_name='артикул')
    image = models.ImageField(verbose_name='изображение')
    description = models.TextField(verbose_name='описание', null=True)
    price = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name='цена'
        )

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class CartProduct(models.Model):
    user = models.ForeignKey(
        'Customer', verbose_name='покупатель', on_delete=models.CASCADE
        )
    cart = models.ForeignKey(
        'Cart', verbose_name='корзина', on_delete=models.CASCADE,
        related_name='related_products'
        )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name='общая цена'
        )

    def __str__(self):
        return f"Продукт: {self.content_object.title} (для корзины)"

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey(
        'Customer', null=True, verbose_name='владелец',
        on_delete=models.CASCADE
        )
    products = models.ManyToManyField(
        CartProduct, blank=True, related_name='related_cart'
        )
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(
        max_digits=9, default=0, decimal_places=2, verbose_name='общая цена'
    )
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(
        User, verbose_name='пользователь', on_delete=models.CASCADE
        )
    phone = models.CharField(
        max_length=20, verbose_name='номер телефона', null=True, blank=True
        )
    address = models.CharField(
        max_length=255, verbose_name='адрес', null=True, blank=True
        )

    def __str__(self):
        return f"Покупатель: {self.user.first_name} {self.user.last_name}"


class Notebook(Product):
    diagonal = models.CharField(max_length=255, verbose_name='диагональ')
    display_type = models.CharField(max_length=255, verbose_name='тип дисплея')
    processor_freq = models.CharField(
        max_length=255, verbose_name='частота процессора'
        )
    ram = models.CharField(max_length=255, verbose_name='оперативная память')
    video = models.CharField(max_length=255, verbose_name='видеокарта')
    time_without_charge = models.CharField(
        max_length=255, verbose_name='время работы аккумулятора'
        )

    def __str__(self):
        return f"{self.category.name}: {self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Smartphone(Product):
    diagonal = models.CharField(max_length=255, verbose_name='диагональ')
    display_type = models.CharField(
        max_length=255, verbose_name='тип дисплея'
        )
    resolution = models.CharField(
        max_length=255, verbose_name='разрешение экрана'
        )
    accum_volume = models.CharField(
        max_length=255, verbose_name='объем батареи'
        )
    ram = models.CharField(max_length=255, verbose_name='оперативная память')
    sd = models.BooleanField(default=True, verbose_name='наличие SD карты')
    sd_volume_max = models.CharField(
        max_length=255,
        verbose_name='максимальный объем встраиваемой памяти',
        null=True,
        blank=True
        )
    main_cam_mp = models.CharField(
        max_length=255, verbose_name='главная камера'
        )
    frontal_cam_mp = models.CharField(
        max_length=255, verbose_name='фронтальная камера'
        )

    def __str__(self):
        return f"{self.category.name}: {self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')
