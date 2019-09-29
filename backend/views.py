# For graphing
# import matplotlib.pyplot as plt
# plt.plot([1, 2, 3, 4])
# plt.ylabel('some numbers')
# plt.show()


# Python imports:
# from collections import OrderedDict 
import csv  # Needed to open .CSV files.
import logging
import os
import re  # Needed to strip punctuation from unfiltered_lyrics.
# import string  # Needed to strip punctuation from unfiltered_lyrics.


# Where am I?
# cwd = os.getcwd()
# files = os.listdir(cwd)
# print(cwd)
# print(files)


# Django imports:
    # from django.views.decorators.cache import never_cache  # This adds headers to a response so that it will never be cached.
# from django.conf import settings  #Disabled for AREPL
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
    # from django.views.generic import TemplateView

    # Serve Single Page Application
    # index = never_cache(TemplateView.as_view(template_name='index.html'))


# SongFeels imports
from common_words import common_words  # A list of common or short words that can be safely ignored since they are not in the VAD database.
# from backend.common_words import common_words  # A list of common or short words that can be safely ignored since they are not in the VAD database.


# file = open(os.path.join(settings.STATICFILES_DIRS, './CSV/testFile.csv'), 'r')  # A smaller version of the VAD database.

# file = open(os.path.join(settings.STATIC_URL, 'testFile.csv'))


# These work locally:
file = open('./CSV/testFile.csv', 'r')  # A smaller version of the VAD database.
# file = open('./CSV/libra.csv', 'r')  # The full version of the VAD database.
librareader = csv.reader(file)  # Saves the CSV file to a variable.



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

    def __init__(self):
        self.title = ''
        self.unfiltered_lyrics = ''  # The original lyrics from the API.
        self.filtered_lyrics = []  # The data-cleaned lyrics for the song.
        self.vad_lyrics = []  # Only the lyrics that appeared in the VAD database.

    def __str__(self):
        return f'The {self.title} song.'

    def callLyricsAPI(self):
        # Makes a call to Lyrics API and returns lyrics.

        self.title = 'The Rising Sun Blues'

        self.unfiltered_lyrics = "There is a house in New Orleans they call the Rising Sun It’s been the ruin of many a poor girl and me, O God, for one If I had listened what Mama said, I’d be at home today Being so young and foolish, poor boy, let a rambler lead me astray Go tell my baby sister never do like I have done To shun that house in New Orleans they call the Rising Sun My mother she’s a tailor, she sewed these new blue jeans My sweetheart, he’s a drunkard, Lord, Lord, drinks down in New Orleans The only thing a drunkard needs is a suitcase and a trunk The only time he’s satisfied is when he’s on a drunk Fills his glasses to the brim, passes them around Only pleasure he gets out of life is hoboin’ from town to town One foot is on the platform and the other one on the train I’m going back to New Orleans to wear that ball and chain Going back to New Orleans, my race is almost run Going back to spend the rest of my days beneath that Rising Sun"

        # Several steps must be taken to prepare the lyrics before comparing to VAD database:
        # Remove special characters and punctuation.
        # Convert to lowercase.
        # Split words into a list.
        # Add into a set to remove any duplicates.
        # Sort words alphabetically.
        # Removes any common or short words that can be safely ignored since they are not in the database.
        # This reduces 'The Rising Sun Blues' lyrics from 190 to 76.
        filtered_lyrics = self.removeSpecialCharacters(self.unfiltered_lyrics)
        filtered_lyrics = self.splitIntoList(filtered_lyrics)
        filtered_lyrics.sort()  # Sorts list alphabetically.
        self.filtered_lyrics = self.removeCommonWords(filtered_lyrics)

        # Searches the VAD database for the filtered_lyrics.
        # This will assign numerical value to each word found.
        # 'The Rising Sun Blues' lyrics have 53 hits.
        self.vad_lyrics = self.compareToVADfile(filtered_lyrics)

        return ""


    def removeSpecialCharacters(self, lyrics):  # Removes all special characters from text and converts to lowercase.
        return re.sub('[^A-Za-z0-9\']+', ' ', lyrics).lower()


    def splitIntoList(self, lyrics):  # Splits into list, adds into set to remove duplicates.
        return list(set(lyrics.split()))


    def removeCommonWords(self, lyrics):  # Removes any lyrics that are common_words.
        for word in common_words:
            if word in lyrics:  # If a common word is in lyrics, it is removed.
                lyrics.remove(word)
            #     print(f'Removing common word: {word}')

        return lyrics


    def compareToVADfile(self, lyrics):
        length = len(lyrics)
        vad_lyrics = []

        for line in librareader:  # For each line in VAD database CSV file.
            word=line[1]  # Takes word from B column of CSV.

            if word in lyrics:  # If current word of CSV matches a word in the lyrics.
                # print(f'Matching word found: {word}')
                vad_lyrics.append(word)

        return vad_lyrics


    def get(self, request):
        return JsonResponse({
            "def get": "This is a get request."
        })



rising_sun = SongView()
rising_sun.callLyricsAPI()

print(rising_sun.title)
print()
print(rising_sun.unfiltered_lyrics.count(' '))
print(rising_sun.unfiltered_lyrics)
print()
print(len(rising_sun.filtered_lyrics))
print(rising_sun.filtered_lyrics)
print()
print(len(rising_sun.vad_lyrics))
print(rising_sun.vad_lyrics)


# print(SongView.get(ThisSong, 'GET'))

# print(common_words)