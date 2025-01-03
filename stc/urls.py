from django.urls import path 
from .import views 


urlpatterns = [
   path('',views.home,name='home'),
   path('login/',views.login_user,name='login'),
   path('logout/',views.logout_user,name='logout'),
   path('register/',views.register_user,name='register'),
   path('stock_chart/', views.stock_graph_view, name='stock_chart'),
   path('buy_sell/', views.buy_sell_views, name='buy_sell'),
   path('forecast/', views.stock_forecast, name='forecast'),
   path('portfolio/', views.portfolio_opt, name='portfolio'),
]
