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
        self.body = ''

    def callLyricsAPI(self, request):
        print('\n***SongView - callLyricsAPI***')
        # Makes a call to AudD API and returns lyrics.

        # print(f'https://api.audd.io/findLyrics/?{request}')

        # try:
        #     data = {
        #         'api_token' : audd_key
        #     }
        #     response = requests.post(f'https://api.audd.io/findLyrics/?{request}', data=data)
        #     body = json.loads(response.content)
        #     # print(body)
        #     # print (body['result'])
        #     print (body['result'][0])
        #     # print (body['result'][0]['lyrics'])
        #     print('Success!')
        #     return JsonResponse({
        #         'lyrics': body['result']
        #     })
        # except:
        #     print('Failure!')
        #     return JsonResponse({
        #         'error': response.status_code,
        #         'message': 'Something went wrong!'
        # })

    def get(self, request): # Switch back to this
    # def get(self):  # For testing only.
        print('\n***SongView - get***')
        print(request)
        query = request.GET.urlencode()
        # print(query)

        # self.title = 'The Rising Sun Blues'

                # api_result = self.callLyricsAPI(query)
                # print(api_result)
                # return JsonResponse({
                #     'api_result': api_result
                # }) 

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







        self.unfiltered_lyrics = "There is a house in New Orleans\r\n They call the Rising Sun\r\n And it's been the ruin of many a poor boy\r\n And God I know I'm one\r\n \r\n My mother was a tailor\r\n She sewed my new bluejeans\r\n My father was a gamblin' man\r\n Down in New Orleans\r\n \r\n Now the only thing a gambler needs\r\n Is a suitcase and trunk\r\n And the only time he's satisfied\r\n Is when he's on a drunk\r\n \r\n [Organ Solo]\r\n \r\n Oh mother tell your children\r\n Not to do what I have done\r\n Spend your lives in sin and misery\r\n In the House of the Rising Sun\r\n \r\n Well, I got one foot on the platform\r\n The other foot on the train\r\n I'm goin' back to New Orleans\r\n To wear that ball and chain\r\n \r\n Well, there is a house in New Orleans\r\n They call the Rising Sun\r\n And it's been the ruin of many a poor boy\r\n And God I know I'm one" # 

        singer = 'animals'
        song = 'rising sun'

        # happy, Excited, fear, sad, anger, bored
        self.body = {"status":"success","result":[
        {"song_id": "87427", "artist_id": "24716", "title": "The House of the Rising Sun", "title_with_featured": "The House of the Rising Sun", "full_title": "The House of the Rising Sun by\xa0The\xa0Animals", "artist": "The Animals", "lyrics": "There is a house in New Orleans\r\n They call the Rising Sun\r\n And it's been the ruin of many a poor boy\r\n And God I know I'm one\r\n \r\n My mother was a tailor\r\n She sewed my new bluejeans\r\n My father was a gamblin' man\r\n Down in New Orleans\r\n \r\n Now the only thing a gambler needs\r\n Is a suitcase and trunk\r\n And the only time he's satisfied\r\n Is when he's on a drunk\r\n \r\n [Organ Solo]\r\n \r\n Oh mother tell your children\r\n Not to do what I have done\r\n Spend your lives in sin and misery\r\n In the House of the Rising Sun\r\n \r\n Well, I got one foot on the platform\r\n The other foot on the train\r\n I'm goin' back to New Orleans\r\n To wear that ball and chain\r\n \r\n Well, there is a house in New Orleans\r\n They call the Rising Sun\r\n And it's been the ruin of many a poor boy\r\n And God I know I'm one", "media": "[{'provider':'apple_music','provider_id':'1108150799','type':'audio','url':'https:\\/\\/itunes.apple.com\\/lookup?entity=song&id=1108150799'},{'native_uri':'spotify:track:61Q9oJNd9hJQFhSDh6Qlap','provider':'spotify','type':'audio','url':'https:\\/\\/open.spotify.com\\/track\\/61Q9oJNd9hJQFhSDh6Qlap'},{'provider':'youtube','start':0,'type':'video','url':'http:\\/\\/www.youtube.com\\/watch?v=0sB3Fjw3Uvc'}]"},
        
        {"song_id":"2332455","artist_id":"2300","title":"Hello","title_with_featured":"Hello","full_title":"Hello by Adele","artist":"Adele","lyrics":"[Verse 1]\r\n Hello, it's me\r\n I was wondering if after all these years you'd like to meet\r\n To go over everything\r\n They say that time's supposed to heal ya, but I ain't done much healing\r\n Hello, can you hear me?\r\n I'm in California dreaming about who we used to be\r\n When we were younger and free\r\n I've forgotten how it felt before the world fell at our feet\r\n There's such a difference between us\r\n And a million miles\r\n \r\n [Chorus]\r\n Hello from the other side\r\n I must've called a thousand times\r\n To tell you I'm sorry\r\n For everything that I've done\r\n But when I call, you never seem to be home\r\n Hello from the outside\r\n At least I can say that I've tried\r\n To tell you I'm sorry, for breaking your heart\r\n But it don't matter\r\n It clearly doesn't tear you apart anymore\r\n \r\n [Verse 2]\r\n Hello, how are you?\r\n It's so typical of me to talk about myself, I'm sorry\r\n I hope that you're well\r\n Did you ever make it out of that town where nothing ever happened?\r\n It's no secret that the both of us\r\n Are running out of time\r\n [Chorus]\r\n So hello from the other side\r\n I must've called a thousand times\r\n To tell you I'm sorry\r\n For everything that I've done\r\n But when I call, you never seem to be home\r\n Hello from the outside\r\n At least I can say that I've tried\r\n To tell you I'm sorry, for breaking your heart\r\n But it don't matter\r\n It clearly doesn't tear you apart anymore\r\n \r\n [Bridge]\r\n (Highs, highs, highs, highs, lows, lows, lows, lows)\r\n Ooh, anymore\r\n (Highs, highs, highs, highs, lows, lows, lows, lows)\r\n Ooh, anymore\r\n (Highs, highs, highs, highs, lows, lows, lows, lows)\r\n Ooh, anymore\r\n (Highs, highs, highs, highs, lows, lows, lows, lows)\r\n Anymore\r\n \r\n [Chorus]\r\n Hello from the other side\r\n I must've called a thousand times\r\n To tell you I'm sorry\r\n For everything that I've done\r\n But when I call, you never seem to be home\r\n Hello from the outside\r\n At least I can say that I've tried\r\n To tell you I'm sorry, for breaking your heart\r\n But it don't matter\r\n It clearly doesn't tear you apart anymore\r\n [Produced by Greg Kurstin]\r\n [Music Video]","media":"[{\"provider\":\"youtube\",\"start\":0,\"type\":\"video\",\"url\":\"http:\\/\\/www.youtube.com\\/watch?v=YQHsXMglC9A\"},{\"provider\":\"apple_music\",\"provider_id\":\"1051394215\",\"type\":\"audio\",\"url\":\"https:\\/\\/itunes.apple.com\\/lookup?entity=song\u0026id=1051394215\"},{\"native_uri\":\"spotify:track:0ENSn4fwAbCGeFGVUbXEU3\",\"provider\":\"spotify\",\"type\":\"audio\",\"url\":\"https:\\/\\/open.spotify.com\\/track\\/0ENSn4fwAbCGeFGVUbXEU3\"},{\"provider\":\"soundcloud\",\"type\":\"audio\",\"url\":\"https:\\/\\/soundcloud.com\\/adelemusic\\/hello\"}]"},
        
        {"song_id":"12345","artist_id":"12345","title":"Wake Me Up Before You Go Go","title_with_featured":"Wake Me Up Before You Go Go","full_title":"Wake Me Up Before You Go Go by Wham!","artist":"Wham!","lyrics":"Jitterbug Jitterbug Jitterbug Jitterbug You put the boom boom into my heart (hoo, hoo) You send my soul sky high when your lovin' starts Jitterbug into my brain (yeah, yeah) Goes a bang-bang-bang 'til my feet do the same But something's bugging you (ha-ha, ha-ha) Something ain't right (ha-ha, ha-ha) My best friend told me what you did last night (ha-ha, ha-ha) Left me sleepin' in my bed (ha-ha, ha-ha) I was dreaming, but I should have been with you instead (ha-ha) Wake me up before you go-go Don't leave me hanging on like a yo-yo Wake me up before you go-go I don't want to miss it when you hit that high Wake me up before you go-go 'Cause I'm not plannin' on going solo Wake me up before you go-go Take me dancing tonight I wanna hit that high (yeah, yeah) You take the grey skies out of my way (hoo, hoo) You make the sun shine brighter than Doris Day Turned a bright spark into a flame (yeah, yeah) My beats per minute never been the same 'Cause you're my lady, I'm your fool (ha-ha, ha-ha) It makes me crazy when you act so cruel (ha-ha, ha-ha) Come on, baby, let's not fight (ha-ha, ha-ha) We'll go dancing, everything will be all right (ha-ha) Wake me up before you go-go Don't leave me hanging on like a yo-yo Wake me up before you go-go I don't want to miss it when you hit that high Wake me up before you go-go 'Cause I'm not plannin' on going solo Wake me up before you go-go Take me dancing tonight I wanna hit that high (yeah, yeah, yeah) Jitterbug (baby) Jitterbug (woo) Cuddle up, baby, move in tight We'll go dancing tomorrow night It's cold out there, but it's warm in bed They can dance, we'll stay home instead Jitterbug Wake me up before you go-go Don't leave me hanging on like a yo-yo Wake me up before you go-go I don't want to miss it when you hit that high Wake me up before you go-go 'Cause I'm not plannin' on going solo Wake me up before you go-go Take me dancing tonight Wake me up before you go-go (don't you dare) Don't leave me hanging on like a yo-yo (Leave me hanging on like a yo-yo, yo-yo, yo) Wake me up before you go-go I don't want to miss it when you hit that high (Take me dancing) (A boom-boom-boom-boom, oh) Wake me up before you go-go 'Cause I'm not plannin' on going solo (A boom-boom-boom-boom) Wake me up before you go-go (ah) (Yeah, yeah, yeah) Take me dancing tonight Ooh ah Yeah","media":"[{\"provider\":\"apple_music\",\"provider_id\":\"12345\",\"type\":\"audio\",\"url\":\"https:\\/\\/itunes.apple.com\\/lookup?entity=song\u0026id=12345\"},{\"native_uri\":\"spotify:track:12345\",\"provider\":\"spotify\",\"type\":\"audio\",\"url\":\"https:\\/\\/open.spotify.com\\/track\\/12345\"},{\"provider\":\"youtube\",\"start\":0,\"type\":\"video\",\"url\":\"http:\\/\\/www.youtube.com\\/watch?v=12345\"}]"},
        {"song_id":"23456","artist_id":"23456","title":"I'm So Excited","title_with_featured":"I'm So Excited","full_title":"I'm So Excited by The Pointer Sisters","artist":"The Pointer Sisters","lyrics":"Tonight's the night we're gonna make it happen Tonight we'll put all other things aside Give in this time and show me some affection We're goin' for those pleasures in the night I want to love you, feel you Wrap myself around you I want to squeeze you, please you I just can't get enough And if you move real slow, I'll let it go I'm so excited, and I just can't hide it I'm about to lose control and I think I like it I'm so excited, and I just can't hide it And I know, I know, I know, I know, I know I want you We shouldn't even think about tomorrow Sweet memories will last a long, long time We'll have a good time, baby, don't you worry And if we're still playin' around, boy, that's just fine Let's get excited, we just can't hide it I'm about to lose control and I think I like it I'm so excited and I just can't hide it And I know, I know, I know, I know, I know I want you, I want you Oh boy, I want to love you, feel you Wrap myself around you I want to squeeze you, please you I just can't get enough And if you move real slow, I'll let it go I'm so excited, and I just can't hide it I'm about to lose control and I think I like it I'm so excited, and I just can't hide it And I know, I know, I know, I know, I know I want you I'm so excited (look what you do to me), and I just can't hide it (you got me burning up) I'm about to lose control and I think I like it (yeah) I'm so excited (how did you get to me?), and I can't deny, no, no, no (I've got to give it up) (Oh, oh, oh, oh)I know, I know, that I want you I'm so excited (look what you do to me), oh boy (you got me burning up) (Oh, oh, oh, oh) Hey, hey I think I like it (yeah) I'm so excited (how did you get to me?), you got me (I've got to give it up) (Oh, oh, oh, oh) Oh, ooh I like it boy I'm so excited (look what you do to me), oh, you got me burning up (burning up) (Oh, oh, oh, oh, ow)","media":"[{\"provider\":\"apple_music\",\"provider_id\":\"23456\",\"type\":\"audio\",\"url\":\"https:\\/\\/itunes.apple.com\\/lookup?entity=song\u0026id=23456\"},{\"native_uri\":\"spotify:track:23456\",\"provider\":\"spotify\",\"type\":\"audio\",\"url\":\"https:\\/\\/open.spotify.com\\/track\\/23456\"},{\"provider\":\"youtube\",\"start\":0,\"type\":\"video\",\"url\":\"http:\\/\\/www.youtube.com\\/watch?v=23456\"}]"},
        {"song_id":"34567","artist_id":"34567","title":"The End","title_with_featured":"The End","full_title":"The End by The Doors","artist":"The Doors","lyrics":"[Intro] [Chorus] This is the end Beautiful friend This is the end My only friend The end [Verse 1] Of our elaborate plans, the end Of everything that stands, the end No safety or surprise, the end I'll never look into your eyes again [Verse 2] Can you picture what will be? So limitless and free Desperately in need Of some stranger's hand In a desperate land [Verse 3] Lost in a Roman wilderness of pain And all the children are insane All the children are insane Waiting for the summer rain, yeah [Verse 4] There's danger on the edge of town Ride the King's Highway, baby Weird scenes inside the gold mine Ride the highway west, baby Ride the snake, ride the snake To the lake, the ancient lake, baby The snake, he's long, seven miles Ride the snake He's old and his skin is cold The west is the best The west is the best Get here and we'll do the rest The blue bus is calling us The blue bus is calling us Driver, where you taking us? [Verse 5] The killer awoke before dawn He put his boots on He took a face from the ancient gallery And he walked on down the hall He went into the room where his sister lived, and then he Paid a visit to his brother, and then he He walked on down the hall, and And he came to a door And he looked inside 'Father?' 'Yes, son?' 'I want to kill you' 'Mother? I want to...' [Bridge] Come on baby, take a chance with us Come on baby, take a chance with us Come on baby, take a chance with us And meet me at the back of the blue bus Of the blue bus, on the blue bus, on the blue bus Come on yeah Fuck, fuck Fuck fuck, fuck, fuck Come on baby, fuck me baby yeah Fuck fuck fuck fuck fuck Come on baby, fuck me baby Fuck fuck fuck fuck fuck Come on Fuck fuck Alright Fuck fuck Kill, kill, kill, kill [Chorus] This is the end Beautiful friend This is the end My only friend, the end [Verse 6] It hurts to set you free But you'll never follow me The end of laughter and soft lies The end of nights we tried to die This is the end","media":"[{\"provider\":\"apple_music\",\"provider_id\":\"34567\",\"type\":\"audio\",\"url\":\"https:\\/\\/itunes.apple.com\\/lookup?entity=song\u0026id=34567\"},{\"native_uri\":\"spotify:track:34567\",\"provider\":\"spotify\",\"type\":\"audio\",\"url\":\"https:\\/\\/open.spotify.com\\/track\\/34567\"},{\"provider\":\"youtube\",\"start\":0,\"type\":\"video\",\"url\":\"http:\\/\\/www.youtube.com\\/watch?v=34567\"}]"},
        {"song_id":"45678","artist_id":"45678","title":"When the Party's over","title_with_featured":"When the Party's over","full_title":"When the Party's over by Billie Eilish","artist":"Billie Eilish","lyrics":"Don't you know I'm no good for you? I've learned to lose you, can't afford to Tore my shirt to stop you bleedin' But nothin' ever stops you leavin' Quiet when I'm coming home and I'm on my own I could lie, say I like it like that, like it like that I could lie, say I like it like that, like it like that Don't you know too much already? I'll only hurt you if you let me Call me friend but keep me closer (call me back) And I'll call you when the party's over Quiet when I'm coming home and I'm on my own And I could lie, say I like it like that, like it like that Yeah, I could lie, say I like it like that, like it like that But nothing is better sometimes Once we've both said our goodbyes Let's just let it go Let me let you go Quiet when I'm coming home and I'm on my own I could lie, say I like it like that, like it like that I could lie, say I like it like that, like it like that","media":"[{\"provider\":\"apple_music\",\"provider_id\":\"45678\",\"type\":\"audio\",\"url\":\"https:\\/\\/itunes.apple.com\\/lookup?entity=song\u0026id=45678\"},{\"native_uri\":\"spotify:track:45678\",\"provider\":\"spotify\",\"type\":\"audio\",\"url\":\"https:\\/\\/open.spotify.com\\/track\\/45678\"},{\"provider\":\"youtube\",\"start\":0,\"type\":\"video\",\"url\":\"http:\\/\\/www.youtube.com\\/watch?v=45678\"}]"},
        {"song_id":"56789","artist_id":"56789","title":"Break Stuff","title_with_featured":"Break Stuff","full_title":"Break Stuff by Limp Bizkit","artist":"Limp Bizkit","lyrics":"Its just one of those days Where you don't want to wake up Everything is fucked Everybody sucks You don't really know why But you want to justify Rippin' someone's head off No human contact And if you interact Your life is on contract Your best bet is to stay away motherfucker It's just one of those days It's all about the he-says, she-says bullshit I think you better quit, let the shit slip Or you'll be leaving with a fat lip It's all about the he-says, she-says bullshit I think you better quit, talking that shit Its just one of those days Feeling like a freight train First one to complain Leaves with a bloodstain Damn right I'm a maniac You better watch your back Cause I'm fucking up your program And then your stuck up You just lucked up Next in line to get fucked up Your best bet is to stay away motherfucker It's just one of those days It's all about the he-says, she-says bullshit I think you better quit, let the shit slip Or you'll be leaving with a fat lip It's all about the he-says, she-says bullshit I think you better quit, talking that shit Punk, so come and get it I feel like shit My suggestion, is to keep your distance Cause right now I'm dangerous We've all felt like shit And been treated like shit All those motherfuckers That want to step up I hope you know, I pack a chainsaw I'll skin your ass raw And if my day keeps going this way, I just might Break something tonight I pack a chainsaw I'll skin your ass raw And if my day keeps going this way, I just might Break something tonight I pack a chainsaw I'll skin your ass raw And if my day keeps going this way, I just might Break your fucking face tonight Give me something to break Just give me something to break How bout yer fucking face I hope you know, I pack a chainsaw What! A chainsaw What! A motherfucking chainsaw What! So come and get it It's all about the he-says, she-says bullshit I think you better quit, let the shit slip Or you'll be leaving with a fat lip It's all about the he-says, she-says bullshit I think you better quit, talking that shit Punk, so come and get it","media":"[{\"provider\":\"apple_music\",\"provider_id\":\"56789\",\"type\":\"audio\",\"url\":\"https:\\/\\/itunes.apple.com\\/lookup?entity=song\u0026id=56789\"},{\"native_uri\":\"spotify:track:56789\",\"provider\":\"spotify\",\"type\":\"audio\",\"url\":\"https:\\/\\/open.spotify.com\\/track\\/56789\"},{\"provider\":\"youtube\",\"start\":0,\"type\":\"video\",\"url\":\"http:\\/\\/www.youtube.com\\/watch?v=56789\"}]"},
        {"song_id":"67890","artist_id":"67890","title":"Copperline","title_with_featured":"Copperline","full_title":"Copperline by James Taylor","artist":"James Taylor","lyrics":"Even the old folks never knew Why they call it like they do I was wonderin' since the age of two Down on Copperline Copperhead, copper beech Copper kettles sitting side by each Copper coil, cup o' Georgia peach Down on Copperline Half a mile down to Morgan Creek Leanin' heavy on the end of the week Hercules and a hog-nosed snake Down on Copperline We were down on Copperline One summer night on the Copperline Slip away past supper time Wood smoke and moonshine Down on Copperline One time I saw my daddy dance Watched him moving like a man in a trance He brought it back from the war in France Down onto Copperline Branch water and tomato wine Creosote and turpentine Sour mash and new moon shine Down on Copperline, down on Copperline First kiss, ever I took Like a page from a romance book The sky opened and the earth shook Down on Copperline, down on Copperline, yeah Took a fall from a windy height I only knew how to hold on tight And pray for love enough to last all night Down on Copperline Day breaks and the boy wakes up And the dog barks and the birds sings And the sap rises and the angels sigh, yeah I tried to go back as if I could All spec house and plywood Tore up, tore up good Down on Copperline It doesn't come as a surprise to me It doesn't touch my memory Man, I'm lifting up and rising free Down over Copperline Half a mile down to Morgan Creek I'm only living for the end of the week Hercules and a hog-nosed snake Down on Copperline, yeah Take me down on Copperline Ohhh, down on Copperline Take me down on Copperline","media":"[{\"provider\":\"apple_music\",\"provider_id\":\"67890\",\"type\":\"audio\",\"url\":\"https:\\/\\/itunes.apple.com\\/lookup?entity=song\u0026id=67890\"},{\"native_uri\":\"spotify:track:67890\",\"provider\":\"spotify\",\"type\":\"audio\",\"url\":\"https:\\/\\/open.spotify.com\\/track\\/67890\"},{\"provider\":\"youtube\",\"start\":0,\"type\":\"video\",\"url\":\"http:\\/\\/www.youtube.com\\/watch?v=67890\"}]"}
        ]}

        # new_song.title = query
        # print(new_song)
        # new_song.analyzeLyrics()

        # print(self.body)

        # return JsonResponse({
        #     'songList': self.body['result']
        # })


    




class AnalyzeView(View):

    def __init__(self):
        self.title = ''
        # self.unfiltered_lyrics = ''  # The original lyrics from the API.
        self.filtered_lyrics = []  # The data-cleaned lyrics for the song.
        self.vad_lyrics = []  # Only the lyrics that appeared in the VAD database.

        self.vad__average = {'valence':0, 'arousal':0, 'dominance':0, 'emotion': 'Neutral'}

        self.emotions__sum = {'Anger':0, 'Bored':0, 'Excited':0, 'Fear':0, 'Happy':0, 'Sad':0}  # The total number of times each emotion was experienced.
        self.emotions__percent = {'Anger':0, 'Bored':0, 'Excited':0, 'Fear':0, 'Happy':0, 'Sad':0}  # The percent each emotion was experienced.


    def __str__(self):
    #     return f'The {self.title} song.'
        return 'The AnalyzeView object.'


    def getVADaverages(self):
        print('\n***AnalyzeView - getVADaverages***')
        # count = 0
        word_count = len(self.vad_lyrics)
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


    def compareToVADfile(self, lyrics):
        print('\n***AnalyzeView - compareToVADfile***')
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

    
    def splitIntoList(self, lyrics):  # Splits into list, adds into set to remove duplicates.
        print('\n***AnalyzeView - splitIntoList***')
        return list(set(lyrics.split()))  #TODO - Option to keep duplicate words. Currently removes duplicates.
        return lyrics.split()


    def removeSpecialCharacters(self, lyrics):  # Removes all special characters and numbers from text.
        print('\n***AnalyzeView - removeSpecialCharacters***')
        return re.sub('[^A-Za-z\']+', ' ', lyrics)


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

        self.vad_averages = self.getVADaverages()  



        # return ""


    def get(self, request): # Switch back to this
    # def get(self):  # For testing only.
        print('\n***AnalyzeView - get***')

        # print(request)

        query = request.GET.urlencode()
        print(query)
        # query = int(query, 2)
        query = 0
        print(query)
        # query = 4
        
        print(type(query))
        print(query)

        # These all work:
        # print(new_song_search)
        # print()
        print(new_song_search.body)
        # print()
        # print(new_song_search.body['result'])
        # print()
        # print(new_song_search.body['result'][query])
        # print()
        # print(new_song_search.body['result'][query]['lyrics'])

        # self.analyzeLyrics(new_song_search.body['result'][query]['lyrics'])  # I need this!


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
                            # Calls AuDD API:            ***SongView - callLyricsAPI***

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


# print(SongView.get(ThisSong, 'GET'))

# print(common_words)

# print(new_song.get('animals'))