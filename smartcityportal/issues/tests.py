from io import BytesIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Issue, IssueCategory


class IssueCreateViewTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username="reporter",
			email="reporter@example.com",
			password="password12345",
		)
		self.category = IssueCategory.objects.create(name="Roads", description="Road related issues")

	def _image_file(self):
		return SimpleUploadedFile(
			"issue.png",
			self._png_bytes(),
			content_type="image/png",
		)

	def _png_bytes(self):
		from PIL import Image

		buffer = BytesIO()
		image = Image.new("RGB", (1, 1), color=(255, 0, 0))
		image.save(buffer, format="PNG")
		return buffer.getvalue()

	@patch("cloudinary.uploader.upload")
	def test_issue_create_accepts_multipart_form_data_and_returns_json(self, mocked_upload):
		mocked_upload.return_value = {
			"public_id": "issues/test-upload",
			"secure_url": "https://res.cloudinary.com/demo/image/upload/issues/test-upload.png",
		}

		self.client.force_login(self.user)

		response = self.client.post(
			reverse("issue_create"),
			data={
				"category": self.category.pk,
				"title": "Broken streetlight",
				"description": "Streetlight is not working at night.",
				"location": "Market Road",
				"image": self._image_file(),
			},
			HTTP_X_REQUESTED_WITH="XMLHttpRequest",
			secure=True,
		)

		issue = Issue.objects.latest("id")

		self.assertEqual(response.status_code, 200)
		self.assertJSONEqual(
			response.content,
			{
				"success": True,
				"redirect_url": reverse("issue_detail", kwargs={"pk": issue.pk}),
				"issue_id": issue.pk,
			},
		)
		self.assertEqual(issue.user, self.user)
		self.assertEqual(issue.image.name, "issues/test-upload")
		self.assertEqual(issue.category, self.category)
