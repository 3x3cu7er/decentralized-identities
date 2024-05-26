from django.urls import path,include
from . import views
from  sharing import views as sharing
from blockchain_app import views as blc
from identities import views as did 
from identityManagement import views as id_manager
from manager import views as iman
from ssi_app import views as ssi 
urlpatterns = [
    path("", views.landing,name="land"),
    path("signup", views.authView, name="authView"),
    path("accounts", include("django.contrib.auth.urls")),
    path("home",views.main,name="main"),
    path("my-dashboard",views.myDashboard,name="Dashboard"),
    path("my-profile",views.myProfile,name="Profile"),
    path("repo",views.myVault,name="reporitory"),
    path("credential-repo",views.credential_repo,name="credential repository"),
    path("add-contents",views.addContents,name="add contents to store"),
    # path("create-file",views.create_file,name="files upload"),
    # path("credentials",views.credentials,name="credentials storage"),
    # path("account",views.account,name="account creation"),
    # path("verify-email",views.emailPager,name="emailer"),
    path('share/',sharing.home, name="credential sharing home"),
    path('upload/', sharing.upload, name="upload credential file"),
    path('download/<int:file_id>/', sharing.download, name="download credential file"), # <int:filename>/ gets the file primary id to download.
    path('share/<int:file_id>/', sharing.share, name="share a credential file"),
    path('share-credential/', views.shared_credential_list, name='shared credential'),
    path('add/', views.add_shared_credential, name='add to shared credential'),
    path('edit/<int:shared_text_id>/', views.edit_shared_credential, name='edit shared credential'),
    path("share_data/",blc.share_data,name="share_data"),
    path('mine_block/', blc.mine_block, name='mine'),
    # path('receive_transaction/', blc.receive_transaction, name='receive_transaction'),
    path('manage_identity/', blc.manage_identity, name='manage_identity'),
    path('encrypted_data/', blc.encrypted_data, name='encrypted_data'),
    path('create_identity/', did.create_identity, name='create_identity'),
    path('identity/<int:pk>/', did.view_identity, name='identity_detail'),
    path('upload_data/', did.upload_data, name='upload_data'),
    path('data/<str:ipfs_hash>/', did.view_data, name='view_data'),
    path('list_data/<str:ipfs_hash>/', did.list_data, name='list_data'),
    path('identity_list/', ssi.identity_list, name='identity_list'),
    # path('register/', id_manager.register_identity, name='register_identity'),
    path('share_ipfs_data/', ssi.share_data, name='share_ipfs_data'),
    path('access/<str:address>/', ssi.access_shared_data, name='access_shared_data'),
    path('revoke/', ssi.revoke_data, name='revoke_data'),
    path('id_dashboard/', ssi.dashboard, name='dashboard'),
    path('issue_credential/', ssi.issue_credential, name='issue_credential'),
    path('revoke_credential/<int:credential_id>/', ssi.revoke_credential, name='revoke_credential'),
    path('update_credential/<int:credential_id>/', ssi.update_credential, name='update_credential'),
    # path('list_credentials/', iman.list_credentials, name='list_credentials'),
    path('register_ssi/', ssi.register, name='register'),
    path('authenticate/', ssi.authenticate, name='authenticate'),
]
