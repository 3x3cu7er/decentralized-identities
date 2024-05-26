from django.urls import path
from . import views

urlpatterns = [
    path('encrypted_data/', views.encrypted_data, name='encrypted_data'),
    path('login/', views.user_login, name='login'),
    path('mine_block/', views.mine_block, name='mine'),
    path('send_transaction/', views.send_transaction, name='send_transaction'),
    path('view_blockchain/', views.view_blockchain, name='view_blockchain'),
     path('manage_identity/', views.manage_identity, name='manage_identity'),
    path('send_transaction/', views.send_transaction, name='send_transaction'),
    path('receive_transaction/', views.receive_transaction, name='receive_transaction'),
    path('create_wallet/', views.create_wallet, name='create_wallet'),
    path('share_data/', views.share_data, name='share_data'),
]
