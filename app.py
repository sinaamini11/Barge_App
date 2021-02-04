from flask import Flask, render_template, request, redirect
from utils import plot_barge
import numpy as np
import os

app = Flask(__name__)

app.vars = dict()

@app.route('/')
def start():
    return render_template('index.html')
@app.route('/index', methods=['POST'])
def index():
        #request was a POST
    app.vars['loaded_ft1'] = int(request.form['loaded_ft1'])
    app.vars['loaded_in1'] = int(request.form['loaded_in1'])
    app.vars['loaded_dec1'] = round(app.vars['loaded_ft1'] + app.vars['loaded_in1']/12.0, 1)

    app.vars['unloaded_ft1'] = int(request.form['unloaded_ft1'])
    app.vars['unloaded_in1'] = int(request.form['unloaded_in1'])
    app.vars['unloaded_dec1'] = round(app.vars['unloaded_ft1'] + app.vars['unloaded_in1']/12.0, 1)

    app.vars['loaded_ft2'] = int(request.form['loaded_ft2'])
    app.vars['loaded_in2'] = int(request.form['loaded_in2'])
    app.vars['loaded_dec2'] = round(app.vars['loaded_ft2'] + app.vars['loaded_in2']/12.0, 1)

    app.vars['unloaded_ft2'] = int(request.form['unloaded_ft2'])
    app.vars['unloaded_in2'] = int(request.form['unloaded_in2'])
    app.vars['unloaded_dec2'] = round(app.vars['unloaded_ft2'] + app.vars['unloaded_in2']/12.0, 1)

    app.vars['loaded_ft3'] = int(request.form['loaded_ft3'])
    app.vars['loaded_in3'] = int(request.form['loaded_in3'])
    app.vars['loaded_dec3'] = round(app.vars['loaded_ft3'] + app.vars['loaded_in3']/12.0, 1)

    app.vars['unloaded_ft3'] = int(request.form['unloaded_ft3'])
    app.vars['unloaded_in3'] = int(request.form['unloaded_in3'])
    app.vars['unloaded_dec3'] = round(app.vars['unloaded_ft3'] + app.vars['unloaded_in3']/12.0, 1)

    app.vars['loaded_ft4'] = int(request.form['loaded_ft4'])
    app.vars['loaded_in4'] = int(request.form['loaded_in4'])
    app.vars['loaded_dec4'] = round(app.vars['loaded_ft4'] + app.vars['loaded_in4']/12.0, 1)

    app.vars['unloaded_ft4'] = int(request.form['unloaded_ft4'])
    app.vars['unloaded_in4'] = int(request.form['unloaded_in4'])
    app.vars['unloaded_dec4'] = round(app.vars['unloaded_ft4'] + app.vars['unloaded_in4']/12.0, 1)

    app.vars['loaded_fb'] = np.mean([app.vars['loaded_dec1'],
                                     app.vars['loaded_dec2'],
                                     app.vars['loaded_dec3'],
                                     app.vars['loaded_dec4']])

    app.vars['unloaded_fb'] = np.mean([app.vars['unloaded_dec1'],
                                       app.vars['unloaded_dec2'],
                                       app.vars['unloaded_dec3'],
                                       app.vars['unloaded_dec4']])

    app.vars['material'] = request.form['material']

    app.vars['barge_name'] = request.form['barge_name']

    plot = plot_barge(barge=app.vars['barge_name'],
                       loaded_fb=app.vars['loaded_fb'],
                       unloaded_fb=app.vars['unloaded_fb'],
                       material=app.vars['material'])

    return render_template('result.html', plot=plot)

# @app.route('/about')
# def about():
#   return render_template('about.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    #app.run(debug=True)
