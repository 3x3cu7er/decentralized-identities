"""
URL configuration for foundation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include(("space.urls", "space"), "space")),
    path("",include("space.urls")),
    path("my-dashboard",include("space.urls")),
    path("my-profile",include("space.urls")),
    path("repo",include("space.urls")),
    path("authorize-access",include("space.urls")),
    path("add-contents",include("space.urls")),
    path("create-file",include("space.urls")),
    path("credentials",include("space.urls")),
    path("account",include("space.urls")),
    path("access",include("space.urls")),
    path("issue",include("space.urls")),
    path("verify-email",include("space.urls")),
    path('transfer', include('sharing.urls')),
]+ static(settings.STATIC_URL)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
