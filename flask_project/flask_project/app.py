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

url_mapper = {}
counter = 0

UPLOAD_FOLDER="uploads/"

model_status = {}

def deploy_model(model_name):
    out = subprocess.Popen(['bash','deploy_model.sh',model_name],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    res = str(stdout )
    return res
app = Flask(__name__)

@app.route('/deploy/<model>')
def deploy(model):
    res = deploy_model(model)
    model_status[model] = 'DEPLOYED'   

    
    return res
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        from_language = request.form['from_language']
        to_language = request.form['to_language']
        global counter
        key = from_language+":"+to_language
        val = 'model' + str(counter)
        url_mapper[key] = val
        counter += 1
        f = request.files['file']
        f.save(UPLOAD_FOLDER + val + ".zip")
        model_status[key] = 'UPLOADED'  
        return 'Uploaded successfully'
    else:
        #return "admin1"
        return render_template('admin.html')  
@app.route('/list_models')
def list_models():
    return str(url_mapper)
@app.route('/models/<model_name>')
def check_deployment(model_name):
    reply = requests.get('http://' + model_name + ":8080/dir")  
    return reply.text
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/process_test', methods=['POST','GET'])
def process_test():
    from_language = request.form['from_language']
    to_language = request.form['to_language']
    input_val = request.form['input_val']

    data = { 'paragraph':input_val }
    print('Data:',data)
    request_reply = requests.post(url=url, data=data)
    #request_reply = requests.get(url + input_val)
    output_val = request_reply.text
    print(output_val)
    return jsonify({'output_val' : output_val})

@app.route('/process', methods=['POST','GET'])
def process():
    global counter
    from_language = request.form['from_language']
    to_language = request.form['to_language']
    input_val = request.form['input_val']
    key = from_language + ":" + to_language
    if key not in url_mapper:
        return 'Not found'
    data = { 'paragraph':input_val }
    print('Data:',data)
    end_point = "http://" + url_mapper[key] + ":8080/api/translate/"
    #return str(end_point)
    request_reply = requests.post(url=end_point, data=data)
    #request_reply = requests.get(url + input_val)
    output_val = request_reply.text
    print(output_val)

    return jsonify({'output_val' : output_val})

if __name__ == "__main__":
    
    app.run(debug=True,host='0.0.0.0', port=5000)
