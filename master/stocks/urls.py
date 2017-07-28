from django.conf.urls import url
from . import views

app_name = 'stocks'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<company_id>[0-9]+)/$', views.detail, name='detail'),
    #url(r'^(?P<song_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    #url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),
    url(r'^create_company/$', views.create_company, name='create_company'),
    url(r'^(?P<company_id>[0-9]+)/run_daily_demand/$', views.run_daily_demand, name='run_daily_demand'),
    url(r'^run_demand_selected/$', views.run_demand_selected, name='run_demand_selected'),
    url(r'^run_demand_all/$', views.run_demand_all, name='run_demand_all'),
    url(r'^run_demand_supply_selected/$', views.run_demand_supply_selected, name='run_demand_supply_selected'),
    url(r'^run_demand_supply_all/$', views.run_demand_supply_all, name='run_demand_supply_all'),
    url(r'^(?P<company_id>[0-9]+)/run_weekly_demand/$', views.run_weekly_demand, name='run_weekly_demand'),
    url(r'^(?P<company_id>[0-9]+)/run_monthly_demand/$', views.run_monthly_demand, name='run_monthly_demand'),

    url(r'^(?P<company_id>[0-9]+)/run_daily_supply/$', views.run_daily_supply, name='run_daily_supply'),
    url(r'^run_supply_selected/$', views.run_supply_selected, name='run_supply_selected'),
    url(r'^run_supply_all/$', views.run_supply_all, name='run_supply_all'),
    url(r'^(?P<company_id>[0-9]+)/run_weekly_supply/$', views.run_weekly_supply, name='run_weekly_supply'),
    url(r'^(?P<company_id>[0-9]+)/run_monthly_supply/$', views.run_monthly_supply, name='run_monthly_supply'),

    url(r'^(?P<company_id>[0-9]+)/download_daily_demand/$', views.download_daily_demand, name='download_daily_demand'),
    url(r'^(?P<company_id>[0-9]+)/download_weekly_demand/$', views.download_weekly_demand, name='download_weekly_demand'),
    url(r'^(?P<company_id>[0-9]+)/download_monthly_demand/$', views.download_monthly_demand, name='download_monthly_demand'),

    url(r'^(?P<company_id>[0-9]+)/download_daily_supply/$', views.download_daily_supply, name='download_daily_supply'),
    url(r'^(?P<company_id>[0-9]+)/download_weekly_supply/$', views.download_weekly_supply, name='download_weekly_supply'),
    url(r'^(?P<company_id>[0-9]+)/download_monthly_supply/$', views.download_monthly_supply, name='download_monthly_supply'),
    
    url(r'^download_demand_excel/$', views.download_demand_excel, name='download_demand_excel'),
    url(r'^download_supply_excel/$', views.download_supply_excel, name='download_supply_excel'),

    url(r'^select_all/$', views.select_all, name='select_all'),
    url(r'^deselect_all/$', views.deselect_all, name='deselect_all'),
    #url(r'^(?P<album_id>[0-9]+)/create_song/$', views.create_song, name='create_song'),
    #url(r'^(?P<album_id>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/$', views.delete_song, name='delete_song'),
    url(r'^(?P<company_id>[0-9]+)/company_is_selected/$', views.company_is_selected, name='company_is_selected'),
    url(r'^(?P<company_id>[0-9]+)/favorite_company/$', views.favorite_company, name='favorite_company'),
    url(r'^(?P<company_id>[0-9]+)/delete_company/$', views.delete_company, name='delete_company'),
]
