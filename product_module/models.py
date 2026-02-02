from tkinter.constants import CASCADE
from django.db import models
from django.utils import timezone

from user_module.models import User


# Create your models here.


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام دسته بندی')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='عنوان در url')
    parent = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, max_length=100, verbose_name='والد', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.name


class ProductBrand(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام برند')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام محصول')
    price = models.IntegerField(verbose_name='قیمت محصول')
    discount_price = models.PositiveIntegerField(verbose_name='قیمت با تخفیف', null=True, blank=True)
    start_discount = models.DateTimeField(verbose_name='زمان شروع تخفیف', null=True, blank=True)
    end_discount = models.DateTimeField(verbose_name='زمان پایان تخفیف', null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='دسته بندی')
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, verbose_name='برند محصول')
    image = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='تصویر محصول')
    short_description = models.CharField(max_length=300, verbose_name="توضیحات کوتاه")
    description = models.TextField(verbose_name='توضیحات')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(verbose_name='فعال / غیر فعال')
    is_deleted = models.BooleanField(verbose_name='موجود / ناموجود')

    def check_price(self):
        if self.discount_price:
            if self.discount_price < self.price:
                return self.discount_price < self.price

        return False

    # def discount_percent(self):
    #     if self.check_price():
    #         return (self.price - self.discount_price) / self.price * 100
    #     return 0

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return f'({self.name}) : ({self.price})'


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to='images/product_gallery', verbose_name='تصویر')

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'گالری تصویر'
        verbose_name_plural = 'گالری تصاویر'


class ProductSpecificationGroup(models.Model):
    title = models.CharField(verbose_name='عنوان', max_length=200)
    category = models.ForeignKey(ProductCategory,on_delete=models.CASCADE, verbose_name='دسته بندی')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی مشخصات'
        verbose_name_plural = 'دسته بندی مشخصات'


class ProductSpecification(models.Model):
    title = models.CharField(verbose_name='عنوان', max_length=200)
    value = models.CharField(verbose_name='ویژگی', max_length=200)
    group = models.ForeignKey(ProductSpecificationGroup, on_delete=models.CASCADE, verbose_name='دسته بندی مشخصات')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')

    def __str__(self):
        return f'({self.title}) : {self.value}'

    class Meta:
        verbose_name = 'شاخص'
        verbose_name_plural = 'مشخصات'


class ProductVisit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='کاربر')
    ip = models.CharField(max_length=30, verbose_name='IP')

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدیدهای محصول'

    def __str__(self):
        return f'({self.product.name}) : {self.ip}'


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    parent = models.ForeignKey('ProductComment', on_delete=models.CASCADE, null=True, blank=True, verbose_name='والد')
    create_date = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='تاریخ ثبت')
    text = models.TextField(verbose_name='متن کامنت')

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

    def __str__(self):
        return self.user.get_full_name()