from django.urls import path
from .import views


urlpatterns = [path('',views.home, name='home'),
                path ('signup',views.signup,name='signup'),
                path('login',views.login_view,name='login'),
                path('reportlost',views.reportlost,name='reportlost'),
                path('reportfound',views.reportfound,name='reportfound'),
                path('logout/',views.user_logout,name='logout'),
                path('lost_items/',views.lost_items, name='lost_items'),
                path('found_items/',views.found_items, name='found_items'),  
                path('item_detail/<int:id>/',views.item_detail, name='item_detail'),
                path('edit/<int:id>/<str:type>/',views.edit_item,name='edit_item'),
                path('delete_item/<int:id>/',views.delete_item,name='delete_item'),
                path('claim_item/<int:item_id>',views.claim_item,name='claim'),
                path('mydetails',views.mydetails,name='mydetails'),
 
                path('admin-items/', views.admin_items, name='admin_items'),
                path('approve/<int:id>/', views.approve_item, name='approve_item'),
                path('reject/<int:id>/', views.reject_item, name='reject_item'),
                path('delete/<int:id>/', views.delete_item, name='delete_item'),

               path('approve_claim/<int:id>/', views.approve_claim, name='approve_claim'),
                path('reject_claim/<int:id>/', views.reject_claim, name='reject_claim'),
                path('delete_claim/<int:id>/', views.delete_claim, name='delete_claim'),

                ]
                