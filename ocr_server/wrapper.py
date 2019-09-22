from __future__ import print_function
import os
import cv2
import imageio
import PIL.Image
import PIL.ImageOps as ImageOps
import numpy as np
import tensorflow as tf
from button_detection import ButtonDetector
from character_recognition import CharacterRecognizer
import time


def button_candidates(boxes, scores, image):
  img_height = image.shape[0]
  img_width = image.shape[1]

  button_scores = []
  button_patches = []
  button_positions = []

  for box, score in zip(boxes, scores):
    if score < 0.5: continue

    y_min = int(box[0] * img_height)
    x_min = int(box[1] * img_width)
    y_max = int(box[2] * img_height)
    x_max = int(box[3] * img_width)

    button_patch = image[y_min: y_max, x_min: x_max]
    button_patch = cv2.resize(button_patch, (180, 180))

    button_scores.append(score)
    button_patches.append(button_patch)
    button_positions.append([x_min, y_min, x_max, y_max])
  return button_patches, button_positions, button_scores

def get_image_name_list(target_path):
    assert os.path.exists(target_path)
    image_name_list = []
    file_set = os.walk(target_path)
    for root, dirs, files in file_set:
      for image_name in files:
        image_name_list.append(image_name.split('.')[0])
    return image_name_list

def warm_up(detector, recognizer):
  image = imageio.imread('./test_panels/1.jpg')
  button = imageio.imread('./test_buttons/0_0.png')
  detector.predict(image)
  recognizer.predict(button)


def initialize():
  data_dir = './test_panels'
  data_list = get_image_name_list(data_dir)
  detector = ButtonDetector()
  recognizer = CharacterRecognizer(verbose=False)
  return detector, recognizer


def button_predict(img_path):
  image = PIL.Image.open(tf.gfile.GFile(img_path, 'rb'))
  t1 = time.time()
  img_thumbnail = image.thumbnail((640, 480), PIL.Image.ANTIALIAS)
  delta_w, delta_h= 640 - image.size[0], 480 - image.size[1]
  padding = (delta_w // 2, delta_h // 2, delta_w - (delta_w // 2), delta_h - (delta_h // 2))
  new_im = ImageOps.expand(image, padding)
  img_np = np.copy(np.asarray(new_im))
  
  boxes, scores, _ = detector.predict(img_np)
  button_patches, button_positions, _ = button_candidates(boxes, scores, img_np)
  results = {}
  for i, button_img in enumerate(button_patches):
      button_text, button_score, _ =recognizer.predict(button_img)
      results[button_text] = boxes[i]      
  t2 = time.time()
  
  print('Time elapsed: {:.3f}'.format(t2-t1))
  
  return results

class ButtonOCR:
  def __init__(self):
    self.detector, self.recognizer = initialize()
    warm_up(self.detector, self.recognizer)
   
  def button_predict(self, img_path):
    image = PIL.Image.open(tf.gfile.GFile(img_path, 'rb'))
    t1 = time.time()
    img_thumbnail = image.thumbnail((640, 480), PIL.Image.ANTIALIAS)
    delta_w, delta_h= 640 - image.size[0], 480 - image.size[1]
    padding = (delta_w // 2, delta_h // 2, delta_w - (delta_w // 2), delta_h - (delta_h // 2))
    new_im = ImageOps.expand(image, padding)
    img_np = np.copy(np.asarray(new_im))
    
    boxes, scores, _ = self.detector.predict(img_np)
    button_patches, button_positions, _ = button_candidates(boxes, scores, img_np)
    results = {}
    for i, button_img in enumerate(button_patches):
      button_text, button_score, _ =self.recognizer.predict(button_img)
      results[button_text] = boxes[i].tolist()    
    t2 = time.time()
    
    print('Time elapsed: {:.3f}'.format(t2-t1))
    
    return results

  
if __name__ == "__main__":

  ocr = ButtonOCR()
  
  res = ocr.button_predict('./test_panels/34.jpg')

  for key, value in res.items():
    print("{}: {}".format(key, value))
      
  
  
      




