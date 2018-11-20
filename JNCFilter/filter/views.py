from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.cache import cache

from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
import requests

TITLES_LIST = {
    '0': {'title': 'Occultic;Nine', 'shortTitle': 'Occultic;Nine'},
    '1': {'title': 'My Little Sister Can Read Kanji', 'shortTitle': 'My Little Sister Can Read Kanji'},
    '2': {'title': 'Brave Chronicle: The Ruinmaker', 'shortTitle': 'Brave Chronicle'},
    '3': {'title': 'My Big Sister Lives in a Fantasy World', 'shortTitle': 'My Big Sister Lives in a Fantasy World'},
    '4': {'title': 'Grimgar of Fantasy and Ash', 'shortTitle': 'Grimgar'},
    '5': {'title': 'I Saved Too Many Girls and Caused the Apocalypse', 'shortTitle': 'Little Apocalypse'},
    '6': {'title': 'Mixed Bathing in Another Dimension', 'shortTitle': 'Mixed Bathing in Another Dimension'},
    '7': {'title': 'The Faraway Paladin', 'shortTitle': 'The Faraway Paladin'},
    '8': {'title': 'Paying to Win in a VRMMO', 'shortTitle': 'Paying to Win in a VRMMO'},
    '9': {'title': 'How a Realist Hero Rebuilt the Kingdom', 'shortTitle': 'Realist Hero'},
    '10': {'title': 'In Another World With My Smartphone', 'shortTitle': 'Smartphone'},
    '11': {'title': "Arifureta: From Commonplace to World's Strongest", 'shortTitle': 'Arifureta'},
    '12': {'title': 'Bluesteel Blasphemer', 'shortTitle': 'Bluesteel Blasphemer'},
    '13': {'title': 'Invaders of the Rokujouma!?', 'shortTitle': 'Invaders of the Rokujouma!?'},
    '14': {'title': 'If It’s for My Daughter, I’d Even Defeat a Demon Lord', 'shortTitle': 'For My Daughter'},
    '15': {'title': 'Demon King Daimaou', 'shortTitle': 'Demon King Daimaou'},
    '16': {'title': 'Infinite Dendrogram', 'shortTitle': 'Infinite Dendrogram'},
    '17': {'title': 'Clockwork Planet', 'shortTitle': 'Clockwork Planet'},
    '18': {'title': 'Outbreak Company', 'shortTitle': 'Outbreak Company'},
    '19': {'title': 'How NOT to Summon a Demon Lord', 'shortTitle': 'How NOT to Summon a Demon Lord'},
    '20': {'title': 'Walking My Second Path in Life', 'shortTitle': 'Walking My Second Path in Life'},
    '21': {'title': 'Yume Nikki: I Am Not in Your Dream', 'shortTitle': 'Yume Nikki'},
    '22': {'title': 'Ao Oni', 'shortTitle': 'Ao Oni'},
    '23': {'title': 'Arifureta Zero', 'shortTitle': 'Arifureta Zero'},
    '24': {'title': 'The Master of Ragnarok & Blesser of Einherjar', 'shortTitle': 'The Master of Ragnarok'},
    '25': {'title': "Me, a Genius? I Was Reborn into Another World and I Think They've Got the Wrong Idea!", 'shortTitle': 'Me, a Genius?'},
    '26': {'title': 'The Unwanted Undead Adventurer', 'shortTitle': 'Unwanted Undead'},
    '27': {'title': 'Infinite Stratos', 'shortTitle': 'Infinite Stratos'},
    '28': {'title': 'The Magic in this Other World is Too Far Behind!', 'shortTitle': 'Isekai Mahou'},
    '29': {'title': 'From Truant to Anime Screenwriter: My Path to “Anohana” and “The Anthem of the Heart”', 'shortTitle': 'From Truant to Anime Screenwriter: My Path to “Anohana” and “The Anthem of the Heart”'},
    '30': {'title': 'Lazy Dungeon Master', 'shortTitle': 'Lazy Dungeon Master'},
    '31': {'title': "An Archdemon's Dilemma: How to Love Your Elf Bride", 'shortTitle': 'Elf Bride'},
    '32': {'title': 'Amagi Brilliant Park', 'shortTitle': 'Amagi Brilliant Park'},
    '33': {'title': 'Kokoro Connect', 'shortTitle': 'Kokoro Connect'},
    '34': {'title': 'Seirei Gensouki: Spirit Chronicles', 'shortTitle': 'Seirei Gensouki'},
    '35': {'title': 'Gear Drive', 'shortTitle': 'Gear Drive'},
    '36': {'title': 'JK Haru is a Sex Worker in Another World', 'shortTitle': 'JK Haru'},
    '37': {'title': 'Der Werwolf: The Annals of Veight', 'shortTitle': 'Jinrou'},
    '38': {'title': 'Sorcerous Stabber Orphen: The Wayward Journey', 'shortTitle': 'Orphen'},
    '39': {'title': 'Last and First Idol', 'shortTitle': 'Last and First Idol'},
    '40': {'title': 'ECHO', 'shortTitle': 'ECHO'},
    '41': {'title': 'My Next Life as a Villainess: All Routes Lead to Doom!', 'shortTitle': 'Bakarina'},
    '42': {'title': 'Apparently it\'s My Fault That My Husband Has The Head of a Beast', 'shortTitle': 'Beast Head'},
    '43': {'title': 'Ascendance of a Bookworm (Manga)', 'shortTitle': 'Ascendance of a Bookworm (Manga)'},
    '44': {'title': 'Seirei Gensouki: Spirit Chronicles (Manga)', 'shortTitle': 'Seirei Gensouki (Manga)'},
    '45': {'title': 'A Very Fairy Apartment', 'shortTitle': 'A Very Fairy Apartment'},
    '46': {'title': 'Infinite Dendrogram (Manga)', 'shortTitle': 'Infinite Dendrogram (Manga)'},
    '47': {'title': 'How a Realist Hero Rebuilt the Kingdom (Manga)', 'shortTitle': 'Realist Hero (Manga)'},
}


def set_pref(request):
    if request.GET.get('series'):
        # Set new cookie then redirect
        response = HttpResponseRedirect('/')
        response.set_cookie('series', value=request.GET.get('series'), max_age=31536000)
    else:
        # Show default page to choose
        following_list = request.COOKIES.get('series', '').split()
        render_list = [{'value': key, 'title': value['title'], 'checked':"checked" if key in following_list else ""} for key, value in TITLES_LIST.items()]
        response = render(request, 'set.html', {'series_list': render_list})
    return response


def index(request):
    URL = "https://api.j-novel.club/api/events?filter="
    BASIC_QUERY = {
        "where": {
            "and": [
                {
                    "date": {"lt": "2018-08-01"}
                },
                {
                    "date": {"gte": "2018-07-01"}
                }
            ]
        }
    }
    if request.GET.get('month'):
        m = datetime.strptime(request.GET.get('month'), "%Y-%m")
        mstr = request.GET.get('month')
    else:
        m = datetime.today()
        mstr = m.strftime("%Y-%m")
    if cache.get(mstr):
        data = cache.get(mstr)
    else:
        f = m + relativedelta(day=1)
        t = f + relativedelta(months=+1)
        BASIC_QUERY["where"]["and"][0]["date"]["lt"] = t.strftime("%Y-%m-%d")
        BASIC_QUERY["where"]["and"][1]["date"]["gte"] = f.strftime("%Y-%m-%d")
        query = URL + json.dumps(BASIC_QUERY)
        data = requests.get(query).json()
        cache.set(mstr, data)
    if request.COOKIES.get('series'):
        fl = request.COOKIES.get('series').split()
        following_list = [TITLES_LIST[i]["shortTitle"] for i in fl]
        not_following_list = [TITLES_LIST[i]["shortTitle"] for i in TITLES_LIST.keys() if i not in fl]
    else:
        following_list = [i["shortTitle"] for i in TITLES_LIST.values()]
        not_following_list = []
    data = [i for i in data if any(j in i["name"] for j in following_list) and not any(j in i["name"] for j in not_following_list)]
    for i in data:
        i.pop("attachments", None)
        i["linkFragment"] = "https://j-novel.club" + i["linkFragment"]
        i["released"] = datetime.strptime(i["date"], "%Y-%m-%dT%H:%M:%S.%fZ") < datetime.utcnow()
    next_month = (m+relativedelta(months=+1)).strftime("%Y-%m")
    last_month = (m+relativedelta(months=-1)).strftime("%Y-%m")
    this_month = m.strftime("%Y-%m")
    bookmark_url = request.META["HTTP_HOST"]+"/set/?series="+request.COOKIES.get('series', '')
    return render(request, 'home.html', {'data': data, 'next_month': next_month, 'this_month': this_month, 'last_month': last_month, 'bookmark_url': bookmark_url})
