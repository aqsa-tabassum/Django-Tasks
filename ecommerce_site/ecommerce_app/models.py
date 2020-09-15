from django.db import models


class ProductCategory(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Product(models.Model):
    name = models.CharField(max_length=100)
    arrival_date = models.DateField()
    price = models.FloatField()
    inventory_count = models.IntegerField(default=0)
    brand = models.CharField(max_length=100)
    vendor = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    category = models.ForeignKey(ProductCategory, on_delete = models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.name, self.category.category)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args,**kwargs)

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in = ids)


class CustomerProductRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    product_name = models.CharField(max_length=100)
    product_type = models.CharField(max_length=100)
    product_description = models.TextField()
    request_seen = models.BooleanField(default=False)

    def __str__(self):
        return '{} {} {}'.format(self.name, self.product_name, self.request_seen)