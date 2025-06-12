import keras
import cv2
import numpy as np
from keras import preprocessing
from ultralytics import YOLO
from config import ASSETS_FOLDER, MODEL, YOLO_MODEL_NAME, DONE_FOLDER
import os

class ModelManager:
    def __init__(self):
        self.grape_model = keras.models.load_model(os.path.join(ASSETS_FOLDER, MODEL))
        self.yolo_model = YOLO(os.path.join(ASSETS_FOLDER, YOLO_MODEL_NAME))

    def crop_image_with_yolo(self, image):
        """Обнаруживает и вырезает виноград на изображении с помощью YOLO"""
        results = self.yolo_model(image)
        pathes = []
        i = 0
        
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0]) 
                cropped_image = image[y1:y2, x1:x2]
                output_name = f"{i}_name.jpg"
                pathes.append((os.path.join(DONE_FOLDER, output_name), cropped_image))
                i += 1
                
        return pathes

    def predict_for_image(self, image_path):
        """Предсказывает класс винограда по изображению"""
        img = preprocessing.image.load_img(image_path, target_size=(224, 224))
        img_array = preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        return self.grape_model.predict(img_array)

    def process_image(self, image_path, bind_class_model):
        """Обрабатывает изображение и возвращает предсказание"""
        image = cv2.imread(image_path)
        self.cropped_images = self.crop_image_with_yolo(image)
        
        if not self.cropped_images:
            return None, -1
            
        predictions = []
        for path, img in self.cropped_images:
            cv2.imwrite(path, img)
            pred = self.predict_for_image(path)
            predictions.append(pred)
            
        predictions = np.array(predictions).squeeze()
        if predictions.ndim == 1:
            predictions = predictions.reshape(1, -1)
            
        max_confidences = np.max(predictions, axis=1)
        max_classes = np.argmax(predictions, axis=1)
        
        best_idx = np.argmax(max_confidences)
        best_class = bind_class_model[max_classes[best_idx]]
        best_path = self.cropped_images[best_idx]
        
        return best_path, best_class 
    

    def clear_cropped_images(self):
        if len(self.cropped_images) == 0:
            print("Error: Пустой cropped_images")
            return
         
        for path, img in self.cropped_images:
            os.remove(path)
        
        return
        