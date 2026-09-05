from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from listings.models import CarMake, CarModel, Listing
from users.models import Notification, Profile

from .models import Purchase, PurchaseItem


class CheckoutModelTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.buyer = user_model.objects.create_user(
            username="buyer",
            password="test-password",
        )
        make = CarMake.objects.create(name="Honda")
        model = CarModel.objects.create(name="Civic", car_make=make)
        self.listing = Listing.objects.create(
            car_make=make,
            car_model=model,
            price=18000,
            is_approved=True,
        )

    def test_purchase_and_item_store_snapshot_price(self):
        purchase = Purchase.objects.create(
            buyer=self.buyer,
            purchase_reference="AB12CD34EF56",
            vehicle_total=Decimal("18000.00"),
            delivery_fee=Decimal("100.00"),
            billing_name="Test Buyer",
            billing_email="buyer@example.com",
            billing_address="Billing address",
            delivery_address="Delivery address",
        )
        item = PurchaseItem.objects.create(
            purchase=purchase,
            listing=self.listing,
            agreed_price=Decimal("18000.00"),
        )

        self.assertEqual(purchase.total, Decimal("18100.00"))
        self.assertEqual(item.agreed_price, Decimal("18000.00"))


class CheckoutPageTests(TestCase):
    def test_checkout_page_applies_delivery_fee_below_threshold(self):
        user_model = get_user_model()
        buyer = user_model.objects.create_user(
            username="checkout-buyer",
            password="test-password",
        )
        self.client.force_login(buyer)
        make = CarMake.objects.create(name="Toyota")
        model = CarModel.objects.create(name="Yaris", car_make=make)
        listing = Listing.objects.create(
            car_make=make,
            car_model=model,
            price=19000,
            is_approved=True,
        )
        self.client.post(reverse("select_vehicle", args=[listing.id]))

        response = self.client.get(reverse("checkout:checkout_page"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["selected_listings"]), 1)
        self.assertEqual(response.context["delivery_fee"], Decimal("100.00"))
        self.assertEqual(
            response.context["checkout_total"],
            Decimal("19100.00"),
        )

    def test_create_session_reserves_listing_and_includes_delivery(self):
        user_model = get_user_model()
        buyer = user_model.objects.create_user(
            username="session-buyer",
            password="test-password",
        )
        self.client.force_login(buyer)
        make = CarMake.objects.create(name="Ford")
        model = CarModel.objects.create(name="Focus", car_make=make)
        listing = Listing.objects.create(
            car_make=make,
            car_model=model,
            price=19000,
            is_approved=True,
        )
        self.client.post(reverse("select_vehicle", args=[listing.id]))
        stripe_session = type(
            "StripeSession",
            (),
            {"id": "cs_test_session", "url": "https://checkout.stripe.com/test"},
        )()

        with patch(
            "checkout.views.stripe.checkout.Session.create",
            return_value=stripe_session,
        ) as create_session:
            response = self.client.post(
                reverse("checkout:create_session"),
                {
                    "billing_name": "Test Buyer",
                    "billing_email": "buyer@example.com",
                    "billing_phone": "01234567890",
                    "billing_address": "Billing address",
                    "delivery_address": "Delivery address",
                },
            )

        self.assertRedirects(response, "https://checkout.stripe.com/test", fetch_redirect_response=False)
        purchase = Purchase.objects.get(stripe_checkout_session_id="cs_test_session")
        listing.refresh_from_db()
        self.assertEqual(purchase.delivery_fee, Decimal("100.00"))
        self.assertIsNotNone(listing.checkout_reserved_until)
        line_items = create_session.call_args.kwargs["line_items"]
        self.assertEqual(line_items[-1]["price_data"]["unit_amount"], 10000)
        success_url = create_session.call_args.kwargs["success_url"]
        self.assertIn("{CHECKOUT_SESSION_ID}", success_url)
        self.assertNotIn("%7B", success_url)

    def test_paid_webhook_marks_listing_sold(self):
        user_model = get_user_model()
        buyer = user_model.objects.create_user(
            username="webhook-buyer",
            password="test-password",
        )
        make = CarMake.objects.create(name="Volvo")
        model = CarModel.objects.create(name="XC40", car_make=make)
        listing = Listing.objects.create(
            car_make=make,
            car_model=model,
            price=18000,
            is_approved=True,
        )
        purchase = Purchase.objects.create(
            buyer=buyer,
            vehicle_total=Decimal("18000.00"),
            delivery_fee=Decimal("100.00"),
            billing_name="Test Buyer",
            billing_email="buyer@example.com",
            billing_address="Billing address",
            delivery_address="Delivery address",
        )
        PurchaseItem.objects.create(
            purchase=purchase,
            listing=listing,
            agreed_price=Decimal("18000.00"),
        )
        event = {
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "id": "cs_test_paid",
                    "payment_status": "paid",
                    "payment_intent": "pi_test_paid",
                    "metadata": {"purchase_id": str(purchase.id)},
                },
            },
        }

        with patch("checkout.views.stripe.Webhook.construct_event", return_value=event):
            response = self.client.post(
                reverse("checkout:webhook"),
                data=b"{}",
                content_type="application/json",
                HTTP_STRIPE_SIGNATURE="test-signature",
            )

        self.assertEqual(response.status_code, 200)
        purchase.refresh_from_db()
        listing.refresh_from_db()
        self.assertEqual(purchase.payment_status, Purchase.Status.PAID)
        self.assertTrue(listing.is_sold)
        self.assertTrue(
            Notification.objects.filter(
                profile__user=buyer,
                subject="Purchase confirmed",
            ).exists()
        )

    def test_success_page_clears_bag_and_shows_purchase_items(self):
        user_model = get_user_model()
        buyer = user_model.objects.create_user(
            username="success-buyer",
            password="test-password",
        )
        make = CarMake.objects.create(name="Honda")
        model = CarModel.objects.create(name="Civic", car_make=make)
        listing = Listing.objects.create(
            car_make=make,
            car_model=model,
            price=18000,
            is_approved=True,
        )
        purchase = Purchase.objects.create(
            buyer=buyer,
            stripe_checkout_session_id="cs_test_success",
            vehicle_total=Decimal("18000.00"),
            delivery_fee=Decimal("100.00"),
            billing_name="Test Buyer",
            billing_email="buyer@example.com",
            billing_address="Billing address",
            delivery_address="Delivery address",
        )
        PurchaseItem.objects.create(
            purchase=purchase,
            listing=listing,
            agreed_price=Decimal("18000.00"),
        )
        session = self.client.session
        session["selected_vehicle_ids"] = [str(listing.id)]
        session.save()
        self.client.force_login(buyer)

        response = self.client.get(
            reverse("checkout:success"),
            {"session_id": "cs_test_success"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session["selected_vehicle_ids"], [])
        self.assertContains(response, "Honda Civic")

    def test_sale_pending_vehicle_cannot_be_selected(self):
        user_model = get_user_model()
        buyer = user_model.objects.create_user(
            username="pending-buyer",
            password="test-password",
        )
        make = CarMake.objects.create(name="Kia")
        model = CarModel.objects.create(name="Niro", car_make=make)
        listing = Listing.objects.create(
            car_make=make,
            car_model=model,
            price=18000,
            is_approved=True,
            is_sold=True,
        )
        self.client.force_login(buyer)

        response = self.client.post(reverse("select_vehicle", args=[listing.id]))

        self.assertRedirects(response, reverse("listings_page"))
        self.assertEqual(
            self.client.session.get("selected_vehicle_ids", []),
            [],
        )

    def test_admin_can_reject_paid_sale_and_relist_vehicle(self):
        admin = User.objects.create_user(
            username="admin",
            password="test-password",
            is_staff=True,
        )
        admin_profile = Profile.objects.get(user=admin)
        buyer = User.objects.create_user(
            username="sale-buyer",
            password="test-password",
        )
        buyer_profile = Profile.objects.get(user=buyer)
        make = CarMake.objects.create(name="Audi")
        model = CarModel.objects.create(name="A4", car_make=make)
        listing = Listing.objects.create(
            car_make=make,
            car_model=model,
            price=18000,
            is_approved=True,
            is_sold=True,
        )
        purchase = Purchase.objects.create(
            buyer=buyer,
            vehicle_total=Decimal("18000.00"),
            delivery_fee=Decimal("100.00"),
            payment_status=Purchase.Status.PAID,
            billing_name="Sale Buyer",
            billing_email="buyer@example.com",
            billing_address="Billing address",
            delivery_address="Delivery address",
        )
        PurchaseItem.objects.create(
            purchase=purchase,
            listing=listing,
            agreed_price=Decimal("18000.00"),
        )
        self.client.force_login(admin)

        response = self.client.post(
            reverse("checkout:sale_reviews"),
            {"purchase_id": purchase.id, "action": "reject"},
        )

        self.assertRedirects(response, reverse("checkout:sale_reviews"))
        listing.refresh_from_db()
        purchase.refresh_from_db()
        self.assertFalse(listing.is_sold)
        self.assertEqual(purchase.sale_status, Purchase.SaleStatus.REJECTED)
        self.assertTrue(
            Notification.objects.filter(
                profile=buyer_profile,
                subject="Sale rejected",
            ).exists()
        )
        self.assertFalse(
            Notification.objects.filter(
                profile=admin_profile,
                subject="Sale requires approval",
            ).exists()
        )

    def test_cancelling_duplicate_sale_does_not_relist_genuine_sale(self):
        admin = User.objects.create_user(
            username="duplicate-admin",
            password="test-password",
            is_staff=True,
        )
        genuine_buyer = User.objects.create_user(
            username="genuine-buyer",
            password="test-password",
        )
        duplicate_buyer = User.objects.create_user(
            username="duplicate-buyer",
            password="test-password",
        )
        make = CarMake.objects.create(name="Nissan")
        model = CarModel.objects.create(name="Leaf", car_make=make)
        listing = Listing.objects.create(
            car_make=make,
            car_model=model,
            price=18000,
            is_approved=True,
            is_sold=True,
        )
        genuine_purchase = Purchase.objects.create(
            buyer=genuine_buyer,
            payment_status=Purchase.Status.PAID,
            sale_status=Purchase.SaleStatus.APPROVED,
            vehicle_total=Decimal("18000.00"),
            billing_name="Genuine Buyer",
            billing_email="genuine@example.com",
            billing_address="Billing address",
            delivery_address="Delivery address",
        )
        duplicate_purchase = Purchase.objects.create(
            buyer=duplicate_buyer,
            payment_status=Purchase.Status.PAID,
            sale_status=Purchase.SaleStatus.APPROVED,
            vehicle_total=Decimal("18000.00"),
            billing_name="Duplicate Buyer",
            billing_email="duplicate@example.com",
            billing_address="Billing address",
            delivery_address="Delivery address",
        )
        PurchaseItem.objects.create(
            purchase=genuine_purchase,
            listing=listing,
            agreed_price=Decimal("18000.00"),
        )
        PurchaseItem.objects.create(
            purchase=duplicate_purchase,
            listing=listing,
            agreed_price=Decimal("18000.00"),
        )

        self.client.force_login(admin)
        response = self.client.post(
            reverse("checkout:sale_reviews"),
            {"purchase_id": duplicate_purchase.id, "action": "cancel"},
        )

        self.assertRedirects(response, reverse("checkout:sale_reviews"))
        duplicate_purchase.refresh_from_db()
        listing.refresh_from_db()
        self.assertEqual(
            duplicate_purchase.sale_status,
            Purchase.SaleStatus.CANCELLED,
        )
        self.assertTrue(listing.is_sold)

        self.client.post(
            reverse("checkout:sale_reviews"),
            {"purchase_id": duplicate_purchase.id, "action": "relist"},
        )
        listing.refresh_from_db()
        self.assertTrue(listing.is_sold)