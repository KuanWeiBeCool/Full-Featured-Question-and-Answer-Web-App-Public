from django import template
from urllib.parse import urlencode


register = template.Library()

@register.simple_tag
def url_replace (request, field, value):
    '''
    This function is to modify the url of the search result when combined with pagination. 
    Normally, pagination will change the url to be something like /search/?page=2 from the search result
    like /search/?search=vivian&filter_field=all. This causes page unable to load because the url is different.
    This function modifies the url so that it'll remain /search/?search=vivian&filter_field=all.
    '''
    dict_ = request.GET.copy()
    dict_[field] = value

    return dict_.urlencode()