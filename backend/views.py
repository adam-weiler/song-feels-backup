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


# These are for Django REST framework - Authentication.
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView



# SongFeels imports
from backend.common_words import common_words  # A list of common or short words that can be safely ignored since they are not in the VAD database.
from backend.special_words import special_words  # A list of special words that can be safely ignored since they are not actually part of the lyrics.
# from backend.common_words import common_words  # A list of common or short words that can be safely ignored since they are not in the VAD database.


# file = open(os.path.join(settings.STATICFILES_DIRS, './CSV/testFile.csv'), 'r')  # A smaller version of the VAD database.

# file = open(os.path.join(settings.STATIC_URL, 'testFile.csv'))






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


# class ApiView(View):

#     def get(self, request):
#         return JsonResponse({
#             "def get": "This is a get request."
#         })

#     @csrf_exempt
#     def post(self, request):
#         return JsonResponse({
#             "def post": "This is a post request."
#         })


class SongView(View):

    # These are for Django REST framework - Authentication.
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self):
        self.body = ''

    def get(self, request): # Switch back to this

    # def get(self):  # For testing only.
        print('\n***SongView - get***')
        print(request)
        query = request.GET.urlencode()
        # print(query)

        print(f'https://api.audd.io/findLyrics/?{query}')

        try:
            data = {
                'api_token' : audd_key
            }
            response = requests.post(f'https://api.audd.io/findLyrics/?{query}', data=data)
            self.body = json.loads(response.content)
            # print(self.body)
            print (self.body['result'])
            # print (self.body['result'][0])
            # print (self.body['result'][0]['lyrics'])
            print('Success!')
            return JsonResponse({
                'lyrics': self.body['result']
            })
        except:
            print('Failure!')
            return JsonResponse({
                'error': response.status_code,
                'message': 'Something went wrong!'
        })

        # new_song.title = query
        # print(new_song)
        # new_song.analyzeLyrics()

        # print(self.body)

        # return JsonResponse({
        #     'songList': self.body['result']
        # })


    




class AnalyzeView(View):

    @csrf_exempt
    def __init__(self):
        self.title = ''
        self.unfiltered_lyrics = ''  # The original lyrics from the API.
        self.filtered_lyrics = []  # The data-cleaned lyrics for the song.
        self.vad_lyrics = []  # Only the lyrics that appeared in the VAD database.

        self.vad__average = {'valence':0, 'arousal':0, 'dominance':0, 'emotion': 'Neutral'}

        self.emotions__sum = {'Anger':0, 'Bored':0, 'Excited':0, 'Fear':0, 'Happy':0, 'Sad':0}  # The total number of times each emotion was experienced.
        self.emotions__percent = {'Anger':0, 'Bored':0, 'Excited':0, 'Fear':0, 'Happy':0, 'Sad':0}  # The percent each emotion was experienced.

    @csrf_exempt
    def __str__(self):
    #     return f'The {self.title} song.'
        return 'The AnalyzeView object.'

    @csrf_exempt
    def getVADaverages(self, vad_lyrics):
        print('\n***AnalyzeView - getVADaverages***')
        # count = 0
        word_count = len(vad_lyrics)
        # v_mean_sum__average = 0
        # a_mean_sum__average = 0
        # d_mean_sum__average = 0
        v_mean_sum__sum = 0
        a_mean_sum__sum = 0
        d_mean_sum__sum = 0
        # vad__total = 0

        # self.emotions__sum = {'Anger':0, 'Bored':0, 'Excited':0, 'Fear':0, 'Happy':0, 'Sad':0}
        # self.emotions__percent = {'Anger':0, 'Bored':0, 'Excited':0, 'Fear':0, 'Happy':0, 'Sad':0}
        # emotions__total = 0 ## This is same as word_count.
        
        

        for word in self.vad_lyrics:  # For each lyric that has been found in the VAD database.
            # count = count + 1
            # print(word['v_mean_sum'])
            v_mean_sum__sum += word['v_mean_sum']  # Used for average; keeps positive and negative signs.
            a_mean_sum__sum += word['a_mean_sum']
            d_mean_sum__sum += word['d_mean_sum']

            self.emotions__sum[word['emotionBasic']] += 1

            # v_mean_sum__sum += abs(word['v_mean_sum'])  # Used for total; ignores negative signs.
            # a_mean_sum__sum += abs(word['a_mean_sum'])
            # d_mean_sum__sum += abs(word['d_mean_sum'])


            # vad__total += abs(v_mean_sum__sum) + abs(a_mean_sum__sum) + abs(d_mean_sum__sum)  # Total valence, arousal, and dominance.  Ignores negative sign.

        print ('v_mean_sum__sum', v_mean_sum__sum)
        print ('word count', word_count)
        
        v_mean_sum__average = v_mean_sum__sum / word_count  # average = Total values / words in lyrics.
        a_mean_sum__average = a_mean_sum__sum / word_count
        d_mean_sum__average = d_mean_sum__sum / word_count
        emotion__average = self.whichEmotionBasic(v_mean_sum__average, a_mean_sum__average, d_mean_sum__average)

        self.vad__average = {'valence':v_mean_sum__average, 'arousal':a_mean_sum__average, 'dominance':d_mean_sum__average, 'emotion': emotion__average}

        # vad__total += v_mean_sum__sum + a_mean_sum__sum + d_mean_sum__sum  # Grand total.

        # emotions__total += sum(self.emotions__sum.values())
        anger__average = self.emotions__sum['Anger'] / word_count
        bored__average = self.emotions__sum['Bored'] / word_count
        excited__average = self.emotions__sum['Excited'] / word_count
        fear__average = self.emotions__sum['Fear'] / word_count
        happy__average = self.emotions__sum['Happy'] / word_count
        sad__average = self.emotions__sum['Sad'] / word_count
        self.emotions__percent = {'Anger':anger__average, 'Bored':bored__average, 'Excited':excited__average, 'Fear':fear__average, 'Happy':happy__average, 'Sad':sad__average}


        print (f'{word_count} words')
        print('Averages:')
        # print(v_mean_sum__average)
        # print(a_mean_sum__average)
        # print(d_mean_sum__average)
                    # print(self.whichEmotionBasic(v_mean_sum__average, a_mean_sum__average, d_mean_sum__average))
        print(self.vad__average)
        print()

        # print('Totals:')
        # print(v_mean_sum__sum)
        # print(a_mean_sum__sum)
        # print(d_mean_sum__sum)
        # print(vad__total)

        print('Emotions Sums and Total:')
        print(self.emotions__sum)
        # print(emotions__total)
        print(self.emotions__percent)
        
        # print(self.vad_lyrics)


        # return 42


        

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
                print('Happy')
                return "Happy"  # Joy
            else:
                print('Excited')
                return "Excited"  # Surprise
        else:  # A negative emotion.
            if arousal >= 5:  # A high-energy emotion.
                if dominance >= 4.21:
                    print('Anger')
                    return "Anger"
                else:
                    print('Fear')
                    return "Fear"
            else:  # A low-energy emotion.
                if dominance >= 5.18:
                    print('Bored')  # Disgust
                    return "Bored"
                else:
                    print('Sad')
                    return "Sad"

            # if dominance <= 5:  # A powerless emotion
            #     if arousal >= 7.1:
            #         print('Fear')
            #         return "Fear"
            #     else:
            #         print('Sad')
            #         return "Sad"
            # else:
            #     if arousal >= 7.7:
            #         print('Anger')
            #         return "Anger"
            #     else:
            #         print('Bored')
            #         return "Bored"

    @csrf_exempt
    def compareToVADfile(self, lyrics):
        print('\n***AnalyzeView - compareToVADfile***')

        # These work locally:
        # file = open('backend/testFile.csv', 'r')  # A smaller version of the VAD database.
        file = open('backend/CSV/libra.csv', 'r')  # A smaller version of the VAD database.
        # file = open('./CSV/libra.csv', 'r')  # The full version of the VAD database.
        librareader = csv.reader(file)  # Saves the CSV file to a variable.

        length = len(lyrics)
        print(length)
        print(lyrics)
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
        # Remove special characters and punctuation.
        # Convert to lowercase.
        # Split words into a list.
        # Add into a set to remove any duplicates.
        # Sort words alphabetically.
        # Removes any common or short words that can be safely ignored since they are not in the database.
        # This reduces 'The Rising Sun Blues' lyrics from 190 to 76.


        self.filtered_lyrics = unfiltered_lyrics.lower()  # Converts to lowercase.
        print(f'a {self.filtered_lyrics}\n')

        self.filtered_lyrics = self.removeSpecialCharacters(self.filtered_lyrics)  # Removes special characters.
        print(f'b {self.filtered_lyrics}\n')
        
        self.filtered_lyrics = self.splitIntoList(self.filtered_lyrics)  # Splits each word into an array item.
        print(f'c {self.filtered_lyrics}\n')

        # filtered_lyrics = self.removeSpecialWords(filtered_lyrics)  # Removes special words. ie: [Chorus]  #TODO
        # print(f'd {filtered_lyrics}\n')
        
        self.filtered_lyrics.sort()  # Sorts list alphabetically.
        print(f'e {self.filtered_lyrics}\n')

        self.filtered_lyrics = self.removeCommonWords(self.filtered_lyrics)  # Removes common words.
        print(f'f {self.filtered_lyrics}\n')

        # Searches the VAD database for the filtered_lyrics.
        # This will assign numerical value to each word found.
        # 'The Rising Sun Blues' lyrics have 53 hits.
        self.vad_lyrics = self.compareToVADfile(self.filtered_lyrics)


        # print(self.vad_lyrics) word, v_mean_sum, a_mean_sum, d_mean_sum, emotionBasic

        self.vad_averages = self.getVADaverages(self.vad_lyrics)  



        # return ""

    @csrf_exempt
    def post(self, request): # Trying this for a second.
    # def get(self, request): # Switch back to this
    # def get(self):  # For testing only.
        print('\n***AnalyzeView - get***')
        # print(request)
        # print(request.body)
        # print(json.loads(request.body.decode('utf-8')))

        post_data = json.loads(request.body.decode('utf-8'))
        
        self.unfiltered_lyrics = post_data['original_lyrics']
        print(self.unfiltered_lyrics)

            # post_data = request.session.get('post_data')
            # print('Post_data', post_data)

            # print('/n/n')
            

            # query = request.GET.urlencode()
            # print(query)
            # query = int(query, 2)
            # query = 0
            # print(query)
            # # query = 4
            
            # print(type(query))
            # print(query)

            # These all work:
            # print(new_song_search)
            # print()
            # print(new_song_search.body)
            # print()
            # print(new_song_search.body['result'])
            # print()
            # print(new_song_search.body['result'][query])
            # print()
            # print(new_song_search.body['result'][query]['lyrics'])

            # self.analyzeLyrics(new_song_search.body['result'][query]['lyrics'])  # I need this!


        self.analyzeLyrics(self.unfiltered_lyrics)

        print('\n\n***AnalyzeView - get (again)***')
        print('\nFiltered_lyrics:', len(self.filtered_lyrics), self.filtered_lyrics)
        print('\nLyrics found in VAD database:', len(self.vad_lyrics), self.vad_lyrics)
        # print('\nAverage of all VAD scores:', self.vad__average) #TODO This doesn't work unless words repeat?
        print('\nEmotions sum:', self.emotions__sum)
        print('\nEmotions percent:', self.emotions__percent)


        print()
        return JsonResponse({
            'filtered_lyrics': self.filtered_lyrics,
            'vad_lyrics': self.vad_lyrics,
            'emotions_sum': self.emotions__sum,
            'emotions_percent': self.emotions__percent
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








# new_song = AnalyzeView()
# new_song.analyzeLyrics()

# print(new_song.title)
# print()
# print(new_song.unfiltered_lyrics.count(' '))
# print(new_song.unfiltered_lyrics)
# print()
# print(len(new_song.filtered_lyrics))
# print(new_song.filtered_lyrics)
# print()
# print(len(new_song.vad_lyrics))
# print(new_song.vad_lyrics)

