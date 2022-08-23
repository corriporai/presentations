import glob
import re


repeats = []
strava_dates = {}
for line in open('datas.txt'):
    strava_id, date = line.strip().split('\t')
    if date not in repeats:
        repeats.append(date)
    else:
        print(date, 'repeated')
    strava_dates[strava_id] = date


for file in glob.glob('*.gpx'):
    strava_id = (re.search(r'\d+', file).group(0))
    content = open(file).read()
    content = content.replace('1970-01-01',(strava_dates[strava_id]))
    new = open('adjusted/' + file, 'w')
    new.write(content)
    new.close()