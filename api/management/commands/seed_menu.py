from django.core.management.base import BaseCommand

from api.models import MenuCategory, MenuProduct


class Command(BaseCommand):
    help = "Peuple le menu (catégories et produits) pour menu.html."

    def handle(self, *args, **options):
        categories = [
            ("burgers", "Burgers", "bi-fire", 0),
            ("pizza", "Pizza", "bi-circle", 1),
            ("boissons", "Boissons", "bi-cup-straw", 2),
            ("desserts", "Desserts", "bi-heart", 3),
        ]
        for slug, label, icon, order in categories:
            MenuCategory.objects.update_or_create(
                slug=slug,
                defaults={"label": label, "icon": icon, "order": order},
            )

        products = [
            (
                1,
                "burger-classic",
                "Burger Classic",
                "burgers",
                "Steak haché, cheddar, salade, tomate, sauce maison.",
                2500,
                "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600&q=80",
                0,
            ),
            (
                2,
                "burger-djibouti",
                "Burger Djibouti",
                "burgers",
                "Épices locales, oignons caramélisés, fromage fondu.",
                3200,
                "https://images.unsplash.com/photo-1550547660-d9450f859349?w=600&q=80",
                1,
            ),
            (
                3,
                "burger-veggie",
                "Burger Végétarien",
                "burgers",
                "Galette lentilles, avocat, roquette, sauce yaourt.",
                2800,
                "https://images.unsplash.com/photo-1520072959219-c962dc7182ba?w=600&q=80",
                2,
            ),
            (
                4,
                "pizza-margherita",
                "Pizza Margherita",
                "pizza",
                "Tomate, mozzarella, basilic frais.",
                3500,
                "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=600&q=80",
                0,
            ),
            (
                5,
                "pizza-4-fromages",
                "Pizza 4 Fromages",
                "pizza",
                "Mozzarella, gorgonzola, parmesan, chèvre.",
                4200,
                "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600&q=80",
                1,
            ),
            (
                6,
                "pizza-poulet",
                "Pizza Poulet BBQ",
                "pizza",
                "Poulet grillé, oignons, sauce barbecue.",
                4500,
                "https://images.unsplash.com/photo-1628840042765-356cda07504e?w=600&q=80",
                2,
            ),
            (
                7,
                "jus-orange",
                "Jus d'Orange Frais",
                "boissons",
                "Pressé sur place, sans sucre ajouté.",
                800,
                "https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?w=600&q=80",
                0,
            ),
            (
                8,
                "coca-cola",
                "Coca-Cola",
                "boissons",
                "33 cl, servi frais.",
                500,
                "https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=600&q=80",
                1,
            ),
            (
                9,
                "the-menthe",
                "Thé à la Menthe",
                "boissons",
                "Thé vert, menthe fraîche.",
                600,
                "https://images.unsplash.com/photo-1556678137-a08586f10d4d?w=600&q=80",
                2,
            ),
            (
                10,
                "tiramisu",
                "Tiramisu",
                "desserts",
                "Mascarpone, café, cacao.",
                1500,
                "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=600&q=80",
                0,
            ),
            (
                11,
                "mousse-chocolat",
                "Mousse au Chocolat",
                "desserts",
                "Chocolat noir 70%.",
                1200,
                "https://images.unsplash.com/photo-1541783245831-57603bbbf8e0?w=600&q=80",
                1,
            ),
            (
                12,
                "salade-fruits",
                "Salade de Fruits",
                "desserts",
                "Mangue, papaye, ananas.",
                1000,
                "https://images.unsplash.com/photo-1564093497590-59358234fb39?w=600&q=80",
                2,
            ),
        ]

        for pk, slug, name, cat_slug, description, price, image, order in products:
            MenuProduct.objects.update_or_create(
                id=pk,
                defaults={
                    "slug": slug,
                    "name": name,
                    "category_id": cat_slug,
                    "description": description,
                    "price": price,
                    "image": image,
                    "available": True,
                    "order": order,
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Menu prêt — {MenuCategory.objects.count()} catégories, "
                f"{MenuProduct.objects.count()} produits."
            )
        )
