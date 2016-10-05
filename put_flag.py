import datetime

when_hour = [6, 8, 14, 19]
how_long = 300
h = datetime.datetime.now().hour

if h in when_hour:
    with open('/opt/cyrkulacja/run/pompuj', 'w') as f:
        f.write(str(how_long))

