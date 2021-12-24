import django_filters
from blog.models import Post

class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ['author']
        
        @property
        def qs(self):
            parent = super().qs
            author = getattr(self.request, 'author', None)
            
            return parent.filter(author=author)