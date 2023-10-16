from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


from .models import Profile


def paginate_profiles(request, profiles, results):
    page = request.GET.get('page')
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page) #only get the first page
    
    except PageNotAnInteger: #for first click on profiles where page is not specified
        page = 1

    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    left_index = (int(page) - 4)
    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 5)
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages +1

    custom_range = range(left_index, right_index)

    return custom_range, profiles



def search_profiles(request):
    search_query = ""

    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query) |
        Q(skills__name__icontains=search_query)     
        )
    
    return profiles, search_query