import os
from PIL import Image
import numpy as np
import cv2
import pickle 

BASE_DIR=os.path.dirname(os.path.abspath(__file__)) # find the directory
image_dir =os.path.join(BASE_DIR,"images")
face_cascade =cv2.CascadeClassifier('data/haarcascade_frontalface_alt2.xml')

recognizer =cv2.face.LBPHFaceRecognizer_create()

x_train=[]
y_labels=[]
current_id=0
label_ids ={}

for root,dirs,files in os.walk(image_dir):
	for file in files:
		if file.endswith("png") or file.endswith("jpg") or file.endswith("jfif"):
			path= os.path.join(root,file)
			label =os.path.basename(root).replace(" ","-").lower()
			print(label,path)
			if not label in label_ids:
				
				label_ids[label]=current_id
				current_id+=1

			id_ = label_ids[label]
			#print(label_ids)
			#x_train.append(path)
			#y_labels.append(label)
			pil_image=Image.open(path).convert("L") #grayscale
			size=(550,550)
			final_image=pil_image.resize(size,Image.ANTIALIAS)
			image_array = np.array(final_image)
			#print(image_array)
			faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5,minNeighbors=5)

			for (x ,y,w,h) in faces:
				roi = image_array[y:y+h,x:x+w]
				x_train.append(roi )
				y_labels.append(id_)


#print(x_train)
#print(y_labels)

with open("label.pickle",'wb') as f:
	pickle.dump(label_ids,f)

recognizer.train(x_train,np.array(y_labels))
recognizer.save("trainer.yml")
