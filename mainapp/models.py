from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Product(models.Model):
    category = models.ForeignKey(
        Category, verbose_name='категория', on_delete=models.CASCADE
        )
    title = models.CharField(max_length=255, verbose_name='наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='изображение')
    description = models.TextField(verbose_name='описание', null=True)
    price = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name='цена'
        )

    def __str__(self):
        return self.title

class CartProduct(models.Model):
    user = models.ForeignKey(
        'Customer', verbose_name='покупатель', on_delete=models.CASCADE
        )
    cart = models.ForeignKey(
        'Cart', verbose_name='корзина', on_delete=models.CASCADE,
        related_name='related_products'
        )
    product = models.ForeignKey(
        Product, verbose_name='товар', on_delete=models.CASCADE
        )
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name='общая цена'
        )

    def __str__(self):
        return f"Продукт: {self.product.title} (для корзины)"


class Cart(models.Model):
    owner = models.ForeignKey(
        'Customer', verbose_name='владелец', on_delete=models.CASCADE
        )
    products = models.ManyToManyField(
        CartProduct, blank=True, related_name='related_cart'
        )
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name='общая цена'
    )

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(
        User, verbose_name='пользователь', on_delete=models.CASCADE
        )
    phone = models.CharField(max_length=20, verbose_name='номер телефона')
    address = models.CharField(max_length=255, verbose_name='адрес')

    def __str__(self):
        return f"Покупатель: {self.user.first_name} {self.user.last_name}"


class Specification(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    name = models.CharField(
        max_length=255, verbose_name='имя товара для характеристик'
        )

    def __str__(self):
        return f"Характеристики для товара: {self.name}"
