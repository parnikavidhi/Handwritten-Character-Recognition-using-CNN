# -*- coding: utf-8 -*-
"""final_frontend.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zYY5FkrfKOKuDvCtbEwL3y6dSb3SLCtV

# Importing Libraries

---

* Tkinter- It is a standard Python interface to the Tk GUI toolkit shipped with Python. Python with tkinter outputs the fastest and easiest way to create the GUI applications.

*  PIL-Python Imaging Library (abbreviated as PIL)) is a free library for the Python programming language that adds support for opening, manipulating, and saving many different image file formats
*  Pyperclip-Pyperclip is a cross-platform Python module for copy and paste clipboard functions. 

* Image-The Image module  provides a number of factory functions, including functions to load images from files, and to create new images.

* ImageGrab-The ImageGrab module can be used to copy the contents of the screen or the clipboard to a PIL image memory.

* ImageFilter -The ImageFilter module contains definitions for a pre-defined set of filters, which can be be used with the Image.filter() method.

* sys-This module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter.

* Ipython-IPython (Interactive Python) is a command shell for interactive computing in multiple programming languages, originally developed for the Python programming language, that offers introspection, rich media, shell syntax, tab completion, and history.
"""

from tkinter import *
#from tkinter.colorchooser import askcolor
from PIL import ImageGrab
from PIL import ImageFilter,Image
from IPython import get_ipython
from tkinter.filedialog import askopenfilename
import pyperclip
import sys
import scipy.misc

"""# Intitializing   variables with  values

---
"""

DEFAULT_PEN_SIZE = 10
DEFAULT_COLOR = 'black'

"""# Defining module to save an image

---
"""

def images_save(st):
    im_open = Image.open(st)
    im = Image.open(st).convert('LA') #conversion to gray-scale image
    
    
    width = float(im.size[0])
    height = float(im.size[1])
    newImage = Image.new('L',(300,300),(255))
    if width > height: #check which dimension is bigger
        #Width is bigger. Width becomes 300 pixels.
        nheight = int(round((300.0/width*height),0)) #resize height according to ratio width
        if (nheight == 0): #rare case but minimum is 1 pixel
            nheight = 1
        # resize and sharpen
        img = im.resize((300,nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wtop = int(round(((300 - nheight)/2),0)) #caculate horizontal pozition
        newImage.paste(img, (0,wtop)) #paste resized image on white canvas
    else:
    #Height is bigger. Heigth becomes 300 pixels.
        nwidth = int(round((300.0/height*width),0)) #resize width according to ratio height
        if (nwidth == 0): #rare case but minimum is 1 pixel
            nwidth = 1
     # resize and sharpen
        img = im.resize((nwidth,300), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wleft = int(round(((300 - nwidth)/2),0)) #calculate vertical pozition
        newImage.paste(img, (wleft,0)) #paste resize
    
    rec = list(newImage.getdata())
    rec_im = np.array(rec)
    scipy.misc.imsave('C:/Users/lenovo/Desktop/Handwritten-Character-Recognition-using-CNN/rec.jpg', rec_im.reshape(300,300))
    
    norm = [ (255-x)*1.0/255.0 for x in rec]
    norm = np.array(norm)
    scipy.misc.imsave('C:/Users/lenovo/Desktop/Handwritten-Character-Recognition-using-CNN/norm.jpg', norm.reshape(300,300))

"""# Function for an image of 28X28

---

* The image to be predicted is opened.
* The image is converted to gray scale
* The image is then rescaled,normalized.
* The image returned is the original image ,rescaled image and normalized image.
"""

def input_emnist(st):
	#opening the input image to be predicted
    images_save(st)
    im_open = Image.open(st)
    im = Image.open(st).convert('LA') #conversion to gray-scale image
    width = float(im.size[0])
    height = float(im.size[1])
    newImage = Image.new('L',(28,28),(255))


    if width > height: #check which dimension is bigger
        #Width is bigger. Width becomes 20 pixels.
        nheight = int(round((28.0/width*height),0)) #resize height according to ratio width
        if (nheight == 0): #rare case but minimum is 1 pixel
            nheight = 1
        # resize and sharpen
        img = im.resize((28,nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wtop = int(round(((28 - nheight)/2),0)) #caculate horizontal pozition
        newImage.paste(img, (0,wtop)) #paste resized image on white canvas
    else:
    #Height is bigger. Heigth becomes 20 pixels.
        nwidth = int(round((28.0/height*width),0)) #resize width according to ratio height
        if (nwidth == 0): #rare case but minimum is 1 pixel
            nwidth = 1
     # resize and sharpen
        img = im.resize((nwidth,28), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wleft = int(round(((28 - nwidth)/2),0)) #calculate vertical pozition
        newImage.paste(img, (wleft,0)) #paste resize


# # Normalizing image into pixel values
    tv = list(newImage.getdata())
    tva = [ (255-x)*1.0/255.0 for x in tv]
       
    n_image = np.array(tva)
    
    # return all the images
    return n_image,im_open,newImage

"""#  Emnist Training

---
* Loading EMNIST dataset
* Getting the stored dataset
* Defining functions
* Creating model
"""

####  emnist training
# # Loading EMNIST dataset


import warnings
warnings.filterwarnings('ignore')
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
def model_predict(n_image):
	# the below is commented due to the model already been trained

    
    #getting the stored dataset
    
    from sklearn.preprocessing import OneHotEncoder
    #train data
    get_ipython().magic('store -r n_labels')
    
    shaped_n_labels  = n_labels.reshape(-1,1)
    enc = OneHotEncoder()
    enc.fit(shaped_n_labels)
    train_labels = enc.transform(shaped_n_labels).toarray()
    

# ## Functions

# initialising weights
    def init_weights(shape):
        init_random_dist = tf.truncated_normal(shape,stddev=0.1)
        return tf.Variable(init_random_dist)
    # initialising bias
    def init_bias(shape):
        init_bias_vals = tf.constant(0.1,shape=shape)
        return tf.Variable(init_bias_vals)
    #conv2d
    def conv2d(x,W):
        #x -> [bias,height,width,channels]
        #W -> [Filter H,filter W,Channel In,Channel Out]
        return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding='SAME')
    #pooling layer
    def max_pool_2by2(x):
        return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')
    #Convolutional layer
    def convolutional_layer(input_x,shape):
        W=init_weights(shape)
        bias = init_bias([shape[3]])
        return tf.nn.relu(conv2d(input_x,W)+bias)
    #Fully connected layer
    def normal_full_layer(input_layer,size):
        input_size = int(input_layer.get_shape()[1])
        W = init_weights([input_size,size])
        bias = init_bias([size])
        return tf.matmul(input_layer,W) + bias


    # ## Creating model


    #placeholders
    x = tf.placeholder(tf.float32,shape=[None,784])
    y_true=tf.placeholder(tf.float32,shape=[None,47])

    #layers(input)
    x_image = tf.reshape(x,[-1,28,28,1])

    #first convolutional layer
    convo_1 = convolutional_layer(x_image,shape=[5,5,1,32])
    convo_1_pooling = max_pool_2by2(convo_1)

    #second convolutional layer
    convo_2 = convolutional_layer(convo_1_pooling,shape=[5,5,32,64])
    convo_2_pooling = max_pool_2by2(convo_2)

    #fully connected layer
    convo_flat = tf.reshape(convo_2_pooling,[-1,7*7*64])
    full_layer_one = tf.nn.relu(normal_full_layer(convo_flat,1024))


    #drop out (used to overcome overfitting)

    hold_prob = tf.placeholder(tf.float32)
    full_one_dropout = tf.nn.dropout(full_layer_one,keep_prob=hold_prob)

    y_pred = normal_full_layer(full_one_dropout,47)

    #Loss Function
    
    init = tf.global_variables_initializer()



    saver = tf.train.Saver()
    with tf.Session() as sess:
            sess.run(init)
            saver.restore(sess,"C:/Users/lenovo/Desktop/Handwritten-Character-Recognition-using-CNN/model/cnn_model_1_without_tamil.ckpt")

            prediction=tf.argmax(y_pred,1)
            var = prediction.eval(feed_dict={x: [n_image],y_true:train_labels,hold_prob: 0.5}, session=sess)


    labels_dict ={0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:'A',11:'B',12:'C',13:'D',14:'E',15:'F',16:'G',17:'H',18:'I',19:'J',20:'K',21:'l',22:'M',23:'N',24:'O',25:'P',26:'Q',27:'R',28:'S',29:'T',30:'u',31:'V',32:'W',33:'X',34:'Y',35:'Z',36:'a',37:'b',38:'d',39:'e',40:'f',41:'g',42:'h',43:'n',44:'q',45:'r',46:'t',47:'அ',48:'ஆ',49:'இ',50:'ஈ',51:'உ',52:'ஊ',53:'எ',54:'ஏ',55:'ஐ',56:'ஒ',57:'ஓ',58:'ஔ'}


    s = "Predicted Character : {}".format(labels_dict[var[0]])
    return s,labels_dict[var[0]]

"""# Functions to implement GUI

---
* Functions are defined for using pen,eraser,brush,paint,activate button,to get an image and to exit to implement the GUI .
"""

def use_pen():
    global pen_button
    activate_button(pen_button)

def use_brush():
    global brush_button
    activate_button(brush_button)

def use_eraser():
    global eraser_button
    activate_button(eraser_button, eraser_mode=True)

def activate_button(some_button, eraser_mode=False):
    global active_button
    global eraser_on
    active_button.config(relief=RAISED)
    some_button.config(relief=SUNKEN)
    active_button = some_button
    eraser_on = eraser_mode 

def paint(event):
    global old_x
    global old_y
    global active_button
    global eraser_on
    global line_width
    line_width = 10
    paint_color = 'white' if eraser_on else color
    if old_x and old_y:
        c.create_line(old_x, old_y, event.x, event.y, width=10, fill=paint_color, 
                           capstyle=ROUND, smooth=TRUE, splinesteps=36)
    old_x = event.x
    old_y = event.y

def reset(event):
    global old_x
    global old_y
    old_x, old_y = None, None
        
#from PIL import *

def getter():
    global c
    global root
    root.update()
    x=root.winfo_rootx()+c.winfo_x()+50  #+50#
    y=root.winfo_rooty()+c.winfo_y()+60 #120#
    x1=x+550 #c.winfo_width()             #550#
    y1=y+600 #c.winfo_height()            #510#
    ImageGrab.grab((x,y,x1,y1)).save("C:/Users/lenovo/Desktop/Handwritten-Character-Recognition-using-CNN/image1.jpg")
    root.destroy()


def get_clear():
    global c
    c.delete("all")

def can():
    sys.exit()

def displaydir():
    global path
    fnme = askopenfilename()
    if fnme:
        path = fnme
        
def new_winF():
 # new window definition
    root.destroy()

"""# Creating the main window using Tkinter

---

* The window is created for the GUI.
* The geometry of the window is set.
* The title and the background the window is set.
"""

path='image1.jpg'
root = Tk()
root.geometry("650x700+50+50")
root.title("Handwritten Character Recognition")
root.configure(background='#98A2A4')

"""# Adding widgets to the main window

---
Different widgets are added to the main window:

* Label is added to the main window and the background and other configuration like the font style,font size is set .
* Pen , eraser , clear , browse , predict and exit buttons with some properties  and functionalities are placed on the main window.
* Canvas that is used to draw picture is also added to the window.
"""

lbl1 = Label(root, text='Draw any Alpha-Numeric Character (0-9, A-Z, a-z)',bg='#98A2A4')
lbl1.config(font=("Courier", 15,'bold'))
lbl1.place(x = 5, y = 20, width=650, height=25)
        
pen_button = Button(root, text='Pen', command=use_pen, bd = 5)
pen_button.place(x = 100, y = 70, width=120, height=35)
pen_button.config(font=('bold'))


eraser_button = Button(root, text='Eraser', command=use_eraser, bd=5)
eraser_button.place(x = 270, y = 70, width=120, height=35)
eraser_button.config(font=('bold'))

clear = Button(root, text = "Clear", command = get_clear, bd = 5)
clear.place(x = 440, y = 70, width=120, height=35)
clear.config(font=('bold'))

c = Canvas(root, bg='white', bd = 5, relief='solid')
c.place(x = 50, y = 120, width=550, height=510)
        
brow = Button(root, text ="Browse", command = displaydir, bd = 5)
brow.place(x = 100, y = 645, width=120, height=35)
brow.config(font=('bold'))

submit = Button(root, text ="Predict", command = getter, bd = 5)
submit.place(x = 270, y = 645, width=120, height=35)
submit.config(font=('bold'))

cancel_btn = Button(root, text = "Exit", command = can, bd = 5)
cancel_btn.place(x = 440, y = 645, width=120, height=35)
cancel_btn.config(font=('bold'))

from PIL import Image, ImageTk

old_x = None
old_y = None
line_width = 10
color = DEFAULT_COLOR
eraser_on = False
active_button = pen_button
active_button.config(relief=SUNKEN)
c.bind('<B1-Motion>', paint)
c.bind('<ButtonRelease-1>', reset)

root.mainloop()

"""# Call to Function with name of the file as parameter

---
"""

n_image,image,convo_image = input_emnist(path) #call to Function with name of the file as parameter
res,cpy = model_predict(n_image)
pyperclip.copy(str(cpy)) #copy the predicted character to clipboard

"""# Creating a window to display the original image

---

A new window is created in which the original image is  loaded and displayed .
"""

root = Tk()
root.configure(background='#98A2A4')
root.geometry("400x400+50+50")
lbl = Label(root,text="Original Image", bg ='#98A2A0')
lbl.config(font=("Courier", 15,'bold'))
lbl.place(x= 100, y=10, width =200 ,height = 30)   
load = Image.open("C:/Users/lenovo/Desktop/Handwritten-Character-Recognition-using-CNN/rec.jpg")
render = ImageTk.PhotoImage(load)
img = Label(root, image=render,width=300, height=300)
img.image = render
img.place(x = 50,y=50,width = 300, height = 300)
button1 =Button(root, text ="Next", command =new_winF)
button1.place(x = 300,y = 360, width = 80, height = 30)
button1.config(font=('bold'))

root.mainloop()

"""# Creating a window to display the rescaled image

---

A new window is created in which the rescaled image is  loaded and displayed .
"""

root = Tk()

root.configure(background='#98A2A4')
root.geometry("400x400+50+50")
lbl = Label(root,text="Rescaled Image", bg ='#98A2A0')
lbl.config(font=("Courier", 15,'bold'))
lbl.place(x= 100, y=10, width =200 ,height = 30)   
load = Image.open("C:/Users/lenovo/Desktop/Handwritten-Character-Recognition-using-CNN/rec.jpg")
render = ImageTk.PhotoImage(load)
img = Label(root, image=render,width=300, height=300)
img.image = render
img.place(x = 50,y=50,width = 300, height = 300)
button1 =Button(root, text ="Next", command =new_winF)
button1.config(font=('bold'))
button1.place(x = 300,y = 360, width = 80, height = 30)



root.mainloop()

"""#  Creating a window to display the normalized image

---

A new window is created in which the normalized image is  loaded and displayed .
"""

root = Tk()

root.configure(background='#98A2A4')
root.geometry("400x400+50+50")
lbl = Label(root,text="Normalized Image", bg ='#98A2A0')
lbl.config(font=("Courier", 15,'bold'))
lbl.place(x= 100, y=10, width =250 ,height = 30)   
load = Image.open("C:/Users/lenovo/Desktop/Handwritten-Character-Recognition-using-CNN/norm.jpg")
render = ImageTk.PhotoImage(load)
img = Label(root, image=render,width=300, height=300)
img.image = render
img.place(x = 50,y=50,width = 300, height = 300)
button1 =Button(root, text ="Next", command =new_winF)
button1.place(x = 300,y = 360, width = 80, height = 30)
button1.config(font=('bold'))

root.mainloop()

"""# Transformed Images and Probabilistic graph

---

The window containg the original image,rescaled image , normalized image and the probabilistic graph with the final output displaying the predicted character.
"""

root = Tk()

root.configure(background='#98A2A4')
root.geometry("800x750+50+50")

lbl = Label(root,text="Original Image", bg ='#98A2A0')
lbl.config(font=("Courier", 15,'bold'))
lbl.place(x= 100, y=20, width =200 ,height = 30)   
load = Image.open("C:/Users/lenovo/Desktop/Handwritten-Character-Recognition-using-CNN/rec.jpg")
render = ImageTk.PhotoImage(load)
img = Label(root, image=render,width=300, height=300)
img.image = render
img.place(x = 50,y=50,width = 300, height = 300)

lbl1 = Label(root,text="Rescaled Image", bg ='#98A2A0')
lbl1.config(font=("Courier", 15,'bold'))
lbl1.place(x= 500, y=20, width =200 ,height = 30)   
load = Image.open("C:/Users/lenovo/Desktop/Handwritten-Character-Recognition-using-CNN/rec.jpg")
render = ImageTk.PhotoImage(load)
img = Label(root, image=render,width=300, height=300)
img.image = render
img.place(x = 450,y=50,width = 300, height = 300)

lbl2 = Label(root,text="Normalized Image", bg ='#98A2A0')
lbl2.config(font=("Courier", 15,'bold'))
lbl2.place(x= 100, y=370, width =200 ,height = 30)   
load = Image.open("C:/Users/lenovo/Desktop/Handwritten-Character-Recognition-using-CNN/norm.jpg")
render = ImageTk.PhotoImage(load)
img = Label(root, image=render,width=300, height=300)
img.image = render
img.place(x = 50,y= 400,width = 300, height = 300)

'''lbl3 = Label(root,text="Probabilities graph", bg ='#98A2A0')
lbl3.config(font=("Courier", 15,'bold'))
lbl3.place(x= 450, y=370, width =300 ,height = 30)   
load = Image.open("C:/Users/lenovo/Desktop/Handwritten-Character-Recognition-using-CNN/image1.jpg")
render = ImageTk.PhotoImage(load)
img = Label(root, image=render,width=300, height=300)
img.image = render
img.place(x = 450,y=400,width = 300, height = 300)'''


txt = Label(root, text=res, bg='#98A4A0')
txt.config(font=("Courier", 15,'bold'))
txt.place(x= 450, y=400, width =300 ,height = 30)
'''txt.place(x= 300, y=720, width =300 ,height = 30)'''
root.mainloop()
