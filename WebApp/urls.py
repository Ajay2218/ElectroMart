from django.urls import path
from WebApp import views

urlpatterns = [
    path('',views.home_page,name="Home"),
    path('About/',views.about_page,name="About"),
    path('all_products/',views.all_products,name="all_products"),
    path('filtered/<cat_name>',views.filtered_product,name="filtered"),
    path('single_product/<int:pro_id>',views.single_product,name="single_product"),
    path('sign_in/',views.sign_in,name="sign_in"),
    path('sign_up/',views.sign_up,name="sign_up"),
    path('save_user/',views.save_user,name="save_user"),
    path('user_login/',views.user_login,name="user_login"),
    path('user_logout/',views.user_logout,name="user_logout"),
    path('contact/',views.contact,name="contact"),
    path('save_contact/',views.save_contact,name="save_contact"),
    path('help_page/',views.help_page,name="help_page"),
    path('support_page/',views.support_page,name="support_page"),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('save_to_cart/',views.save_to_cart,name="save_to_cart"),
    path('delete_cart_product/<int:p_id>',views.delete_cart_product,name="delete_cart_product"),
    path('payment/',views.payment_page,name="payment"),
    path('save_order/',views.save_order,name="save_order"),
    path('payment/success/', views.payment_success, name="payment_success"),
    path('payment/failed/', views.payment_failed, name="payment_failed"),
  ]
