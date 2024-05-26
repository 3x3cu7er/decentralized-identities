from django.test import TestCase
from django.test import TestCase, Client
from django.contrib.auth.models import User
from sharing.models import File  
from sharing.fileManagement import user_directory_path, share_file_path
class FileUtilsTest(TestCase):
    def setUp(self):


        self.user = User.objects.create_user(username='testuser', password='testpassword')


        self.client = Client()
        self.client.login(username='testuser', password='testpassword')


        self.file_instance = File.objects.create(owner_id=1, fileSize =9)  

    def test_user_directory_path(self):

        result_path = user_directory_path(self.file_instance, "example.txt")

        expected_path = f'user_{self.file_instance.owner_id}/file/example.txt'


        self.assertEqual(result_path, expected_path)

    def test_share_file_path(self):

        result_path = share_file_path(self.file_instance)


        expected_path = f'media/user_{self.file_instance.owner_id}/file'


        self.assertEqual(result_path, expected_path)

    def tearDown(self):
        self.file_instance.delete()
