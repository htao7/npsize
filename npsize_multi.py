import cv2
import numpy as np
import os
from matplotlib import pyplot as plt

IMG_R = 4
FONT = cv2.FONT_HERSHEY_SIMPLEX

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

    img_mag = img[2500:2600,3100:3296] # mag num image
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
    mag = float(magi)/(sbcont[0][0][0][0]-sbcont[10][0][0][0])
    return mag

def FindSphere():
    center = (int(x),int(y))
    r = int(r)
    if w > 20 and area/(3.14*(w/2)**2)>0.85:
        cv2.circle(im,center,r,(0,255,0),2)
        cv2.putText(im,str(npn+count),center,FONT,1,(0,255,0),2,cv2.LINE_AA)
        size_img.append(w)
        return 1
    else:
        return 0
    

def FindCube():
    if w > 30 and h/w <1.2 and area/(w*h)>0.88:
        cv2.drawContours(im, [box], 0, (0,255,0), 2)
        center = (int(rect[0][0]),int(rect[0][1]))
        cv2.putText(im,str(npn+count),center,FONT,1,(0,255,0),2,cv2.LINE_AA)
        size_img.append((h+w)/2)
        return 1
    else:
        return 0

def FindRod():
    if w > 15 and h/w >3 and area/(w*h)>0.8:
        cv2.drawContours(im, [box], 0, (0,255,0), 2)
        center = (int(rect[0][0]),int(rect[0][1]))
        cv2.putText(im,str(npn+count),center,FONT,1,(0,255,0),2,cv2.LINE_AA)
        size_img.append((h,w))
        return 1
    else:
        return 0

def enlarge(event,x,y,flags,param):
    global ix,iy,captureflag,x1,x2,y1,y2

    if event == cv2.EVENT_LBUTTONDOWN:
        captureflag = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if captureflag == True:
            x1 = min(ix,x)
            x2 = max(ix,x)
            y1 = min(iy,y)
            y2 = max(iy,y)

    elif event == cv2.EVENT_LBUTTONUP:
        captureflag = False

def ExportSize():
    size_file = open(dirpath + '\\' + foldername + '\\npsize.txt','w')
    if nptype == 2:
        size_file.write("%s \n%s \n%s \n\n" % \
                        ('AVG_length = ' + str(nph/npn),'AVG_width = ' + str(npw/npn),'AVG_ar = ' + str(nph/npw)))
    else:
        size_file.write("%s \n\n" % \
                        ('AVG_length/diameter = ' + str((npw+nph)/2/npn)))
    for i,size in enumerate(size_all):
        if nptype == 2:
            size_file.write("%s %s %s\n" % (i,size[0],size[1]))
        else:
            size_file.write("%s %s\n" % (i,size))
    
    size_file.close()


dirpath = os.getcwd()
nptype = -1 #nanoparticle type

for foldername in os.listdir(dirpath):
    if foldername.startswith('sphere'):
        nptype = 0 
    elif foldername.startswith('cube'):
        nptype = 1
    elif foldername.startswith('rod'):
        nptype = 2
    else:
        continue
    size_all = []
    nph = 0
    npw = 0
    npn = 0
    captureflag = False
    for filename in os.listdir(dirpath + '\\' + foldername):
        if filename.endswith('.jpg') or filename.endswith('.tif'):
            img0 = cv2.imread(dirpath + '\\' + foldername + '\\' + filename)
            img = cv2.cvtColor(img0,cv2.COLOR_BGR2GRAY)
            x1 = y1 = 0
            x2 = y2 = 1
            r,c = img.shape # 2788 * 3296
            r2 = int(r/IMG_R)
            c2 = int(c/IMG_R)
            mag = calc_mag()
            #img_blur = cv2.GaussianBlur(img,(5,5),0)
            img_blur = cv2.medianBlur(img[0:2450,0:3296],5)
            #plt.hist(img_blur.ravel(),256,(0,255))
            #plt.show()
            cv2.namedWindow('dst')
            cv2.createTrackbar('Thresh','dst',50,100,nothing)
            cv2.setMouseCallback('dst',enlarge)
            threshflag = -1
            while(True):
                thresh = cv2.getTrackbarPos('Thresh','dst')
                if thresh != threshflag:
                    otsu,img_bw = cv2.threshold(img_blur,thresh,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
                    ret,img_bw = cv2.threshold(img_blur,otsu - 60 + thresh,255,cv2.THRESH_BINARY_INV)
                    #print (ret)
                    _,cont,_= cv2.findContours(img_bw,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                    im = np.copy(img0)
                    width = 0
                    height = 0
                    count = 0
                    size_img = []
                    for conti in cont:
                        #cv2.drawContours(im, [conti], 0, (0,0,255), 2)
                        rect = cv2.minAreaRect(conti)
                        area = cv2.contourArea(conti)*mag**2
                        box = np.int0(cv2.boxPoints(rect))
                        w = min(rect[1])*mag
                        h = max(rect[1])*mag
                        isnp = 0
                        if nptype == 0:
                            (x,y),r = cv2.minEnclosingCircle(conti)
                            h = w = 2*r*mag
                            isnp = FindSphere()
                        elif nptype == 1:
                            isnp = FindCube()
                        elif nptype == 2:
                            isnp = FindRod()
                        if isnp == 1:
                            width += w
                            height += h
                            count += 1
                    if count > 0:
                            print ('n=' + str(count) + '\n')
                    threshflag = thresh
                im_resize = cv2.resize(im,(c2,r2),interpolation = cv2.INTER_AREA)
                cv2.rectangle(im_resize,(x1,y1),(x2,y2),(0,0,255),1)
                cv2.imshow('dst',im_resize)
                if captureflag == False:
                    im_inset = im[y1*IMG_R:y2*IMG_R,x1*IMG_R:x2*IMG_R]
                    cv2.imshow('inset',im_inset)
                k = cv2.waitKey(10) & 0xFF
                if k == ord('n'):
                    size_all.extend(size_img)
                    cv2.imwrite(dirpath + '\\' + foldername + '\\' + \
                                    os.path.splitext(filename)[0] + '_labelled.jpg',im)
                    npw += width
                    nph += height
                    npn += count
                    if npn == 0:
                        break
                    print ('Until now:')
                    if nptype == 2:
                        print ('w=' + str(npw/npn) + '\nh=' + str(nph/npn) + '\nnum=' + str(npn) + '\n')
                    else:
                        print ('l(/d)=' + str((npw+nph)/2/npn) + '\nnum=' + str(npn) + '\n')
                        
                    cv2.destroyAllWindows()
                    break
                elif k == 27:
                    cv2.destroyAllWindows()
                    exit()
    ExportSize()
    
cv2.waitKey(0)
