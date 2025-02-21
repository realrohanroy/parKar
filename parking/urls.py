from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('authentications/', views.user_login, name='authentications'),
    path('listingpage/', views.listingpage, name='listingpage'),
    path('add-photos/', views.add_photos, name='addphotos'),
    path('set-pricing/<int:space_id>/', views.set_pricing, name='setpricing'),
    path('dummy/', views.dummy_page, name='dummy_page'),
    path('dummy2/', views.dummy_page2, name='dummy_page2'),
    path('dummy3/', views.dummy_page3, name='dummy_page3'),
    path('dummy4/', views.dummy_page4, name='dummy_page4'),
    path('search/', views.search_results, name='search_results'),
    path('details/<int:id>/', views.result_details, name='result_details'),
    path('payment/<int:id>/', views.payment, name='payment'),
    path('confirmation/<int:id>/', views.booking_confirmation, name='booking_confirmation'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)