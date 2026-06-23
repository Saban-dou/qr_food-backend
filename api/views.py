from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MenuCategory, MenuProduct, Restaurant, Table, Order, OrderItem
from .serializers import (
    AccueilSerializer, MenuCategorySerializer, MenuProductSerializer,
    TableSerializer, OrderSerializer, OrderItemSerializer,
)


class AccueilView(APIView):
    """Données dynamiques pour la page d'accueil (acceuil.html)."""

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        restaurant = Restaurant.objects.prefetch_related("features").first()
        if restaurant is None:
            return Response(
                {"detail": "Aucune configuration restaurant. Lancez les migrations."},
                status=503,
            )
        serializer = AccueilSerializer(restaurant)
        return Response(serializer.data)


class MenuView(APIView):
    """Catégories et produits pour la page menu (menu.html)."""

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        categories = MenuCategory.objects.all()
        products = MenuProduct.objects.filter(available=True).select_related("category")

        if not categories.exists():
            return Response(
                {"detail": "Aucun menu configuré. Lancez seed_menu."},
                status=503,
            )

        return Response(
            {
                "title": "Notre Menu",
                "subtitle": " · ".join(c.label for c in categories),
                "categories": MenuCategorySerializer(categories, many=True).data,
                "products": MenuProductSerializer(products, many=True).data,
            }
        )


from django.db.models import Sum, Count
from django.utils import timezone
from rest_framework import status as http_status

from .models import Table, Order, OrderItem


class AdminOrderListView(APIView):
    """GET toutes les commandes / POST nouvelle commande."""
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        orders = Order.objects.prefetch_related("items").select_related("table").all()
        return Response(OrderSerializer(orders, many=True).data)

    def post(self, request):
        data = request.data
        # Générer une référence unique
        last = Order.objects.order_by("-id").first()
        ref_num = (last.id + 1001) if last else 1001
        ref = f"QF-{ref_num}"

        table = None
        if data.get("table"):
            table, _ = Table.objects.get_or_create(
                number=data["table"],
                defaults={"qr_code": f"T{data['table']}-QRF-2026"}
            )

        order = Order.objects.create(
            ref=ref,
            order_type=data.get("order_type", "dine_in"),
            table=table,
            customer_name=data.get("customer_name", ""),
            phone=data.get("phone", ""),
            pickup_time=data.get("pickup_time", ""),
            payment_method=data.get("payment_method", "cash"),
            payment_status=data.get("payment_status", "unpaid"),
            total=data.get("total", 0),
        )
        for item in data.get("items", []):
            OrderItem.objects.create(
                order=order,
                name=item["name"],
                qty=item.get("qty", 1),
                price=item.get("price", 0),
            )
        return Response(OrderSerializer(order).data, status=http_status.HTTP_201_CREATED)


class AdminOrderDetailView(APIView):
    """PATCH pour changer le statut d'une commande."""
    authentication_classes = []
    permission_classes = []

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return None

    def patch(self, request, pk):
        order = self.get_object(pk)
        if not order:
            return Response({"detail": "Commande introuvable."}, status=404)
        for field in ("status", "payment_status", "payment_method"):
            if field in request.data:
                setattr(order, field, request.data[field])
        order.save()
        return Response(OrderSerializer(order).data)


class AdminTableListView(APIView):
    """GET toutes les tables."""
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        tables = Table.objects.prefetch_related("order_set").all()
        return Response(TableSerializer(tables, many=True).data)


class AdminStatsView(APIView):
    """Statistiques du dashboard."""
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        today = timezone.now().date()
        orders_today = Order.objects.filter(created_at__date=today)
        revenue_today = orders_today.filter(payment_status="paid").aggregate(
            total=Sum("total")
        )["total"] or 0
        tables_total = Table.objects.count()
        tables_occupied = Table.objects.filter(
            order__status__in=["pending", "validated", "preparing", "ready"]
        ).distinct().count()
        pending = Order.objects.filter(status="pending").count()

        # 7 derniers jours
        revenue_by_day = []
        orders_by_day = []
        for i in range(6, -1, -1):
            day = today - timezone.timedelta(days=i)
            day_orders = Order.objects.filter(created_at__date=day)
            revenue_by_day.append(
                day_orders.filter(payment_status="paid").aggregate(t=Sum("total"))["t"] or 0
            )
            orders_by_day.append(day_orders.count())

        # Plats populaires
        popular = (
            OrderItem.objects.values("name")
            .annotate(count=Count("id"))
            .order_by("-count")[:5]
        )

        return Response({
            "orders_today": orders_today.count(),
            "revenue_today": revenue_today,
            "tables_occupied": tables_occupied,
            "tables_total": tables_total,
            "pending_orders": pending,
            "popular_dishes": list(popular),
            "revenue_by_day": revenue_by_day,
            "orders_by_day": orders_by_day,
        })