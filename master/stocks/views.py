from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import CompanyForm,UserForm
from .models import Company
from demand_monthly_phase1v1 import demand_month_execute
from demand_weekly_phase1v1 import demand_week_execute
from demand_phase2v1allparam import demand_execute_function
from supply_monthly_phase1v1 import supply_month_execute
from supply_weekly_phase1v1 import supply_week_execute
from supply_phase2v1allparam import supply_execute_function
from django.http import HttpResponse
from wsgiref.util import FileWrapper  
import os
from django.conf import settings
import datetime
from datetime import datetime
from datetime import timedelta

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_company(request):
    if not request.user.is_authenticated():
        return render(request, 'stocks/login.html')
    else:
        form = CompanyForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            company = form.save(commit=False)
            company.user = request.user
            company.company_logo = request.FILES['company_logo']
            file_type = company.company_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'company': company,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'stocks/create_company.html', context)
            company.save()
            return render(request, 'stocks/detail.html', {'company': company})
        context = {
            "form": form,
        }
        return render(request, 'stocks/create_company.html', context)


'''def create_song(request, album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        albums_songs = album.song_set.all()
        for s in albums_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'music/create_song.html', context)
        song = form.save(commit=False)
        song.album = album
        song.audio_file = request.FILES['audio_file']
        file_type = song.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'album': album,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, or OGG',
            }
            return render(request, 'music/create_song.html', context)

        song.save()
        return render(request, 'music/detail.html', {'album': album})
    context = {
        'album': album,
        'form': form,
    }
    return render(request, 'music/create_song.html', context)'''


def delete_company(request, company_id):
    company = Company.objects.get(pk=company_id)
    company.delete()
    companies = Company.objects.filter(user=request.user)
    return render(request, 'stocks/index.html', {'companies': companies})


'''def delete_song(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request, 'music/detail.html', {'album': album})'''


def detail(request, company_id):
    if not request.user.is_authenticated():
        return render(request, 'stocks/login.html')
    else:
        user = request.user
        company = get_object_or_404(Company, pk=company_id)
        return render(request, 'stocks/detail.html', {'company': company, 'user': user})


'''def favorite(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})'''


def favorite_company(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    try:
        if company.is_favorite:
            company.is_favorite = False
        else:
            company.is_favorite = True
        company.save()
    except (KeyError, Company.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})

def company_is_selected(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    try:
        if company.is_selected:
            company.is_selected = False
        else:
            company.is_selected = True
        company.save()
    except (KeyError, Company.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})
        
def index(request):
    if not request.user.is_authenticated():
        return render(request, 'stocks/login.html')
    else:
        companies = Company.objects.filter(user=request.user)
        query = request.GET.get("q")
        if query:
            companies = companies.filter(
                Q(company_name__icontains=query) |
                Q(company_stock_code__icontains=query)
            ).distinct()
            return render(request, 'stocks/index.html', {
                'companies': companies,
            })
        else:
            return render(request, 'stocks/index.html', {'companies': companies})

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'stocks/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                companies = Company.objects.filter(user=request.user)
                return render(request, 'stocks/index.html', {'companies': companies})
            else:
                return render(request, 'stocks/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'stocks/login.html', {'error_message': 'Invalid login'})
    return render(request, 'stocks/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                companies = Company.objects.filter(user=request.user)
                return render(request, 'stocks/index.html', {'companies': companies})
    context = {
        "form": form,
    }
    return render(request, 'stocks/register.html', context)


'''def songs(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Album.DoesNotExist:
            users_songs = []
        return render(request, 'music/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
        })
'''

def run_daily_demand(request,company_id):
    company = get_object_or_404(Company, pk=company_id)
    company_stock_code=company.company_stock_code
    company.demand_daily_under_proc=False
    company.save()
    #return render(request, 'stocks/detail.html', {'company': company})
    #demand_daily_status(request,company_id)
    company.demand_daily_entry,company.demand_daily_stoploss,company.demand_monthly_entry,company.demand_monthly_stoploss,company.demand_weekly_entry,company.demand_weekly_stoploss=demand_execute_function(company_stock_code)
    company.demand_daily_under_proc=True
    company.demand_daily_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
    company.demand_weekly_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
    company.demand_monthly_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
    company.save()
    return render(request, 'stocks/detail.html', {'company': company})

def demand_daily_status(request,company_id):
    company = get_object_or_404(Company, pk=company_id)
    return render(request, 'stocks/detail.html', {'company': company})

def supply_daily_status(request,company_id):
    company = get_object_or_404(Company, pk=company_id)
    return render(request, 'stocks/detail.html', {'company': company})

def run_weekly_demand(request,company_id):
    company = get_object_or_404(Company, pk=company_id)
    company_stock_code=company.company_stock_code
    company.demand_weekly_under_proc=False
    company.demand_weekly_entry,company.demand_weekly_stoploss=demand_week_execute(company_stock_code,1000)
    company.demand_weekly_under_proc=True
    company.demand_weekly_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
    company.save()
    return render(request, 'stocks/detail.html', {'company': company})

def run_monthly_demand(request,company_id):
    company = get_object_or_404(Company, pk=company_id)
    company_stock_code=company.company_stock_code
    company.demand_monthly_under_proc=False
    company.demand_monthly_entry,company.demand_monthly_stoploss=demand_month_execute(company_stock_code,1000)
    company.demand_monthly_under_proc=True
    company.demand_monthly_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
    company.save()
    return render(request, 'stocks/detail.html', {'company': company})

def run_daily_supply(request,company_id):
    company = get_object_or_404(Company, pk=company_id)
    company_stock_code=company.company_stock_code
    company.supply_daily_under_proc=False
    company.supply_daily_entry,company.supply_daily_stoploss,company.supply_monthly_entry,company.supply_monthly_stoploss,company.supply_weekly_entry,company.supply_weekly_stoploss=supply_execute_function(company_stock_code)
    company.supply_daily_under_proc=True
    company.supply_daily_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
    company.supply_weekly_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
    company.supply_monthly_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
    return render(request, 'stocks/detail.html', {'company': company})

def run_weekly_supply(request,company_id):
    company = get_object_or_404(Company, pk=company_id)
    company_stock_code=company.company_stock_code
    company.supply_weekly_under_proc=False
    company.supply_weekly_entry,company.supply_weekly_stoploss=supply_week_execute(company_stock_code,1000)
    company.supply_weekly_under_proc=True
    company.supply_weekly_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
    company.save()
    return render(request, 'stocks/detail.html', {'company': company})

def run_monthly_supply(request,company_id):
    company = get_object_or_404(Company, pk=company_id)
    company_stock_code=company.company_stock_code
    company.supply_monthly_under_proc=False
    company.supply_monthly_entry,company.supply_monthly_stoploss=supply_month_execute(company_stock_code,1000)
    company.supply_monthly_under_proc=True
    company.supply_monthly_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
    company.save()
    return render(request, 'stocks/detail.html', {'company': company})


def download_daily_demand(request,company_id):
    company = get_object_or_404(Company, pk=company_id)
    file_name="Demand_Daywise_files/"+company.company_stock_code+"_demand.txt"
    myfile=open(os.path.join(settings.MEDIA_ROOT, file_name),"r+")
    response = HttpResponse(myfile, content_type='application/txt')
    my_file_name=company.company_stock_code+"_demand.txt"
    response['Content-Disposition'] = 'attachment; filename='+my_file_name
    return response

def download_weekly_demand(request,company_id):
    company = get_object_or_404(Company, pk=company_id)
    file_name="Demand_Weekly_files/Demand_weekly_"+company.company_stock_code+".txt"
    myfile=open(os.path.join(settings.MEDIA_ROOT, file_name),"r+")
    response = HttpResponse(myfile, content_type='application/txt')
    my_file_name="Demand_weekly_"+company.company_stock_code+".txt"
    response['Content-Disposition'] = 'attachment; filename='+my_file_name
    return response

def download_monthly_demand(request,company_id):
    company = get_object_or_404(Company, pk=company_id)
    file_name="Demand_Monthly_files/Demand_monthly_"+company.company_stock_code+".txt"
    myfile=open(os.path.join(settings.MEDIA_ROOT, file_name),"r+")
    response = HttpResponse(myfile, content_type='application/txt')
    my_file_name="Demand_monthly_"+company.company_stock_code+".txt"
    response['Content-Disposition'] = 'attachment; filename='+my_file_name
    return response

def download_daily_supply(request,company_id):
    company = get_object_or_404(Company, pk=company_id)
    file_name="Supply_Daywise_files/"+company.company_stock_code+"_supply.txt"
    myfile=open(os.path.join(settings.MEDIA_ROOT, file_name),"r+")
    response = HttpResponse(myfile, content_type='application/txt')
    my_file_name=company.company_stock_code+"_supply.txt"
    response['Content-Disposition'] = 'attachment; filename='+my_file_name
    return response

def download_weekly_supply(request,company_id):
    company = get_object_or_404(Company, pk=company_id)
    file_name="Supply_Weekly_files/Supply_weekly_"+company.company_stock_code+".txt"
    myfile=open(os.path.join(settings.MEDIA_ROOT, file_name),"r+")
    response = HttpResponse(myfile, content_type='application/txt')
    my_file_name="Demand_supply_"+company.company_stock_code+".txt"
    response['Content-Disposition'] = 'attachment; filename='+my_file_name
    return response

def download_monthly_supply(request,company_id):
    company = get_object_or_404(Company, pk=company_id)
    file_name="Supply_Monthly_files/Supply_monthly_"+company.company_stock_code+".txt"
    myfile=open(os.path.join(settings.MEDIA_ROOT, file_name),"r+")
    response = HttpResponse(myfile, content_type='application/txt')
    my_file_name="Demand_supply_"+company.company_stock_code+".txt"
    response['Content-Disposition'] = 'attachment; filename='+my_file_name
    return response

def run_demand_selected(request):
    companies = Company.objects.all()
    target = open(os.path.join(settings.MEDIA_ROOT,"Demand_Daily_Stock_Entry_Stoploss.txt"), 'w+')
    for company in companies:
        if(company.is_selected):
            company_stock_code=company.company_stock_code
            company.demand_daily_entry,company.demand_daily_stoploss,company.demand_monthly_entry,company.demand_monthly_stoploss,company.demand_weekly_entry,company.demand_weekly_stoploss=demand_execute_function(company_stock_code)
            company.demand_daily_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
            company.demand_weekly_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
            company.demand_monthly_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
            company.save()
            if(company.demand_daily_entry==-1 and company.demand_daily_stoploss==-1 ):
                target.write("%s,No zone found,No zone found\n"%(company.company_stock_code))
            else:
                target.write("%s,%f,%f\n"%(company.company_stock_code,company.demand_daily_entry,company.demand_daily_stoploss))

    return render(request, 'stocks/index.html', {'companies': companies})

def run_supply_selected(request):
    companies = Company.objects.all()
    target = open(os.path.join(settings.MEDIA_ROOT,"Supply_Daily_Stock_Entry_Stoploss.txt"), 'w+')
    for company in companies:
        if(company.is_selected):
            company_stock_code=company.company_stock_code
            company.supply_daily_entry,company.supply_daily_stoploss,company.supply_monthly_entry,company.supply_monthly_stoploss,company.supply_weekly_entry,company.supply_weekly_stoploss=supply_execute_function(company_stock_code)
            company.supply_daily_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
            company.supply_weekly_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
            company.supply_monthly_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
            company.save()
            if(company.supply_daily_entry==-1 and company.supply_daily_stoploss==-1 ):
                target.write("%s,No zone found,No zone found\n"%(company.company_stock_code))
            else:
                target.write("%s,%f,%f\n"%(company.company_stock_code,company.supply_daily_entry,company.supply_daily_stoploss))

    return render(request, 'stocks/index.html', {'companies': companies})

def run_demand_supply_selected(request):
    companies = Company.objects.all()
    target1 = open(os.path.join(settings.MEDIA_ROOT,"Demand_Daily_Stock_Entry_Stoploss.txt"), 'w+')
    target2 = open(os.path.join(settings.MEDIA_ROOT,"Supply_Daily_Stock_Entry_Stoploss.txt"), 'w+')
    for company in companies:
        if(company.is_selected):
            company_stock_code=company.company_stock_code
            company.demand_daily_entry,company.demand_daily_stoploss,company.demand_monthly_entry,company.demand_monthly_stoploss,company.demand_weekly_entry,company.demand_weekly_stoploss=demand_execute_function(company_stock_code)
            company.demand_daily_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
            company.demand_weekly_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
            company.demand_monthly_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
            company.save()
            if(company.demand_daily_entry==-1 and company.demand_daily_stoploss==-1 ):
                target1.write("%s,No zone found,No zone found\n"%(company.company_stock_code))
            else:
                target1.write("%s,%f,%f\n"%(company.company_stock_code,company.demand_daily_entry,company.demand_daily_stoploss))
            company.supply_daily_entry,company.supply_daily_stoploss,company.supply_monthly_entry,company.supply_monthly_stoploss,company.supply_weekly_entry,company.supply_weekly_stoploss=supply_execute_function(company_stock_code)
            company.supply_daily_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
            company.supply_weekly_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
            company.supply_monthly_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
            company.save()
            if(company.supply_daily_entry==-1 and company.supply_daily_stoploss==-1 ):
                target2.write("%s,No zone found,No zone found\n"%(company.company_stock_code))
            else:
                target2.write("%s,%f,%f\n"%(company.company_stock_code,company.supply_daily_entry,company.supply_daily_stoploss))

    return render(request, 'stocks/index.html', {'companies': companies})


def run_demand_all(request):
    companies = Company.objects.all()
    target = open(os.path.join(settings.MEDIA_ROOT,"Demand_Daily_Stock_Entry_Stoploss.txt"), 'w+')
    for company in companies:
        company_stock_code=company.company_stock_code
        company.demand_daily_entry,company.demand_daily_stoploss,company.demand_monthly_entry,company.demand_monthly_stoploss,company.demand_weekly_entry,company.demand_weekly_stoploss=demand_execute_function(company_stock_code)
        company.demand_daily_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
        company.demand_weekly_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
        company.demand_monthly_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
        company.save()
        if(company.demand_daily_entry==-1 and company.demand_daily_stoploss==-1 ):
            target.write("%s,No zone found,No zone found\n"%(company.company_stock_code))
        else:
            target.write("%s,%f,%f\n"%(company.company_stock_code,company.demand_daily_entry,company.demand_daily_stoploss))

    return render(request, 'stocks/index.html', {'companies': companies})

def run_supply_all(request):
    companies = Company.objects.all()
    target = open(os.path.join(settings.MEDIA_ROOT,"Supply_Daily_Stock_Entry_Stoploss.txt"), 'w+')
    for company in companies:
        company_stock_code=company.company_stock_code
        company.supply_daily_entry,company.supply_daily_stoploss,company.supply_monthly_entry,company.supply_monthly_stoploss,company.supply_weekly_entry,company.supply_weekly_stoploss=supply_execute_function(company_stock_code)
        company.supply_daily_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
        company.supply_weekly_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
        company.supply_monthly_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
        company.save()
        if(company.supply_daily_entry==-1 and company.supply_daily_stoploss==-1 ):
            target.write("%s,No zone found,No zone found\n"%(company.company_stock_code))
        else:
            target.write("%s,%f,%f\n"%(company.company_stock_code,company.supply_daily_entry,company.supply_daily_stoploss))

    return render(request, 'stocks/index.html', {'companies': companies})

def run_demand_supply_all(request):
    companies = Company.objects.all()
    target1 = open(os.path.join(settings.MEDIA_ROOT,"Demand_Daily_Stock_Entry_Stoploss.txt"), 'w+')
    target2 = open(os.path.join(settings.MEDIA_ROOT,"Supply_Daily_Stock_Entry_Stoploss.txt"), 'w+')
    for company in companies:
        if(1==1):
            company_stock_code=company.company_stock_code
            company.demand_daily_entry,company.demand_daily_stoploss,company.demand_monthly_entry,company.demand_monthly_stoploss,company.demand_weekly_entry,company.demand_weekly_stoploss=demand_execute_function(company_stock_code)
            company.demand_daily_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
            company.demand_weekly_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
            company.demand_monthly_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
            company.save()
            if(company.demand_daily_entry==-1 and company.demand_daily_stoploss==-1 ):
                target1.write("%s,No zone found,No zone found\n"%(company.company_stock_code))
            else:
                target1.write("%s,%f,%f\n"%(company.company_stock_code,company.demand_daily_entry,company.demand_daily_stoploss))
            company.supply_daily_entry,company.supply_daily_stoploss,company.supply_monthly_entry,company.supply_monthly_stoploss,company.supply_weekly_entry,company.supply_weekly_stoploss=supply_execute_function(company_stock_code)
            company.supply_daily_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
            company.supply_weekly_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
            company.supply_monthly_lastmodified_date=(datetime.now()+timedelta(hours=5,minutes=30)).strftime("%I:%M %p %B %d, %Y")
            company.save()
            if(company.supply_daily_entry==-1 and company.supply_daily_stoploss==-1 ):
                target2.write("%s,No zone found,No zone found\n"%(company.company_stock_code))
            else:
                target2.write("%s,%f,%f\n"%(company.company_stock_code,company.supply_daily_entry,company.supply_daily_stoploss))

    return render(request, 'stocks/index.html', {'companies': companies})

def download_demand_excel(request):
    file_name="Demand_Daily_Stock_Entry_Stoploss.txt"
    myfile=open(os.path.join(settings.MEDIA_ROOT, file_name),"r+")
    response = HttpResponse(myfile, content_type='application/txt')
    my_file_name="Demand_Daily_Stock_Entry_Stoploss.csv"
    response['Content-Disposition'] = 'attachment; filename='+my_file_name
    return response

def download_supply_excel(request):
    file_name="Supply_Daily_Stock_Entry_Stoploss.txt"
    myfile=open(os.path.join(settings.MEDIA_ROOT, file_name),"r+")
    response = HttpResponse(myfile, content_type='application/txt')
    my_file_name="Supply_Daily_Stock_Entry_Stoploss.csv"
    response['Content-Disposition'] = 'attachment; filename='+my_file_name
    return response

def select_all(request):
    companies = Company.objects.all()
    for company in companies:
        company.is_selected=True
        company.save()
    return render(request, 'stocks/index.html', {'companies': companies})
    
def deselect_all(request):
    companies = Company.objects.all()
    for company in companies:
        company.is_selected=False
        company.save()
    return render(request, 'stocks/index.html', {'companies': companies})    





    