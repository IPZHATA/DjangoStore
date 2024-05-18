from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import contact, index

urlpatterns = [
    path("", index, name="index"),
    path("contact/", contact, name="contact"),
    path("admin/", admin.site.urls),
    path("items/", include("item.urls")),
    path("orders/", include("order.urls")),
    path("cart/", include("cart.urls"), name="cart"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
