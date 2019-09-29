import logging
import os


    # from django.views.decorators.cache import never_cache  # This adds headers to a response so that it will never be cached.
# from django.conf import settings  #Disabled for AREPL
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
    # from django.views.generic import TemplateView

    # Serve Single Page Application
    # index = never_cache(TemplateView.as_view(template_name='index.html'))


from common_words import common_words  # A list of common or short words that can be safely ignored since they are not in the database.
# from backend.common_words import common_words  # A list of common or short words that can be safely ignored since they are not in the database.

import csv  # Needed to open .CSV files.
# import string  # Needed to strip punctuation from unfiltered_lyrics.
import re  # Needed to strip punctuation from unfiltered_lyrics.
# from collections import OrderedDict 

# file = open(os.path.join(settings.STATICFILES_DIRS, './CSV/testFile.csv'), 'r')  # A smaller version of the word database.

# file = open(os.path.join(settings.STATIC_URL, 'testFile.csv'))

# Where am I?
# cwd = os.getcwd()
# files = os.listdir(cwd)
# print(cwd)
# print(files)


# These work locally:
file = open('./CSV/testFile.csv', 'r')  # A smaller version of the word database.
# file = open('./CSV/libra.csv', 'r')  # The full version of the word database.
# librareader = csv.reader(file)  # Saves the CSV file to a variable.





class FrontendAppView(View):
    """
    Serves the compiled frontend entry point (only works if you have run `yarn
    run build`).
    """

    def get(self, request):
        try:
            with open(os.path.join(settings.STATIC_ROOT, 'index.html')) as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            logging.exception('Production build of app not found')
            return HttpResponse(
                """
                This URL is only used when you have built the production
                version of the app. Visit http://localhost:3000/ instead, or
                run `yarn run build` to test the production version.
                """,
                status=501,
            )


class ApiView(View):

    def get(self, request):
        return JsonResponse({
            "def get": "This is a get request."
        })

    @csrf_exempt
    def post(self, request):
        return JsonResponse({
            "def post": "This is a post request."
        })


class SongView(View):

    def __init__(self, title):
        self.title = title

    def __str__(self):
        return f'The {self.title} song.'

    def get(self, request):
        return JsonResponse({
            "def get": "This is a get request."
        })



watchtower = SongView('All Along the WatchTower')
print(watchtower)
# print(watchtower.get())

# print(SongView.get(ThisSong, 'GET'))

print(common_words)