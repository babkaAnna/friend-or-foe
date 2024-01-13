import os
import time
import numpy as np
from datetime import datetime
import pyttsx3
import cv2 as cv

print ("Если хотите анализ фото произвести, то нажмите 1. Если хотите включить камеру, то нажмите 2")
k = int(input())
if k==1:
    print ("Если хотите базовые фотки, то нажмите 1. Если хотите реальные фотки, то нажмите 2")
    k = int(input())
    if k==1:
        k = "baza"
    elif k==2:
        k = "really"
    else:
        print ("Вы ввели неправильное значение, запустите программу сначала")
        exit()
    engine = pyttsx3.init()
    engine.setProperty('rate', 145)
    engine.setProperty('volume', 1.0)
    root_dir = os.path.abspath('.')
    gunfire_path = os.path.join(root_dir, 'gunfire.wav')
    tone_path = os.path.join(root_dir, 'tone.wav')


    path= "D:/Python/Lib/site-packages/cv2/data/"
    face_cascade = cv.CascadeClassifier(path + 'haarcascade_frontalface_default.xml')
    assert not face_cascade.empty()
    eye_cascade = cv.CascadeClassifier(path + 'haarcascade_eye.xml')
    assert not eye_cascade.empty()


    os.chdir('C:/Users/uncle/Desktop/курсач/picture_'+k)
    contents = sorted(os.listdir())

    
    for image in contents:
        print(f"\nОбнаружено движение...{datetime.now()}") # Обнаружено движение
        discharge_weapon = True
        
        ######Голос о том, что зафиксировано движение
        engine.say("Если Вы человек, то Вам не о чем беспокоиться. \
                Повернитесь лицом к турели.")
        engine.runAndWait()
        time.sleep(1)
        
        #####Импортирование и вывод фото
        img_gray = cv.imread(image, cv.IMREAD_GRAYSCALE)
        qwerty = cv.imread(image, cv.IMREAD_GRAYSCALE)
        height, width = np.shape(img_gray)
        cv.imshow(f'1 {image}', img_gray)
        cv.waitKey(3000)
        cv.destroyWindow(f'1 {image}')
        
        #####Запись всех возможных лиц
        face_rect_list = []
        face_rect_list.append(face_cascade.detectMultiScale(image=img_gray, scaleFactor=1.1, minNeighbors=5))
        
        #####Вывод всех возможных лиц
        for j in face_rect_list:
            for i in j:
                cv.rectangle(qwerty, (i[0], i[1]), (i[0]+i[2], i[1]+i[3]),(255,255,255), 2) 
        cv.imshow(f'2 {image}', qwerty)
        cv.waitKey(3000)
        cv.destroyWindow(f'2 {image}')

        #####Голос о том, что зафиксированно лицо
        engine.say("Лицо зафиксированно. \
                Производится дополнительная проверка.")
        engine.runAndWait()
        time.sleep(1)
        
        #####Проверка на наличие глаз в лицах
        print(f"Для достоверности ведётся поиск глаз в {image}")
        for rect in face_rect_list:
            for (x, y, w, h) in rect:
                rect_4_eyes = img_gray[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(image=rect_4_eyes, scaleFactor=1.05, minNeighbors=2)
                for (xe, ye, we, he) in eyes:
                    center = (int(xe + 0.5 * we), int(ye + 0.5 * he))
                    radius = int((we + he) / 3)
                    cv.circle(rect_4_eyes, center, radius, 255, 2)
                    cv.rectangle(img_gray, (x, y), (x+w, y+h), (255, 255, 255), 2)
                    discharge_weapon = False
                    cv.imshow(f'Motion detected {image}', img_gray)
                    cv.waitKey(3000)
                    cv.destroyWindow(f'Motion detected {image}')
                    break
                
        #####Вывод решение
        if discharge_weapon == False:
            print(f"Глаза найдены.")
            cv.putText(img_gray, 'Open ^_^', (int(width / 2) - 20, int(height / 2)), cv.FONT_HERSHEY_PLAIN, 3, 255, 3)
            engine.say("Заходи, бродяга.")
            engine.runAndWait()
            time.sleep(1)
            cv.imshow('Detected Faces', img_gray)
            cv.waitKey(2000)
            cv.destroyWindow('Detected Faces')
            time.sleep(1)
        else:
            print(f"Глаза не найдены.")
            cv.putText(img_gray, 'Fire!', (int(width / 2) - 20, int(height / 2)), cv.FONT_HERSHEY_PLAIN, 3, 255, 3)
            engine.say("Активировать протокол Земля пухом - Царство небесное.")
            engine.runAndWait()
            time.sleep(1)
            cv.imshow('Mutant', img_gray)
            cv.waitKey(2000)
            cv.destroyWindow('Mutant')
            time.sleep(1)
        engine.stop()
        print ("Введите 0, если хотите продолжить, или 1, если хотите завершить")
        k = int(input())
        if k == 1:
            break
        elif k == 0:
            continue
        else:
            print ("Введен неверный символ")
        
elif k==2:
    path= "D:/Python/Lib/site-packages/cv2/data/"
    face_cascade = cv.CascadeClassifier(path + 'haarcascade_frontalface_default.xml')
    cap = cv.VideoCapture(0)
    while True:
        _, frame = cap.read()
        face_rects = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=3)
        for (x, y, w, h) in face_rects:
            cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv.imshow('frame', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()
else:
    print ("Вы ввели неправильное значение, запустите программу сначала")
