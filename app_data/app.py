from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        routine = request.form['routine']
        input_params = {
            'prog': routine,
            'set_temp': request.form['set_temp'],
            'init_temp': request.form['init_temp'],
            'target_temp': request.form['target_temp'],
            'rise_rate': request.form['rise_rate'],
            'hold_time': request.form['hold_time'],
            'fall_rate': request.form['fall_rate'],
            'end_temp': request.form['end_temp']
        }

        # Run the provided Python script as a subprocess
        output = subprocess.check_output(['thermobath_v3.py'], input=str(input_params), text=True)

        return render_template('index.html', output=output)

    return render_template('index.html', output=None)

if __name__ == '__main__':
    app.run(debug=True)
