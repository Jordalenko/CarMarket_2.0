from django.urls import path

from . import views


app_name = "checkout"

urlpatterns = [
    path("", views.checkout_page, name="checkout_page"),
    path("create-session/", views.create_checkout_session, name="create_session"),
    path("success/", views.checkout_success, name="success"),
    path("cancel/", views.checkout_cancel, name="cancel"),
    path("purchases/", views.purchase_history, name="purchase_history"),
    path("sale-reviews/", views.sale_reviews, name="sale_reviews"),
    path("webhook/", views.stripe_webhook, name="webhook"),
]