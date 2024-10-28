"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from myapp.views import  LoginViews,CategorieViews,SousCategorieViews,ProduitViews,ClientViews
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',LoginViews.index_view, name='index_view'),
    path('indexAdmin/',LoginViews.indexAdmin_view, name='indexAdmin_view'),
    #Categorie
    path('categories/', CategorieViews.as_view(), name='get'),    
    path('categories/add/', CategorieViews.add_category, name='add_category'),
    path('categories/update/<str:code_cate>/', CategorieViews.update_category, name='update_category'),
    path('categories/delete/<str:code_cate>/', CategorieViews.delete_category, name='delete_category'),
    #Sous categories
    path('SousCategories/', SousCategorieViews.as_view(), name='get'),    
    path('SousCategories/add/', SousCategorieViews.add_sous_category, name='add_sous_category'),
    path('SousCategories/update/<str:code_Souscate>/', SousCategorieViews.update_sous_category, name='update_sous_category'),
    path('SousCategories/delete/<str:code_Souscate>/', SousCategorieViews.delete_sous_category, name='delete_sous_category'),
    #produits    
    path('produits/', ProduitViews.as_view(), name='get'),    
    path('produits/add/', ProduitViews.add_produit, name='add_produit'),
    path('produits/update/<str:idProd>/', ProduitViews.update_produit, name='update_produit'),
    path('produits/delete/<str:idProd>/', ProduitViews.delete_produit, name='delete_produit'),
    path('store/', ProduitViews.list_produits, name='list_produits'),
    path('store/details/<str:idProd>/', ProduitViews.product_detail, name='product_detail'),
    #path('store/addToCart/<str:idProd>/', ProduitViews.add_to_cart, name='add_to_cart'),
    path('store/more-products/', ProduitViews.more_products, name='more_products'),
    path('store/search_products/', ProduitViews.search_products, name='search_products'),
    path('store/cart/', ProduitViews.cart, name='cart'),
    path('update_cart/<int:idProd>/', ProduitViews.update_cart, name='update_cart'),
    path('checkout/', ProduitViews.checkout, name='checkout'),
    path('checkout_confirmation/', ProduitViews.checkout_confirmation, name='checkout_confirmation'),
    path('cart/remove/<int:idProd>/', ProduitViews.remove_from_cart, name='remove_from_cart'),

    path('shop/',LoginViews.shop_view, name='shop_view'),
    path('signup/',LoginViews.signup_view, name='signup'),
    path('login/',LoginViews.login_view, name='login_view'),
    path('signupClient/',LoginViews.signupClient_view, name='signupClient'),
    path('loginClient/',LoginViews.loginClient_view, name='loginClient_view'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)