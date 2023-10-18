from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.contrib import messages


from .models import Project
from .forms import ProjectForm, ReviewForm
from .utils import search_projects



def projects(request):
    projects, search_query = search_projects(request)
    page = request.GET.get('page', 1)
    results = 6
    paginator = Paginator(projects, results)

    elided_page_range = paginator.get_elided_page_range(number=page)
    projects = paginator.page(page)
    
    context = {
            'projects':projects, 
            'search_query':search_query, 
            "paginator":paginator, 
            'elided_page_range':elided_page_range
            }
    
    return render(request, "projects/projects.html", context)



def project(request, pk):
    project_obj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = project_obj
            review.owner = request.user.profile
            review.save()

            project_obj.get_vote_count

            messages.success(request, "Review submitted!")
            return redirect("project", pk=project_obj.id)

    context = {
        "project": project_obj,
        "form": form,
    }

    return render(request, "projects/single-project.html", context)



@login_required(login_url='login')
def create_project(request):
    form = ProjectForm()
    profile = request.user.profile

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect("account")

    context = {'form': form}
    return render(request, "projects/project_form.html", context)



@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("account")

    context = {'form': form}
    return render(request, "projects/project_form.html", context)



@login_required(login_url='login')
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect("account")
    context = {
        "object": project,
    }
    return render(request, "delete_template.html", context)


