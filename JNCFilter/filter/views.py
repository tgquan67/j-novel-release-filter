from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.cache import cache

from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
import requests

TITLES_LIST = {
    '0': {'title': 'Occultic;Nine', 'shortTitle': ['Occultic;Nine', ]},
    '1': {'title': 'My Little Sister Can Read Kanji', 'shortTitle': ['My Little Sister Can Read Kanji', ]},
    '2': {'title': 'Brave Chronicle: The Ruinmaker', 'shortTitle': ['Brave Chronicle', ]},
    '3': {'title': 'My Big Sister Lives in a Fantasy World', 'shortTitle': ['My Big Sister Lives in a Fantasy World', ]},
    '4': {'title': 'Grimgar of Fantasy and Ash', 'shortTitle': ['Grimgar', ], 'seriesType': 'Novel'},
    '5': {'title': 'I Saved Too Many Girls and Caused the Apocalypse', 'shortTitle': ['Little Apocalypse', ], 'seriesType': 'Novel'},
    '6': {'title': 'Mixed Bathing in Another Dimension', 'shortTitle': ['Mixed Bathing in Another Dimension', ]},
    '7': {'title': 'The Faraway Paladin', 'shortTitle': ['The Faraway Paladin', ]},
    '8': {'title': 'Paying to Win in a VRMMO', 'shortTitle': ['Paying to Win in a VRMMO', ]},
    '9': {'title': 'How a Realist Hero Rebuilt the Kingdom', 'shortTitle': ['Realist Hero', 'How a Realist Hero Rebuilt the Kingdom', ]},
    '10': {'title': 'In Another World With My Smartphone', 'shortTitle': ['Smartphone', ]},
    '11': {'title': "Arifureta: From Commonplace to World's Strongest", 'shortTitle': ['Arifureta', "Arifureta: From Commonplace to World's Strongest", ]},
    '12': {'title': 'Bluesteel Blasphemer', 'shortTitle': ['Bluesteel Blasphemer', ]},
    '13': {'title': 'Invaders of the Rokujouma!?', 'shortTitle': ['Invaders of the Rokujouma!?', 'Rokujouma!?', ]},
    '14': {'title': 'If It’s for My Daughter, I’d Even Defeat a Demon Lord', 'shortTitle': ['For My Daughter', ]},
    '15': {'title': 'Demon King Daimaou', 'shortTitle': ['Demon King Daimaou', ]},
    '16': {'title': 'Infinite Dendrogram', 'shortTitle': ['Infinite Dendrogram', ]},
    '17': {'title': 'Clockwork Planet', 'shortTitle': ['Clockwork Planet', ]},
    '18': {'title': 'Outbreak Company', 'shortTitle': ['Outbreak Company', ]},
    '19': {'title': 'How NOT to Summon a Demon Lord', 'shortTitle': ['How NOT to Summon a Demon Lord', ], 'seriesType': 'Novel'},
    '20': {'title': 'Walking My Second Path in Life', 'shortTitle': ['Watafuta', ]},
    '21': {'title': 'Yume Nikki: I Am Not in Your Dream', 'shortTitle': ['Yume Nikki', ]},
    '22': {'title': 'Ao Oni', 'shortTitle': ['Ao Oni', ]},
    '23': {'title': 'Arifureta Zero', 'shortTitle': ['Arifureta Zero', ]},
    '24': {'title': 'The Master of Ragnarok & Blesser of Einherjar', 'shortTitle': ['The Master of Ragnarok', ]},
    '25': {'title': "Me, a Genius? I Was Reborn into Another World and I Think They've Got the Wrong Idea!", 'shortTitle': ['Me, a Genius?', ]},
    '26': {'title': 'The Unwanted Undead Adventurer', 'shortTitle': ['Unwanted Undead', ]},
    '27': {'title': 'Infinite Stratos', 'shortTitle': ['Infinite Stratos', ], 'seriesType': 'Novel'},
    '28': {'title': 'The Magic in this Other World is Too Far Behind!', 'shortTitle': ['Isekai Mahou', ]},
    '29': {'title': 'From Truant to Anime Screenwriter: My Path to “Anohana” and “The Anthem of the Heart”', 'shortTitle': ['Mari Okada Autobio', ]},
    '30': {'title': 'Lazy Dungeon Master', 'shortTitle': ['Lazy Dungeon Master', ], 'seriesType': 'Novel'},
    '31': {'title': "An Archdemon's Dilemma: How to Love Your Elf Bride", 'shortTitle': ['Elf Bride', ], 'seriesType': 'Novel'},
    '32': {'title': 'Amagi Brilliant Park', 'shortTitle': ['Amagi Brilliant Park', ]},
    '33': {'title': 'Kokoro Connect', 'shortTitle': ['Kokoro Connect', ], 'seriesType': 'Novel'},
    '34': {'title': 'Seirei Gensouki: Spirit Chronicles', 'shortTitle': ['Seirei Gensouki', ]},
    '35': {'title': 'Gear Drive', 'shortTitle': ['Gear Drive', ]},
    '36': {'title': 'JK Haru is a Sex Worker in Another World', 'shortTitle': ['JK Haru', ]},
    '37': {'title': 'Der Werwolf: The Annals of Veight', 'shortTitle': ['Jinrou', ]},
    '38': {'title': 'Sorcerous Stabber Orphen: The Wayward Journey', 'shortTitle': ['Orphen', ]},
    '39': {'title': 'Last and First Idol', 'shortTitle': ['Last and First Idol', ]},
    '40': {'title': 'ECHO', 'shortTitle': ['ECHO', ]},
    '41': {'title': 'My Next Life as a Villainess: All Routes Lead to Doom!', 'shortTitle': ['Bakarina', ]},
    '42': {'title': 'Apparently it\'s My Fault That My Husband Has The Head of a Beast', 'shortTitle': ['Beast Head', ]},
    '43': {'title': 'Ascendance of a Bookworm (Manga)', 'shortTitle': ['Ascendance of a Bookworm (Manga)', ], 'seriesType': 'Manga'},
    '44': {'title': 'Seirei Gensouki: Spirit Chronicles (Manga)', 'shortTitle': ['Seirei Gensouki (Manga)', ], 'seriesType': 'Manga'},
    '45': {'title': 'A Very Fairy Apartment', 'shortTitle': ['A Very Fairy Apartment', ], 'seriesType': 'Manga'},
    '46': {'title': 'Infinite Dendrogram (Manga)', 'shortTitle': ['Infinite Dendrogram (Manga)', ], 'seriesType': 'Manga'},
    '47': {'title': 'How a Realist Hero Rebuilt the Kingdom (Manga)', 'shortTitle': ['Realist Hero (Manga)', ], 'seriesType': 'Manga'},
    '48': {'title': 'I Shall Survive Using Potions!', 'shortTitle': ['Potion Loli', ], 'seriesType': 'Novel'},
    '49': {'title': 'Cooking with Wild Game', 'shortTitle': ['Cooking with Wild Game', ], 'seriesType': 'Novel'},
    '50': {'title': 'I Shall Survive Using Potions! (Manga)', 'shortTitle': ['I Shall Survive Using Potions!', ], 'seriesType': 'Manga'},
    '51': {'title': 'The Magic in this Other World is Too Far Behind! (Manga)', 'shortTitle': ['The Magic in this World is Too Far Behind!', ], 'seriesType': 'Manga'},
    '52': {'title': 'An Archdemon\'s Dilemma: How to Love Your Elf Bride (Manga)', 'shortTitle': ['Elf Bride Manga', ], 'seriesType': 'Manga'},
    '53': {'title': 'Animeta!', 'shortTitle': ['Animeta!', ], 'seriesType': 'Manga'},
    '54': {'title': 'Welcome to Japan, Ms. Elf!', 'shortTitle': ['Welcome to Japan, Ms. Elf!', ], 'seriesType': 'Novel'},
    '55': {'title': 'The Master of Ragnarok & Blesser of Einherjar (Manga)', 'shortTitle': ['The Master of Ragnarok (Manga)', ], 'seriesType': 'Manga'},
    '56': {'title': "The Greatest Magicmaster's Retirement Plan", 'shortTitle': ['Magicmaster', ], 'seriesType': 'Novel'},
    '57': {'title': "Campfire Cooking in Another World with My Absurd Skill", 'shortTitle': ['Campfire Cooking', ], 'seriesType': 'Novel'},
    '58': {'title': "Ascendance of a Bookworm", 'shortTitle': ['Bookworm (LN)', ], 'seriesType': 'Novel'},
    '59': {'title': "Full Metal Panic!", 'shortTitle': ['Full Metal Panic!', ], 'seriesType': 'Novel'},
    '60': {'title': 'Discommunication', 'shortTitle': ['Discommunication', ], 'seriesType': 'Manga'},
    '61': {'title': 'Sweet Reincarnation', 'shortTitle': ['Sweet Reincarnation', ], 'seriesType': 'Manga'},
    '62': {'title': 'Marginal Operation', 'shortTitle': ['Marginal Operation', ], 'seriesType': 'Manga'},
    '63': {'title': 'The Faraway Paladin (Manga)', 'shortTitle': ['The Faraway Paladin (Manga)', ], 'seriesType': 'Manga'},
    '64': {'title': "Crest of the Stars", 'shortTitle': ['Crest of the Stars', ], 'seriesType': 'Novel'},
    '65': {'title': "Record of Wortenia War", 'shortTitle': ['Wortenia', ], 'seriesType': 'Novel'},
    '66': {'title': "Side-By-Side Dreamers", 'shortTitle': ['Side-By-Side Dreamers', ], 'seriesType': 'Novel'},
    '67': {'title': "Seriously Seeking Sister! Ultimate Vampire Princess Just Wants Little Sister; Plenty of Service Will Be Provided!", 'shortTitle': ['Yuri Vampire', ], 'seriesType': 'Novel'},
}


def set_pref(request):
    if request.GET.get('series'):
        # Set new cookie then redirect
        if request.GET.get('json'):
            response = HttpResponseRedirect('/?json=1')
        else:
            response = HttpResponseRedirect('/')
        response.set_cookie('series', value=request.GET.get('series'), max_age=31536000)
    else:
        # Show default page to choose
        bookmark_url = request.META["HTTP_HOST"]+"/series/"
        following_list = request.COOKIES.get('series', '').split()
        render_list = [{'value': str(key), 'title': TITLES_LIST[str(key)]['title'], 'checked':"checked" if str(key) in following_list else ""} for key in range(len(TITLES_LIST))]
        response = render(request, 'set.html', {'series_list': render_list, 'bookmark_url': bookmark_url})
    return response


def cleanup_title(title):
    if title[-1] in "1234567890":
        return title.rsplit(" V", 1)[0].strip()
    elif ":" in title:
        return title.rsplit(":", 1)[0].strip()
    else:
        return title.strip()


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
        following_list = [j for i in request.COOKIES.get('series').split() for j in TITLES_LIST[i]["shortTitle"]]
    else:
        following_list = [j for i in TITLES_LIST.values() for j in i["shortTitle"]]
    data = [i for i in data if cleanup_title(i["name"]) in following_list]
    for i in data:
        i.pop("attachments", None)
        i["linkFragment"] = "https://j-novel.club" + i["linkFragment"]
        if datetime.strptime(i["date"], "%Y-%m-%dT%H:%M:%S.%fZ") < datetime.utcnow():
            i["released"] = True
        else:
            i["released"] = False
            time_remaining = datetime.strptime(i["date"], "%Y-%m-%dT%H:%M:%S.%fZ") - datetime.utcnow()
            i["date"] += ' (in {})'.format(str(time_remaining))
    next_month = (m+relativedelta(months=+1)).strftime("%Y-%m")
    last_month = (m+relativedelta(months=-1)).strftime("%Y-%m")
    this_month = m.strftime("%Y-%m")
    bookmark_url = request.META["HTTP_HOST"]+"/set/?series="+request.COOKIES.get('series', '')
    if request.GET.get('json'):
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        return render(request, 'home.html', {'data': data, 'next_month': next_month, 'this_month': this_month, 'last_month': last_month, 'bookmark_url': bookmark_url})


def get_series(request, series):
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
    try:
        following_list = TITLES_LIST[series]["shortTitle"]
    except KeyError:
        return HttpResponse("Invalid series")
    data = [i for i in data if cleanup_title(i["name"]) in following_list]
    for i in data:
        i.pop("attachments", None)
        i["linkFragment"] = "https://j-novel.club" + i["linkFragment"]
        if datetime.strptime(i["date"], "%Y-%m-%dT%H:%M:%S.%fZ") < datetime.utcnow():
            i["released"] = True
        else:
            i["released"] = False
            time_remaining = datetime.strptime(i["date"], "%Y-%m-%dT%H:%M:%S.%fZ") - datetime.utcnow()
            i["date"] += ' (in {})'.format(str(time_remaining))
    next_month = (m+relativedelta(months=+1)).strftime("%Y-%m")
    last_month = (m+relativedelta(months=-1)).strftime("%Y-%m")
    this_month = m.strftime("%Y-%m")
    bookmark_url = request.META["HTTP_HOST"]+"/series/"+str(series)
    if request.GET.get('json'):
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        return render(request, 'home.html', {'data': data, 'next_month': next_month, 'this_month': this_month, 'last_month': last_month, 'bookmark_url': bookmark_url})
