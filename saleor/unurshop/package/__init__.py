class PackageStatus:
    DRAFT = "draft"
    SHIPPING = "shipping"
    INMONGOLIA = "inmongolia"
    RECEIVED = "received"
    DELAYED = "delayed"
    CANCELED = "canceled"

    CHOICES = [
        (DRAFT, "Draft"),
        (SHIPPING, "Shipping"),
        (INMONGOLIA, "In Mongolia"),
        (RECEIVED, "Received"),
        (DELAYED, "Delayed"),
        (CANCELED, "Canceled")
    ]
