import argparse
import os
import random
import tensorflow as tf
import re
import subprocess
import pyonmttok
import threading
import flask
from flask import request, jsonify
# TensorFlow Addons lazily loads custom ops. So we call the op with invalid inputs
# just to trigger the registration.
# See also: https://github.com/tensorflow/addons/issues/1151.
import tensorflow_addons as tfa
try:
    tfa.seq2seq.gather_tree(0, 0, 0, 0)
except tf.errors.InvalidArgumentError:
    pass






class EnDeTranslator(object):
  __shared_instance = None

  @staticmethod
  def getInstance(export_dir):
    """Static Access Method"""
    if EnDeTranslator.__shared_instance == None:
        
      __shared_instance = EnDeTranslator(export_dir) 
    return EnDeTranslator.__shared_instance  

  def __init__(self, export_dir):
    if EnDeTranslator.__shared_instance != None: 
      raise Exception ("This class is a singleton class !") 
    else: 

      imported = tf.saved_model.load(export_dir)
      self._translate_fn = imported.signatures["serving_default"]
      sp_model_path = os.path.join(export_dir, "assets.extra", "wmtende.model")
      self._tokenizer = pyonmttok.Tokenizer("none", sp_model_path=sp_model_path)
      EnDeTranslator.__shared_instance = self

  def translate(self, texts):
    """Translates a batch of texts."""
    inputs = self._preprocess(texts)

    outputs = self._translate_fn(**inputs)
    return self._postprocess(outputs)

  def _preprocess(self, texts):
    all_tokens = []
    lengths = []
    max_length = 0
    for text in texts:
      tokens, _ = self._tokenizer.tokenize(text)
      length = len(tokens)
      all_tokens.append(tokens)
      lengths.append(length)
      max_length = max(max_length, length)
    for tokens, length in zip(all_tokens, lengths):
      if length < max_length:
        tokens += [""] * (max_length - length)

    inputs = {
        "tokens": tf.constant(all_tokens, dtype=tf.string),
        "length": tf.constant(lengths, dtype=tf.int32)}
    return inputs

  def _postprocess(self, outputs):
    texts = []
    for tokens, length in zip(outputs["tokens"].numpy(), outputs["length"].numpy()):
      tokens = tokens[0][:length[0]].tolist()
      texts.append(self._tokenizer.detokenize(tokens))
    return texts



#parser = argparse.ArgumentParser(description="Translation client example")
#parser.add_argument("export_dir", help="Saved model directory")
#args = parser.parse_args()

r = random.randrange(1, 100)



def get_my_ip():

    out = subprocess.Popen(['hostname','-I',],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    res = str(stdout )
    my_ip = res
    return my_ip

ip = get_my_ip()
ip = str(ip[2:-3])
translator = None
def load_model():
    global translator
    translator = EnDeTranslator.getInstance("averaged-ende-export500k-v2")




app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route("/get_ip")
def get_ip():
    return ip

@app.route('/dir')
def dir():
  
  return str(os.listdir(os.getcwd()))

@app.route('/')
def index():
  
  return str(r)
@app.route('/api/translate/<paragraph>', methods=['GET'])
def get_translation_english_to_german(paragraph):
  translator = EnDeTranslator.getInstance("averaged-ende-export500k-v2")

  print("API called:", paragraph)
  
  output = translator.translate([paragraph])
  res = { }
  res['output_val'] = str('\n'.join(output))
  res['ip_address'] = ip
  return jsonify(res)  

@app.route('/api/translate/', methods=['POST'])
def post_translation_english_to_german():
  paragraph = request.form['paragraph']

  print("API called:", paragraph)
  inputs = re.split('\.|\n',paragraph)
  #inputs = re.split('\n',paragraph)
  inputs = [i for i in inputs if i not in ['', ' ']] 

  print('Inputs:',inputs)
  global translator
  translator = EnDeTranslator.getInstance("averaged-ende-export500k-v2")
  output = translator.translate(inputs )
  res = { }
  res['output_val'] = str('\n'.join(output))
  res['ip_address'] = ip
  return jsonify(res)


if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=8080)


