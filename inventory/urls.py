from django.urls import path

from inventory import views

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('new', views.item_create, name='item_new'),
    path('detail/<int:pk>', views.item_detail, name='item_detail'),
    path('edit/<int:pk>', views.item_update, name='item_edit'),
    path('delete/<int:pk>', views.item_delete, name='item_delete'),
    path('search_results', views.search_results, name='search_results'),
    path('api/get_items', views.get_items, name='get_items')
]
