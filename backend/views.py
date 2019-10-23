# Python imports:
import csv  # Used to open .CSV files.
import dotenv  # Used to load APIkey from .env file.
import json  # Used to work with JSON files.
import logging  # Not used in production.
import os  # Used to load APIkey from .env file.
import re  # Used to strip punctuation from unfiltered_lyrics.
import requests  # Used to make API calls.

dotenv.load_dotenv()
audd_key = os.environ.get('AUDD_API_KEY')


# Django imports:
from django.conf import settings  # Not used in production.
from django.http import HttpResponse, JsonResponse  # Used to send a response back to user.
from django.views.decorators.csrf import csrf_exempt  # Remove this later to restrict CSRF access.
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import requires_csrf_token
from django.views.generic import View  # Used for Django's Views.


# from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



# These are for Django REST framework - Authentication:
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView



from ratelimit.decorators import ratelimit  # Used to limit number of searches user can perform.


# SongFeels imports
from backend.common_words import common_words  # A list of common or short words that can be safely ignored since they are not in the VAD database.
from backend.special_words import special_words  # A list of special words that can be safely ignored since they are not actually part of the lyrics.



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


class SongView(View):

    # These are for Django REST framework - Authentication.
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    # @requires_csrf_token
    def __init__(self):
        self.body = ''

    # @requires_csrf_token
    def __str__(self):
        return 'The SongView object.'

    # @requires_csrf_token
    # @csrf_protect
    @method_decorator(csrf_protect)

    # @ratelimit(key='ip', method=ratelimit.ALL)
    @ratelimit(key='ip', method='GET', rate='1/d')  # Current limit is set to 20 requests a day.
    def get(self, request):  # User has submit song request, which will be sent to API.
        print('\n***SongView - get***')
        was_limited = getattr(request, 'limited', False)  # Saves if user has exceeded rate-limit.
        # print(was_limited)

        if was_limited == True:  # User has exceeded rate-limit, will not query API.
            print('User has exceeded API request limit.')
            return JsonResponse({
                'error': 403,
                'message': 'User has exceeded API request limit. Please try again later.'
            })

        else:  # User has not exceeded rate-limit, will now try to query API.
            print('User still has API requests available.')
            query = request.GET.urlencode()
            # print(request)
            # print(f'https://api.audd.io/findLyrics/?{query}')

            try:
                data = {
                    'api_token' : audd_key
                }
                response = requests.post(f'https://api.audd.io/findLyrics/?{query}', data=data)
                self.body = json.loads(response.content)
                # print (self.body['result'])
                print('Request to AuDD has succeeded.')
                return JsonResponse({
                    'lyrics': self.body['result']
                })
            except:
                print('Request to AuDD has failed.')
                return JsonResponse({
                    'error': 500,
                    'message': 'Unable to reach API at the moment. Please try again later.'
                })


class AnalyzeView(View):

    @csrf_exempt
    def __init__(self):
        self.unfiltered_lyrics = ''  # The original lyrics from the API.
        self.filtered_lyrics = []  # The data-cleaned lyrics for the song.
        self.vad_lyrics = []  # Only the lyrics that appeared in the VAD database.
        self.vad__average = {'valence':0, 'arousal':0, 'dominance':0, 'emotion': 'Neutral'}  # Average of VAD stats for song.
        self.emotions__sum_percent = {'Anger':[0,0], 'Bored':[0,0], 'Excited':[0,0], 'Fear':[0,0], 'Happy':[0,0], 'Sad':[0,0]}  # The total number of times each emotion was experienced, and the overall percent each emotion was experienced.


    @csrf_exempt
    def __str__(self):
        return 'The AnalyzeView object.'

    @csrf_exempt
    def getVADaverages(self, vad_lyrics):
        print('\n***AnalyzeView - getVADaverages***')
        word_count = len(vad_lyrics)
        v_mean_sum__sum = 0
        a_mean_sum__sum = 0
        d_mean_sum__sum = 0

        for word in self.vad_lyrics:  # For each lyric that has been found in the VAD database.
            v_mean_sum__sum += word['v_mean_sum']  # Used for average.
            a_mean_sum__sum += word['a_mean_sum']
            d_mean_sum__sum += word['d_mean_sum']

            self.emotions__sum_percent[word['emotionBasic']][0] += 1

        # print ('v_mean_sum__sum', v_mean_sum__sum)
        
        v_mean_sum__average = v_mean_sum__sum / word_count  # average = Total values / words in lyrics.
        a_mean_sum__average = a_mean_sum__sum / word_count
        d_mean_sum__average = d_mean_sum__sum / word_count
        emotion__average = self.whichEmotionBasic(v_mean_sum__average, a_mean_sum__average, d_mean_sum__average)

        self.vad__average = {'valence':v_mean_sum__average, 'arousal':a_mean_sum__average, 'dominance':d_mean_sum__average, 'emotion': emotion__average}

        # vad__total += v_mean_sum__sum + a_mean_sum__sum + d_mean_sum__sum  # Grand total.

        self.emotions__sum_percent['Anger'][1] = self.emotions__sum_percent['Anger'][0] / word_count
        self.emotions__sum_percent['Bored'][1] = self.emotions__sum_percent['Bored'][0] / word_count
        self.emotions__sum_percent['Excited'][1] = self.emotions__sum_percent['Excited'][0] / word_count
        self.emotions__sum_percent['Fear'][1] = self.emotions__sum_percent['Fear'][0] / word_count
        self.emotions__sum_percent['Happy'][1] = self.emotions__sum_percent['Happy'][0] / word_count
        self.emotions__sum_percent['Sad'][1] = self.emotions__sum_percent['Sad'][0] / word_count

        # print (f'{word_count} words')
        # print('Averages:')
        # print(v_mean_sum__average)
        # print(a_mean_sum__average)
        # print(d_mean_sum__average)
                    # print(self.whichEmotionBasic(v_mean_sum__average, a_mean_sum__average, d_mean_sum__average))
        # print(self.vad__average)

        # print('Totals:')
        # print(v_mean_sum__sum)
        # print(a_mean_sum__sum)
        # print(d_mean_sum__sum)
        # print(vad__total)

        # print('Emotions Sums and Total:')
        # print(self.emotions__sum_percent)
        
        # print(self.vad_lyrics)
        

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

    @csrf_exempt
    def whichEmotionBasic(self, valence, arousal, dominance):  # Tries to assign an emotion based on Valence, Arousal, and Dominance values.
        # print('\n***AnalyzeView - whichEmotionBasic***')
        if valence >= 5.9:  # A positive emotion.
            if valence >= 7:
                # print('Happy')
                return "Happy"  # Joy
            else:
                # print('Excited')
                return "Excited"  # Surprise
        else:  # A negative emotion.
            if arousal >= 5:  # A high-energy emotion.
                if dominance >= 4.21:
                    # print('Anger')
                    return "Anger"
                else:
                    # print('Fear')
                    return "Fear"
            else:  # A low-energy emotion.
                if dominance >= 5.18:
                    # print('Bored')  # Disgust
                    return "Bored"
                else:
                    # print('Sad')
                    return "Sad"


    @csrf_exempt
    def compareToVADfile(self, lyrics):
        print('\n***AnalyzeView - compareToVADfile***')

        # file = open('backend/testFile.csv', 'r')  # A smaller version of the VAD database.
        file = open('backend/CSV/libra.csv', 'r')  # The full version of the VAD database.
        librareader = csv.reader(file)  # Saves the CSV file to a variable.

        length = len(lyrics)
        vad_lyrics = []

        for line in librareader:  # For each line in VAD database CSV file.
            word = line[1]  # Takes word from B column of CSV.

            if word in lyrics:  # If current word of CSV matches a word in the lyrics.
                # print(f'Matching word found: {word}')
                v_mean_sum = float(line[2])  # Valence Mean sum.
                a_mean_sum = float(line[5])  # Arousal Mean sum.
                d_mean_sum = float(line[8])  # Dominance Mean sum

                emotionBasic = self.whichEmotionBasic(v_mean_sum, a_mean_sum, d_mean_sum)

                vad_lyrics.append({'word':word, 'v_mean_sum':v_mean_sum, 'a_mean_sum':a_mean_sum, 'd_mean_sum':d_mean_sum, 'emotionBasic':emotionBasic})

        return vad_lyrics

    @csrf_exempt
    def removeCommonWords(self, lyrics):  # Removes any lyrics that are common_words.
        print('\n***AnalyzeView - removeCommonWords***')
        for word in common_words:
            if word in lyrics:  # If a common word is in lyrics, it is removed.
                lyrics.remove(word)
            #     print(f'Removing common word: {word}')

        return lyrics


    # def removeSpecialWords(self, lyrics):  # Removes any lyrics that are special_words.
    #     print('\n***AnalyzeView - removeSpecialWords***')
    #     for word in special_words:
    #         if word in lyrics:  # If a special word is in lyrics, it is removed.
    #             lyrics.remove(word)
    #         #     print(f'Removing special word: {word}')

    #     return lyrics

    @csrf_exempt
    def splitIntoList(self, lyrics):  # Splits into list, adds into set to remove duplicates.
        print('\n***AnalyzeView - splitIntoList***')
        return list(set(lyrics.split()))  #TODO - Option to keep duplicate words. Currently removes duplicates.
        return lyrics.split()

    @csrf_exempt
    def removeSpecialCharacters(self, lyrics):  # Removes all special characters and numbers from text.
        print('\n***AnalyzeView - removeSpecialCharacters***')
        return re.sub('[^A-Za-z\']+', ' ', lyrics)

    @csrf_exempt
    def analyzeLyrics(self, unfiltered_lyrics):
        print('\n***AnalyzeView - analyzeLyrics***')

        # Several steps must be taken to prepare the lyrics before comparing to VAD database:
        #1 Convert to lowercase.
        #2 Remove special characters and punctuation.  
        #3 Split words into a list and add into a set to remove any duplicates.
        #4 Sort words alphabetically.
        #5 Removes any common or short words that can be safely ignored since they are not in the database.
        # This reduces 'The Rising Sun Blues' lyrics from 190 words to 50.

        self.filtered_lyrics = unfiltered_lyrics.lower()  # Converts to lowercase.
        # print(f'#1 Lower-case: {self.filtered_lyrics}\n')

        self.filtered_lyrics = self.removeSpecialCharacters(self.filtered_lyrics)  # Removes special characters.
        # print(f'#2 Remove special characters: {self.filtered_lyrics}\n')
        
        self.filtered_lyrics = self.splitIntoList(self.filtered_lyrics)  # Splits each word into an array item.
        # print(f'#3 Split into list: {self.filtered_lyrics}\n')

        # filtered_lyrics = self.removeSpecialWords(filtered_lyrics)  # Removes special words. ie: [Chorus]  #TODO
        # print(f'#x Remove special words: {filtered_lyrics}\n')
        
        self.filtered_lyrics.sort()  # Sorts list alphabetically.
        # print(f'#4 Sort list alphabetically. {self.filtered_lyrics}\n')

        self.filtered_lyrics = self.removeCommonWords(self.filtered_lyrics)  # Removes common words.
        # print(f'#5 Remove common words: {self.filtered_lyrics}\n')

        # Searches the VAD database for the filtered_lyrics.
        # This will assign numerical value to each word found.
        # 'The Rising Sun Blues' lyrics have 53 hits.
        self.vad_lyrics = self.compareToVADfile(self.filtered_lyrics)

        # print(self.vad_lyrics) word, v_mean_sum, a_mean_sum, d_mean_sum, emotionBasic
        self.vad_averages = self.getVADaverages(self.vad_lyrics)  


    @csrf_exempt
    def post(self, request):  # User has clicked Analyze button.
        print('\n***AnalyzeView - get***')
        
        post_data = json.loads(request.body.decode('utf-8'))  # Original lyrics from hidden field.
        self.unfiltered_lyrics = post_data['original_lyrics']  # Stores original lyrics.
        # print(self.unfiltered_lyrics)
            
        self.analyzeLyrics(self.unfiltered_lyrics)

        print('\n\n***AnalyzeView - get (again)***')
        print('\nFiltered_lyrics:', len(self.filtered_lyrics), self.filtered_lyrics)
        print('\nLyrics found in VAD database:', len(self.vad_lyrics), self.vad_lyrics)
        # print('\nAverage of all VAD scores:', self.vad__average) #TODO This doesn't work unless words repeat?
        print('\nEmotions sum & percent:', self.emotions__sum_percent)
        
        return JsonResponse({
            'filtered_lyrics': self.filtered_lyrics,
            'vad_lyrics': self.vad_lyrics,
            'emotions_sum_percent': self.emotions__sum_percent
        })
    
new_song_search = SongView() 
new_analysis = AnalyzeView()




##These are for testing only.
# new_song_search.get() # User searches for a song.  ***SongView - get***
                        # Calls AuDD API:            ***SongView - get***

# new_analysis.get()    # User analyzes a song.         ***AnalyzeView - get***
                            # Calls smaller functions.   ***AnalyzeView - analyzeLyrics***
                                # Removes special characters. 	***AnalyzeView - removeSpecialCharacters***
                                # Splits into list.         	***AnalyzeView - splitIntoList***
                                # Removes common words.     	***AnalyzeView - removeCommonWords***
                                # Compare lyrics to VAD file.	***AnalyzeView - compareToVADfile***
                                    # Assign emotion to each word.		***AnalyzeView - whichEmotionBasic***
                                # Get VAD average for lyrics.	***AnalyzeView - getVADaverages***


# For graphing
# import matplotlib.pyplot as plt
# plt.plot([1, 2, 3, 4])
# plt.ylabel('some numbers')
# plt.show()

# Find location of directory.
# cwd = os.getcwd()
# files = os.listdir(cwd)
# print(cwd)
# print(files)
