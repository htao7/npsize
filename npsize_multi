import cv2
import numpy as np
import os

def nothing(x):
    pass

def calc_mag():
    sb_list = [100,200,500,1000,2000]
    img_scalebar = []
    img_scalebar.append(cv2.imread(dirpath + "\mag\\100nm.png",0))
    img_scalebar.append(cv2.imread(dirpath + "\mag\\200nm.png",0))
    img_scalebar.append(cv2.imread(dirpath + "\mag\\500nm.png",0))
    img_scalebar.append(cv2.imread(dirpath + "\mag\\1um.png",0))
    img_scalebar.append(cv2.imread(dirpath + "\mag\\2um.png",0))

    img_mag = img[2500:2600,3100:3296] #magnum image
    #cv2.imwrite('2um.png',img_mag)
    score_max = 0
    magi = 0
    for i,sb in enumerate(sb_list):
        res = cv2.matchTemplate(img_mag,img_scalebar[i],cv2.TM_CCOEFF)
        (_,score,_,_) = cv2.minMaxLoc(res)
        if score >= score_max:
            score_max = score
            magi = sb
    img_sb = img[2475:2485,1600:3296] #scalebar image
    ret,img_sb = cv2.threshold(img_sb,50,255,cv2.THRESH_BINARY_INV)
    _,sbcont,_ = cv2.findContours(img_sb,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    mag = float(magi)/(sbcont[0][0][0][0]-sbcont[10][0][0][0])
    return mag

def findsphere():
    pass

def findcube():
    if w > 20 and h/w <1.2 and area*mag**2/(w*h)>0.9:
        cv2.drawContours(im, [box], 0, (0,255,0), 3)
        return 1

def findrod():
    if w > 20 and h/w >3 and area*mag**2/(w*h)>0.8:
        cv2.drawContours(im, [box], 0, (0,255,0), 3)
        return 1
    
dirpath = os.getcwd()
nptype = -1 #nanoparticle type
rodh = 0
rodw = 0
rodn = 0

for foldername in os.listdir(dirpath):
    if foldername.startswith('sphere'):
        nptype = 0 
    elif foldername.startswith('cube'):
        nptype = 1
    elif foldername.startswith('rod'):
        nptype = 2
    for filename in os.listdir(dirpath + '\\' + foldername):
        print (filename)
        if filename.endswith('.jpg') or filename.endswith('.tif'):
            img0 = cv2.imread(dirpath + '\\' + foldername + '\\' + filename)
            img = cv2.cvtColor(img0,cv2.COLOR_BGR2GRAY)
            r,c = img.shape
            mag = calc_mag()
            img_blur = cv2.GaussianBlur(img,(5,5),0)
            cv2.namedWindow('dst')
            cv2.createTrackbar('Thresh','dst',0,255,nothing)
            threshflag = 0
            while(True):
                thresh = cv2.getTrackbarPos('Thresh','dst')
                if thresh != threshflag:
                    ret,img_bw = cv2.threshold(img_blur,thresh,255,cv2.THRESH_BINARY_INV)
                    _,cont,_= cv2.findContours(img_bw,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                    im = np.copy(img0)
                    width = 0
                    height = 0
                    count = 0
                    for conti in cont:
                        #cv2.drawContours(im, [conti], 0, (0,0,255), 2)
                        rect = cv2.minAreaRect(conti)
                        area = cv2.contourArea(conti)
                        box = np.int0(cv2.boxPoints(rect))
                        #cv2.putText(im,str(rect[1]),tuple(int(i) for i in rect[0]),\
                        #            cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),2,cv2.LINE_AA)
                        w = min(rect[1])*mag
                        h = max(rect[1])*mag
                        isnp = 0
                        if nptype == 0:
                            isnp = findsphere()
                        elif nptype == 1:
                            isnp = findcube()
                        elif nptype == 2:
                            isnp = findrod()
                        if isnp == 1:
                            width += w
                            height += h
                            count += 1
                    if count > 0:
                            print ('w='+str(width/count)+'\nh='+str(height/count)+'\n'+str(count)+'\n')
                    im_resize = cv2.resize(im,(int(c/4),int(r/4)),interpolation = cv2.INTER_AREA)
                    cv2.imshow('dst',im_resize)
                    threshflag = thresh
                k = cv2.waitKey(10) & 0xFF
                if k == ord('n'):
                    rodw += width
                    rodh += height
                    rodn += count
                    print ('Until now:')
                    print ('w='+str(rodw/rodn)+'\nh='+str(rodh/rodn)+'\nnum='+str(rodn)+'\n')
                    cv2.destroyAllWindows()
                    break
                if k == 27:
                    cv2.destroyAllWindows()
                    exit()
cv2.waitKey(0)
