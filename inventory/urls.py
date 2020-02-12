from django.urls import path

from inventory import views

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('add', views.item_add, name='item_add'),
    path('detail/<int:pk>', views.item_detail, name='item_detail'),
    path('edit/<int:pk>', views.item_edit, name='item_edit'),
    path('delete/<int:pk>', views.item_delete, name='item_delete'),
    path('search_results', views.search_results, name='search_results'),
    path('api/get_items', views.get_items, name='get_items'),
    path('transactions', views.transactions, name="transactions")
]
