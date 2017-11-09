from flask import Flask, render_template, send_file
from yr.libyr import Yr
import codecs

import datetime

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

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
    print('_generate_svg')

    today = datetime.datetime.now().strftime("%B %d - kl %H:%M")

    # Open SVG to process
    output = codecs.open('static/templates/landscape.svg', 'r', encoding='utf-8').read()

    # Insert icons and temperatures
    output = output.replace('Today', today)
    print(today)

    # Write output
    filename = 'static/after-weather.svg'
    codecs.open(filename, 'w', encoding='utf-8').write(output)
    return filename

@app.route('/')
def show_png():
    svg = _generate_svg()

    #drawing = svg2rlg("static/after-weather.svg")
    drawing = svg2rlg(svg)
    #renderPDF.drawToFile(drawing, "static/after.pdf")
    renderPM.drawToFile(drawing, "static/image.png")

    #return render_template('show_image.html', entries=None)
    return send_file("static/image.png", mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
