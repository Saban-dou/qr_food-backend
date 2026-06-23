from rest_framework import serializers

from .models import HomeFeature, MenuCategory, MenuProduct, OrderModeOption, Restaurant


class HomeFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeFeature
        fields = ("icon", "title", "description", "order")


class OrderModeOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModeOption
        fields = (
            "slug",
            "title",
            "description",
            "icon",
            "button_label",
            "button_variant",
            "enabled",
            "order",
        )


class AccueilSerializer(serializers.ModelSerializer):
    features = HomeFeatureSerializer(many=True, read_only=True)
    order_modes = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = (
            "name",
            "hero_badge",
            "hero_title",
            "hero_subtitle",
            "hero_text",
            "modes_title",
            "modes_subtitle",
            "cta_title",
            "cta_text",
            "location",
            "hours",
            "is_open",
            "features",
            "order_modes",
        )

    def get_order_modes(self, obj):
        modes = OrderModeOption.objects.filter(enabled=True)
        return OrderModeOptionSerializer(modes, many=True).data


class MenuCategorySerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="slug")

    class Meta:
        model = MenuCategory
        fields = ("id", "label", "icon", "order")


class MenuProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category_id")

    class Meta:
        model = MenuProduct
        fields = ("id", "slug", "name", "category", "description", "price", "image")


from .models import Table, Order, OrderItem


class TableSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    order_id = serializers.SerializerMethodField()
    qr = serializers.CharField(source="qr_code")

    class Meta:
        model = Table
        fields = ("id", "number", "qr", "status", "order_id")

    def get_status(self, obj):
        active = obj.order_set.filter(status__in=["pending", "validated", "preparing", "ready"]).first()
        return "occupied" if active else "free"

    def get_order_id(self, obj):
        active = obj.order_set.filter(status__in=["pending", "validated", "preparing", "ready"]).first()
        return active.ref if active else None


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("name", "qty", "price")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    table = serializers.SerializerMethodField()
    customer = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "id", "ref", "order_type", "table", "customer_name", "phone",
            "pickup_time", "status", "payment_method", "payment_status",
            "total", "items", "customer", "time", "date",
        )

    def get_table(self, obj):
        return obj.table.number if obj.table else None

    def get_customer(self, obj):
        if obj.order_type == "dine_in" and obj.table:
            return f"Client — Table {obj.table.number}"
        return f"{obj.customer_name} — À emporter"

    def get_time(self, obj):
        return obj.created_at.strftime("%H:%M")

    def get_date(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")
