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
    '6': {'title': 'Mixed Bathing in Another Dimension', 'shortTitle': ['Mixed Bathing in Another Dimension', 'Mixed Bathing']},
    '7': {'title': 'The Faraway Paladin', 'shortTitle': ['The Faraway Paladin', ]},
    '8': {'title': 'Paying to Win in a VRMMO', 'shortTitle': ['Paying to Win in a VRMMO', ]},
    '9': {'title': 'How a Realist Hero Rebuilt the Kingdom', 'shortTitle': ['Realist Hero', 'How a Realist Hero Rebuilt the Kingdom', ]},
    '10': {'title': 'In Another World With My Smartphone', 'shortTitle': ['Smartphone', ]},
    '11': {'title': "Arifureta: From Commonplace to World's Strongest", 'shortTitle': ['Arifureta', "Arifureta: From Commonplace to World's Strongest", ]},
    '12': {'title': 'Bluesteel Blasphemer', 'shortTitle': ['Bluesteel Blasphemer', ]},
    '13': {'title': 'Invaders of the Rokujouma!?', 'shortTitle': ['Invaders of the Rokujouma!?', 'Rokujouma!?', ]},
    '14': {'title': "If It's for My Daughter, I'd Even Defeat a Demon Lord", 'shortTitle': ['For My Daughter', ]},
    '15': {'title': 'Demon King Daimaou', 'shortTitle': ['Demon King Daimaou', ]},
    '16': {'title': 'Infinite Dendrogram', 'shortTitle': ['Infinite Dendrogram', ]},
    '17': {'title': 'Clockwork Planet', 'shortTitle': ['Clockwork Planet', ]},
    '18': {'title': 'Outbreak Company', 'shortTitle': ['Outbreak Company', ]},
    '19': {'title': 'How NOT to Summon a Demon Lord', 'shortTitle': ['How NOT to Summon a Demon Lord', ], 'seriesType': 'Novel'},
    '20': {'title': 'Walking My Second Path in Life', 'shortTitle': ['Watafuta', ]},
    '21': {'title': 'Yume Nikki: I Am Not in Your Dream', 'shortTitle': ['Yume Nikki', ]},
    '22': {'title': 'Ao Oni', 'shortTitle': ['Ao Oni', ]},
    '23': {'title': 'Arifureta Zero', 'shortTitle': ['Arifureta Zero', 'Arifureta Zero:', ]},
    '24': {'title': 'The Master of Ragnarok & Blesser of Einherjar', 'shortTitle': ['The Master of Ragnarok', ]},
    '25': {'title': "Me, a Genius? I Was Reborn into Another World and I Think They've Got the Wrong Idea!", 'shortTitle': ['Me, a Genius?', ]},
    '26': {'title': 'The Unwanted Undead Adventurer', 'shortTitle': ['Unwanted Undead', ]},
    '27': {'title': 'Infinite Stratos', 'shortTitle': ['Infinite Stratos', ], 'seriesType': 'Novel'},
    '28': {'title': 'The Magic in this Other World is Too Far Behind!', 'shortTitle': ['Isekai Mahou', ]},
    '29': {'title': 'From Truant to Anime Screenwriter: My Path to "Anohana" and "The Anthem of the Heart"', 'shortTitle': ['Mari Okada Autobio', ]},
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
    '42': {'title': "Apparently it's My Fault That My Husband Has The Head of a Beast", 'shortTitle': ['Beast Head', ]},
    '43': {'title': 'Ascendance of a Bookworm (Manga)', 'shortTitle': ['Ascendance of a Bookworm (Manga)', ], 'seriesType': 'Manga'},
    '44': {'title': 'Seirei Gensouki: Spirit Chronicles (Manga)', 'shortTitle': ['Seirei Gensouki (Manga)', ], 'seriesType': 'Manga'},
    '45': {'title': 'A Very Fairy Apartment', 'shortTitle': ['A Very Fairy Apartment', ], 'seriesType': 'Manga'},
    '46': {'title': 'Infinite Dendrogram (Manga)', 'shortTitle': ['Infinite Dendrogram (Manga)', ], 'seriesType': 'Manga'},
    '47': {'title': 'How a Realist Hero Rebuilt the Kingdom (Manga)', 'shortTitle': ['Realist Hero (Manga)', ], 'seriesType': 'Manga'},
    '48': {'title': 'I Shall Survive Using Potions!', 'shortTitle': ['Potion Loli', ], 'seriesType': 'Novel'},
    '49': {'title': 'Cooking with Wild Game', 'shortTitle': ['Cooking with Wild Game', ], 'seriesType': 'Novel'},
    '50': {'title': 'I Shall Survive Using Potions! (Manga)', 'shortTitle': ['I Shall Survive Using Potions!', 'Potion Loli (Manga)', ], 'seriesType': 'Manga'},
    '51': {'title': 'The Magic in this Other World is Too Far Behind! (Manga)', 'shortTitle': ['The Magic in this World is Too Far Behind!', 'The Magic in this Other World is Too Far Behind!'], 'seriesType': 'Manga'},
    '52': {'title': "An Archdemon's Dilemma: How to Love Your Elf Bride (Manga)", 'shortTitle': ['Elf Bride Manga', 'Elf Bride (Manga)', ], 'seriesType': 'Manga'},
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
    '68': {'title': "The Unwanted Undead Adventurer (Manga)", 'shortTitle': ['Unwanted Undead (Manga)', ], 'seriesType': 'Manga'},
    '69': {'title': "Middle-Aged Businessman, Arise in Another World!", 'shortTitle': ['Middle-Aged Businessman, Arise in Another World!', 'Businessman Isekai', ], 'seriesType': 'Novel'},
    '70': {'title': "Otherside Picnic", 'shortTitle': ['Otherside Picnic', ], 'seriesType': 'Novel'},
    '71': {'title': "The Combat Baker and Automaton Waitress", 'shortTitle': ['Combat Baker:', 'Combat Baker', ], 'seriesType': 'Novel'},
    '72': {'title': "There Was No Secret Evil-Fighting Organization (srsly?!), So I Made One MYSELF!", 'shortTitle': ['Secret Organization', ], 'seriesType': 'Novel'},
    '73': {'title': "Cooking WIth Wild Game (Manga)", 'shortTitle': ['Cooking WIth Wild Game (Manga)', ], 'seriesType': 'Manga'},
    '74': {'title': "Sexiled: My Sexist Party Leader Kicked Me Out, So I Teamed Up With a Mythical Sorceress!", 'shortTitle': ['Sexiled', ], 'seriesType': 'Novel'},
    '75': {'title': "Demon Lord, Retry!", 'shortTitle': ['Demon Lord, Retry!', ], 'seriesType': 'Novel'},
    '76': {'title': "Sorcerous Stabber Orphen: The Reckless Journey", 'shortTitle': ['Sorcerous Stabber Orphen: The Reckless Journey', ], 'seriesType': 'Manga'},
    '77': {'title': "Altina the Sword Princess", 'shortTitle': ['Altina', ], 'seriesType': 'Novel'},
    '78': {'title': "Demon Lord, Retry! (Manga)", 'shortTitle': ['Demon Lord, Retry! (Manga)', ], 'seriesType': 'Manga'},
    '79': {'title': "The Holy Knight's Dark Road", 'shortTitle': ['Holy Knight\'s Dark Road', ], 'seriesType': 'Novel'},
}


def set_pref(request):
    if request.GET.get('series'):
        # Set new cookie then redirect
        if request.GET.get('json'):
            response = HttpResponseRedirect('/?json=1')
        elif request.GET.get('rss'):
            response = HttpResponseRedirect('/?rss=1')
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


def filter_to_month_and_series(series, month=None, rss=False):
    if series:
        try:
            following_list = [j for i in series.split() for j in TITLES_LIST[i]["shortTitle"]]
        except KeyError:
            return HttpResponse("Invalid series")
    else:
        following_list = [j for i in TITLES_LIST.values() for j in i["shortTitle"]]
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
    if month:
        m = datetime.strptime(month, "%Y-%m")
        mstr = month
    else:
        m = datetime.today()
        mstr = m.strftime("%Y-%m")
    if rss:
        mstr += "_rss"
    if cache.get(mstr):
        data = cache.get(mstr)
    else:
        if rss:
            f = m + relativedelta(day=1, months=-1)
            t = f + relativedelta(months=+2)
        else:
            f = m + relativedelta(day=1)
            t = f + relativedelta(months=+1)
        BASIC_QUERY["where"]["and"][0]["date"]["lt"] = t.strftime("%Y-%m-%d")
        BASIC_QUERY["where"]["and"][1]["date"]["gte"] = f.strftime("%Y-%m-%d")
        query = URL + json.dumps(BASIC_QUERY)
        data = requests.get(query).json()
        cache.set(mstr, data)
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
    return (data, next_month, this_month, last_month)


def index(request):
    data, next_month, this_month, last_month = filter_to_month_and_series(series=request.COOKIES.get('series'), month=request.GET.get('month'))
    setcookie_url = "http://"+request.META["HTTP_HOST"]+"/set/?series="+request.COOKIES.get('series', '')
    quickview_url = "http://"+request.META["HTTP_HOST"]+"/series/"+request.COOKIES.get('series', '')
    rss_url = "http://"+request.META["HTTP_HOST"]+"/rss/"+request.COOKIES.get('series', '')
    if request.GET.get('json'):
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        return render(request, 'home.html', {'data': data, 'next_month': next_month, 'this_month': this_month, 'last_month': last_month, 'setcookie_url': setcookie_url, 'quickview_url': quickview_url, 'rss_url': rss_url})


def get_series(request, series):
    data, next_month, this_month, last_month = filter_to_month_and_series(series=series, month=request.GET.get('month'))
    setcookie_url = "http://"+request.META["HTTP_HOST"]+"/set/?series="+series
    quickview_url = "http://"+request.META["HTTP_HOST"]+"/series/"+series
    rss_url = "http://"+request.META["HTTP_HOST"]+"/rss/"+series
    if request.GET.get('json'):
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        return render(request, 'home.html', {'data': data, 'next_month': next_month, 'this_month': this_month, 'last_month': last_month, 'setcookie_url': setcookie_url, 'quickview_url': quickview_url, 'rss_url': rss_url})


def get_rss(request, series):
    data, next_month, this_month, last_month = filter_to_month_and_series(series=series, month=request.GET.get('month'), rss=True)
    rss_url = "http://"+request.META["HTTP_HOST"]+"/rss/"+series
    data = [i for i in data if i["released"]]
    for i in data:
        i["date"] = datetime.strftime(datetime.strptime(i["date"], "%Y-%m-%dT%H:%M:%S.%fZ"), "%a, %d %b %Y %H:%M")
    lastBuildDate = datetime.strftime(datetime.utcnow(), "%a, %d %b %Y %H:%M")
    set_url = request.META["HTTP_HOST"] + "/set/"
    description = "Data for series {}, visit {} to get series names".format(series, set_url)
    return render(request, 'rss.xml', {'data': data, 'rss_url': rss_url, 'lastBuildDate': lastBuildDate, 'description': description})
