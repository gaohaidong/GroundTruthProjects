# -*- coding: UTF-8 -*-
# pip install qrcode
# pip install colorama
# https://blog.csdn.net/henni_719/article/details/54580732?locationNum=3&fps=1
# https://blog.csdn.net/jy692405180/article/details/65937077

import qrcode
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from random import randint

content = ''
for i in range(2500):
    #content += str(randint(0,9))
    content += chr(randint(0,255))
print(content)
    
# way 1: default
#img = qrcode.make(content)      
#img.save("test_qrcode.png")
# way 2: control
qr = qrcode.QRCode(version=20,
                   error_correction=qrcode.constants.ERROR_CORRECT_L,  
                   box_size=5,
                   border=4)
qr.add_data(content)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")     
img.save("test_qrcode.png")
