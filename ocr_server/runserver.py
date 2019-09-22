from flask import Flask, jsonify, request
from wrapper import ButtonOCR


if __name__ == "__main__":
  ocr = ButtonOCR()
  
  app = Flask(__name__)
  
  @app.route("/", methods=["GET"])
  def index():
    return jsonify({"This is": "the index page."})
  
  
  @app.route("/predict", methods=["POST"])
  def predict():
    img_path = request.form.get("img_path")
    
    res = ocr.button_predict(img_path)
    return jsonify(res)
    
  host_addr = "127.0.0.1"
  port_num = "8080"
  
  app.run(host=host_addr, port=port_num)
  
    
