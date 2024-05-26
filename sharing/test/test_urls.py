from django.test import SimpleTestCase
from django.urls import reverse, resolve
from sharing.views import home, upload, download, share


class Testurls(SimpleTestCase):

    def test_home(self):

        #reverse generate a url.
        url = reverse('sharing_app:home')

        #resolve function returns info about the url such as function name, namespace etc.
        self.assertEquals(resolve(url).func, home)

    def test_upload(self):
        
        url = reverse('sharing_app:upload')
        self.assertEquals(resolve(url).func, upload)

    def test_download(self):

        url = reverse('sharing_app:download', args=[1])
        self.assertEquals(resolve(url).func, download)

    def test_share(self):

        url = reverse('sharing_app:share', args=[1])
        self.assertEquals(resolve(url).func, share)
