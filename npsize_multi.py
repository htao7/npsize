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
    img_sb = img[2475:2485,1600:3296] # scale bar image
    ret,img_sb = cv2.threshold(img_sb,50,255,cv2.THRESH_BINARY_INV)
    _,sbcont,_ = cv2.findContours(img_sb,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    mag = float(magi)/(sbcont[0][0][0][0]-sbcont[10][0][0][0]) # distance between first and last bar (11 in total)
    return mag

def findsphere():
    pass

def findcube():
    if w > 20 and h/w <1.2 and area*mag**2/(w*h)>0.9: # width, aspect ratio and squareness
        cv2.drawContours(im, [box], 0, (0,255,0), 3)
        return 1

def findrod():
    if w > 20 and h/w >3 and area*mag**2/(w*h)>0.8: # width, aspect ratio and squareness
        cv2.drawContours(im, [box], 0, (0,255,0), 3)
        return 1
    
dirpath = os.getcwd()
nptype = -1 # nanoparticle type (0: sphere, 1: cube, 2: rod)
nph = 0 # height of np
npw = 0 # width of np
npn = 0 # count of np
kernel = np.ones((5,5),np.uint8)


for foldername in os.listdir(dirpath):
    if foldername.startswith('sphere'):
        nptype = 0 
    elif foldername.startswith('cube'):
        nptype = 1
    elif foldername.startswith('rod'):
        nptype = 2
    for filename in os.listdir(dirpath + '\\' + foldername):
        if filename.endswith('.jpg') or filename.endswith('.tif'):
            img0 = cv2.imread(dirpath + '\\' + foldername + '\\' + filename)
            img = cv2.cvtColor(img0,cv2.COLOR_BGR2GRAY)
            r,c = img.shape
            mag = calc_mag()
            img_blur = cv2.GaussianBlur(img,(5,5),0)
            cv2.namedWindow('dst')
            cv2.createTrackbar('Thresh','dst',0,100,nothing) # threshhold of image
            #cv2.createTrackbar('Dist','dst',0,100,nothing)
            threshflag = 0
            distflag = 0
            while(True):
                thresh = cv2.getTrackbarPos('Thresh','dst')
                #dist = cv2.getTrackbarPos('Dist','dst')
                if thresh != threshflag: # only calculate when threshhold changes
                    ret,img_bw = cv2.threshold(img_blur,20+thresh,255,cv2.THRESH_BINARY_INV)
                    
                    # watershed separation, not good
                    #img_bw = cv2.morphologyEx(img_bw,cv2.MORPH_OPEN,kernel,iterations = 2)
                    #sure_bg = cv2.dilate(img_bw,kernel,iterations = 1)
                    #dist_transform = cv2.distanceTransform(img_bw,cv2.DIST_L2,5)
                    #ret, sure_fg = cv2.threshold(dist_transform,dist,255,cv2.THRESH_BINARY)
                    #sure_fg = np.uint8(sure_fg)
                    #unknown = cv2.subtract(sure_bg,sure_fg)
                    #ret, markers = cv2.connectedComponents(sure_fg)
                    #markers = markers+1
                    #markers[unknown == 255] = 0
                    #markers = cv2.watershed(img0,markers)
                    #img_bw[markers == -1] = 0
                    #img_bw_resize = cv2.resize(img_bw,(800,600),interpolation = cv2.INTER_AREA)
                    #cv2.imshow('bw',img_bw_resize)
                    
                    _,cont,_= cv2.findContours(img_bw,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                    im = np.copy(img0)
                    width = 0
                    height = 0
                    count = 0
                    for conti in cont:
                        #cv2.drawContours(im, [conti], 0, (0,0,255), 2)
                        rect = cv2.minAreaRect(conti) # minimal rectangle around np
                        area = cv2.contourArea(conti)
                        box = np.int0(cv2.boxPoints(rect))
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
                            print ('n='+str(count)+'\n')
                    im_resize = cv2.resize(im,(800,600),interpolation = cv2.INTER_AREA)
                    cv2.imshow('dst',im_resize)
                    threshflag = thresh
                    #distflag = dist
                k = cv2.waitKey(10) & 0xFF
                if k == ord('n'):
                    npw += width
                    nph += height
                    npn += count
                    print ('Until now:')
                    if nptype == 0:
                        print ('r='+str((npw+nph)/2/npn)+'\nnum='+str(npn)+'\n')
                    elif nptype == 1:
                        print ('d='+str((npw+nph)/2/npn)+'\nnum='+str(npn)+'\n')
                    elif nptype == 2:
                        print ('w='+str(npw/npn)+'\nh='+str(nph/npn)+'\nnum='+str(npn)+'\n')
                    cv2.destroyAllWindows()
                    break
                if k == 27:
                    cv2.destroyAllWindows()
                    exit()
cv2.waitKey(0)
