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


def create_masking(image): 

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('gray',gray)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    #cv2.imshow('blur',gray)
    #binary
    ret,thresh1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
    return thresh1

def extract_shirt(filename):
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
    
    area = []
    loc = []
    for c in cnts:
        area.append(cv2.contourArea(c))
        loc.append(cv2.boundingRect(c))
    
    max_area = np.argmax(area)
    coord = loc[max_area]
    x,y,w,h = coord
    orig = image.copy()
    cv2.rectangle(orig,(x,y),(x+w,y+h),(0,0,225 ),2)
    return orig,coord

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


def main(filename_customer,filename_seller):
    
    #read image
    im_seller = cv2.imread(filename_seller)
    im_cust = cv2.imread(filename_customer)
    
    #get bbox coordinat from t-shirt
    im1,coord_jual = extract_shirt(filename_seller)
    im2,coord_customer = extract_shirt(filename_customer)
    
    #crop bbox from original image
    crop_seller = get_position(im_seller,coord_jual)
    crop_cust = get_position(im_cust,coord_customer)
    
    #resize to customer image
    crop_seller_resize = im_resize(crop_cust,crop_seller)

    #create masking seller image
    crop_seller_resize_masking = create_masking(crop_seller_resize)
    inv_crop_seller_resize_masking = cv2.bitwise_not(crop_seller_resize_masking)
    
    bg = cv2.bitwise_and(crop_cust,crop_cust,mask=crop_seller_resize_masking)
    fg = cv2.bitwise_and(crop_seller_resize,crop_seller_resize,mask = inv_crop_seller_resize_masking)
    
    final = cv2.add(bg,fg)
    result = im_cust[coord_customer[1]:coord_customer[1]+coord_customer[3],coord_customer[0]:coord_customer[0]+coord_customer[2]] = final
    cv2.imshow('',result)
    return result

if __name__=='__main__':
    image_seller = 'tes_image10.jpg'
    image_customer = 'tes_image7.jpg'
    main(image_customer,image_seller)
        
