from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "ecommerce_app"

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('home/', views.home, name='home'),

    path('update_product/<int:id>', views.update_product, name='update_product'),
    path('delete_product/<int:pk>', views.delete_product, name='delete_product'),
    path('all_products/', views.all_products, name='all_products'),
    path('category_wise_products/<str:category>', views.category_wise_products, name='category_wise_products'),

    path('create_product/', views.create_product, name="create_product"),
    path('create_category/', views.create_category_popup, name="create_category"),
    path('category/ajax/get_category_id', views.get_category_id, name="get_category_id"),
    url(r'^category/(?P<pk>\d+)/edit', views.edit_category_popup, name="edit_category"),

    path('home/request_new_product/', views.request_new_product, name='request_new_product'),
    path('request_new_product/', views.request_new_product, name='request_new_product'),
    path('home/show_unseen_product_requests/', views.show_unseen_product_requests, name = 'show_unseen_product_requests'),
    path('show_unseen_product_requests/', views.show_unseen_product_requests, name = 'show_unseen_product_requests'),
    path('show_unseen_product_requests/mark_requests_as_read/', views.mark_requests_as_read, name = 'mark_requests_as_read'),
    path('home/show_unseen_product_requests/mark_requests_as_read/', views.mark_requests_as_read, name = 'mark_requests_as_read'),

    path('user_cart/', views.user_cart, name='user_cart'),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)