"""
URL configuration for bookshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path

# Image work
from django.conf.urls.static import static
from django.conf import settings

from ecom import admin_view
from ecom import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #Public urls
    path("",views.homepage, name="homepage"),
    
    path('cart/', views.cart, name="cart"),
    path('/add-to-cart/<int:book_id>', views.addToCart, name="addToCart"),
    path('/remove-from-cart/<int:book_id>', views.removeFromCart, name="removeFromCart"),
    path('/apply-coupon/', views.applyCoupon, name="applyCoupon"),
    path('checkout/', views.checkout, name="checkout"),

    path("search/",views.search,name="search"),
    path("genre/filter/<int:genre_id>/",views.filterBygenre,name="filterByGenre"),
    path("book/<int:book_id>/",views.bookDetails,name="bookDetails"),
    path("account/login/",views.login,name="login"),
    path("register/",views.register,name="register"),
    path("account/logout/",views.logout,name="logout"),

    #Superadmin
    path("superadmin/",admin_view.admin_dashboard, name="admin_dashboard"),
    path("superadmin/book/insert",admin_view.insert_book, name="insert_book"),
    path("superadmin/genre/insert",admin_view.insert_genre, name="insert_genre"),
    path("superadmin/genre/delete/<int:id>/",admin_view.delete_genre, name="delete_genre"),
    path("superadmin/book/delete/<int:id>/",admin_view.delete_book, name="delete_book"),
    path("superadmin/book/edit/<int:id>/",admin_view.edit_book, name="edit_book"),
    path("superadmin/genre/edit/<int:id>/",admin_view.edit_genre, name="edit_genre"),
    path("superadmin/genre/",admin_view.manage_genre, name="manage_genre"),
    path("superadmin/books/",admin_view.manage_books, name="manage_books"),
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)