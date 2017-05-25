# -*- coding: utf-8 -*-
"""
Created on Sun May 21 13:40:33 2017

@author: adam
"""

from flask import Flask, render_template,jsonify
from flask import abort
from flask import request
from flask import make_response, send_file
import os
from werkzeug.utils import secure_filename
import get_shirt2
import cv2
from flask import send_from_directory
app = Flask(__name__)
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]
#==============================================================================
# @app.route('/tes',methods=['GET'])
# def index():
#     #tv_show = "The office"
#     return jsonify({'tasks': tasks})
#     #return render_template("index.html",show = tv_show)
#==============================================================================
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_tasks(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.route('/task', methods=['GET'])
def get_tasks2():
    return jsonify({'tasks': tasks})

@app.route('/hello')
#http://127.0.0.1:5000/hello?name=Luis&class=2a
def api_hello():
    if 'name' in request.args:
        a =  'Hello ' + request.args['name']
    if 'class' in request.args:
        b = ' from  ' + request.args['class']
    return a + b

@app.route('/image')
#http://127.0.0.1:5000/image?image_cust=tes_image10.jpg&image_sell=tes_image7.jpg
def image():
    upload_folder_path = os.path.join(os.getcwd(),'upload')
    app.config['UPLOAD_FOLDER'] = upload_folder_path
    base_path = app.config['UPLOAD_FOLDER']
    #print upload_folder_path
    image_cust_address = request.args['image_cust']
    _file = request.args['image_cust']
    _filename = secure_filename(_file.filename)
    print "upload_folder_path",upload_folder_path
    if _filename != '':
        filename_path = os.path.join(base_path, _filename)
        _file.save(filename_path)
    #image_sell_address = request.args['image_sell']
    #print 'image_cust_address ',image_cust_address
    #print 'image_sell_address ',image_sell_address
    #print "upload_folder_path",upload_folder_path
    return 'image_cust_address ' + image_cust_address +" upload_folder_path "+ upload_folder_path

@app.route('/upload')
def upload():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   upload_folder_path = os.path.join(os.getcwd(),'upload')
   output_folder_path = os.path.join(os.getcwd(),'output')
   app.config['UPLOAD_FOLDER'] = upload_folder_path
   base_path = app.config['UPLOAD_FOLDER']
   if request.method == 'POST':
      _file_customer = request.files['file_customer']
      _filename_customer = secure_filename(_file_customer.filename)
      filename_customer_path = os.path.join(base_path, _filename_customer)
      _file_customer.save(filename_customer_path)
      
      _file_seller = request.files['file_seller']
      _filename_seller = secure_filename(_file_seller.filename)
      filename_seller_path = os.path.join(base_path,_filename_seller)
      _file_seller.save(filename_seller_path)
      
#==============================================================================
#       image = [
#               {
#                   'title' : filename_customer_path        
#               },
#              {
#                   'title' : filename_seller_path       
#               }
#               ]
#==============================================================================
      im_output = get_shirt2.main(filename_customer_path,filename_seller_path)
      im_name = 'im_output.jpg'
      output = os.path.join(output_folder_path,im_name)
      cv2.imwrite(output,im_output)
      #response = make_response(image_binary)
      im_name = [
              {
                'im_out_address' : 'http://127.0.0.1/BL_image/output/im_output.jpg'
                      }
              ]
      #return send_file(output, mimetype='image/gif')
      return jsonify(im_name)
  
@app.route("/output/<path:path>")
def images(path):
    #generate_img(path)
    fullpath = "D:\works\BL_image\output\im_output.jpg"
    im = cv2.imread(fullpath)
    return response


if __name__ == '__main__':
    app.run(debug=True)