from django.urls.converters import SlugConverter

class EmptyOrSlugConverter(SlugConverter):
    regex = '[-a-zA-Z0-9_]*'