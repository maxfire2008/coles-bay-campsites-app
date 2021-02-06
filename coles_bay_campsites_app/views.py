from django.http import HttpResponse
import requests, json

from io import StringIO
import csv
import time
latest_review_load = -10**50

def loadreviews():
    global reviews
    global latest_review_load
    r=requests.get("https://docs.google.com/spreadsheet/ccc?key=1lAhfx55PorM3F83iJDEnZF_UzsxVsxwSbs1rPsQxk5k&output=csv")
    f=StringIO(r.content.decode())
    reader = csv.reader(f, delimiter=',')
    rows = []
    for row in reader:
        rows.append(row)
    reviews=rows
    latest_review_load=time.time()
def getreviews():
    global reviews
    global latest_review_load
    if (latest_review_load+600)<time.time():
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
    return windrating,locationrating,privacyrating
##def getreviews

##def getcolor(rating):
##    if rating == 0:
##        wind_color = "black"
##    elif rating == 1:
##        wind_color = "darkblue"
##    elif rating == 2:
##        wind_color = "green"
##    elif rating == 3:
##        wind_color = "orange"
##    elif rating == 4:
##        wind_color = "red"
##    elif rating == 5:
##        wind_color = "hotpink"
##    else:
##        wind_color = "black"
##    return wind_color
##def getrating(rating):
##    

def index(request):
    campsites_document = requests.get("https://cdn.jsdelivr.net/gh/maxfire2008/coles-bay-campsites@master/campsites.csv").content.decode().split("\n")
    campsites_wn = json.loads(requests.get("https://cdn.jsdelivr.net/gh/maxfire2008/coles-bay-campsites@master/sitedata.json").content.decode())
    campsites = ""
    for site_number in campsites_document:
        try:
            campsite_test=str(int(site_number))
        except:
            campsite_test=None
        if campsite_test:
##            site_color = getcolor(campsites_wn[campsite_test]["wind"])
            site_color="black"
            campsites+="""<li><a href="/viewcamp?id="""+campsite_test+"""" style="color:"""+site_color+"""">"""+campsite_test+"""</a></li>"""
    return HttpResponse("""<!DOCTYPE hmtl>
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
        h1 {
            font-family: sans-serif;
            font-size: 15vmin;
        }
        li {
            font-family: sans-serif;
            font-size: 5vmin;
        }
        ul {
            column-count: 3;
        }
        p {
    font-size: 5vmin;
}
    </style>
</head>
<body>
    <h1>Coles Bay Campsites</h1>
    <ul>
        """+campsites+"""
    </ul>
    <br><br>
    <p>
    <a href="/about">About</a><br>
    <a href="/donate">Donate</a><br>
    <a href="https://www.maxstuff.net">My Other Work</a>
    </p>
</body>""")

def viewcamp(request):
    campsite_id = request.GET.get("id",None)
    campsites_wn = json.loads(requests.get("https://cdn.jsdelivr.net/gh/maxfire2008/coles-bay-campsites@master/sitedata.json").content.decode())
    if campsite_id and campsite_id in campsites_wn:
##        wind_color = getcolor(campsites_wn[campsite_id]["wind"])
        wind_color="black"
        desfield = ""
        ratings = getratings(campsite_id)
        ratingstextlist = []
        averagelist = []
        if ratings[0]:
            ratingstextlist.append("""Wind <span class="Stars" style="--rating: """+str(float(ratings[0]))+""";--star-size: 4vmin;"></span>""")
            averagelist.append(ratings[0])
        else:
            ratingstextlist.append("""Wind <span class="Stars" style="--rating: """+str(float(campsites_wn[campsite_id]["wind"]))+""";--star-size: 4vmin;"></span>""")
            averagelist.append(campsites_wn[campsite_id]["wind"])
        if ratings[1]:
            ratingstextlist.append("""Utility Distance <span class="Stars" style="--rating: """+str(float(ratings[1]))+""";--star-size: 4vmin;"></span>""")
            averagelist.append(ratings[1])
        if ratings[2]:
            ratingstextlist.append("""Privacy <span class="Stars" style="--rating: """+str(float(ratings[2]))+""";--star-size: 4vmin;">""")
            averagelist.append(ratings[2])
        print(averagelist)
        average=sum(averagelist)/len(averagelist)
        ratingstext="<br>".join(ratingstextlist)
        if "note" in campsites_wn[campsite_id]:
            desfield="""<div style="display:inline-block;vertical-align:top;font-size:3vmin;">"""+campsites_wn[campsite_id]["note"].replace("\n","<br>")+"""</div>"""
        return HttpResponse("""<!DOCTYPE hmtl>
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
        .heading {
            font-family: sans-serif;
            font-size: 15vmin;
            margin-bottom:0;
            font-weight: bold;
            /*color: """+wind_color+""";*/
        }
        .ratingtext {
            font-family: sans-serif; font-size: 5vmin; font-weight:
            bold; /*color: """+wind_color+""";*/
        }
        li {
            font-family: sans-serif;
            font-size: 4vmin;
        }
        ul {
            column-count: 3;
        }
        @charset "UTF-8";
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
p {
    font-size: 5vmin;
}
    </style>
</head>
<body>
    <p class="heading">Campsite """+campsite_id+"""</p>
    <p class="ratingtext">Rating <span class="Stars" style="--rating: """+str(float(average))+""";--star-size: 6vmin;"></span><br>
    <span style="font-size:3.5vmin">"""+ratingstext+"""</span>
    </span></p>
    <p><a href="https://docs.google.com/forms/d/e/1FAIpQLScok1NIAGXhXBfzmRwv0q_4rlJdkAsSy2IOoeXZspRJ6Q6mMg/viewform?usp=pp_url&entry.1764404320="""+campsite_id+"""">Leave a rating or review</a></p>
    <iframe width="90%" height="70%" allowfullscreen style="border-style:none;" src="https://cdn.pannellum.org/2.5/pannellum.htm#panorama=https://cdn.jsdelivr.net/gh/maxfire2008/coles-bay-campsites@master/images/cb-"""+campsite_id+""".jpeg"></iframe>
<p>"""+desfield+"""</p><br>
<img alt="Map not currently avalible." src="https://cdn.jsdelivr.net/gh/maxfire2008/coles-bay-campsites@master/maps/"""+str(campsite_id)+""".svg" width=100% height=100%>
<br><br>
<p>
    <a href="/about">About</a><br>
    <a href="/donate">Donate</a><br>
    <a href="https://www.maxstuff.net">My Other Work</a>
</p>
</body>""")
    else:#
        return HttpResponse("Campsite Non-existant")

def donate(request):
    images = open("images.txt","rb").read().decode().split("\n")
    return HttpResponse("""<!DOCTYPE hmtl>
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
        h1 {
            font-family: sans-serif;
            font-size: 15vmin;
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
            max-width: 50vw;
            max-height: 50vh;
        }
    </style>
    <title>Donate</title>
</head>
<body>
    <h1>Donate money to me</h1>
    <h2>Donations of $10 to $100 (preferred)</h2>
    <p><a href="https://spriggy.me/maxb39"><img src=\""""+images[0]+"""\"></a></p>
    <h2>Donations of any amount</h2>
    <p>Coming soon. Watch this space. (PayPal)</p>
</body>""")
def about(request):
    return HttpResponse("""<!DOCTYPE hmtl>
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
<p>I hope you enjoy this service, and you can always contact me at <a href="me@maxstuff.net">me@maxstuff.net</a></p>
</body>""")
