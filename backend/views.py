from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache  # This adds headers to a response so that it will never be cached.

# Serve Single Page Application
index = never_cache(TemplateView.as_view(template_name='index.html'))
