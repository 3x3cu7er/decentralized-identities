project_name/
|-- manage.py
|-- project_name/
|   |-- __init__.py
|   |-- settings.py
|   |-- urls.py
|   |-- wsgi.py
|-- books/
|   |-- __init__.py
|   |-- models.py
|   |-- signals.py
|   |-- apps.py
|-- library/
|   |-- __init__.py
|   |-- models.py
|   |-- apps.py
|   |-- views.py


# books/models.py

from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.title
# library/models.py

from django.db import models

class LibraryBook(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.title
# books/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from books.models import Book
from library.models import LibraryBook

@receiver(post_save, sender=Book)
def transfer_book_data(sender, instance, created, **kwargs):
    if created:
        LibraryBook.objects.create(title=instance.title, author=instance.author)
# books/apps.py

from django.apps import AppConfig

class BooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'books'

    def ready(self):
        import books.signals
# products/models.py

from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
# products/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from inventory.models import InventoryItem
from products.models import Product

@receiver(post_save, sender=Product)
def transfer_product_data(sender, instance, created, **kwargs):
    if created:
        # When a new product is created, transfer it to the inventory
        inventory_item = InventoryItem(product=instance, quantity=0)
        inventory_item.save()
# inventory/models.py

from django.db import models
from products.models import Product

class InventoryItem(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - Quantity: {self.quantity}"
# products/__init__.py

default_app_config = 'products.apps.ProductsConfig'

# Import signals to connect them
import products.signals








//////////////////////////algorithm //////////////////////////////
Start

1. Initialize Django project and create two apps: 'products' and 'inventory'.
   - Use django-admin to create the project and apps.

2. Define models for 'products' and 'inventory' apps:
   - In 'products' app, define a Product model.
   - In 'inventory' app, define an InventoryItem model.

3. Define a signal handler in the 'products' app:
   - Create a function to handle the post_save signal for the Product model.
   - Inside the signal handler function, create an InventoryItem object corresponding to the new Product object.

4. Connect the signal handler to the post_save signal:
   - Import the signal handler function in the 'products' app's __init__.py file.

5. Register both apps in the INSTALLED_APPS list in the project's settings.py file.

6. Test the data transfer functionality:
   - Create or update Product objects.
   - Verify that corresponding InventoryItem objects are created automatically.

End



////////////////// infura  url/////////
https://mainnet.infura.io/v3/b8211144561c422bbeeb55546e0d27d2
///////////////// infura key //////////
b8211144561c422bbeeb55546e0d27d2
