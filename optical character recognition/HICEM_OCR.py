import cv2
import csv
import pytesseract
import os
import mysql.connector
import pycountry
import argparse
import subprocess
from langdetect import detect_langs

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'


# parser for use in command line; command should include -c followed by the path to the collection 
parser = argparse.ArgumentParser()
parser.add_argument('-c', '--collection', help='path to collection')
args = parser.parse_args()

# checks to see if directory is passed and that it is in fact a directory
if args.collection and os.path.isdir(args.collection):
    path = args.collection

    
# checks for all the files in passed directory, then all images in those files
path = os.path.abspath(path)
files = os.listdir(path)
image_paths = [os.path.join(path, file) for file in files if file.endswith(('.jpg', '.jpeg', '.tif'))]

# loop through all images, cv to read in image, pytesseract to produce string, pycountry to identify language; if language confidence is above 0.4, enter the image hocr to database
for image_path in image_paths:
   
    img = cv2.imread(image_path,0)
    thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(thresh)
          
    try:
        detected_lang = detect_langs(text)
        print(detected_lang[0].lang)
    
        lang = pycountry.languages.lookup(detected_lang[0].lang)
        confidence = float(detected_lang[0].prob)
        print(lang.alpha_3)
        print(confidence)
        
    except Exception as e:
        print(e)
        continue
    
    if lang.alpha_3 and float(confidence) > 0.4:
        image_basename = os.path.basename(image_path)
        image_basename_no_ext = os.path.splitext(image_basename)[0]
        print(image_path)
        print(os.path.splitext(image_path)[0])
        subprocess.call(['tesseract', image_path, os.path.splitext(image_path)[0], '-l', lang.alpha_3, 'hocr'], shell=True)
        
        try:
            hocr_file = (os.path.splitext(image_path)[0]) + '.hocr'
            htext = open(hocr_file, "r", encoding="utf-8")
            hocr_text = htext.read()
            
            conn = mysql.connector.connect(host="<enter hostname>", user="<enter user>", password="<enter password>", database="<enter database>")
            
            c = conn.cursor()
        
            c.execute("INSERT INTO <table> VALUES (%s,%s,%s,%s,%s,%s)",(image_path, image_basename, lang.alpha_3, confidence, text, hocr_text))
        except Exception as e:
            print(e)
            continue

        print(f"Current file: {image_basename}")
        conn.commit()
        conn.close()



