from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Notification, Profile


class InboxReplyTests(TestCase):
	def setUp(self):
		user_model = get_user_model()
		self.buyer = user_model.objects.create_user(
			username="buyer",
			password="test-password",
		)
		self.admin = user_model.objects.create_user(
			username="admin",
			password="test-password",
			is_staff=True,
		)
		self.buyer_profile = Profile.objects.get(user=self.buyer)
		self.admin_profile = Profile.objects.get(user=self.admin)

	def test_user_reply_is_received_by_admin(self):
		notification = Notification.objects.create(
			profile=self.buyer_profile,
			sender=self.admin_profile,
			subject="Original message",
			message="Please review this.",
		)

		self.client.force_login(self.buyer)
		response = self.client.post(
			reverse("inbox"),
			{
				"action": "reply",
				"notification_id": str(notification.id),
				"reply_message": "Thanks, I have replied.",
			},
		)

		self.assertRedirects(response, reverse("inbox"))
		reply = Notification.objects.get(
			profile=self.admin_profile,
			sender=self.buyer_profile,
		)
		self.assertEqual(reply.message, "Thanks, I have replied.")
		self.assertEqual(reply.thread_id, notification.thread_id)

	def test_admin_reply_is_received_by_original_user(self):
		notification = Notification.objects.create(
			profile=self.admin_profile,
			sender=self.buyer_profile,
			subject="Reply from buyer: Original message",
			message="Please review this.",
		)

		self.client.force_login(self.admin)
		response = self.client.post(
			reverse("inbox"),
			{
				"action": "reply",
				"notification_id": str(notification.id),
				"reply_message": "Thanks for your message.",
			},
		)

		self.assertRedirects(response, reverse("inbox"))
		reply = Notification.objects.get(
			profile=self.buyer_profile,
			sender=self.admin_profile,
		)
		self.assertEqual(reply.message, "Thanks for your message.")
		self.assertEqual(reply.thread_id, notification.thread_id)
