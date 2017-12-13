from flask import Flask, render_template, send_file, request

from yr.libyr import Yr
import codecs
import subprocess

#import datetime
from datetime import datetime, timedelta

import dateutil.parser

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from reportlab.graphics.shapes import Image, Drawing
from reportlab.platypus.flowables import Image

import json

app = Flask(__name__)

# @app.route('/')
# def show_template():
#     return render_template('show_html.html', entries=None)
#
#     print('aaaa')
#     today = datetime.datetime.now().strftime("%B %d - kl %H:%M")
#
#     # Open SVG to process
#     output = codecs.open('static/templates/landscape.svg', 'r', encoding='utf-8').read()
#
#     # Insert icons and temperatures
#     output = output.replace('Today', today)
#     print(today)
#
#     # Write output
#     codecs.open('static/after-weather.svg', 'w', encoding='utf-8').write(output)
#
#     # weather = Yr(location_name='Norge/Telemark/Skien/Skien')
#     # now = weather.now(as_json=True)
#     # weather = Yr(location_name='Norge/Telemark/Skien/Skien', forecast_link='forecast_hour_by_hour')
#     # for forecast in weather.forecast(as_json=True):
#     #     print(forecast)
#     # print(now)
#
#     return render_template('show_svg.html', entries=None)
#
#     return 'Hello World from Docker! jaaaa'

def _find_time(d):
    '''
    Find the three hours we display wether for
    :return:
    '''
    c = []
    h = d.strftime("%H")
    h = int(h)
    print(h, 'h')

    if (h > 21):
        c = [0,6,12]
    elif (h > 18):
        c = [21, 3, 9]
    elif (h > 15):
        c = [18, 0, 6]
    elif (h > 12):
        c = [18, 0, 6]
    elif (h > 9):
        c = [12, 18, 0]
    elif (h > 6):
        c = [9, 15, 21]
    elif (h > 3):
        c = [6, 12, 18]
    elif (h >= 0):
        c = [3, 9, 15]
    return c


def _generate_svg():
    '''
    Modifies the svn with the information we want
    :return:
    '''
    print('func _generate_svg')

    # @todo Add timezone as setting
    d = datetime.now() + timedelta(hours=1)
    today = d.strftime("%A %d.%m - kl %H:%M:%S")

    # Open SVG to process
    output = codecs.open('static/templates/landscape.svg', 'r', encoding='utf-8').read()

    # Insert icons and temperatures
    output = output.replace('Today', today)

    # Set times
    t = _find_time(d)
    print('t', t)
    output = output.replace('Time_0', "%i%s" % ((t[0]),':00'))
    output = output.replace('Time_1', "%i%s" % ((t[1]),':00'))
    output = output.replace('Time_2', "%i%s" % ((t[2]),':00'))

    forecasts = []
    #weather = Yr(location_name='Norge/Telemark/Skien/Skien')
    #now = weather.now(as_json=True)
    weather = Yr(location_name='Norge/Telemark/Skien/Skien', forecast_link='forecast_hour_by_hour')
    for forecast in weather.forecast(as_json=True):
        f = json.loads(forecast)
        yourdate = dateutil.parser.parse(f['@from'])
        #print('aaa2', yourdate.hour)

        if yourdate.hour in t:
            forecasts.append(f)

    # Insert temperature
    output = output.replace('Temp_0', "%s%s" % (forecasts[0]['temperature']['@value'], '°C'))
    output = output.replace('Temp_1', "%s%s" % (forecasts[1]['temperature']['@value'], '°C'))
    output = output.replace('Temp_2', "%s%s" % (forecasts[2]['temperature']['@value'], '°C'))
    print('forecasts', forecasts[2])

    # Insert symbols
    n = forecasts[0]['symbol']['@number']
    n = str(n).zfill(2)
    s = "static/symbols/%s.svg" % (n)
    symbol = codecs.open(s, 'r', encoding='utf-8').read()
    symbol = symbol.replace('viewBox="0 0 100 100"', "%s" % ('viewBox="0 0 800 600"'))
    output = output.replace('<text>Icon_1</text>', "%s" % (symbol))
    print('s', s)


    n = forecasts[1]['symbol']['@number']
    n = str(n).zfill(2)
    s = "static/symbols/%s.svg" % (n)
    symbol = codecs.open(s, 'r', encoding='utf-8').read()
    symbol = symbol.replace('viewBox="0 0 100 100"', "%s" % ('viewBox="0 0 800 600"'))
    output = output.replace('<text>Icon_2</text>', "%s" % (symbol))
    print('s', s)

    n = forecasts[2]['symbol']['@number']
    n = str(n).zfill(2)
    s = "static/symbols/%s.svg" % (n)
    symbol = codecs.open(s, 'r', encoding='utf-8').read()
    symbol = symbol.replace('viewBox="0 0 100 100"', "%s" % ('viewBox="0 0 800 600"'))
    output = output.replace('<text>Icon_3</text>', "%s" % (symbol))
    print('s', s)

    #output = output.replace('<text>Icon_1</text>', "%s" % (symbol))

    # for idx, val in enumerate(t):
    #     print(idx, val)
    print('find time, ', t)



    # Write output
    filename = 'static/after-weather.svg'
    codecs.open(filename, 'w', encoding='utf-8').write(output)
    return filename

@app.route('/index.png')
@app.route('/weather-script-output.png')
def show_png():
    debug = request.args.get('debug', '')

    svg = _generate_svg()

    # Disse som brukes
    drawing = svg2rlg(svg)
    renderPM.drawToFile(drawing, "static/image.png", fmt='png')


    # Rotate
    if not debug:
        drawing.translate(0, 800)
        drawing.rotate(-90)
        d = Drawing(600, 800)
        d.add(drawing)
        drawing = d

    renderPM.drawToFile(drawing, "static/image.png", fmt='png')

    # Make png compatible with Kindle
    subprocess.call('/usr/local/bin/pngcrush -q -c 0 static/image.png static/image2.png > /dev/null 2>&1', shell=True)

    return send_file("static/image2.png", mimetype='image/png')

@app.route('/weather.svg')
def show_svg():
    debug = request.args.get('debug', '')

    filename = _generate_svg()

    return send_file(filename, mimetype='image/svg+xml')

@app.route('/')
def show_index():
    return render_template('show_html.html', entries=None)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
