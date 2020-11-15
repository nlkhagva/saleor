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

class PackageType:
    ORDER = "order"
    SELF = "self"
    CARGO = "cargo"

    CHOICES = [
        (ORDER, "Захиалга"),
        (SELF, "Өөрөө авах"),
        (CARGO, "Илгээмж"),
    ]


class PackageNetOrGross:
    NET = "net"  # group of products in an order marked as fulfilled
    GROSS = "gross"  # fulfilled group of products in an order marked as canceled

    CHOICES = [
        (NET, "Цэвэр жин"),
        (GROSS, "Оврийн жин"),
    ]
