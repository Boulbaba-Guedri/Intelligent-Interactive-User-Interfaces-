#--------------------------
# Copyright (c) 2025 Boulbaba Guedri
# Licence : MIT
# Corresponding Author : boulbaba.guedri@gmail.com (Boulbaba Guedri), rached.gharbi@ensit.rnu.tn (Rached Gharbi).
# Institutions : Laboratoire d’Ingénierie des Systèmes Industriels et des Energies Renouvelables (LISIER). Ecole Nationale Supérieure d'Ingénieurs de Tunis (ENSIT), University of Tunis, 05 Ave Taha Hussein, 1008 Montfleury Tunis, TUNISIA
# Intelligent Interactive User Interfaces (IIUI),
# Journal : The visual computer
# Year : 2025
# Title of Manuscript: Transformative User Interface Design: Enabling Intuitive Interaction through AI-Driven Image Recognition.
#--------------------------

from picamera import PiCamera
from time import sleep
import datetime
import time
import string 
import numpy as np
import cv2
import math
from math import sqrt
import numpy as np
from picamera.array import PiRGBArray
import picamera
import io
import os
import glob
from PIL import Image
from PIL import ImageTk
import shutil
import pygame
import time
import webbrowser


#************************************************************************************************************ Define the lists
#liste_x_objet = []  # cordonner premier point de contour d'un objet
#liste_y_objet = []

liste_CBO = [] # code a barre objet

liste_X_objet = [1] # 1 c'est aleatoire , cordonner click sorie 
liste_Y_objet = [1]


liste_cx_objet = [] # cordonner centroide d'un objet
liste_cy_objet = []

liste_d_objet = []   # distance entre centroide et point de contour d'objet
liste_dc_objet = []   # distance entre centroide et point click sorie
liste_z_distance= []  # z = d - dc
liste_sum1 =[]
liste_tab =[]#cette tableau pour connaitre la forme et couleur dun objet choisie par clik
#------------------------------------------------------------------------------------------------------------



 
#****************************************************************************************************************Capture par camera
#with picamera.PiCamera() as camera:
      #camera.resolution = (640,480)
      #camera.start_preview(fullscreen=False, window=(250,130,817,790))
      #time.sleep(1) #minuteur_capture
      #camera.capture('/home/pi/Desktop/Fichier_Systeme/Capture_Photos/Manuel/Manuel/Non_Traite/image.png')
      #camera.stop_preview()
#---------------------------------------------------------------------------------------------------------------- 

           
#*****************************************************************************************************************Click sourie
#----------fichier
def click_event(event, X, Y, flags, param):
    
  if event == cv2.EVENT_LBUTTONDOWN:
      liste_X_objet[0]= X
      liste_Y_objet[0]= Y
#----------fin fichier
img = cv2.imread('/home/pi/Desktop/tests-IUI/test-1/images/digital-image/test-1.jpg')
cv2.namedWindow("IUI", cv2.WINDOW_NORMAL)
cv2.resizeWindow("IUI",400,350)
cv2.imshow("IUI", img)
cv2.moveWindow("IUI",360, 200)

cv2.setMouseCallback('IUI', click_event)

cv2.waitKey(0)
cv2.destroyAllWindows()
#---------------------------------------------------------------------------------------------------------------- 


#*****************************************************************************************************************Determiner le couleur de forme
colors={"Red":[0,15],
      "Orange":[16,75],
      "Green":[76,150],#[76,135]#[76,150]
      "Blue":[151,220],#[136,260]#[151,260]
      "Purple":[220,260],
      "red":[261,360]}
        
def detect_couleur(image,cnt,colors):
    
  image_hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    
  mask = np.zeros(image_hsv.shape[:2], dtype="uint8")
    
  cv2.drawContours(mask, [cnt], -1, 255, -1)
    
  mask = cv2.erode(mask, None, iterations=2)
  cv2.imwrite('/home/pi/Desktop/tests-IUI/test-1/images/online-traitement/Mask.jpg',mask)    
  mean = cv2.mean(image_hsv, mask=mask)
     
  for color in colors:
      if int(2*mean[0]) in range(colors[color][0],colors[color][1]):
          return(color)
#---------------------------------------------------------------------------------------------------------------- 

            
#*****************************************************************************************************************Determiner la forme 

image = cv2.imread('/home/pi/Desktop/tests-IUI/test-1/images/digital-image/test-1.jpg')

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
cv2.imwrite('/home/pi/Desktop/tests-IUI/test-1/images/online-traitement/RGB to HSV.jpg',hsv)  
lower_couleur = np.array([0, 0, 84]) 
upper_couleur = np.array([255, 255, 255]) 
thresh = cv2.inRange(hsv, lower_couleur, upper_couleur)
cv2.imwrite('/home/pi/Desktop/tests-IUI/test-1/images/online-traitement/HSV to Thresh.jpg',thresh)  
kernel = np.ones((3,3), np.uint8)

opening = cv2.morphologyEx (thresh, cv2.MORPH_OPEN, kernel)
cv2.imwrite('/home/pi/Desktop/tests-IUI/test-1/images/online-traitement/Thresh to Morphology.jpg',opening)  
edges = cv2.Canny(opening, 200, 250)
cv2.imwrite('/home/pi/Desktop/tests-IUI/test-1/images/online-traitement/Morphology to Contour.jpg',edges) 
contours,h = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # claculer le nombre total d'objet dans image, soit 'contours'


for cnt in contours:
    
  perimetre=cv2.arcLength(cnt,True)
  approx = cv2.approxPolyDP(cnt,0.02*perimetre,True)
    
  area = cv2.contourArea(approx)
  area = round(area)
  
  if 0 < area < 4000:
   areaa = "1"
   areaaa = "short"
  elif 5000 < area < 10000:
   areaa = "2"
   areaaa = "average"
  else:
   areaa = "3" 
   areaaa = "tall"
   
  liste_tab.append(areaa)
   
  if (area)>650: # filtration par area (AFM), pour supprimer filtre remplacer 1000 par 1
        #print (area)
        cv2.drawContours(image,[cnt],0,(0,255,0),3)

        (x, y, w, h) = cv2.boundingRect(approx)
        #liste_x_objet.append(x)
        #liste_y_objet.append(y)
        xx = x + 90#- 7
        yy = y - 10
        color = detect_couleur(image,cnt,colors)

        if color == "Red":
         colorr = "1"
        elif color == "Orange":
         colorr = "2"
        elif color == "Green":
         colorr = "4"
        elif color == "Blue":
         colorr = "6"
        elif color == "Purple":
         colorr = "3"
        elif color == "red":
         colorr = "1"
        else:
         colorr = "0"
                
        liste_tab.append(colorr)
        
        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        liste_tab.append(cX)
        liste_cx_objet.append(cX)
        liste_cy_objet.append(cY)# c est ps impo (on peut supprimer)     
     
        if len(approx)==3:
        
           shape = "triangle"
           shapee = "1"
           liste_tab.append(shapee)

        elif len(approx)==5:       

           shape = "pentagon"
           shapee = "2"
           liste_tab.append(shapee)
           
        #elif len(approx)==4 or len(approx)==6:       

           #shape = "rectangle"
           #shapee = "3"
           #liste_tab.append(shapee)

        elif len(approx)==4:       

           shape = "rectangle"
           shapee = "3"
           liste_tab.append(shapee)

        elif len(approx)==6:       

           shape = "hexagon"
           shapee = "8"
           liste_tab.append(shapee)

        else:
           shape = "cercle"
           shapee = "6"
           liste_tab.append(shapee)
             
           
        #cv2.putText(image, str(cX)+ "," +str(cY)+ " "+color+ " " +shape+ " " +areaaa , (xx, yy), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)   
        #cv2.imwrite('/home/pi/Desktop/tests-IUI/test-1/images/online-traitement/Attribute-shapes.jpg',image)
        cv2.putText(image, " SBC:" +str(cX)+ "" +str(colorr)+ ""+ str(shapee) + "" +str(areaa) , (xx, yy), cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,255,0),1)
        cv2.imwrite('/home/pi/Desktop/tests-IUI/test-1/images/online-traitement/SBC-code.jpg',image)
#---------------------------------------------------------------------------------------------------------------- 


#*****************************************************************************************************************Suite click sourie : calcule de distances et comparer et envoyer cx et cy de forme cliquer 
     
        d=sqrt(((x-cX)**2)+((y-cY)**2)) 
        liste_d_objet.append(d) 
     
        X=liste_X_objet [0]
        Y=liste_Y_objet [0]
 
        d2=sqrt(((X-cX)**2)+((Y-cY)**2)) 
        liste_dc_objet.append(d2)

        z = d-d2 
        liste_z_distance.append(z)   

kk2=[ round(elem, 1) for elem in liste_dc_objet] 
kk3=[ round(elem, 1) for elem in liste_d_objet]
kk4=[ round(elem, 1) for elem in liste_z_distance]
kk5=[ round(elem, 1) for elem in liste_sum1]

for i in range( 0, len (kk4)): 
 if kk4 [i]>0:
   dd=kk4[i]

for i in kk2: 
 
 kk5.append(i+dd) 
 kk5=[ round(elem, 1) for elem in kk5]   

for i in range( 0, len (kk3)):
      if kk3 [i]== kk5[i]:
          
        m1 = liste_cx_objet[i]
        m2 = liste_cy_objet[i]# c est ps impo (on peut supprimer)

        for a in range( 0, len (liste_tab)): 
         if liste_tab [a] == m1:
           formee = liste_tab [a+1]# case apres  position a dans tableau cest contien code de forme
           couleuree = liste_tab [a-1]           
           areaaaa = liste_tab [a-2] 
#---------------------------------------------------------------------------------------------------------------- 


#***************************************************************************************************************Enregistrement sur fichier
        fichier = open ('/home/pi/Desktop/tests-IUI/test-1/action/Chosen-shape','a')
        
        ccc1 = str(m1)
        #ccc2 = str(m2)# c est ps impo (on peut supprimer)
 
        if   areaaaa == "1"  :
            areaaaaa = "Short"
        elif areaaaa == "2"  :
            areaaaaa = "Average"
        elif areaaaa == "3"  :
            areaaaaa = "Tall"
 
          
        if   formee == "1"  :
            formeee = "Triangle"
        elif formee == "3"  :
            formeee = "Rectangle"
        elif formee == "2"  :
            formeee = "pentagon"
        elif formee == "6"  :
            formeee = "Cercle"
        elif formee == "8"  :
            formeee = "Hexagon"

            
        if   couleuree == "1"  :
            couleureee = "Rouge"
        elif couleuree == "2"  :
            couleureee = "Orange"
        elif couleuree == "4" :
            couleureee = "Vert"
        elif couleuree == "6"  :
            couleureee = "Bleu" 
        elif couleuree == "3"  :
            couleureee = "Burple" 
        elif couleuree == "0"  :
            couleureee = "color inconu" 
            
        fichier.write('Cx='+ccc1+' '+couleureee+' '+formeee+' '+areaaaaa+' '+'-->'+' '+'SBC='+ccc1+''+couleuree+''+formee+''+areaaaa+'\n')
        fichier.close()

#---------------------------------------------------------------------------------------------------------------- 


#*****************************************************************************************************************Action

        if   areaaaa == "3" and formee == "6" and couleuree == "3" :# cercle violet
			pygame.init()
			pygame.mixer.music.load("/home/pi/Desktop/tests-IUI/test-1/action/1.mp3")
			pygame.mixer.music.play()
			time.sleep(10)
            

        elif areaaaa == "3" and formee == "8" and couleuree == "4"  :# hexagon vert

			pygame.init()
			pygame.mixer.music.load("/home/pi/Desktop/tests-IUI/test-1/action/2.mp3")
			pygame.mixer.music.play()
			time.sleep(10)

        elif areaaaa == "3" and formee == "2" and couleuree == "2"  :# pentagon orange

			pygame.init()
			pygame.mixer.music.load("/home/pi/Desktop/tests-IUI/test-1/action/3.mp3")
			pygame.mixer.music.play()
			time.sleep(10)
						
			
		#elif areaaaa == "3" and formee == "8" and couleuree == "6"  :# bleu hexagon tall

            #webbrowser.open_new("http://sciencedirect.com")
			
		#elif areaaaa == "3" and formee == "3" and couleuree == "2"  :# orange pentagon tall

			#pygame.init()
			#pygame.mixer.music.load("/home/pi/Desktop/1.mp3")
			#pygame.mixer.music.play()
			#time.sleep(5)
#---------------------------------------------------------------------------------------------------------------- 


