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
    <title>Coles Bay Campsites</title>
    <style>
        h1 {
            font-family: sans-serif;
        }
        p {
            font-family: sans-serif;
        }
    </style>
</head>
<body>
    <h1>Coles Bay Campsites</h1>
    <ul>
        """+campsites+"""
    </ul>
</body>""")

