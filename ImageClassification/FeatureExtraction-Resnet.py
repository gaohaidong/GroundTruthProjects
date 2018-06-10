import numpy as np
#from scipy.misc import imread, imresize
#from imagenet_classes import class_names
import os

# image interface
import matplotlib.pyplot as plt
#import cv2
from PIL import Image

# tf interface
import tensorflow as tf
import tensorflow.contrib.slim as slim
import tensorflow.contrib.slim.nets as nets
#from tensorflow.contrib.slim.preprocessing import vgg_preprocessing

from utils import get_jpgs_d1, get_jpgs_d0

def get_feas_resnet(sess, jpg_lst, nf=2048):
    # s3: 
    ni = len(jpg_lst)
    feas = np.zeros((ni, nf), dtype=np.float)
    for i in range(ni):
        jpg_pth = jpg_lst[i]
        print('#%05d ==> ' %i + jpg_pth)
        
        img_rsz = Image.open(jpg_pth).resize((image_size, image_size))
        img_f64 = np.array(img_rsz) / 255.0
        img_f32 = img_f64.astype(np.float32)
            
        img_in, logits = sess.run([t_image, t_logits], {t_image:[img_f32]})
        feas[i, :] = logits.flatten()
    return feas


if __name__ == '__main__':
    ckpt_dir = '/workspace/TensorFlow/tf-offical/resnet_v1_50_ckpt'
    ckpt_file = ckpt_dir + '/' + 'resnet_v1_50.ckpt'
    
    
    # s1: reading and processing images
    img_pth = 'xx.jpg'
    img_data = tf.image.decode_jpeg(tf.read_file(img_pth), channels=3)
    tr_dir = 'xx'
    cb_dir = 'xx'
  
    #jpg_lst = get_jpgs_d0(tr_dir)
    jpg_lst, _ = get_jpgs_d1(cb_dir)
    
    
    # s1: preparered work
    image_size = nets.resnet_v1.resnet_v1.default_image_size
    
    # s2: creaing the resnet_v1 network
    arg_scope = nets.resnet_v1.resnet_arg_scope()
    with slim.arg_scope(arg_scope):
        t_image = tf.placeholder('float32', [1, image_size, image_size, 3], name='input_image')
        t_logits, t_end_points = nets.resnet_v1.resnet_v1_50(t_image, is_training=False)
    
    #
    saver = tf.train.Saver()
    
    #sess = tf.Session()
    with tf.Session() as sess:
        saver.restore(sess, ckpt_file)
        #feas = get_feas_resnet(sess, jpg_lst, nf=2048)
        #np.save('tr_feas_resnet.npy', feas)
        #f = open('train_images.txt', 'w')
        #f.write('\n'.join(jpg_lst))
        #f.close()
        feas = get_feas_resnet(sess, jpg_lst, nf=2048)
        np.save('cb_feas_resnet.npy', feas)
        f = open('calib_images.txt', 'w')
        f.write('\n'.join(jpg_lst))
        f.close()
