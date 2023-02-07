from io import BytesIO
from django.test import TestCase
from django.core.files import File
from django.db import IntegrityError

from PIL import Image as TestImage

from auth_app.models import User
from .models import Image


class ImageModelTestCase(TestCase):

    @staticmethod
    def get_image_file():
        file_obj = BytesIO()
        image = TestImage.new('RGB', (20, 20))
        image.save(file_obj, 'png')
        file_obj.seek(0)
        return File(file_obj, name='name')

    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')

    def test_create_image(self):
        image = Image.objects.create(title='Test Image',
                                     image=self.get_image_file(),
                                     user=self.user)
        self.assertEqual(image.title, 'Test Image')
        self.assertIsNotNone(image.created_date)
        self.assertIsNotNone(image.update_at)
        self.assertEqual(image.user, self.user)

    def test_create_image_without_user(self):
        image = Image(title='Test Image', image=self.get_image_file())
        with self.assertRaises(IntegrityError):
            image.save()

    def test_update_image(self):
        image = Image.objects.create(title='Test Image',
                                     image=self.get_image_file(),
                                     user=self.user)
        self.assertEqual(image.title, 'Test Image')
        self.assertIsNotNone(image.created_date)
        self.assertIsNotNone(image.update_at)

        image.title = 'Updated Test Image'
        image.save()
        image.refresh_from_db()
        self.assertEqual(image.title, 'Updated Test Image')
        self.assertIsNotNone(image.created_date)
        self.assertIsNotNone(image.update_at)
