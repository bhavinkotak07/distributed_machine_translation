import argparse
import os
import random
import tensorflow as tf

# TensorFlow Addons lazily loads custom ops. So we call the op with invalid inputs
# just to trigger the registration.
# See also: https://github.com/tensorflow/addons/issues/1151.
import tensorflow_addons as tfa
try:
    tfa.seq2seq.gather_tree(0, 0, 0, 0)
except tf.errors.InvalidArgumentError:
    pass

import pyonmttok

import flask
from flask import request, jsonify




class EnDeTranslator(object):

  def __init__(self, export_dir):
    imported = tf.saved_model.load(export_dir)
    self._translate_fn = imported.signatures["serving_default"]
    sp_model_path = os.path.join(export_dir, "assets.extra", "wmtende.model")
    self._tokenizer = pyonmttok.Tokenizer("none", sp_model_path=sp_model_path)

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


app = flask.Flask(__name__)
app.config["DEBUG"] = True
#parser = argparse.ArgumentParser(description="Translation client example")
#parser.add_argument("export_dir", help="Saved model directory")
#args = parser.parse_args()
translator = EnDeTranslator("averaged-ende-export500k-v2")

r = random.randrange(1, 100)

@app.route('/dir')
def dir():
  return str(os.listdir(os.getcwd()))

@app.route('/')
def index():
  return str(r)

@app.route('/api/translate/<paragraph>', methods=['GET'])
def get_translation_english_to_german(paragraph):

  print("API called:", paragraph)
  
  output = translator.translate([paragraph])
  return output[0]
  #return "he"

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080)



