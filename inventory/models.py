from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator

class InventoryOrderManager(models.Manager):
    def get_item_with_no_location(self):
        return super().get_queryset().filter(location_text__isnull=True)

    def get_item_by_location(self, location):
        return super().get_queryset().filter(location_text=location)

class Item(models.Model):
    name_text = models.CharField(max_length=200, blank=False, null=False)
    quantity_integer = models.PositiveIntegerField(validators=[MaxValueValidator(9999999999)], blank=False, null=False)
    link_text = models.CharField(max_length=200, blank=True, null=True)
    price_decimal = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    description_text = models.CharField(max_length=400, blank=True, null=True)
    location_text = models.CharField(max_length=200, blank=True, null=True)
    vendor_text = models.CharField(max_length=200, blank=True, null=True)
    vendor_id_text = models.CharField(max_length=200, blank=True, null=True)
    manufacturer_text = models.CharField(max_length=200, blank=True, null=True)
    manufacturer_id_text = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    objects = InventoryOrderManager()

    def __str__(self):
        return self.name_text

class History(models.Model):
    item_object = models.ForeignKey(Item, on_delete=models.CASCADE)
    username_text = models.CharField(max_length=30, blank=False, null=False)
    type_text = models.CharField(max_length=50, blank=True, null=True)
    quantity_integer = models.PositiveIntegerField(blank=False, null=False)
    last_modified_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.item_object.name_text

    class Meta: 
        ordering = (['-last_modified_date'])
