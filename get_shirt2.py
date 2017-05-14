# -*- coding: utf-8 -*-
"""
Created on Thu May 11 21:12:49 2017

@author: adam
"""
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2


def extract_shirt(filename):
    """
    filename : image location 
    this function create or find shirt location
    
    """
    
    #load image
    image = cv2.imread(filename)
    #convert to gray
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('gray',gray)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    #cv2.imshow('blur',gray)
    #binary
    ret,thresh1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    #cv2.imshow('binary',thresh1)
    
    #edge + dilation +erotion
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    #cv2.imshow('tes2',edged)
    
    #find contours
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    
    (cnts, _) = contours.sort_contours(cnts)
    
    for c in cnts:
        #print c
    	# if the contour is not sufficiently large, ignore it
        if cv2.contourArea(c) < 100:
            print 'c failed',cv2.contourArea(c)
            continue
        print 'c ok',cv2.contourArea(c)
        
        orig = image.copy()
        (x, y, w, h) = cv2.boundingRect(c)
        
        print 'x,y,w,h',x,y,w,h,'shape',image.shape  #x,y,width,height
        cv2.rectangle(orig,(x,y),(x+w,y+h),(0,0,225 ),2)
        #cv2.imshow('orig',orig)
        #cv2.waitKey(0)
        return orig,(x,y,w,h)

def get_position(im,coord):
    result = im[coord[1]:coord[1]+coord[3],coord[0]:coord[0]+coord[2]]
    return result

def im_resize(im1,im2):
    """
    im1 : image customer
    im2 : image seller
    
    resize image seller to image customer
    output is image seller with size same as image customer
    """
    h,w,d = im1.shape
    result = cv2.resize(im2,(w,h))
    return result

def create_masking(image): 

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('gray',gray)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    #cv2.imshow('blur',gray)
    #binary
    ret,thresh1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    return thresh1

def create_invert_masking(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('gray',gray)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    #cv2.imshow('blur',gray)
    #binary
    ret,thresh1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    thresh1 = (255-thresh1)
    return thresh1

def apply_mask(im1,im2):
    """
    im1: RGB image 
    im2: masking image
    
    """
    b, g, r = cv2.split(im1)
    result = im1.copy()
    result[:,:,0] = cv2.bitwise_and(b,b,mask = im2)
    result[:,:,1] = cv2.bitwise_and(g,g,mask = im2)
    result[:,:,2] = cv2.bitwise_and(r,r,mask = im2)
    return result

def apply_mask_rgb(im1,im2):
    """
    im1 : image customer
    im2 : image seller after masking 
    
    apply masking from image seller to customer
    """
    b,g,r = cv2.split(im2)
    result = im1.copy()
    result[:,:,0] = cv2.bitwise_or(result[:,:,0],result[:,:,0],mask=b)
    result[:,:,1] = cv2.bitwise_or(result[:,:,1],result[:,:,1],mask=g)
    result[:,:,2] = cv2.bitwise_or(result[:,:,2],result[:,:,2],mask=r)
    return result
    
image_jual = 'tes_image10.jpg'
image_customer = 'tes_image7.jpg'
im1,coord_jual = extract_shirt(image_jual)
im2,coord_customer = extract_shirt(image_customer)


#tempel image jual ke customer 
im_seller = cv2.imread(image_jual)
im_cust = cv2.imread(image_customer)
#==============================================================================
# cv2.imshow('im_seller',im_seller)
# cv2.imshow('im_cust',im_cust)
#==============================================================================

crop_seller = get_position(im_seller,coord_jual)
crop_cust = get_position(im_cust,coord_customer)
#==============================================================================
# cv2.imshow('crop_seller',crop_seller)
# cv2.imshow('crop_cust',crop_cust)
#==============================================================================

crop_seller_resize = im_resize(crop_cust,crop_seller)
#cv2.imshow('crop_jual_resize',crop_seller_resize)
print 'shape jual crop',crop_seller_resize.shape,crop_cust.shape

crop_seller_resize_masking = create_invert_masking(crop_seller_resize)
crop_cust_masking = create_masking(crop_cust)
#==============================================================================
# cv2.imshow('masking crop seller',crop_seller_resize_masking)
# cv2.imshow('masking customer',crop_cust_masking)
# 
#==============================================================================
crop_seller_resize_after_masking = apply_mask(crop_seller_resize,crop_seller_resize_masking)
crop_cust_after_masking = apply_mask(crop_cust,crop_cust_masking)
#cv2.imshow('after masking seller',crop_seller_resize_after_masking)
#cv2.imshow('after masking cust',crop_cust_after_masking)
#next split rgb each image 
#apply to masking image 
#and swap image

join_mask = apply_mask_rgb(crop_seller_resize,crop_cust_after_masking)
cv2.imshow('join mask1',crop_seller_resize)
cv2.imshow('join mask2',crop_cust_after_masking)
cv2.imshow('join mask3',join_mask)
