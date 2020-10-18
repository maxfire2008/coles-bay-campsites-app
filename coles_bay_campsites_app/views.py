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
    campsites_document = requests.get("https://raw.githubusercontent.com/maxfire2008/coles-bay-campsites/main/campsites.csv").content.decode().split("\n")
    campsites_wn = json.loads(requests.get("https://raw.githubusercontent.com/maxfire2008/coles-bay-campsites/main/sitedata.json").content.decode())
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
    campsites_wn = json.loads(requests.get("https://raw.githubusercontent.com/maxfire2008/coles-bay-campsites/main/sitedata.json").content.decode())
    wind_color = getcolor(campsites_wn[campsite_id]["wind"])
    if campsite_id:
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
            font-family: sans-serif;
            font-size: 2vmin;
            font-weight: bold;
            color: """+wind_color+""";
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
    <p class="heading">Campsite """+campsite_id+"""</p>
    <p class="wind">Wind Rating """+str(campsites_wn[campsite_id]["wind"])+"""/5</p>
    <iframe width="60%" height="70%" allowfullscreen style="border-style:none;" src="https://cdn.pannellum.org/2.5/pannellum.htm#panorama=https://raw.githubusercontent.com/maxfire2008/coles-bay-campsites/main/images/cb-"""+campsite_id+""".jpeg"></iframe>
</body>""")
    else:
        return HttpResponse("Error")
