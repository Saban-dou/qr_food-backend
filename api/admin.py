from django.contrib import admin

from .models import HomeFeature, MenuCategory, MenuProduct, OrderModeOption, Restaurant


class HomeFeatureInline(admin.TabularInline):
    model = HomeFeature
    extra = 0


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "is_open", "updated_at")
    inlines = [HomeFeatureInline]


@admin.register(OrderModeOption)
class OrderModeOptionAdmin(admin.ModelAdmin):
    list_display = ("slug", "title", "enabled", "order")
    list_editable = ("enabled", "order")


class MenuProductInline(admin.TabularInline):
    model = MenuProduct
    extra = 0


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ("slug", "label", "order")
    list_editable = ("order",)
    inlines = [MenuProductInline]


@admin.register(MenuProduct)
class MenuProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "available", "order")
    list_filter = ("category", "available")
    list_editable = ("available", "order")
