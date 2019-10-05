# For graphing
# import matplotlib.pyplot as plt
# plt.plot([1, 2, 3, 4])
# plt.ylabel('some numbers')
# plt.show()


# Python imports:
# from collections import OrderedDict 
import csv  # Needed to open .CSV files.
import dotenv
import json
import logging
import os
import re  # Needed to strip punctuation from unfiltered_lyrics.
import requests  # Needed to make API calls.
# import string  # Needed to strip punctuation from unfiltered_lyrics.

dotenv.load_dotenv()
audd_key = os.environ.get('AUDD_API_KEY')


# Where am I?
# cwd = os.getcwd()
# files = os.listdir(cwd)
# print(cwd)
# print(files)


# Django imports:
    # from django.views.decorators.cache import never_cache  # This adds headers to a response so that it will never be cached.
from django.conf import settings  #Disabled for AREPL
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
    # from django.views.generic import TemplateView

    # Serve Single Page Application
    # index = never_cache(TemplateView.as_view(template_name='index.html'))


# SongFeels imports
from backend.common_words import common_words  # A list of common or short words that can be safely ignored since they are not in the VAD database.
from backend.special_words import special_words  # A list of special words that can be safely ignored since they are not actually part of the lyrics.
# from backend.common_words import common_words  # A list of common or short words that can be safely ignored since they are not in the VAD database.


# file = open(os.path.join(settings.STATICFILES_DIRS, './CSV/testFile.csv'), 'r')  # A smaller version of the VAD database.

# file = open(os.path.join(settings.STATIC_URL, 'testFile.csv'))


# These work locally:
file = open('backend/testFile.csv', 'r')  # A smaller version of the VAD database.
# file = open('backend/libra.csv', 'r')  # A smaller version of the VAD database.
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

    def removeSpecialCharacters(self, lyrics):  # Removes all special characters and numbers from text.
        return re.sub('[^A-Za-z\']+', ' ', lyrics)


    def splitIntoList(self, lyrics):  # Splits into list, adds into set to remove duplicates.
        return list(set(lyrics.split()))


    def removeCommonWords(self, lyrics):  # Removes any lyrics that are common_words.
        for word in common_words:
            if word in lyrics:  # If a common word is in lyrics, it is removed.
                lyrics.remove(word)
            #     print(f'Removing common word: {word}')

        return lyrics

    def removeSpecialWords(self, lyrics):  # Removes any lyrics that are special_words.
        for word in special_words:
            if word in lyrics:  # If a special word is in lyrics, it is removed.
                lyrics.remove(word)
            #     print(f'Removing special word: {word}')

        return lyrics


    # def convertToVad(self, num):  # Converts the database value (1 to 10) into a Vad number (-1 to 1).
    #     num = ((float(num) - 5) / 10)

    #     if num > 0:
    #         num = num + .5
    #     else:
    #         num = num - .5
    #     return num


    def whichEmotionBasic(self, valence, arousal, dominance):  # Tries to assign an emotion based on Valence, Arousal, and Dominance values.
        if valence >= 6:  # A positive emotion.
            if valence >= 8.47:
                return "Happy"  # Joy
            else:
                return "Excited"  # Surprise
        else:  # A negative emotion.
            if dominance <= 5:  # A powerless emotion
                if arousal >= 7.1:
                    return "Fear"
                else:
                    return "Sad"
            else:
                if arousal >= 7.7:
                    return "Anger"
                else:
                    return "Bored"




    # def whichEmotionSpecific(self, valence, arousal, dominance):  # Tries to assign an emotion based on Valence, Arousal, and Dominance values.
    #     # Gloomy
    #     if (valence <= -.75 and arousal <= 0):
    #         return "Sadness"
    #     elif (valence <= -.75 and arousal > 0):
    #         return "Fear"
    #     elif (valence <= -.64 and arousal > 0):
    #         return "Disgust"
    #     elif (valence <= -.54 and arousal > 0):
    #         return "Anger"
    #     # Bored
    #     # Indifferent
    #     # Overwhelmed
    #     # Anxious
    #     # Shy

    #     # Consoled
    #     # Hopeful
    #     # Inspired
    #     # Relaxed
    #     # Peaceful
    #     # Plesant
    #     elif (valence >= .8 and arousal > 0):
    #         return "Joy"
    #     elif (valence >= .64 and arousal > 0):
    #         return "Surprise"
    #     else:
    #         return "Neutral"


    def getVADaverages(self):
        print('\nhihihi\n')
        # count = 0
        word_count = len(rising_sun.vad_lyrics)
        v_mean_sum__average = 0
        a_mean_sum__average = 0
        d_mean_sum__average = 0
        v_mean_sum__total = 0
        a_mean_sum__total = 0
        d_mean_sum__total = 0

        vad_total = 0

        for word in self.vad_lyrics:  # For each lyric that has been found in the VAD database.
            # count = count + 1
            # print(word['v_mean_sum'])
            v_mean_sum__average += word['v_mean_sum']  # Used for average; keeps positive and negative signs.
            a_mean_sum__average += word['a_mean_sum']
            d_mean_sum__average += word['d_mean_sum']

            v_mean_sum__total += abs(word['v_mean_sum'])  # Used for total; ignores negative signs.
            a_mean_sum__total += abs(word['a_mean_sum'])
            d_mean_sum__total += abs(word['d_mean_sum'])


            # vad_total += abs(v_mean_sum__total) + abs(a_mean_sum__total) + abs(d_mean_sum__total)  # Total valence, arousal, and dominance.  Ignores negative sign.

        v_mean_sum__average = v_mean_sum__average / word_count  # average = Total values / words in lyrics.
        a_mean_sum__average = a_mean_sum__average / word_count
        d_mean_sum__average = d_mean_sum__average / word_count

        vad_total += v_mean_sum__total + a_mean_sum__total + d_mean_sum__total  # Grand total; ignores negative sign.

        print(f'{len(rising_sun.vad_lyrics)} words')
        print(v_mean_sum__average)
        print(a_mean_sum__average)
        print(d_mean_sum__average)
        print(self.whichEmotionBasic(v_mean_sum__average, a_mean_sum__average, d_mean_sum__average))
        print()

        print(v_mean_sum__total)
        print(a_mean_sum__total)
        print(d_mean_sum__total)
        print(vad_total)
        
        # print(self.vad_lyrics)
        



    def compareToVADfile(self, lyrics):
        length = len(lyrics)
        vad_lyrics = []

        for line in librareader:  # For each line in VAD database CSV file.
            word = line[1]  # Takes word from B column of CSV.

            if word in lyrics:  # If current word of CSV matches a word in the lyrics.
                print(f'Matching word found: {word}')
                v_mean_sum = float(line[2])  # Valence Mean sum.
                a_mean_sum = float(line[5])  # Arousal Mean sum.
                d_mean_sum = float(line[8])  # Dominance Mean sum

                emotionBasic = self.whichEmotionBasic(v_mean_sum, a_mean_sum, d_mean_sum)

                vad_lyrics.append({'word':word, 'v_mean_sum':v_mean_sum, 'a_mean_sum':a_mean_sum, 'd_mean_sum':d_mean_sum, 'emotionBasic':emotionBasic})

        return vad_lyrics


    def get(self, request):
        singer = 'animals'
        song = 'rising sun'

        query = request.GET.urlencode()
        print(query)

        return JsonResponse({
            'query': query
        })

        # try:
            # data = {
            #     'api_token' : audd_key
            # }
            # response = requests.get(f'https://api.audd.io/findLyrics/?q={singer}%20{song}', data=data)
            # body = json.loads(response.content)
            # print (body['result'][0]['lyrics'])
            # return JsonResponse({
            #     'lyrics': body['result'][0]['lyrics']
        # })
        # except:
        #     return JsonResponse({
        #         'error': response.status_code,
        #         'message': 'Something went wrong!'
        # })

    def callLyricsAPI(self):
        # Makes a call to Lyrics API and returns lyrics.

        self.title = 'The Rising Sun Blues'

        self.unfiltered_lyrics = "Every night in my dreams I see you, I feel you That is how I know you go on Far across the distance And spaces between us You have come to show you go on Near, far, wherever you are I believe that the heart does go on Once more you open the door And you're here in my heart And my heart will go on and on Love can touch us one time And last for a lifetime And never let go till we're gone Love was when I loved you One true time I hold to In my life we'll always go on Near, far, wherever you are I believe that the heart does go on Once more you open the door And you're here in my heart And my heart will go on and on You're here, there's nothing I fear And I know that my heart will go on We'll stay forever this way You are safe in my heart and My heart will go on and on " # 

        # Several steps must be taken to prepare the lyrics before comparing to VAD database:
        # Remove special characters and punctuation.
        # Convert to lowercase.
        # Split words into a list.
        # Add into a set to remove any duplicates.
        # Sort words alphabetically.
        # Removes any common or short words that can be safely ignored since they are not in the database.
        # This reduces 'The Rising Sun Blues' lyrics from 190 to 76.

        filtered_lyrics = self.unfiltered_lyrics.lower()  # Converts to lowercase.
        print(f'a {filtered_lyrics}\n')

        filtered_lyrics = self.removeSpecialCharacters(filtered_lyrics)  # Removes special characters.
        print(f'b {filtered_lyrics}\n')
        
        filtered_lyrics = self.splitIntoList(filtered_lyrics)  # Splits each word into an array item.
        print(f'c {filtered_lyrics}\n')

        # filtered_lyrics = self.removeSpecialWords(filtered_lyrics)  # Removes special words. ie: [Chorus]  #TODO
        # print(f'd {filtered_lyrics}\n')
        
        filtered_lyrics.sort()  # Sorts list alphabetically.
        print(f'e {filtered_lyrics}\n')

        self.filtered_lyrics = self.removeCommonWords(filtered_lyrics)  # Removes common words.
        print(f'f {filtered_lyrics}\n')

        # Searches the VAD database for the filtered_lyrics.
        # This will assign numerical value to each word found.
        # 'The Rising Sun Blues' lyrics have 53 hits.
        self.vad_lyrics = self.compareToVADfile(filtered_lyrics)

        self.vad_averages = self.getVADaverages()  



        return ""


    



rising_sun = SongView()
rising_sun.callLyricsAPI()

# print(rising_sun.title)
# print()
# print(rising_sun.unfiltered_lyrics.count(' '))
# print(rising_sun.unfiltered_lyrics)
# print()
# print(len(rising_sun.filtered_lyrics))
# print(rising_sun.filtered_lyrics)
# print()
# print(len(rising_sun.vad_lyrics))
# print(rising_sun.vad_lyrics)


# print(SongView.get(ThisSong, 'GET'))

# print(common_words)

# print(rising_sun.get('animals'))