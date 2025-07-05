from django.db import models
from django.conf import settings

class Asset(models.Model):
    ASSET_TYPE_CHOICES = [
        ('land', 'Land'),
        ('tangible', 'Tangible (Gold, Silver, ect)'),
        ('share', 'Share'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    purchase_date = models.DateField()
    value = models.DecimalField(max_digits=12, decimal_places=2)
    document = models.FileField(upload_to='asset_documents/', blank=True, null=True)
    type = models.CharField(max_length=20, choices=ASSET_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

class LandAsset(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    area = models.DecimalField(max_digits=10, decimal_places=2, help_text='Size in Square Feet')
    ownership = models.DecimalField(max_digits=3, decimal_places=2, help_text='Ownership in present')

class TangibleAssetType(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Price per Grams')

    def __str__(self):
        return f'{self.name} - {self.price}'

class TangibleAsset(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    asset_type = models.ForeignKey(TangibleAssetType, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=10, decimal_places=2, help_text='Weight in Grams')
    quality = models.CharField(max_length=100)

class ShareAsset(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    number_of_shares = models.PositiveIntegerField()
    market_price = models.DecimalField(max_digits=12, decimal_places=2)
