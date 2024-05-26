from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from sharing.models import File



class TestViews(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Log in the user using the client
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_home_view_authenticated_user(self):


        File.objects.create(owner=self.user, fileName='file1.txt', fileSize=1024, fileType='txt', fileHash='abcdef123456', sender = None)
        File.objects.create(owner=self.user, fileName='file2.txt', fileSize=2048, fileType='txt', fileHash='123456abcdef', sender = None)

        # Access the home view using the client
        response = self.client.get(reverse('sharing_app:home'))


        self.assertEqual(response.status_code, 200)

    def test_home_view_unauthenticated_user(self):

        self.client.logout()

        # Access the home view using the client
        response = self.client.get(reverse('sharing_app:home'))

        # Check if the response status code is 302 (redirect to login page for unauthenticated users)
        self.assertEqual(response.status_code, 302)

        # Check if the user is redirected to the login page
        self.assertRedirects(response, reverse('user_app:login') + f'?next={reverse("sharing_app:home")}')

##$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$##

    def test_upload_view(self):

        uploaded_file = SimpleUploadedFile("file.txt", b"file_content")

        # Prepare the form data
        form_data = {
            'fileName': 'Test File',
            'fileDir': uploaded_file,
        }


        response = self.client.post('/upload/', data=form_data)


        self.assertEqual(response.status_code, 200)


        self.assertEqual(File.objects.count(), 1)

##$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$##

    def test_download_view(self):

        uploaded_file = SimpleUploadedFile("file.txt", b"file_content")
        response_upload = self.client.post(reverse('sharing_app:upload'), {
            'fileName': 'Test File',
            'fileDir': uploaded_file,
        })


        self.assertEqual(response_upload.status_code, 200)


        uploaded_file_obj = File.objects.last()


        response_download = self.client.get(reverse('sharing_app:download', args=[uploaded_file_obj.id]))


        self.assertEqual(response_download.status_code, 200)


        self.assertEqual(response_download['Content-Type'], 'application/octet-stream')

##$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$##

    def test_share_view(self):


        self.user1 = User.objects.create_user(username='testuser1', password='testpassword1')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword2')


        self.uploaded_file = SimpleUploadedFile("file.txt", b"file_content")


        response_upload = self.client.post(reverse('sharing_app:upload'), {
            'fileName': 'Test File',
            'fileDir': self.uploaded_file,
        })


        self.client.login(username='testuser1', password='testpassword1')


        self.test_file = File.objects.first()
        form_data = {'username': 'testuser2'}  

        response = self.client.post(reverse('sharing_app:share', args=[self.test_file.id]), data=form_data)

        # Check if the file upload was successful 
        self.assertEqual(response_upload.status_code, 200)



    def tearDown(self):
        self.client.logout()

