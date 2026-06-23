from django.core.management.base import BaseCommand

from api.models import HomeFeature, OrderModeOption, Restaurant


class Command(BaseCommand):
    help = "Peuple les données initiales pour la page d'accueil (acceuil.html)."

    def handle(self, *args, **options):
        restaurant, created = Restaurant.objects.get_or_create(
            pk=1,
            defaults={
                "name": "QR Food Djibouti",
                "hero_badge": "Scan & Commande",
                "hero_title": "Commandez en un scan,",
                "hero_subtitle": "savourez sans attendre",
                "hero_text": (
                    "Sur place ou à emporter — commandez depuis votre téléphone, "
                    "sans application à installer."
                ),
                "modes_title": "Comment souhaitez-vous commander ?",
                "modes_subtitle": "Choisissez une option — pas de livraison à domicile",
                "cta_title": "Prêt à commander ?",
                "cta_text": "Découvrez burgers, pizzas, boissons et desserts.",
                "location": "Djibouti-ville",
                "hours": "11h – 23h",
                "is_open": True,
            },
        )

        features = [
            ("bi-qr-code-scan", "Sur place ou à emporter", "Deux modes simples, adaptés à votre situation.", 0),
            ("bi-lightning-charge", "Commande rapide", "Menu clair, ajout au panier en un clic.", 1),
            ("bi-phone", "Mobile Money", "Payez par Mobile Money ou en espèces.", 2),
        ]
        for icon, title, description, order in features:
            HomeFeature.objects.update_or_create(
                restaurant=restaurant,
                title=title,
                defaults={"icon": icon, "description": description, "order": order},
            )

        modes = [
            (
                "dine_in",
                "Sur place",
                "Vous mangez au restaurant. Scannez le QR sur votre table ou indiquez votre numéro de table au paiement.",
                "bi-qr-code-scan",
                "Commander sur place",
                "primary",
                0,
            ),
            (
                "takeaway",
                "À emporter",
                "Vous récupérez votre commande au comptoir. Indiquez votre nom et l'heure de retrait au paiement.",
                "bi-bag-check",
                "Commander à emporter",
                "outline",
                1,
            ),
        ]
        for slug, title, description, icon, button_label, button_variant, order in modes:
            OrderModeOption.objects.update_or_create(
                slug=slug,
                defaults={
                    "title": title,
                    "description": description,
                    "icon": icon,
                    "button_label": button_label,
                    "button_variant": button_variant,
                    "enabled": True,
                    "order": order,
                },
            )

        action = "créé" if created else "mis à jour"
        self.stdout.write(self.style.SUCCESS(f"Restaurant {action} — accueil prêt pour l'API."))
