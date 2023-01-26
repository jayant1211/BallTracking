import cv2 
import numpy as np
from collections import Counter
import time

'''
EMPIRICAL DIMENSIONS FOR QUADRANTS
1918, 1080

q3 - 770,0 1220,520
q4 - 1220,0 1740, 520
q2 - 770,520 1220,1040
q1  - 1220,520 1740,1040 

width of q3 q2 = 450
width of q4 q1 = 520
height of all quadrants = 520
center 1220,520
'''


vid = cv2.VideoCapture('AI Assignment video.mp4')
fps = vid.get(cv2.CAP_PROP_FPS)
print(fps)
ctr = 1
qf1 = []
qf2 = []
qf3 = []
qf4 = []

qf = ["Exited","Exited","Exited","Exited"]
i=1

with open('res_Method1_usingThresholding.txt', 'w') as f:
    t_start = time.time()
    while True:
        _, frame = vid.read()
        if not _: break

        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        ret,thresh1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
        thresh1=cv2.dilate(thresh1,(5,5))
        #at start
        #img[y:y+h, x:x+w]
        '''
        q3 - 770,0 1220,520
        q4 - 1220,0 1740, 520
        q2 - 770,520 1220,1040
        q1  - 1220,520 1740,1040 
        '''
        if i:
            stock_q1 = thresh1[520+50:1040-50,1220+50:1740-50]
            stock_q2 = thresh1[520+50:1040-50,770+50:1220-50]
            stock_q3 = thresh1[0+50:520-50,770+50:1220-50]
            stock_q4 = thresh1[0+50:520-50,1220+50:1740-50]
            i=0
        
        #check img 
        q1 = thresh1[520+50:1040-50,1220+50:1740-50]
        q2 = thresh1[520+50:1040-50,770+50:1220-50]
        q3 = thresh1[0+50:520-50,770+50:1220-50]
        q4 = thresh1[0+50:520-50,1220+50:1740-50]
        
        d1 = cv2.absdiff(stock_q1, q1)
        s1 = d1.sum()

        d2 = cv2.absdiff(stock_q2, q2)
        s2 = d2.sum()

        d3 = cv2.absdiff(stock_q3, q3)
        s3 = d3.sum()

        d4 = cv2.absdiff(stock_q4, q4)
        s4 = d4.sum()

        s1=s1//1000
        s2=s2//1000
        s3=s3//1000
        s4=s4//1000
        print(s1,s2,s3,s4)
        ctr+=1
        modulo=int(fps)
        if ctr%modulo==0:
            #q1
            if s1>1999:
                s1_status="Entered"
            else: s1_status="Exited"
            print(s1_status)
            if qf[0]!=s1_status:
                qf[0]=s1_status
                f.write('{}, Quadrant 1, Unknown Colour,{}\n'.format(time.time()-t_start,s1_status))
            
            #q2
            if s2>1999:
                s2_status="Entered"
            else: s2_status="Exited"
            if qf[1]!=s2_status:
                qf[1]=s2_status
                f.write('{}, Quadrant 2, Unknown Colour,{}\n'.format(time.time()-t_start,s2_status))

            #q3
            if s3>1999:
                s3_status="Entered"
            else: s3_status="Exited"
            if qf[2]!=s3_status:
                qf[2]=s3_status
                f.write('{}, Quadrant 3, Unknown Colour,{}\n'.format(time.time()-t_start,s3_status))

            #q4
            if s4>1999:
                s4_status="Entered"
            else: s4_status="Exited"
            if qf[3]!=s4_status:
                qf[3]=s4_status
                f.write('{}, Quadrant 4, Unknown Colour,{}\n'.format(time.time()-t_start,s4_status))

        frame=cv2.resize(frame,(600,400))
        thresh1=cv2.resize(thresh1,(600,400))
        cv2.imshow("Circles",frame)
        #cv2.imshow("Gray",gray)
    
        cv2.imshow("Thresh",thresh1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    vid.release()
    cv2.destroyAllWindows()
    elapsed = time.time()-t_start
    f.write("Elapsed time: " + time.strftime("%H:%M:%S.{}".format(str(elapsed % 1)[2:])[:15], time.gmtime(elapsed)))
f.close()
