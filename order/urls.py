from django.urls import path

from . import views

app_name = "order"

urlpatterns = [
    path("", views.index, name='orders_index'),
    path("check", views.checkout, name='checkout'),
    path("payment/<int:pk>/", views.payment, name='payment'),
    path("<int:pk>/", views.detail, name='detail')
]