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

    def get(self, request):
        singer = 'animals'
        song = 'rising sun'

        query = request.GET.urlencode()
        print(query)

        # happy, Excited, fear, sad, anger, bored
        body = {"status":"success","result":[
            {"song_id":"12345","artist_id":"12345","title":"Wake Me Up Before You Go Go","title_with_featured":"Wake Me Up Before You Go Go","full_title":"Wake Me Up Before You Go Go by Wham!","artist":"Wham!","lyrics":"Jitterbug Jitterbug Jitterbug Jitterbug You put the boom boom into my heart (hoo, hoo) You send my soul sky high when your lovin' starts Jitterbug into my brain (yeah, yeah) Goes a bang-bang-bang 'til my feet do the same But something's bugging you (ha-ha, ha-ha) Something ain't right (ha-ha, ha-ha) My best friend told me what you did last night (ha-ha, ha-ha) Left me sleepin' in my bed (ha-ha, ha-ha) I was dreaming, but I should have been with you instead (ha-ha) Wake me up before you go-go Don't leave me hanging on like a yo-yo Wake me up before you go-go I don't want to miss it when you hit that high Wake me up before you go-go 'Cause I'm not plannin' on going solo Wake me up before you go-go Take me dancing tonight I wanna hit that high (yeah, yeah) You take the grey skies out of my way (hoo, hoo) You make the sun shine brighter than Doris Day Turned a bright spark into a flame (yeah, yeah) My beats per minute never been the same 'Cause you're my lady, I'm your fool (ha-ha, ha-ha) It makes me crazy when you act so cruel (ha-ha, ha-ha) Come on, baby, let's not fight (ha-ha, ha-ha) We'll go dancing, everything will be all right (ha-ha) Wake me up before you go-go Don't leave me hanging on like a yo-yo Wake me up before you go-go I don't want to miss it when you hit that high Wake me up before you go-go 'Cause I'm not plannin' on going solo Wake me up before you go-go Take me dancing tonight I wanna hit that high (yeah, yeah, yeah) Jitterbug (baby) Jitterbug (woo) Cuddle up, baby, move in tight We'll go dancing tomorrow night It's cold out there, but it's warm in bed They can dance, we'll stay home instead Jitterbug Wake me up before you go-go Don't leave me hanging on like a yo-yo Wake me up before you go-go I don't want to miss it when you hit that high Wake me up before you go-go 'Cause I'm not plannin' on going solo Wake me up before you go-go Take me dancing tonight Wake me up before you go-go (don't you dare) Don't leave me hanging on like a yo-yo (Leave me hanging on like a yo-yo, yo-yo, yo) Wake me up before you go-go I don't want to miss it when you hit that high (Take me dancing) (A boom-boom-boom-boom, oh) Wake me up before you go-go 'Cause I'm not plannin' on going solo (A boom-boom-boom-boom) Wake me up before you go-go (ah) (Yeah, yeah, yeah) Take me dancing tonight Ooh ah Yeah","media":"[{\"provider\":\"apple_music\",\"provider_id\":\"12345\",\"type\":\"audio\",\"url\":\"https:\\/\\/itunes.apple.com\\/lookup?entity=song\u0026id=12345\"},{\"native_uri\":\"spotify:track:12345\",\"provider\":\"spotify\",\"type\":\"audio\",\"url\":\"https:\\/\\/open.spotify.com\\/track\\/12345\"},{\"provider\":\"youtube\",\"start\":0,\"type\":\"video\",\"url\":\"http:\\/\\/www.youtube.com\\/watch?v=12345\"}]"},
            {"song_id":"12345","artist_id":"12345","title":"I'm So Excited","title_with_featured":"I'm So Excited","full_title":"I'm So Excited by Wham!","artist":"Wham!","lyrics":"Tonight's the night we're gonna make it happen Tonight we'll put all other things aside Give in this time and show me some affection We're goin' for those pleasures in the night I want to love you, feel you Wrap myself around you I want to squeeze you, please you I just can't get enough And if you move real slow, I'll let it go I'm so excited, and I just can't hide it I'm about to lose control and I think I like it I'm so excited, and I just can't hide it And I know, I know, I know, I know, I know I want you We shouldn't even think about tomorrow Sweet memories will last a long, long time We'll have a good time, baby, don't you worry And if we're still playin' around, boy, that's just fine Let's get excited, we just can't hide it I'm about to lose control and I think I like it I'm so excited and I just can't hide it And I know, I know, I know, I know, I know I want you, I want you Oh boy, I want to love you, feel you Wrap myself around you I want to squeeze you, please you I just can't get enough And if you move real slow, I'll let it go I'm so excited, and I just can't hide it I'm about to lose control and I think I like it I'm so excited, and I just can't hide it And I know, I know, I know, I know, I know I want you I'm so excited (look what you do to me), and I just can't hide it (you got me burning up) I'm about to lose control and I think I like it (yeah) I'm so excited (how did you get to me?), and I can't deny, no, no, no (I've got to give it up) (Oh, oh, oh, oh)I know, I know, that I want you I'm so excited (look what you do to me), oh boy (you got me burning up) (Oh, oh, oh, oh) Hey, hey I think I like it (yeah) I'm so excited (how did you get to me?), you got me (I've got to give it up) (Oh, oh, oh, oh) Oh, ooh I like it boy I'm so excited (look what you do to me), oh, you got me burning up (burning up) (Oh, oh, oh, oh, ow)","media":"[{\"provider\":\"apple_music\",\"provider_id\":\"12345\",\"type\":\"audio\",\"url\":\"https:\\/\\/itunes.apple.com\\/lookup?entity=song\u0026id=12345\"},{\"native_uri\":\"spotify:track:12345\",\"provider\":\"spotify\",\"type\":\"audio\",\"url\":\"https:\\/\\/open.spotify.com\\/track\\/12345\"},{\"provider\":\"youtube\",\"start\":0,\"type\":\"video\",\"url\":\"http:\\/\\/www.youtube.com\\/watch?v=12345\"}]"},
            {"song_id":"12345","artist_id":"12345","title":"The End","title_with_featured":"The End","full_title":"The End by The Doors","artist":"Wham!","lyrics":"[Intro] [Chorus] This is the end Beautiful friend This is the end My only friend The end [Verse 1] Of our elaborate plans, the end Of everything that stands, the end No safety or surprise, the end I'll never look into your eyes again [Verse 2] Can you picture what will be? So limitless and free Desperately in need Of some stranger's hand In a desperate land [Verse 3] Lost in a Roman wilderness of pain And all the children are insane All the children are insane Waiting for the summer rain, yeah [Verse 4] There's danger on the edge of town Ride the King's Highway, baby Weird scenes inside the gold mine Ride the highway west, baby Ride the snake, ride the snake To the lake, the ancient lake, baby The snake, he's long, seven miles Ride the snake He's old and his skin is cold The west is the best The west is the best Get here and we'll do the rest The blue bus is calling us The blue bus is calling us Driver, where you taking us? [Verse 5] The killer awoke before dawn He put his boots on He took a face from the ancient gallery And he walked on down the hall He went into the room where his sister lived, and then he Paid a visit to his brother, and then he He walked on down the hall, and And he came to a door And he looked inside 'Father?' 'Yes, son?' 'I want to kill you' 'Mother? I want to...' [Bridge] Come on baby, take a chance with us Come on baby, take a chance with us Come on baby, take a chance with us And meet me at the back of the blue bus Of the blue bus, on the blue bus, on the blue bus Come on yeah Fuck, fuck Fuck fuck, fuck, fuck Come on baby, fuck me baby yeah Fuck fuck fuck fuck fuck Come on baby, fuck me baby Fuck fuck fuck fuck fuck Come on Fuck fuck Alright Fuck fuck Kill, kill, kill, kill [Chorus] This is the end Beautiful friend This is the end My only friend, the end [Verse 6] It hurts to set you free But you'll never follow me The end of laughter and soft lies The end of nights we tried to die This is the end","media":"[{\"provider\":\"apple_music\",\"provider_id\":\"12345\",\"type\":\"audio\",\"url\":\"https:\\/\\/itunes.apple.com\\/lookup?entity=song\u0026id=12345\"},{\"native_uri\":\"spotify:track:12345\",\"provider\":\"spotify\",\"type\":\"audio\",\"url\":\"https:\\/\\/open.spotify.com\\/track\\/12345\"},{\"provider\":\"youtube\",\"start\":0,\"type\":\"video\",\"url\":\"http:\\/\\/www.youtube.com\\/watch?v=12345\"}]"},
            {"song_id":"12345","artist_id":"12345","title":"When the Party's over","title_with_featured":"When the Party's over","full_title":"When the Party's over by Billie Eilish","artist":"Billie Eilish","lyrics":"Don't you know I'm no good for you? I've learned to lose you, can't afford to Tore my shirt to stop you bleedin' But nothin' ever stops you leavin' Quiet when I'm coming home and I'm on my own I could lie, say I like it like that, like it like that I could lie, say I like it like that, like it like that Don't you know too much already? I'll only hurt you if you let me Call me friend but keep me closer (call me back) And I'll call you when the party's over Quiet when I'm coming home and I'm on my own And I could lie, say I like it like that, like it like that Yeah, I could lie, say I like it like that, like it like that But nothing is better sometimes Once we've both said our goodbyes Let's just let it go Let me let you go Quiet when I'm coming home and I'm on my own I could lie, say I like it like that, like it like that I could lie, say I like it like that, like it like that","media":"[{\"provider\":\"apple_music\",\"provider_id\":\"12345\",\"type\":\"audio\",\"url\":\"https:\\/\\/itunes.apple.com\\/lookup?entity=song\u0026id=12345\"},{\"native_uri\":\"spotify:track:12345\",\"provider\":\"spotify\",\"type\":\"audio\",\"url\":\"https:\\/\\/open.spotify.com\\/track\\/12345\"},{\"provider\":\"youtube\",\"start\":0,\"type\":\"video\",\"url\":\"http:\\/\\/www.youtube.com\\/watch?v=12345\"}]"},

            {"song_id":"12345","artist_id":"12345","title":"Break Stuff","title_with_featured":"Break Stuff","full_title":"Break Stuff by Limp Bizkit","artist":"Limp Bizkit","lyrics":"Its just one of those days Where you don't want to wake up Everything is fucked Everybody sucks You don't really know why But you want to justify Rippin' someone's head off No human contact And if you interact Your life is on contract Your best bet is to stay away motherfucker It's just one of those days It's all about the he-says, she-says bullshit I think you better quit, let the shit slip Or you'll be leaving with a fat lip It's all about the he-says, she-says bullshit I think you better quit, talking that shit Its just one of those days Feeling like a freight train First one to complain Leaves with a bloodstain Damn right I'm a maniac You better watch your back Cause I'm fucking up your program And then your stuck up You just lucked up Next in line to get fucked up Your best bet is to stay away motherfucker It's just one of those days It's all about the he-says, she-says bullshit I think you better quit, let the shit slip Or you'll be leaving with a fat lip It's all about the he-says, she-says bullshit I think you better quit, talking that shit Punk, so come and get it I feel like shit My suggestion, is to keep your distance Cause right now I'm dangerous We've all felt like shit And been treated like shit All those motherfuckers That want to step up I hope you know, I pack a chainsaw I'll skin your ass raw And if my day keeps going this way, I just might Break something tonight I pack a chainsaw I'll skin your ass raw And if my day keeps going this way, I just might Break something tonight I pack a chainsaw I'll skin your ass raw And if my day keeps going this way, I just might Break your fucking face tonight Give me something to break Just give me something to break How bout yer fucking face I hope you know, I pack a chainsaw What! A chainsaw What! A motherfucking chainsaw What! So come and get it It's all about the he-says, she-says bullshit I think you better quit, let the shit slip Or you'll be leaving with a fat lip It's all about the he-says, she-says bullshit I think you better quit, talking that shit Punk, so come and get it","media":"[{\"provider\":\"apple_music\",\"provider_id\":\"12345\",\"type\":\"audio\",\"url\":\"https:\\/\\/itunes.apple.com\\/lookup?entity=song\u0026id=12345\"},{\"native_uri\":\"spotify:track:12345\",\"provider\":\"spotify\",\"type\":\"audio\",\"url\":\"https:\\/\\/open.spotify.com\\/track\\/12345\"},{\"provider\":\"youtube\",\"start\":0,\"type\":\"video\",\"url\":\"http:\\/\\/www.youtube.com\\/watch?v=12345\"}]"},
            
            {"song_id":"12345","artist_id":"12345","title":"Copperline","title_with_featured":"Copperline","full_title":"Copperline by James Taylor","artist":"James Taylor","lyrics":"Even the old folks never knew Why they call it like they do I was wonderin' since the age of two Down on Copperline Copperhead, copper beech Copper kettles sitting side by each Copper coil, cup o' Georgia peach Down on Copperline Half a mile down to Morgan Creek Leanin' heavy on the end of the week Hercules and a hog-nosed snake Down on Copperline We were down on Copperline One summer night on the Copperline Slip away past supper time Wood smoke and moonshine Down on Copperline One time I saw my daddy dance Watched him moving like a man in a trance He brought it back from the war in France Down onto Copperline Branch water and tomato wine Creosote and turpentine Sour mash and new moon shine Down on Copperline, down on Copperline First kiss, ever I took Like a page from a romance book The sky opened and the earth shook Down on Copperline, down on Copperline, yeah Took a fall from a windy height I only knew how to hold on tight And pray for love enough to last all night Down on Copperline Day breaks and the boy wakes up And the dog barks and the birds sings And the sap rises and the angels sigh, yeah I tried to go back as if I could All spec house and plywood Tore up, tore up good Down on Copperline It doesn't come as a surprise to me It doesn't touch my memory Man, I'm lifting up and rising free Down over Copperline Half a mile down to Morgan Creek I'm only living for the end of the week Hercules and a hog-nosed snake Down on Copperline, yeah Take me down on Copperline Ohhh, down on Copperline Take me down on Copperline","media":"[{\"provider\":\"apple_music\",\"provider_id\":\"12345\",\"type\":\"audio\",\"url\":\"https:\\/\\/itunes.apple.com\\/lookup?entity=song\u0026id=12345\"},{\"native_uri\":\"spotify:track:12345\",\"provider\":\"spotify\",\"type\":\"audio\",\"url\":\"https:\\/\\/open.spotify.com\\/track\\/12345\"},{\"provider\":\"youtube\",\"start\":0,\"type\":\"video\",\"url\":\"http:\\/\\/www.youtube.com\\/watch?v=12345\"}]"}
            
            ]}

        return JsonResponse({
            'songList': body['result']
        })





class AnalyzeView(View):

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

        self.unfiltered_lyrics = "There is a house in New Orleans they call the Rising Sun It’s been the ruinof many a poor girl and me, O God, for one If I had listened what Mama said, I’d be at home today Being so young and foolish, poor boy, let a rambler lead me astray Go tell my baby sister never do like I have done To shun that house in New Orleans they call the Rising Sun My mother she’s a tailor, she sewed these new blue jeans My sweetheart, he’s a drunkard, Lord, Lord, drinks down in New Orleans The only thing a drunkard needs is a suitcase and a trunk The only time he’s satisfied is when he’s on a drunk Fills his glasses to the brim, passes them around Only pleasure he gets out of life is hoboin’ from town to town One foot is on the platform and the other one on the train I’m going back to New Orleans to wear that ball and chain Going back to New Orleans, my race is almost run Going back to spend the rest of my days beneath that Rising Sun " # 

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


    



rising_sun = AnalyzeView()
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