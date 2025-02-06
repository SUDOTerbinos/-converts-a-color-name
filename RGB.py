from flask import Flask, render_template, request
from PIL import Image
import numpy as np
import cv2
from colormap import rgb2hex, hex2rgb, name2rgb

app = Flask(__name__)

def get_dominant_color(image_path):
    image = Image.open(image_path)
    image = image.resize((50, 50))  
    pixels = np.array(image).reshape(-1, 3)  
    avg_color = np.mean(pixels, axis=0).astype(int)  
    return tuple(avg_color)

@app.route('/', methods=['GET', 'POST'])
def index():
    rgb_result = None
    if request.method == 'POST':
        if 'color_name' in request.form and request.form['color_name']:
            color_name = request.form['color_name'].lower()
            try:
                rgb_result = name2rgb(color_name)
            except:
                rgb_result = "Invalid color name"
        
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                image_path = "static/uploaded_image.jpg"
                image.save(image_path)
                rgb_result = get_dominant_color(image_path)
    
    return render_template('index.html', rgb_result=rgb_result)

if __name__ == '__main__':
    app.run(debug=True)
