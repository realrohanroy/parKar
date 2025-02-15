from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('listingpage/', views.listingpage, name='listingpage'),
    path('addphotos/',views.addphotos, name='addphotos'),
    path('setpricing/', views.setpricing, name='setpricing'),

    path('search/', views.search_results, name='search_results'),
    path('details/<int:id>/', views.result_details, name='result_details'),
    path('payment/<int:id>/', views.payment, name='payment'),
    path('confirmation/<int:id>/', views.booking_confirmation, name='booking_confirmation'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)