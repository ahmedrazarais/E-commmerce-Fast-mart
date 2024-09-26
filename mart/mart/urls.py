"""
URL configuration for mart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.extract_cataegories_home_page ,name="home"),
    path('search/', views.search_page ,name="search"),

    path('about/', views.about_page ,name="about"),
    path("signup/" , include("signup.urls")),
    path("signin/" , include("signin.urls")),
    path("cart/" , include("cart.urls")),
    path("checkout/" , include("checkout.urls")),
    path("history/" , include("history.urls")),
    

     # Add this new route for category-specific products
    path('products/<int:category_id>/', views.category_products, name='category_products'),
    
    # Add this new route for product details use this url to view product details
    path('product/<int:product_id>/', views.product_details, name='product_details')

]
# Add this to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)