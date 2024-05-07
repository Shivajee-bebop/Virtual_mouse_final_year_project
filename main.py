from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_main')
def run_main():
    subprocess.Popen(['python', 'virtualmouse.py'])
    return 'Virtual Mouse is running!'

@app.route('/run_volume_control')
def run_volume_control():
    subprocess.Popen(['python', 'volControl.py'])
    return 'Volume Control is running!'

if __name__ == '__main__':
    app.run(debug=True)
