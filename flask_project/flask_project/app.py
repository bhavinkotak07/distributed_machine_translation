from flask import Flask, render_template, request, jsonify, redirect
import requests
import subprocess
import threading
import time
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
running_instances = {}
def get_my_ip():
    out = subprocess.Popen(['hostname','-I',],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    res = str(stdout )
    my_ip = res
    return my_ip

ip = get_my_ip()
ip = str(ip[2:-3])
def change_status(model):
    print('Model:', model)
    time.sleep(10)
    model_status[model] = 'DEPLOYED'

def deploy_model(model_name, instances):
    out = subprocess.Popen(['bash','deploy_model.sh', model_name, instances],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    res = str(stdout )
    print('Model status:', model_status)
    model_status[model_name] = 'DEPLOYED'
    running_instances[model_name] = instances
    print('Model status:', model_status)
    return res
def stop_model(model_name):
    out = subprocess.Popen(['bash','stop_model.sh', model_name],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    res = str(stdout )
    model_status[model_name] = 'STOPPED'

    print('Model status:', model_status)
    return res


app = Flask(__name__)
@app.route("/get_ip")
def get_ip():
    return ip

@app.route('/api/stop', methods=['GET','POST'])
def stop():
    if request.method == 'GET':
        model = request.args.get('button_id')
        #instances = request.args.get('instances')
    else:
        model = request.form['button_id']
    model_status[model] = 'STOPPING' 
    running_instances[model] = 0
    t = threading.Thread(target=stop_model, args=[model] )
    t.start()
    return redirect("/show_models")
    #return redirect("/show_models")

@app.route('/api/deploy', methods=['GET', 'POST'])
def deploy():
    #res = deploy_model(model)
    if request.method == 'GET':
        model = request.args.get('button_id')
        instances = request.args.get('instances')
        
    else:
        model = request.form['button_id']
        instances = request.form['instances']
    #return str(model + "|" + instances)

    model_status[model] = 'IN PROGRESS' 

    t = threading.Thread(target=deploy_model, args=[model,instances] )
    t.start()
    return redirect("/show_models")
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        from_language = request.form['from_language']
        to_language = request.form['to_language']
        global counter
        key = from_language+"|"+to_language
        val = 'model' + str(counter)
        url_mapper[key] = val
        counter += 1
        f = request.files['file']
        f.save(UPLOAD_FOLDER + val + ".zip")
        model_status[val] = 'UPLOADED' 
        running_instances[val] = "0" 
        return redirect("/show_models")
    else:
        #return "admin"
        return render_template('admin.html')  
@app.route('/show_models')
def show_models():
    return render_template('show_models.html')
@app.route('/api/list_models')
def list_models():
    result = []
    for key in url_mapper:
        data = {}
        model_name = url_mapper[key]
        data["model"] = model_name
        data["from_language"], data["to_language"] = key.split("|")
        data["status"] = model_status[model_name]
        data["instances"] = running_instances[model_name]
        result.append(data)
    return jsonify(result)
@app.route('/models/<model_name>')
def check_deployment(model_name):
    reply = requests.get('http://' + model_name + ":8080/get_ip")  
    return reply.text
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/process1', methods=['POST','GET'])
def process1():
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
    key = from_language + "|" + to_language
    if key not in url_mapper:
        return 'Not found'
    data = { 'paragraph':input_val }
    print('Data:',data)
    end_point = "http://" + url_mapper[key] + ":8080/api/translate/"
    #return str(end_point)
    request_reply = requests.post(url=end_point, data=data)
    output_val = request_reply.text
    print(output_val)

    return output_val
    #return jsonify({'output_val' : output_val})

if __name__ == "__main__":
    
    app.run(debug=True,host='0.0.0.0', port=5000)
