from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def get_fields_for_filter_in_template(self):
        return ProductFeatures.objects.filter(
            category=self,
            use_in_filter=True
        ).prefetch_related('category').value(
            'feature_key',
            'feature_measure',
            'feature_name',
            'filter_type'
        )


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

    def get_model_name(self):
        return self.__class__.__name__.lower()

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})


class ProductFeatures(models.Model):

    RADIO = 'radio'
    CHECKBOX = 'checkbox'

    FILTER_TYPE_CHOICES = (
        (RADIO, 'радиокнопка'),
        (CHECKBOX, 'Чекбокс')
    )

    feature_key = models.CharField(
        max_length=100, verbose_name='ключ характеристики'
        )
    feature_name = models.CharField(
        max_length=255, verbose_name='наименование характеристики'
        )
    category = models.ForeignKey(
        Category, verbose_name='категории', on_delete=models.CASCADE
        )
    postfix_for_value = models.CharField(
        max_length=20, null=True, blank=True,
        verbose_name='постфикс для значения',
        help_text=f'например для характеристики "Часы работы" к значению ' \
                f'можно добавить постфикс "часов" и как результат значение ' \
                f'"10 часов"'
        )
    use_in_filter = models.BooleanField(
        default=False,
        verbose_name='использовать в фильтрации товаров в шаблоне'
        )
    filter_type = models.CharField(
        max_length=20, verbose_name='тип фильтра', default=CHECKBOX,
        choices=FILTER_TYPE_CHOICES
        )
    filter_measure = models.CharField(
        max_length=50, verbose_name='единица измерения для фильтра',
        help_text='единица измерения для конкретного фильтра'
        )

    def __str__(self):
        return f'Категория - "{self.category.name}" | ' \
            f'Характеристика - "{self.feature_name}" | ' \
            f'Значение = "{self.feature_value}"'


class ProductFeatureValidators(models.Model):

    category = models.ForeignKey(
        Category, verbose_name='категории', on_delete=models.CASCADE
        )
    feature = models.ForeignKey(
        ProductFeatures, verbose_name='характеристики', null=True, blank=True,
        on_delete=models.CASCADE
        )
    feature_value = models.CharField(
        max_length=255, unique=True, null=True, blank=True,
        verbose_name='значение характеристики'
        )

    def __str__(self):
        if not self.feature:
            return f'Валидотор категории "{self.category.name}" - '\
                f'характеристика не выбрана'
        return f'Валидатор категории "{self.category.name}" |' \
                f'Характеристика - "{self.feature.feature_name}"'


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

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey(
        'Customer', null=True, verbose_name='владелец',
        on_delete=models.CASCADE
        )
    products = models.ManyToManyField(
        CartProduct, blank=True, related_name='related_cart'
        )
    total_products = models.PositiveIntegerField(default=0, null=True)
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
    orders = models.ManyToManyField(
        'Order', verbose_name='Заказы покупателя',
        related_name='related_customer'
        )

    def __str__(self):
        return f"Покупатель: {self.user.first_name} {self.user.last_name}"


class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'новый заказ'),
        (STATUS_IN_PROGRESS, 'заказ в обработке'),
        (STATUS_READY, 'заказ готов'),
        (STATUS_COMPLETED, 'заказ выполнен')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'самовывоз'),
        (BUYING_TYPE_DELIVERY, 'доставка'),
    )

    customer = models.ForeignKey(
        Customer, verbose_name='покупатель', related_name='related_orders',
        on_delete=models.CASCADE
        )
    first_name = models.CharField(max_length=255, verbose_name='имя')
    last_name = models.CharField(max_length=255, verbose_name='фамилия')
    phone = models.CharField(max_length=20, verbose_name='телефон')
    cart = models.ForeignKey(
        Cart, verbose_name='корзина', on_delete=models.CASCADE, null=True,
        blank=True
        )
    address = models.CharField(
        max_length=255, verbose_name='адрес доставки', null=True, blank=True
        )
    status = models.CharField(
        max_length=100, verbose_name='статус заказа', choices=STATUS_CHOICES,
        default=STATUS_NEW
        )
    buying_type = models.CharField(
        max_length=100, verbose_name='тип заказа', choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
        )
    comment = models.TextField(
        verbose_name='комментарий к заказу', null=True, blank=True
        )
    created_at = models.DateTimeField(
        auto_now=True, verbose_name='дата создания заказа'
        )
    order_date = models.DateField(
        verbose_name='дата получения заказа', default=timezone.now
        )

    def __str__(self):
        return str(self.id)
