from django.urls import path
from . import views

urlpatterns = [
    path('signup',views.Signup,name = 'signup'), #mariam
    path('login',views.login,name='login'), # reem
    path('tasklist',views.tasklist,name='tasklist'), # samar
    path('addTask', views.add_task, name='addTask'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('completeTask/<int:task_id>/', views.complete_task, name = 'completeTask'),
    path('editTask/<int:task_id>/', views.editTask, name = 'editTask'),
    path('search', views.search, name = 'search'),
    path('completedTasks', views.completedTasks, name = 'completedTasks'),

]