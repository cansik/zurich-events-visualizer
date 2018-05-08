import urllib
import json
from datetime import datetime, timedelta

from gmplot import gmplot
import random


def load_events(date):
    # 1525903200
    url = "https://www.zuerich.com/en/filter-page/events-for-date?date=%s&id=2460" % date.strftime('%s')
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return data


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def save_json(file_name, data):
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)


def load_json(file_name):
    with open(file_name) as f:
        return json.load(f)


radius = 50
load_data = False

if load_data:
    start_date = datetime(2018, 1, 1)
    end_date = datetime(2018, 12, 31)

    events = []

    for d in date_range(start_date, end_date):
        print("loading events for %s..." % d.strftime('%d.%m %Y'))
        events += load_events(d)

    print("saving events...")
    save_json('events_2018.json', events)

events = load_json('events_2018.json')

print("converting %s events..." % len(events))
# locations = map(lambda e: (e["latitude"], e["longitude"]), events)
locations = filter(lambda e: "latitude" in e and "longitude" in e, events)
locations = map(lambda e: (e["latitude"] + random.random() / 10000, e["longitude"] + random.random() / 10000), locations)

print("event count: %s" % len(locations))

events_lats, events_lons = zip(*locations)

# create plot
print("creating heatmap...")
gmap = gmplot.GoogleMapPlotter(47.3769, 8.5417, 13)
gmap.heatmap(events_lats, events_lons, threshold=radius, radius=radius, gradient=None, opacity=0.6, dissipating=True)
# gmap.scatter(events_lats, events_lons, '#3B0B39', size=40, marker=False)
gmap.draw("events_heatmap.html")

print("done!")
