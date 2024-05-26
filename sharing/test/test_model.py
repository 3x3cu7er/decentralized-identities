from django.test import TestCase
from django.contrib.auth.models import User
from sharing.models import File


class FileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_make_share_file(self):

        test_file = File.objects.create(
            fileName='Test File',
            fileSize=1024,
            fileType='txt',
            fileHash='hash123',
            owner=self.user,
            sender=None
        )

        recipient = User.objects.create_user(username='recipientuser', password='recipientpassword')

        shared_file = test_file.make_share_file(recipient)

        self.assertEqual(shared_file.fileName, 'Test File')
        self.assertEqual(shared_file.fileSize, 1024)
        self.assertEqual(shared_file.fileType, 'txt')
        self.assertEqual(shared_file.fileHash, 'hash123')
        self.assertEqual(shared_file.owner, recipient)
        self.assertEqual(shared_file.shared, True)
        self.assertEqual(shared_file.sender, self.user)

    def test_file_model_str_method(self):

        test_file = File.objects.create(
            fileName='Test File',
            fileSize=1024,
            fileType='txt',
            fileHash='hash123',
            owner=self.user,
            sender=None
        )

        self.assertEqual(str(test_file), 'Test File')
