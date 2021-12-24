from django.shortcuts import get_object_or_404, render, get_list_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.views.generic.edit import FormMixin
from .models import Category, Post, Comment
from django.db.models import Q
from.forms import CommentForm, FilterForm, CreateForm, UpdateForm
from django.http import HttpResponseRedirect
from django.urls import reverse

# Class based views
class PostListView(ListView):
    '''
    This view is for the home page. It inherits from a ListView for a list of posts
    '''
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted'] # latest to be on the top
    paginate_by = 1 # show 1 posts per page
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = FilterForm(initial={
            'search': self.request.GET.get('search', ''),
            'filter_field': self.request.GET.get('filter_field', ''),
        })
        context['category_list'] = Category.objects.all()
        return context

class SearchResultsView(ListView):
    '''
    This view is for the search results
    '''
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 1 # show 1 posts per page
    
    def get_queryset(self):
        query = self.request.GET.get('search')
        filter_field = self.request.GET.get('filter_field')
        if filter_field == "all":
            result =  Post.objects.filter(
                    Q(author__username__icontains=query) |
                    Q(title__icontains=query) |
                    Q(content__icontains=query)
                )
            if result:
                return result.order_by('-date_posted')
            else:
                return result
        elif filter_field == "author":
            result = Post.objects.filter(Q(author__username__icontains=query))
            if result:
                return result.order_by('-date_posted')
            else:
                return result 
        elif filter_field == "title":
            result = Post.objects.filter(Q(title__icontains=query))    
            if result:
                return result.order_by('-date_posted')
            else:
                return result       
        elif filter_field == "content":
            result = Post.objects.filter(Q(content__icontains=query))  
            if result:
                return result.order_by('-date_posted')
            else:
                return result 
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = FilterForm(initial={
            'search': self.request.GET.get('search', ''),
            'filter_field': self.request.GET.get('filter_field', ''),
        })
        context['category_list'] = Category.objects.all()

        return context
    
class PostDetailView(FormMixin, DetailView):
    '''
    This view is for the individual post once user click the post title
    '''
    model = Post
    context_object_name = 'post'
    form_class = CommentForm
    
    def get_success_url(self):
        return reverse('post-detail', kwargs = {
            'pk': self.object.id
        })
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context  
        
    def post(self, request, *args, **kwargs):
        self.object = super().get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form):
        form.instance.post = self.get_object()
        form.instance.author = self.request.user
        form = form.save()
        return super().form_valid(form)

# class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, FormMixin, DetailView):
#     '''
#     This view is for the individual post once user click the post title
#     '''
#     model = Post
#     context_object_name = 'post'
#     template_name = "blog/comment_update_form.html"
#     form_class = CommentForm
    
#     def get_success_url(self):
#         return reverse('post-detail', kwargs = {
#             'pk': self.kwargs.get('pk')
#         })
        
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         form = self.get_form()
#         form.instance = get_object_or_404(Comment, id=self.kwargs.get('pk_comment'))
#         print(form.instance)
#         context['form'] = form
#         return context  
    
#     def post(self, request, *args, **kwargs):
#         self.object = super().get_object()
#         form = self.get_form()
#         print(form.is_valid())
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
        
#     def form_valid(self, form):
#         form.instance = get_object_or_404(Comment, id=self.kwargs.get('pk_comment'))
#         print(form.instance)
#         form = form.save()
#         return super().form_valid(form)
#     # Test to see if the user that attempts to update the post is actually the user loggin
#     def test_func(self):
#         comment_id = self.kwargs.get('pk_comment')
#         comment = Comment.objects.filter(id=comment_id).first()
#         if self.request.user == comment.author:
#             return True
#         return False



class PostCreateView(LoginRequiredMixin, CreateView):
    '''
    This view is for creating the post. Login required
    '''
    model = Post
    fields = ['title', 'category', 'content']
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = CreateForm(initial={
            'title': self.request.GET.get('title', ''),
            'category': self.request.GET.get('category', ''),
            'content': self.request.GET.get('content', ''),           
        })

        return context    
    # Set the author of the post to be the author currently login
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    '''
    This view is for updating the post. Login required
    '''
    model = Post
    fields = ['title', 'category', 'content']
    template_name = 'blog/update_form.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # Get the form pre-filled by the original content
        original_post = self.get_form_kwargs().get('instance')
        context['form'] = UpdateForm(initial={
            'title': self.request.GET.get('title', original_post.title),
            'category': self.request.GET.get('category', original_post.category),
            'content': self.request.GET.get('content', original_post.content),           
        })
        
        return context
    
    # Set the author of the post to be the author currently login
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)   
    
    # Test to see if the user that attempts to update the post is actually the user loggin
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
    
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    '''
    This view is for updating the comment. Login required
    '''
    model = Comment
    fields = ['content']
    template_name = 'blog/comment_update_form.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # Get the form pre-filled by the original content
        original_comment = self.get_form_kwargs().get('instance')
        context['form'] = CommentForm(initial={
            'content': self.request.GET.get('content', original_comment.content),           
        })   
        return context
    
    # Set the author of the post to be the author currently login
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)   
    
    # Test to see if the user that attempts to update the post is actually the user loggin
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False    
    
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''
    This view is for deleting a post
    '''
    model = Post
    success_url = '/' # Once successfully deleted we go to the home page
    # Test to see if the user that attempts to update the post is actually the user loggin
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
  
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''
    This view is for deleting a post
    '''
    model = Comment
    template_name = "blog/comment_confirm_delete.html"
    def get_success_url(self):
        return reverse('post-detail', kwargs = {
            'pk': self.object.post.id
        })
    # Test to see if the user that attempts to update the post is actually the user loggin
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False    
    
class PostCategoryView(ListView):
    '''
    This view is for filtering by category. 
    '''
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 1 # show 1 posts per page
    
    # Override get_queryset for the filter
    def get_queryset(self):
        category = self.kwargs.get('category')
        return Post.objects.filter(category=category).order_by('-date_posted')
    
        
    # Override get_context_data for the highlight of the buton
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['form'] = FilterForm(initial={
            'search': self.request.GET.get('search', ''),
            'filter_field': self.request.GET.get('filter_field', ''),
        })
        category = self.kwargs.get('category')
        context[category] = 'active'

        return context


class CategorySearchResultView(ListView):
    '''
    This view is for filtering by category. 
    '''
    model = Post
    template_name = 'blog/search_results_with_category.html'
    context_object_name = 'posts'
    paginate_by = 1 # show 1 posts per page
    
    def get_queryset(self):
        query = self.request.GET.get('search')
        filter_field = self.request.GET.get('filter_field')
        category = self.kwargs.get('category')
        if filter_field == "all":
            result =  Post.objects.filter(
                    Q(category__icontains=category) &
                    (Q(author__username__icontains=query) |
                    Q(title__icontains=query) |
                    Q(content__icontains=query))
                )
            if result:
                return result.order_by('-date_posted')
            else:
                return result
        elif filter_field == "author":
            result = Post.objects.filter(Q(category__icontains=category) & Q(author__username__icontains=query))
            if result:
                return result.order_by('-date_posted')
            else:
                return result 
        elif filter_field == "title":
            result = Post.objects.filter(Q(category__icontains=category) & Q(title__icontains=query))    
            if result:
                return result.order_by('-date_posted')
            else:
                return result       
        elif filter_field == "content":
            result = Post.objects.filter(Q(category__icontains=category) & Q(content__icontains=query))  
            if result:
                return result.order_by('-date_posted')
            else:
                return result 
        
    # Override get_context_data for the highlight of the buton
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['form'] = FilterForm(initial={
            'search': self.request.GET.get('search', ''),
            'filter_field': self.request.GET.get('filter_field', ''),
        })

        return context
  
  
  
def LikeView(request, pk):
    '''
    This view is for post like button. It saves the like into database
    '''
    post = get_object_or_404(Post, id=request.POST.get('post_id')) # Note post_id is the name of the like button in the html
    post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))

def CommentLikeView(request, pk):
    '''
    This view is for comment like button. It saves the like into database
    '''
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id')) # Note comment_id is the name of the like button in the html
    comment.likes.add(request.user)
    
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


class CommentCreateView(LoginRequiredMixin, CreateView):
    '''
    This view is for creating the post. Login required
    '''
    model = Post
    fields = ['post', 'content']
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = CreateForm(initial={
            'content': self.request.GET.get('content', ''),           
        })

        return context    
    # Set the author of the post to be the author currently login
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

  
def CommentAddView(request, pk):
    '''
    This view is for comment like button. It saves the like into database
    '''
    post = get_object_or_404(Post, id=request.POST.get('make_comment')) # Note comment_id is the name of the like button in the html
    comment = Comment()
    
    comment.likes.add(request.user)
    
    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))  
# def home(request):
#     '''
#     Handle the traffic of the Home Page for the blog app
#     '''

#     context = {
#         'posts': Post.objects.all(),
#         'title': "Kuan"
#     }
#     # Using context parameter, whatever information we pass in as the context will be accessible in the templates
#     return render(request, 'blog/home.html', context=context)    

# def about(request):
#     '''
#     Handle the traffic of the About Page for the blog app
#     '''

#     return render(request, 'blog/about.html', context={'title':'Vivian'})