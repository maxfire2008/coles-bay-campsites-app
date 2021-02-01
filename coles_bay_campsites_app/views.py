from django.http import HttpResponse
import requests, json

def getcolor(rating):
    if rating == 0:
        wind_color = "black"
    elif rating == 1:
        wind_color = "darkblue"
    elif rating == 2:
        wind_color = "green"
    elif rating == 3:
        wind_color = "orange"
    elif rating == 4:
        wind_color = "red"
    elif rating == 5:
        wind_color = "hotpink"
    else:
        wind_color = "black"
    return wind_color

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
            site_color = getcolor(campsites_wn[campsite_test]["wind"])
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
    </style>
</head>
<body>
    <h1>Coles Bay Campsites</h1>
    <ul>
        """+campsites+"""
    </ul>
</body>""")

def viewcamp(request):
    campsite_id = request.GET.get("id",None)
    campsites_wn = json.loads(requests.get("https://cdn.jsdelivr.net/gh/maxfire2008/coles-bay-campsites@master/sitedata.json").content.decode())
    if campsite_id and campsite_id in campsites_wn:
        wind_color = getcolor(campsites_wn[campsite_id]["wind"])
        desfield = ""
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
            color: """+wind_color+""";
        }
        .wind {
            font-family: sans-serif; font-size: 5vmin; font-weight:
            bold; color: """+wind_color+""";
        }
        li {
            font-family: sans-serif;
            font-size: 4vmin;
        }
        ul {
            column-count: 3;
        }
    </style>
</head>
<body>
    <p class="heading">Campsite """+campsite_id+"""</p>
    <p class="wind">Wind Rating """+str(campsites_wn[campsite_id]["wind"])+"""/5</p>
    <iframe width="90%" height="70%" allowfullscreen style="border-style:none;" src="https://cdn.pannellum.org/2.5/pannellum.htm#panorama=https://cdn.jsdelivr.net/gh/maxfire2008/coles-bay-campsites@master/images/cb-"""+campsite_id+""".jpeg"></iframe>
<p>"""+desfield+"""</p><br>
<img alt="Map not currently avalible." src="https://cdn.jsdelivr.net/gh/maxfire2008/coles-bay-campsites@master/maps/"""+str(campsite_id)+""".svg" width=100% height=100%>
</body>""")
    else:
        return HttpResponse("Campsite Non-existant")
