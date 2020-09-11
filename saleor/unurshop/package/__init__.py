class PackageStatus:
    DRAFT = "draft"
    NEW = "new"
    SHIPPING = "shipping"
    INMONGOLIA = "inmongolia"
    RECEIVED = "received"
    DELAYED = "delayed"
    CANCELED = "canceled"

    CHOICES = [
        (NEW, "New"),
        (DRAFT, "Draft"),
        (SHIPPING, "Shipping"),
        (INMONGOLIA, "In Mongolia"),
        (RECEIVED, "Received"),
        (DELAYED, "Delayed"),
        (CANCELED, "Canceled")
    ]
