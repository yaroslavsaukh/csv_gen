from django.urls import path
from .views import *

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('', DataSchemasView.as_view(), name='data_schemas'),
    path('<int:pk>/data-sets/', DataSetsView.as_view(), name='data_sets'),
    path('create_schema/', SchemaCreateView.as_view(), name='create_schema'),
    path('schema/<int:pk>/', SchemaUpdateView.as_view(), name='show_schema'),
    path('schema/<int:pk>/delete/', delete_schema, name='delete_schema'),

    path('colunm/<int:pk>/add/', AddColumn.as_view(), name='add_column'),
    path('column/<int:pk>/delete/', delete_column, name='delete_column'),

    path('download/<int:pk>/', download_file, name='download_file')
]
