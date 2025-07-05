from django.contrib import admin
from .models import Asset, LandAsset, TangibleAsset, ShareAsset, TangibleAssetType

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'type', 'purchase_date', 'value')
    list_filter = ('type', 'user')
    search_fields = ('name', 'user__username')

@admin.register(LandAsset)
class LandAssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'location', 'area', 'ownership')
    search_fields = ('name', 'location')

@admin.register(TangibleAssetType)
class TangibleAssetTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    search_fields = ('name',)

@admin.register(TangibleAsset)
class TangibleAssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'asset_type', 'weight', 'quality')
    search_fields = ('name', 'quality')

@admin.register(ShareAsset)
class ShareAssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'number_of_shares', 'market_price')
    search_fields = ('name', 'company_name')
