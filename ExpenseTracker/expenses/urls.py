from django.urls import path
from . import views

app_name = "expense"
urlpatterns=[
    path('',views.home,name='home'),
    path('add/', views.add_expense, name = 'add_expense'),
    path('delete/<int:expense_id>/', views.delete, name='delete')
]
