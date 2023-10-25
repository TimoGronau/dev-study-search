from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage


from .models import Profile, User
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from .utils import search_profiles

def profiles(request):
    profiles, search_query = search_profiles(request)
    page = request.GET.get('page', 1)
    results = 4
    paginator = Paginator(profiles, results)

    elided_page_range = paginator.get_elided_page_range(number=page)
    profiles = paginator.page(page)


    context = {
        'profiles':profiles, 
        'search_query':search_query, 
        "paginator":paginator, 
        'elided_page_range':elided_page_range
        }
    
    return render(request, "users/profiles.html", context)


def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)

    top_skills = profile.skills.exclude(description__exact="")
    other_skills = profile.skills.filter(description="")

    context = {
        'profile': profile,
        'top_skills': top_skills,
        'other_skills': other_skills,
    }

    return render(request, "users/user-profile.html", context)


def login_user(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == "POST":
        username = request.POST['username']#.lower()
        password = request.POST['password'] 

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # creates session and stores it in browsers cookies
            login(request, user)
            return redirect(request.GET["next"] if "next" in request.GET else "account") #redirect to next value from url!
        else:
            messages.error(request, "Username or password incorrect!")

    return render(request, "users/login_register.html")


def logout_user(request):
    logout(request)
    messages.success(request, "User was logged out successfully")
    return redirect('login')


def register_user(request):
    page = 'register'
    form = CustomUserCreationForm

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # creates a user instance for further processing before saving
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "Account was created successfully!")

            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(
                request, 'An error has occured during registration!')
    context = {
        'page': page,
        'form': form,
    }
    return render(request, 'users/login_register.html', context)


@login_required(login_url="login")
def user_account(request):
    # always gives u the currently logged in user that is doing the requesting
    profile = request.user.profile
    skills = profile.skills.all()
    projects = profile.project_set.all()
    context = {
        "profile": profile,
        "skills": skills,
        "projects": projects,
    }
    return render(request, 'users/account.html', context)


@login_required(login_url="login")
def edit_account(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {
        'form': form
    }

    return render(request, "users/profile_form.html", context)


@login_required(login_url='login')
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save()
            profile.skills.add(skill)
            messages.success(request, f"Added your new skill: {skill.name}")
            return redirect("account")

    context = {
        "form": form
    }

    return render(request, "users/skill_form.html", context)


@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skills.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect("account")

    context = {
        "form": form
    }

    return render(request, "users/skill_form.html", context)


@login_required(login_url='login')
def delete_skill(request, pk):
    profile = request.user.profile
    skill = profile.skills.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(
            request, f'Skill "{skill.name}" was deleted successfully!')
        return redirect("account")
    context = {
        "object": skill  # needs to be object bc specified as such in template
    }

    return render(request, "delete_template.html", context)






# @login_required(login_url="login")
# def view_message(request, pk):
#     profile = request.user.profile
#     message = profile.messages.get(id=pk)
#     if message.is_read == False:
#         message.is_read = True
#         message.read_at = message.modified_at
#         message.save()
    
#     context = {
#         "message": message
#     }

#     return render(request, "users/message.html", context)


# def send_message(request, pk):
#     recipient = Profile.objects.get(id=pk)
#     form = MessageForm()

#     try:
#         sender = request.user.profile
#     except:
#         sender = None

#     if request.method == "POST":
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.sender = sender
#             message.recipient = recipient

#             if sender:
#                 message.name = sender.name
#                 message.email = sender.email
#             message.save()

#             messages.success(request, "Your message was sent successfully!")
#             return redirect("user-profile", pk=recipient.id)
     
#     context = {
#         "recipient": recipient,
#         "form": form,
#     }

#     return render(request, "users/message_form.html", context)