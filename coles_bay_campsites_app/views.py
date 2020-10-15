from django.http import HttpResponse
import requests

def index(request):
    campsites_document = requests.get("https://raw.githubusercontent.com/maxfire2008/coles-bay-campsites/main/campsites.csv").content.decode().split("\n")
    campsites = ""
    for site_number in campsites_document:
        try:
            campsite_test=str(int(site_number))
        except:
            campsite_test=None
        if campsite_test:
            campsites+="""<li><a href="/viewcamp?id="""+campsite_test+"""">"""+campsite_test+"""</a></li>"""
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
    <h1>Campsite """+campsite_id+"""</h1>
    <iframe width="60%" height="70%" allowfullscreen style="border-style:none;" src="https://cdn.pannellum.org/2.5/pannellum.htm#panorama=https://raw.githubusercontent.com/maxfire2008/coles-bay-campsites/main/images/cb-"""+campsite_id+""".jpeg"></iframe>
</body>""")
    else:
        return HttpResponse("Error")
