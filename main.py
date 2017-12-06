from flask import Flask, render_template, send_file
from yr.libyr import Yr
import codecs
import subprocess

import datetime

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
from reportlab.graphics.shapes import Image, Drawing
from reportlab.platypus.flowables import Image

app = Flask(__name__)

# @app.route('/')
# def show_svg():
#     print('aaaa')
#
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


def _generate_svg():
    '''
    Modifies the svn with the information we want
    :return:
    '''
    print('_generate_svg')

    today = datetime.datetime.now().strftime("%B %d - kl %H:%M:%s")

    # Open SVG to process
    output = codecs.open('static/templates/landscape.svg', 'r', encoding='utf-8').read()

    # Insert icons and temperatures
    output = output.replace('Today', today)
    print(today)

    # Write output
    filename = 'static/after-weather.svg'
    codecs.open(filename, 'w', encoding='utf-8').write(output)
    return filename

@app.route('/index.png')
@app.route('/weather-script-output.png')
def show_png():
    svg = _generate_svg()

    # Disse som brukes
    drawing = svg2rlg(svg)
    renderPM.drawToFile(drawing, "static/image.png", fmt='png')


    # Rotate
    #drawing.translate(600, 0)
    drawing.translate(0, 800)
    drawing.rotate(-90)
    d = Drawing(600, 800)
    d.add(drawing)
    drawing = d


    renderPM.drawToFile(drawing, "static/image.png", fmt='png')

    # pngcrush -q -c 0 weather-processed.png weather-script-output.png > /dev/null 2>&1
    subprocess.call('/usr/local/bin/pngcrush -q -c 0 static/image.png static/image.png > /dev/null 2>&1', shell=True)

    return send_file("static/image.png", mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
