import base64
import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json

from io import StringIO
import csv
import time
latest_review_load = -10**50


def loadreviews():
    global reviews
    global latest_review_load
    r = requests.get(
        "https://docs.google.com/spreadsheet/ccc?key=1lAhfx55PorM3F83iJDEnZF_UzsxVsxwSbs1rPsQxk5k&output=csv")
    f = StringIO(r.content.decode())
    reader = csv.reader(f, delimiter=',')
    rows = []
    for row in reader:
        rows.append(row)
    reviews = rows
    latest_review_load = time.time()


def getreviews():
    global reviews
    global latest_review_load
    if (latest_review_load+600) < time.time():
        loadreviews()
    return reviews


def getratings(campsite_number_to_check):
    windratings = []
    locationratings = []
    privacyratings = []
    for review in getreviews()[1:]:
        if review[2] == str(campsite_number_to_check):
            try:
                windratings.append(int(review[3]))
            except:
                None
            try:
                locationratings.append(int(review[4]))
            except:
                None
            try:
                privacyratings.append(int(review[5]))
            except:
                None
    try:
        windrating = sum(windratings)/len(windratings)
    except:
        windrating = None
    try:
        locationrating = sum(locationratings)/len(locationratings)
    except:
        locationrating = None
    try:
        privacyrating = sum(privacyratings)/len(privacyratings)
    except:
        privacyrating = None
    return windrating, locationrating, privacyrating


def getreviewstoshow(campsite_number_to_check):
    reviews_allowed = []
    for review in getreviews()[1:]:
        if review[10] == "TRUE" and review[2] == campsite_number_to_check:
            if review[7]:
                reviews_allowed.append([review[6], review[7]])
            else:
                reviews_allowed.append(
                    [review[6], "A colesbay.maxstuff.net user"])
    return reviews_allowed
# def getcolor(rating):
# if rating == 0:
##        wind_color = "black"
# elif rating == 1:
##        wind_color = "darkblue"
# elif rating == 2:
##        wind_color = "green"
# elif rating == 3:
##        wind_color = "orange"
# elif rating == 4:
##        wind_color = "red"
# elif rating == 5:
##        wind_color = "hotpink"
# else:
##        wind_color = "black"
# return wind_color
# def getrating(rating):
##


def index(request):
    campsites_document = open("/repositories/coles-bay-campsites/campsites.csv", "rb").read().decode().split("\n")
    campsites_wn = json.loads(open("/repositories/coles-bay-campsites/sitedata.json", "rb").read().decode())
    campsites = ""
    for site_number in campsites_document:
        try:
            campsite_test = str(int(site_number))
        except:
            campsite_test = None
        if campsite_test:
            ##            site_color = getcolor(campsites_wn[campsite_test]["wind"])
            site_color = "black"
            campsites += """<li><a href="/viewcamp?id="""+campsite_test + \
                """" style="color:"""+site_color+"""">"""+campsite_test+"""</a></li>"""
    return HttpResponse("""<!DOCTYPE html>
<head>
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=UA-160826511-4"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'UA-160826511-4');
    </script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Coles Bay Campsites</title>
    <style>
    * {
    font-family: sans-serif;
    }
        @media screen and (orientation:portrait) {
            h1 {
                font-family: sans-serif;
                font-size: 10vmin;
            }
            li {
                font-family: sans-serif;
                font-size: 7vmin;
                margin: 5vmin;
            }
            ul {
                column-count: 1;
            }
            p {
                font-size: 7vmin;
            }
        }
        @media screen and (orientation:landscape) {
            h1 {
                font-family: sans-serif;
                font-size: 10vmin;
            }
            li {
                font-family: sans-serif;
                font-size: 5vmin;
                padding: 1vmin;
            }
            ul {
                column-count: 7;
            }
            p {
                font-size: 5vmin;
            }
        }
    </style>
</head>
<body>
    <h1>Coles Bay Campsites</h1>
    <p>Detailed information, maps, and panormas for  the Richardsons Beach Campsites at Freycinet National Park</p>
    <ul>
        """+campsites+"""
    </ul>
    <br>
    <p>
    <a href="/about">About</a><br>
    <a href="/donate">Donate</a><br>
    <a href="https://www.maxstuff.net">My Other Work</a>
    </p>
</body>""")


def viewcamp(request):
    campsite_id = request.GET.get("id", None)
    campsites_wn = json.loads(open("/repositories/coles-bay-campsites/sitedata.json", "rb").read().decode())
    if campsite_id and campsite_id in campsites_wn:
        ##        wind_color = getcolor(campsites_wn[campsite_id]["wind"])
        wind_color = "black"
        desfield = ""
        ratings = getratings(campsite_id)
        ratingstextlist = []
        averagelist = []
        if ratings[0]:
            ratingstextlist.append("""Wind <span class="Stars" style="--rating: """+str(
                float(ratings[0]))+""";--star-size: 4vmin;"></span>""")
            averagelist.append(ratings[0])
        else:
            ratingstextlist.append("""Wind <span class="Stars" style="--rating: """+str(
                float(campsites_wn[campsite_id]["wind"]))+""";--star-size: 4vmin;"></span>""")
            averagelist.append(campsites_wn[campsite_id]["wind"])
        if ratings[1]:
            ratingstextlist.append("""Utility Distance <span class="Stars" style="--rating: """+str(
                float(ratings[1]))+""";--star-size: 4vmin;"></span>""")
            averagelist.append(ratings[1])
        if ratings[2]:
            ratingstextlist.append("""Privacy <span class="Stars" style="--rating: """+str(
                float(ratings[2]))+""";--star-size: 4vmin;"></span>""")
            averagelist.append(ratings[2])
        print(averagelist)
        average = sum(averagelist)/len(averagelist)
        ratingstext = "<br>".join(ratingstextlist)
        reviewscollectedandformatted = []
        for review in getreviewstoshow(campsite_id):
            reviewscollectedandformatted.append(
                f'<div class="review" style="font-family: sans-serif;margin-bottom: 1vh;width: 90%;margin-left: 5%;margin-right: 5%;text-align: center;">{review[0]}<br><div class="reviewauthor" style="text-align: right;color: darkslategrey;">- {review[1]}</div></div>')
        if len(reviewscollectedandformatted) > 0:
            reviewsfetched = ''.join(reviewscollectedandformatted)
        else:
            reviewsfetched = """<div class="review" style="font-family: sans-serif;margin-bottom: 1vh;width: 90%;margin-left: 5%;margin-right: 5%;text-align: center;">No reviews yet. Be the first to <a id="review_link_one" href="https://docs.google.com/forms/d/e/1FAIpQLScok1NIAGXhXBfzmRwv0q_4rlJdkAsSy2IOoeXZspRJ6Q6mMg/viewform?usp=pp_url&entry.1764404320="""+campsite_id+"""">leave one</a>!</div>"""
        print(campsites_wn)
        if "note" in campsites_wn[campsite_id]:
            desfield = """<div style="display:inline-block;vertical-align:top;font-size:5vmin;margin-top:5vmin;margin-bottom:5vmin;">""" + \
                campsites_wn[campsite_id]["note"].replace(
                    "\n", "<br>")+"""</div>"""
        google_form_b64 = base64.urlsafe_b64encode(
            ("https://docs.google.com/forms/d/e/1FAIpQLScok1NIAGXhXBfzmRwv0q_4rlJdkAsSy2IOoeXZspRJ6Q6mMg/viewform?usp=pp_url&entry.1764404320="+campsite_id).encode()).decode()
        return HttpResponse("""<!DOCTYPE html>
<head>
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=UA-160826511-4"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'UA-160826511-4');
    </script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Campsite """+campsite_id+"""</title>
    <style>
    * {
    font-family: sans-serif;
}

:root {
    --star-color: #999;
    --star-background: #fc0;
}

.Stars {
    --percent: calc(var(--rating) / 5 * 100%);
    display: inline-block;
    font-size: var(--star-size);
    font-family: Times;
    line-height: 1;
}

.Stars::before {
    content: "★★★★★";
    letter-spacing: 3px;
    background: linear-gradient(90deg, var(--star-background) var(--percent), var(--star-color) var(--percent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.threesixtycontainer {
    height: 80vh;
    width: 80vw;
}

.heading {
    font-family: sans-serif;
    font-size: 15vw;
    margin-bottom: 0;
    font-weight: bold;
    /*color: """+wind_color+""";*/
    margin-top: 0;
}

.ratingtext {
    font-family: sans-serif;
    font-size: 5vmin;
    font-weight:
        bold;
    /*color: """+wind_color+""";*/
}

@media screen and (orientation:portrait) {
    li {
        font-family: sans-serif;
        font-size: 4vmin;
    }

    ul {
        font-family: sans-serif;
        column-count: 3;
    }

    p {
        font-size: 5vmin;
    }

    .reviewsdiv {
        text-align: center;
    }

    .review {
        font-family: sans-serif;
        margin-bottom: 1vh;
        width: 90%;
        margin-left: 5%;
        margin-right: 5%;
        text-align: center;
    }

    .reviewauthor {
        width: 100%;
        font-family: sans-serif;
        text-align: right;
        color: darkslategrey;
    }

    .threesixtycontainer {
        height: 50vh;
        width: 90vw;
    }
}

@media screen and (orientation:landscape) {
    .heading {
        font-size: 10vmin;
    }
    li {
        font-family: sans-serif;
        font-size: 4vmin;
    }

    ul {
        font-family: sans-serif;
        column-count: 3;
    }

    p {
        font-size: 5vmin;
    }

    .reviewsdiv {
        text-align: center;
    }

    .review {
        font-family: sans-serif;
        margin-bottom: 1vh;
        width: 90%;
        margin-left: 5%;
        margin-right: 5%;
        text-align: center;
    }

    .reviewauthor {
        width: 100%;
        font-family: sans-serif;
        text-align: right;
        color: darkslategrey;
    }

    .subrating {
        color: pink;
    }

    .threesixtycontainer {
        height: 80vh;
        width: 80vw;
    }
}
    </style>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.css"/>
    <script type="text/javascript" src="https://cdn.jsdelivr.net/npm/pannellum@2.5.6/build/pannellum.js"></script>
</head>
<body>
    <p class="heading">Campsite """+campsite_id+"""</p>
    <p class="ratingtext">Rating <span class="Stars" style="--rating: """+str(float(average))+""";--star-size: 6vmin;"></span><br>
    <span style="font-size:3.5vmin;">"""+ratingstext+"""</span>
    </span></p>
    <p><a id="review_link_two" href="https://docs.google.com/forms/d/e/1FAIpQLScok1NIAGXhXBfzmRwv0q_4rlJdkAsSy2IOoeXZspRJ6Q6mMg/viewform?usp=pp_url&entry.1764404320="""+campsite_id+"""">Leave a rating or review</a></p>
    <div class="threesixtycontainer">
    <noscript>
    <iframe width="100%" height="100%" allowfullscreen style="border-style:none;" src="https://cdn.pannellum.org/2.5/pannellum.htm#panorama=http://localhost:5000/static/repositories/coles-bay-campsites/images/cb-"""+campsite_id+""".jpeg&amp;autoLoad=true&amp;minHfov=40&amp;maxHfov=150"></iframe>
    </noscript>
    <script>
    let viewer_div = document.createElement('div');
    viewer_div.id = 'panorama';
    document.getElementsByClassName('threesixtycontainer')[0].appendChild(viewer_div);
    // if portrait orientation
    let maxhfov;
    if (window.innerHeight > window.innerWidth) {
        maxhfov = 120;
    } else {
        maxhfov = 150;
    }
    pannellum.viewer('panorama', {
        "type": "equirectangular",
        "panorama": "http://localhost:5000/static/repositories/coles-bay-campsites/images/cb-"""+campsite_id+""".jpeg",
        "autoLoad": true,
        "minHfov": 40,
        "maxHfov": maxhfov,
        "friction": 0.5,
    });
    </script>
    </div>
"""+desfield+"""
<img alt="Map not currently available." src="http://localhost:5000/static/repositories/coles-bay-campsites/maps/"""+str(campsite_id)+""".svg" style="max-height: 90vh; max-width: 90vw;">
<h2>Reviews</h2>
<div class="reviewsdiv" style="text-align: center;">
"""+reviewsfetched+"""
</div>
<br>
<p>
    <a href="/about">About</a><br>
    <a href="/donate">Donate</a><br>
    <a href="https://www.maxstuff.net">My Other Work</a>
</p>
</body>""")
    else:
        return HttpResponse("Campsite Non-existant")


def donate(request):
    images = open("images.txt", "rb").read().decode().split("\n")
    return HttpResponse("""<!DOCTYPE html>
<head>
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=UA-160826511-4"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'UA-160826511-4');
    </script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
    * { font-family: sans-serif; }
        a {
            text-decoration: none;
            color: black;
        }
        h1 {
            font-family: sans-serif;
            font-size: 10vmin;
        }
        h2 {
            font-family: sans-serif;
            font-size: 7vmin;
        }
        p {
            font-family: sans-serif;
            font-size: 5vmin;
        }
        img {
            max-width: 25vw;
            max-height: 25vh;
        }
        input {
            font-size: 4vmin;
            text-align: right;
            width: 10vmax;
        }
        .fineprint {
            font-size: 3vmin;
        }
        .somewhatfine {
            font-size: 5vmin;
        }
    </style>
    <title>Donate</title>
</head>
<body>
    <h1>Donate money to me</h1>
    <p>Money collected will go towards upgrading my computer to advance my programming skills, etc.</p>
    <p>$<input type="number" value="1" id="amountInput" min=0>.<input type="number" value="0" min=-1 max=100 id="amountInputCents"></p>
    <p class="fineprint">Some amounts only available with certain methods. Methods listed in my order of preference.</p>
    <a href="https://spriggy.me/maxb39" id="spriggyMethod"><h2>Donate with <img src=\""""+images[0]+"""\" alt="Spriggy"> (AUD)<br><span class="somewhatfine">Needs Australian Debit Card</span></h2></a>
    <a href="https://paypal.me/maxstuffnet/1AUD" id="paypalMethod"><h2>Donate with <img src=\""""+images[1]+"""\" alt="PayPal"> (AUD)<br><span class="somewhatfine">Needs PayPal Account</span></h2></a>
    <a href="https://paypal.me/maxstuffnet/"><h2>Donate with <img src=\""""+images[1]+"""\" alt="PayPal"> (Any Currency)<br><span class="somewhatfine">Needs PayPal Account</span></h2></a>
    <script>
        function updateMethod () {
            if (amountInputCents.value<0) {
                if (amountInput.value>0) {
                    amountInput.value=Number(amountInput.value)-1;
                    amountInputCents.value=99;
                } else {
                    amountInputCents.value=0;
                }
            } else if (amountInputCents.value>99) {
                amountInput.value=Number(amountInput.value)+1;
                amountInputCents.value=0;
            }
            total_amount = Number(amountInput.value);
            total_amount += (Number(amountInputCents.value)/100);
            amountInputCents.value="0".repeat(2-amountInputCents.value.length)+amountInputCents.value;
            if (amountInput.value>=10 && amountInput.value<=100) {
                spriggyMethod.style.display = "";
            } else {
                spriggyMethod.style.display = "none";
            }
            spriggyMethod.href = "https://spriggy.me/maxb39?amount="+total_amount;
            paypalMethod.style.display = "";
            paypalMethod.href = "https://paypal.me/maxstuffnet/"+total_amount+"AUD";

        }
        amountInput.onchange = updateMethod;
        amountInput.oninput = updateMethod;
        amountInputCents.onchange = updateMethod;
        amountInputCents.oninput = updateMethod;
        updateMethod();
        updateInteval = setInterval(updateMethod,100);
        setTimeout(function() {clearInterval(updateInteval)}, 10000);
    </script>
</body>""")


def about(request):
    return HttpResponse("""<!DOCTYPE html>
<head>
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=UA-160826511-4"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'UA-160826511-4');
    </script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
    * { font-family: sans-serif; }
        h1 {
            font-family: sans-serif;
            font-size: 7vmin;
        }
        p {
            font-family: sans-serif;
            font-size: 5vmin;
        }
        img {
            max-width: 50vw;
            max-height: 50vh;
        }
    </style>
    <title>About</title>
</head>
<body>
    <h1>About colesbay.maxstuff.net</h1>
    <p>Hi, I am Max, and I am 12 long has my family wondered "I wonder if this will be a good campsite" especially in times other then summer when the ballot is in use.</p>
<p>I decided to take 360-degree photos of every campsite and I also made measurements down to the last centimetre. I took a wind-rating. I then put it all on this website where you can see all that info you can even leave reviews and star ratings on each campsite.</p>
<p>I hope you enjoy this service, and you can always contact me at Email - <span>me<span>(at</span>)maxstuff</span>(<span>dot)net</span> <sup><span style="color:blue" title="This is used to prevent automated bots from getting my email.">[?]</span></sup><br></p>
</body>""")

# curl -X POST http://localhost:5000/update_repositories --data UPDATE_REPOSITORIES_TOKEN=abc


@csrf_exempt
def update_repositories(request):
    if request.method == 'POST':
        if os.environ.get('UPDATE_REPOSITORIES_TOKEN') == request.POST.get('UPDATE_REPOSITORIES_TOKEN'):
            os.system(
                "find ../repositories -mindepth 1 -maxdepth 1 -type d " +
                "-exec git -C {} pull \; 2>&1 > /dev/null"
            )
            return HttpResponse("Updated")
        else:
            return HttpResponse("Wrong token")
    else:
        return HttpResponse("Wrong method")
