from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=150)
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title


STARS = (
    (1, '*'),
    (2, '**'),
    (3, '***'),
    (4, '****'),
    (5, '*****'),
)


class Review(models.Model):
    text = models.CharField(max_length=100)
    value = models.IntegerField(choices=STARS)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='reviews')

    def __str__(self):
        return self.text
