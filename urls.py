from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('index/',views.index,name='index'),
    path('userregister/',views.userregist,name='userregister'),
    path('login/',views.userlogin,name='userlogin'),
    path('profile/',views.profile,name='profile'),
    path('editprofile/<int:eid>/',views.editprofile,name='editprofile'),
    path('dashboard/',views.dashboard,name='dashboard'),
   
    path('userlist/', views.user_list, name='user_list'),
    path('delete_user/<int:did>/',views.delete_user,name='delete_user'),
  
    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('feedback_rate/',views.feedback,name='feedback_rate'),
    path('userindex/',views.userindex,name='userindex'),
    path('feedbacklist/',views.feedbacklist,name='feedbacklist'),
    path('confirmfeedback/<int:f_id>/', views.confirmfeedback, name='confirmfeedback'),

    path('feedbackdelete/<int:did>/',views.feedbackdelete,name='feedbackdelete'),
    path('contact_view/',views.contact_view,name='contact_view'),
    path('contact_list/',views. contact_list, name='contact_list'),
    path('logout/',views.logout, name='logout'),
    path('userlogout/',views.userlogout, name='userlogout'),
    path('add_category/',views.add_category, name='add_category'),

    path('error/',views.error,name='error'),
    
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:id>', views.edit_product, name='edit_product'),
    
    path('categories/',views.category_list, name='category-list'),
    path('<int:category_id>/products/',views.product_list, name='product-list'),
    path('addcart/<int:id>/',views.addcarts,name='addcart'),
    path('add_cart/',views.add_cart, name='add_cart'),





    path('cart/',views.view_cart, name='view_cart'),
    path('cart/remove/<int:item_id>/',views.remove_from_cart, name='remove_from_cart'),
    path('payment/<int:order_id>/',views.payment, name='payment'),
    path('paymenthandler/',views.paymenthandler, name='paymenthandler'),
    path('payment2/',views.payment2,name='payment2'),
    path('paymenthandler2/',views.paymenthandler2,name='paymenthandler2'),


    path('pay_failed/',views.pay_failed,name='pay_failed'),
    path('pay_success/',views.pay_success,name='pay_success'),

    path('pc_home/',views.pc_home,name='pc_home'),
    path('add_prebuild/',views.add_prebuild,name='add_prebuild'),
    path('prebuild_list/',views.prebuild_list,name='prebuild_list'),
    path('search/',views.search,name='search'),
    path('payment3/<int:id>/', views.payment3, name='payment3'),
    path('paymenthandler3/', views.paymenthandler3, name='paymenthandler3'),
    path('view_prebuild/',views.view_prebuild,name='view_prebuild'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('delete_products/<int:id>/', views.delete_products, name='delete_products'),
    path('<int:category_id>/view_products/',views.view_products, name='view_products'),
    path('view_category/',views.view_category, name='view_category'),
    path('edit_category/<int:category_id>', views.edit_category, name='edit_category'),
    path('delete_category/<int:category_id>', views.delete_category, name='delete_category'),
    
    path('temp/', views.temp, name='temp'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'), 
    path('my_cart/', views.cart_view, name='my_cart'),
    path('payments/', views.buy_product, name='payments'),
    
    
    
]




    


    


 


    






    
    




    
    



   

