from django.urls import path
from .views import (
    AccueilView, MenuView,
    AdminOrderListView, AdminOrderDetailView,
    AdminTableListView, AdminStatsView,
)

urlpatterns = [
    # Frontend client
    path("accueil/", AccueilView.as_view(), name="accueil"),
    path("menu/", MenuView.as_view(), name="menu"),

    # Dashboard admin
    path("admin/orders/", AdminOrderListView.as_view(), name="admin-orders"),
    path("admin/orders/<int:pk>/", AdminOrderDetailView.as_view(), name="admin-order-detail"),
    path("admin/tables/", AdminTableListView.as_view(), name="admin-tables"),
    path("admin/stats/", AdminStatsView.as_view(), name="admin-stats"),
]
