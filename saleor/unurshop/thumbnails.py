from ..celeryconf import app
from ..core.utils import create_thumbnails
from .models import Shop


@app.task
def create_ushop_logo_image_thumbnails(ushop_id):
    """Take a Product model and create the background image thumbnails for it."""
    create_thumbnails(
        pk=ushop_id,
        model=Shop,
        size_set="user_avatars",
        image_attr="avatar",
    )
