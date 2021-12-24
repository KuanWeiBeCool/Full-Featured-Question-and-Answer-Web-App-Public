from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import forms
from blog.models import Post
from django_filters.views import FilterView
from .filtersets import PostFilter
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView



def register_login(request):
    '''
    View for both sign in and sign up page.
    '''
    form = forms.RegisterForm()
    if request.method == "POST":
        if 'email' in request.POST:
            # Register
            # request.POST contains a dictionary with the fields. e.g.
            # <QueryDict: {'csrfmiddlewaretoken': ['2MYOE0z4pz2RGG2DKYjGi5hPYXFeWc5ZXK2SauvS4JBY6QszJ55ImccaKrj0fSZS'], 
            # # 'username': ['kuanw'], 'email': ['kuan.wei0413@gmail.com'], 'password1': ['1234'], 'password2': ['1234']}>
            
            form = forms.RegisterForm(request.POST)
            
            if form.is_valid():
                form.save()
                username = request.POST['username']
                password = request.POST['password1']
                user = authenticate(request, username=username, password=password)
                login(request, user)
                messages.success(request, f"Welcome, {username}!")
                return redirect('user-confirmation')
            # leave sign_up checked so that the page will remain on the sign up page
            return render(request, 'users/login.html', {'form':form, 'sign_up':"checked", 'sign_in':""})
        else:
            # Login
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {username}!")
                return redirect('blog-home')
            else:
                messages.error(request, "Whoops, your username and password didn't match. Please try again.")
                return render(request, 'users/login.html', {'form':form, 'sign_up':"", 'sign_in':"checked"})
            # leave sign_up checked so that the page will remain on the sign up page

    # When just entered the page, by default will be sign in page
    return render(request, 'users/login.html', {'form':form, 'sign_up':"", 'sign_in':"checked"})


def confirmation(request):
    '''
    View for successfully signed up.
    '''
    return render(request, "users/confirmation.html")


def logout_user(request):
    '''
    View for the logout. 
    '''
    logout(request)
    messages.info(request, "You've logged out!")
    return redirect('blog-home')


class PostListView(ListView):
    '''
    This view is for profile page. It inherits from ListView, and applies the filter to select only the posts
    that matches the author.
    '''
    model = Post
    template_name = 'users/my_posts.html'
    context_object_name = 'posts'
    paginate_by = 1 # show 3 posts per page
    
    
    # Override get_queryset for the filter
    def get_queryset(self):
        return self.request.user.post_set.all().order_by('-date_posted')
    
    
    # Override get_context_data for the highlight of the buton
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['active_1'] = 'active'
        return context
    

class PostListViewGuest(ListView):
    '''
    This view is for guest visit page. It inherits from ListView, and applies the filter to select only the posts
    that matches the author.
    '''
    model = Post
    template_name = 'users/guest_posts.html'
    context_object_name = 'posts'
    paginate_by = 1 # show 3 posts per page
    
    
    # Override get_queryset for the filter
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return user.post_set.all().order_by('-date_posted')
    
        
    # Override get_context_data for the highlight of the buton
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        return context




@login_required
def update_profile(request):
    '''
    View to update the profile of a user. Need to login first.
    '''
    # In update_profile.html, there is a form with method "POST". Once click "Update", the form will submit
    # and change the request method to "POST". If no submission is performed, we simply display the page.
    print(request.user)
    if request.method == 'POST':

        u_form = forms.UserUpdateForm(request.POST, instance = request.user) # request.user gets the instance of the user in the request
        if u_form.is_valid:
            u_form.save()
            messages.success(request, "You've just updated your profile!")
            return redirect('user-profile')
    else:
        u_form = forms.UserUpdateForm(instance = request.user)

    # "active_i is for the highlight of the column on the right"
    context = {
        'u_form':u_form,
        'active_1':'',
        'active_2':'active',
        'active_3':'',
        'active_4':'',
    }

    return render(request, 'users/update_profile.html', context=context)

@login_required
def update_password(request):
    '''
    View to update the password of a user. Need to login first.
    '''
    if request.method == 'POST':
        pw_form = PasswordChangeForm(request.user, request.POST)
        if pw_form.is_valid():
            user = pw_form.save()
            update_session_auth_hash(request, user)  # update the session so that the user won't be forced logging out due to the change of password
            messages.success(request, "You've just updated your password!")
            return redirect('user-password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        pw_form = PasswordChangeForm(request.user)
        
        # "active_i is for the highlight of the column on the right"
    context = {
        'pw_form':pw_form,
        'active_1':'',
        'active_2':'',
        'active_3':'active',
        'active_4':'',
    }
    return render(request, 'users/update_password.html', context=context)



@login_required
def update_picture(request):
    '''
    View to update the profile picture of a user. Need to login first.
    '''
    if request.method == 'POST':
        p_form = forms.ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
        if p_form.is_valid:
            p_form.save()
            messages.success(request, "You've just updated your profile picture!")
            return redirect('user-picture')
    else:
        p_form = forms.ProfileUpdateForm(instance = request.user.profile)
        
    # "active_i is for the highlight of the column on the right"
    context = {
        'p_form':p_form,
        'active_1':'',
        'active_2':'',
        'active_3':'',
        'active_4':'active',
    }

    return render(request, 'users/update_picture.html', context=context)



# @login_required
# def my_posts(request):
#     '''
#     View to see the posts for this user. Need to login first.
#     '''
#     # get all posts by the user
#     username = request.user
#     user_posts = Post.objects.filter(author = username)
#     paginated_by = 2
#     p = Paginator(user_posts, paginated_by)
    
#     context = {
#         'posts': user_posts,
#         'page_obj': p,
#         'active_1':'active',
#         'active_2':'',
#         'active_3':'',
#         'active_4':'',
#     }
#     # Using context parameter, whatever information we pass in as the context will be accessible in the templates
#     return render(request, 'users/my_posts.html', context=context)