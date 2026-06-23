from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=120, default="QR Food Djibouti")
    hero_badge = models.CharField(max_length=120, default="Scan & Commande")
    hero_title = models.CharField(max_length=200, default="Commandez en un scan,")
    hero_subtitle = models.CharField(max_length=200, default="savourez sans attendre")
    hero_text = models.TextField(
        default="Sur place ou à emporter — commandez depuis votre téléphone, sans application à installer."
    )
    modes_title = models.CharField(max_length=200, default="Comment souhaitez-vous commander ?")
    modes_subtitle = models.CharField(
        max_length=200, default="Choisissez une option — pas de livraison à domicile"
    )
    cta_title = models.CharField(max_length=200, default="Prêt à commander ?")
    cta_text = models.CharField(
        max_length=200, default="Découvrez burgers, pizzas, boissons et desserts."
    )
    location = models.CharField(max_length=200, default="Djibouti-ville")
    hours = models.CharField(max_length=120, default="11h – 23h")
    is_open = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"

    def __str__(self):
        return self.name


class HomeFeature(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="features"
    )
    icon = models.CharField(max_length=60, default="bi-star")
    title = models.CharField(max_length=120)
    description = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Atout accueil"
        verbose_name_plural = "Atouts accueil"

    def __str__(self):
        return self.title


class OrderModeOption(models.Model):
    BUTTON_VARIANTS = [
        ("primary", "Primary"),
        ("outline", "Outline"),
    ]

    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=120)
    description = models.TextField()
    icon = models.CharField(max_length=60, default="bi-bag")
    button_label = models.CharField(max_length=80)
    button_variant = models.CharField(max_length=20, choices=BUTTON_VARIANTS, default="primary")
    enabled = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Mode de commande"
        verbose_name_plural = "Modes de commande"

    def __str__(self):
        return self.title


class MenuCategory(models.Model):
    slug = models.SlugField(primary_key=True, max_length=40)
    label = models.CharField(max_length=80)
    icon = models.CharField(max_length=60, default="bi-grid")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "slug"]
        verbose_name = "Catégorie menu"
        verbose_name_plural = "Catégories menu"

    def __str__(self):
        return self.label


class MenuProduct(models.Model):
    slug = models.SlugField(unique=True, max_length=80)
    name = models.CharField(max_length=120)
    category = models.ForeignKey(
        MenuCategory, on_delete=models.PROTECT, related_name="products"
    )
    description = models.TextField()
    price = models.PositiveIntegerField(help_text="Prix en FDJ")
    image = models.URLField(max_length=500)
    available = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Produit menu"
        verbose_name_plural = "Produits menu"

    def __str__(self):
        return self.name


class Table(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    qr_code = models.CharField(max_length=40, unique=True)

    class Meta:
        ordering = ["number"]
        verbose_name = "Table"
        verbose_name_plural = "Tables"

    def __str__(self):
        return f"Table {self.number}"


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "En attente"),
        ("validated", "Validée"),
        ("preparing", "En préparation"),
        ("ready", "Prête"),
        ("served", "Servie"),
        ("cancelled", "Annulée"),
    ]
    TYPE_CHOICES = [
        ("dine_in", "Sur place"),
        ("takeaway", "À emporter"),
    ]
    PAYMENT_METHOD_CHOICES = [
        ("mobile_money", "Mobile Money"),
        ("cash", "Espèces"),
    ]
    PAYMENT_STATUS_CHOICES = [
        ("paid", "Payée"),
        ("unpaid", "Non payée"),
    ]

    ref = models.CharField(max_length=20, unique=True)  # ex: QF-1042
    order_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    table = models.ForeignKey(Table, null=True, blank=True, on_delete=models.SET_NULL)
    customer_name = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    pickup_time = models.CharField(max_length=10, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="pending")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default="cash")
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default="unpaid")
    total = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"

    def __str__(self):
        return self.ref


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=120)
    qty = models.PositiveSmallIntegerField(default=1)
    price = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Ligne de commande"
        verbose_name_plural = "Lignes de commande"

    def __str__(self):
        return f"{self.qty}x {self.name}"
