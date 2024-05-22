from django.urls import path
from AppName import views
urlpatterns = [
    path('',views.home,name='hom'),
    path('midle',views.mid,name='midl'),
    path('midlem',views.set_preference,name='setp'),
    path('data',views.data,name='dat'),
    path('contact',views.contact,name='con'),
    path('guide',views.guide,name='guide'),
    #following is for getting .sql file in temp database
    path('temp_db',views.upload_sql,name='upl'),
    
]
