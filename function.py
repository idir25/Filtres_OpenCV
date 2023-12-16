import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageTk
import tkinter as tk

# Param global :
closeWindow = False
activeSunglasses = False
activedog = False
activecigare = False
activelunette = False
activeberet = False
activemoustache = False
activeHat = False
luminositeValue = 0
ContrastValue = 100

# Load the cascade
face_cascade = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')
eye_cascade = cv.CascadeClassifier('./haarcascades/haarcascade_eye_tree_eyeglasses.xml')
sunglasses = cv.imread('Filters/glasses.png', cv.IMREAD_UNCHANGED)
beret = cv.imread('Filters/beret.png', cv.IMREAD_UNCHANGED)
cigare = cv.imread('Filters/cigarette.png', cv.IMREAD_UNCHANGED)
hat = cv.imread('Filters/beret.png', cv.IMREAD_UNCHANGED)
dog = cv.imread('Filters/dog.png',cv.IMREAD_UNCHANGED)
moustache = cv.imread('Filters/moustache.png',cv.IMREAD_UNCHANGED)
lunette = cv.imread('Filters/lunette.png',cv.IMREAD_UNCHANGED)





def ajuster_luminosite_contraste(image, luminosite, contraste):
    # Convertir l'image en espace de couleur HSV
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    # Ajuster la luminosité et le contraste
    contraste = float(contraste) / 100
    hsv[:, :, 2] = cv.addWeighted(hsv[:, :, 2], float(contraste), 0, 0, float(luminosite))
    # Convertir l'image de nouveau en espace de couleur BGR
    nouvelle_image = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
    return nouvelle_image



def tracer_rectangle(image, point1, point2, couleur=(0, 255, 0)):
    # Copier l'image pour éviter de modifier l'original
    img_rect = image.copy()
    # Tracer le rectangle à partir des deux points
    cv.rectangle(img_rect, point1, point2, couleur)
    return img_rect


def convert_image_for_tkinter(image):
    # Convertir l'image OpenCV en format RGB pour Tkinter
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    # Convertir l'image en objet ImageTk pour Tkinter
    image = Image.fromarray(image)
    return ImageTk.PhotoImage(image)


def closeWindowF():
    global closeWindow
    closeWindow = True


def on_checkbox_checked_sunglasses(checkbox_var):
    global activeSunglasses
    if checkbox_var.get():
        activeSunglasses = True
    else:
        activeSunglasses = False

def on_checkbox_checked_lunette(checkbox_var):
    global activelunette
    if checkbox_var.get():
        activelunette = True
    else:
        activelunette = False

def on_checkbox_checked_moustache(checkbox_var):
    global activemoustache
    if checkbox_var.get():
        activemoustache = True
    else:
        activemoustache = False

def on_checkbox_checked_beret(checkbox_var):
    global activeberet
    if checkbox_var.get():
        activeberet = True
    else:
        activeberet = False

def on_checkbox_checked_cigare(checkbox_var):
    global activecigare
    if checkbox_var.get():
        activecigare = True
    else:
        activecigare = False
        
def on_checkbox_checked_dog(checkbox_var):
    global activedog
    if checkbox_var.get():
        activedog = True
    else:
        activedog = False


def on_checkbox_checked_hat(checkbox_var):
    global activeHat
    if checkbox_var.get():
        activeHat = True
    else:
        activeHat = False


def insideImg(webcamImage,point1,point2,img):
    resized_hat = cv.resize(img, (point2[0] - point1[0], point2[1] - point1[1])) 
    mask = resized_hat[:, :, 3] / 255.0
    for c in range(3):
        webcamImage[point1[1]:point2[1], point1[0]:point2[0], c] = (
        webcamImage[point1[1]:point2[1], point1[0]:point2[0], c] * (1 - mask) +
        resized_hat[:, :, c] * mask)
    return webcamImage

def onSliderChangeLuminosity(value):
    global luminositeValue
    luminositeValue=value

def onSliderChangeContraste(value):
    global ContrastValue
    ContrastValue=value


def getWebcamVideo(width, height):

    videoWebcam = cv.VideoCapture(0)
    point1 = (0,0)
    point2 = (0,0)

    # Créer une fenêtre Tkinter
    window = tk.Tk()
    window.protocol("WM_DELETE_WINDOW", closeWindowF)
    window.configure(bg="#201c1c")
    window.title("Filtre vidéo")
    window.geometry(str(width) + 'x' + str(height))

    # Texte
    label = tk.Label(window, text="Paramètres :")
    label.place(x=650, y=10)
    
    # Créations des cases à cocher
    checkbox_var_sunglasses = tk.BooleanVar()
    checkbox = tk.Checkbutton(window, text="Lunettes de soleil", variable=checkbox_var_sunglasses, command=lambda: on_checkbox_checked_sunglasses(checkbox_var_sunglasses))
    checkbox.place(x=650, y=30)

    checkbox_var_hat = tk.BooleanVar()
    checkboxHat = tk.Checkbutton(window, text="Chapeau", variable=checkbox_var_hat, command=lambda: on_checkbox_checked_hat(checkbox_var_hat))
    checkboxHat.place(x=650, y=50)

    checkbox_var_dog = tk.BooleanVar()
    checkbox = tk.Checkbutton(window, text="dog", variable=checkbox_var_dog, command=lambda: on_checkbox_checked_dog(checkbox_var_dog))
    checkbox.place(x=650, y=70)

    checkbox_var_beret = tk.BooleanVar()
    checkbox = tk.Checkbutton(window, text="beret", variable=checkbox_var_beret, command=lambda: on_checkbox_checked_beret(checkbox_var_beret))
    checkbox.place(x=650, y=270)

    checkbox_var_cigare = tk.BooleanVar()
    checkbox = tk.Checkbutton(window, text="cigare", variable=checkbox_var_cigare, command=lambda: on_checkbox_checked_cigare(checkbox_var_cigare))
    checkbox.place(x=650, y=290)

    checkbox_var_lunette = tk.BooleanVar()
    checkbox = tk.Checkbutton(window, text="lunette", variable=checkbox_var_lunette, command=lambda: on_checkbox_checked_lunette(checkbox_var_lunette))
    checkbox.place(x=650, y=310)

    checkbox_var_moustache = tk.BooleanVar()
    checkbox = tk.Checkbutton(window, text="moustache", variable=checkbox_var_moustache, command=lambda: on_checkbox_checked_moustache(checkbox_var_moustache))
    checkbox.place(x=650, y=330)



    # Création de boutons de défilement (slider)
    sliderLuminosity = tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, command=onSliderChangeLuminosity)
    sliderLuminosity.place(x=650, y=110)
    label = tk.Label(window, text="Luminosité")
    label.place(x=650, y=90)

    sliderContraste = tk.Scale(window, from_=0, to=200, orient=tk.HORIZONTAL, command=onSliderChangeContraste)
    sliderContraste.place(x=650, y=170)
    label = tk.Label(window, text="Contraste")
    label.place(x=650, y=150)

    # Créer un canevas Tkinter pour afficher l'image
    canvas = tk.Canvas(window, width=640, height=480)
    canvas.place(x=0, y=0)

    # On fait une boucle infinie pour faire la capture en temps réel
    while True:
        returnValue, webcamImage = videoWebcam.read()
        faces = face_cascade.detectMultiScale(webcamImage, 1.1, 4)

        for (xf,yf,wf,hf) in faces:
            i=0
            #webcamImage = cv.ellipse(webcamImage, (xf + int(wf*0.5), yf + int(hf*0.5)), (int(wf*0.5),int(hf*0.5)), 0,0,360,(255, 0, 255), 4)

             # Option pour le dog
            if (activedog == True):
                point1 = (xf+15,yf+int(0.25*hf))
                point2 = (xf+wf-15,yf+hf-int(0.45*hf))
                try:
                    webcamImage = insideImg(webcamImage,point1,point2,dog)
                    #webcamImage = tracer_rectangle(webcamImage, point1, point2, couleur=(0, 255, 0))
                except Exception as e:
                    print(f"Une erreur s'est produite : {e}")


            # Option pour le beret
            if (activeberet == True):
                point1 = (xf+15,yf+int(0.25*hf))
                point2 = (xf+wf-15,yf+hf-int(0.45*hf))
                try:
                    webcamImage = insideImg(webcamImage,point1,point2,beret)
                    #webcamImage = tracer_rectangle(webcamImage, point1, point2, couleur=(0, 255, 0))
                except Exception as e:
                    print(f"Une erreur s'est produite : {e}")


            # Option pour le cigare
            if (activecigare == True):
                point1 = (xf+15,yf+int(0.25*hf))
                point2 = (xf+wf-15,yf+hf-int(0.45*hf))
                try:
                    webcamImage = insideImg(webcamImage,point1,point2,cigare)
                    #webcamImage = tracer_rectangle(webcamImage, point1, point2, couleur=(0, 255, 0))
                except Exception as e:
                    print(f"Une erreur s'est produite : {e}")


            # Option pour le lunette
            if (activelunette == True):
                point1 = (xf+15,yf+int(0.25*hf))
                point2 = (xf+wf-15,yf+hf-int(0.45*hf))
                try:
                    webcamImage = insideImg(webcamImage,point1,point2,lunette)
                    #webcamImage = tracer_rectangle(webcamImage, point1, point2, couleur=(0, 255, 0))
                except Exception as e:
                    print(f"Une erreur s'est produite : {e}")


            # Option pour le moustache
            if (activemoustache == True):
                point1 = (xf+15,yf+int(0.25*hf))
                point2 = (xf+wf-15,yf+hf-int(0.45*hf))
                try:
                    webcamImage = insideImg(webcamImage,point1,point2,moustache)
                    #webcamImage = tracer_rectangle(webcamImage, point1, point2, couleur=(0, 255, 0))
                except Exception as e:
                    print(f"Une erreur s'est produite : {e}")


            # Option pour les lunettes de soleil
            if (activeSunglasses == True):
                point1 = (xf+15,yf+int(0.25*hf))
                point2 = (xf+wf-15,yf+hf-int(0.45*hf))
                try:
                    webcamImage = insideImg(webcamImage,point1,point2,sunglasses)
                    #webcamImage = tracer_rectangle(webcamImage, point1, point2, couleur=(0, 255, 0))
                except Exception as e:
                    print(f"Une erreur s'est produite : {e}")

            # Option pour le chapeau
            if (activeHat == True):
                point1 = (xf-15,yf-int(0.60*hf))
                point2 = (xf+wf+15,yf+hf-int(0.80*hf))
                try:
                    webcamImage = insideImg(webcamImage,point1,point2,hat)
                    #webcamImage = tracer_rectangle(webcamImage, point1, point2, couleur=(0, 255, 0))
                except Exception as e:
                    print(f"Une erreur s'est produite : {e}")
                    
            # Option luminosité et contraste :
            webcamImage = ajuster_luminosite_contraste(webcamImage,luminositeValue,ContrastValue)

        # Convertir l'image pour Tkinter
        img_tk = convert_image_for_tkinter(webcamImage)

        # Mettre à jour le canevas avec la nouvelle image
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
        canvas.update()

        if closeWindow == True:
            break

    videoWebcam.release()
    cv.destroyAllWindows()
    canvas.destroy()
    window.destroy()

getWebcamVideo(800, 480)