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


    def convertToVad(self, num):  # Converts the database value (1 to 10) into a Vad number (-1 to 1).
        num = ((float(num) - 5) / 10)

        if num > 0:
            num = num + .5
        else:
            num = num - .5
        return num


    def whichEmotionBasic(self, valence, arousal, dominance):  # Tries to assign an emotion based on Valence, Arousal, and Dominance values.
        if valence >= 0:  # A positive emotion.
            if arousal > .4:
                return "Happy"  # Joy
            else:
                return "Excited"  # Surprise
        else:  # A negative emotion.
            if valence <= -.75:
                if arousal >= 0:
                    return "Fear"  # Fear
                else:
                    return "Sad"  # Sadness
            elif valence <= -.50:
                return "Bored"  # Disgust
            elif valence <= -.25:
                return "Angry"  # Anger
            else:
                return "IDK"


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
                v_mean_sum = self.convertToVad(line[2])  # Valence Mean sum.
                a_mean_sum = self.convertToVad(line[5])  # Arousal Mean sum.
                d_mean_sum = self.convertToVad(line[8])  # Dominance Mean sum

                emotionBasic = self.whichEmotionBasic(v_mean_sum, a_mean_sum, d_mean_sum)

                vad_lyrics.append({'word':word, 'v_mean_sum':v_mean_sum, 'a_mean_sum':a_mean_sum, 'd_mean_sum':d_mean_sum, 'emotionBasic':emotionBasic})

        return vad_lyrics


    def get(self, request):
        return JsonResponse({
            "def song get": self.convertToVad(7)
        })

    def callLyricsAPI(self):
        # Makes a call to Lyrics API and returns lyrics.

        self.title = 'The Rising Sun Blues'

        self.unfiltered_lyrics = "[Verse 1] Hello, it's me I was wondering if after all these years you'd like to meet To go over everything They say that time's supposed to heal ya, but I ain't done much healing Hello, can you hear me? I'm in California dreaming about who we used to be When we were younger and free I've forgotten how it felt before the world fell at our feet There's such a difference between us And a million miles [Chorus] Hello from the other side I must've called a thousand times To tell you I'm sorry For everything that I've done But when I call, you never seem to be home Hello from the outside At least I can say that I've tried To tell you I'm sorry, for breaking your heart But it don't matter It clearly doesn't tear you apart anymore [Verse 2] Hello, how are you? It's so typical of me to talk about myself, I'm sorry I hope that you're well Did you ever make it out of that town where nothing ever happened? It's no secret that the both of us Are running out of time [Chorus] So hello from the other side I must've called a thousand times To tell you I'm sorry For everything that I've done But when I call, you never seem to be home Hello from the outside At least I can say that I've tried To tell you I'm sorry, for breaking your heart But it don't matter It clearly doesn't tear you apart anymore [Bridge] (Highs, highs, highs, highs, lows, lows, lows, lows) Ooh, anymore (Highs, highs, highs, highs, lows, lows, lows, lows) Ooh, anymore (Highs, highs, highs, highs, lows, lows, lows, lows) Ooh, anymore (Highs, highs, highs, highs, lows, lows, lows, lows) Anymore [Chorus] Hello from the other side I must've called a thousand times To tell you I'm sorry For everything that I've done But when I call, you never seem to be home Hello from the outside At least I can say that I've tried To tell you I'm sorry, for breaking your heart But it don't matter It clearly doesn't tear you apart anymore [Produced by Greg Kurstin] [Music Video]"
        #There is a house in [verse] [Verse] [chorus] [Chorus] [refrain] [Refrain] New Orleans they call the Rising SunIt’s been the ruinof many a poor girl and me, O God, for one If I had listened what Mama said, I’d be at home today Being so young and foolish, poor boy, let a rambler lead me astray Go tell my baby sister never do like I have done To shun that house in New Orleans they call the Rising Sun My mother she’s a tailor, she sewed these new blue jeans My sweetheart, he’s a drunkard, Lord, Lord, drinks down in New Orleans The only thing a drunkard needs is a suitcase and a trunk The only time he’s satisfied is when he’s on a drunk Fills his glasses to the brim, passes them around Only pleasure he gets out of life is hoboin’ from town to town One foot is on the platform and the other one on the train I’m going back to New Orleans to wear that ball and chain Going back to New Orleans, my race is almost run Going back to spend the rest of my days beneath that Rising Sun" # 

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