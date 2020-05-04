from flask import Flask, render_template, request, jsonify
import requests
import subprocess
def get_url():

    out = subprocess.Popen(['minikube','service','list','|','grep', 'mt2'],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    res = str(stdout)
    #print(res.split('\\n') )
    url = None
    for line in res.split('\\n'):
        #print(line)
        if 'mt2' in line:
            url = line.split('|')[4].strip()
            print(url )
    return url
url = None
#url = get_url()
if url == None:
    url = "http://mt2:8080"
url += "/api/translate/"
print(url)


app = Flask(__name__)

    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST','GET'])
def process():
    from_language = request.form['from_language']
    to_language = request.form['to_language']
    input_val = request.form['input_val']

    request_reply = requests.get(url + input_val)
    output_val = request_reply.text
    print(output_val)

    return jsonify({'output_val' : output_val})

if __name__ == "__main__":
    
    app.run(debug=True,host='0.0.0.0', port=5000)
