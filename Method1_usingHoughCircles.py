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
(x,y) = (600,400)
center = (int((1220/1920)*x),int((520/1080)*y))
width_left_quaters = center[0] - int((450/1920)*x)
width_right_quaters = center[0] + int((520/1920)*x)
height_quaters = int((520/1080)*y)

#bounds
#point x,y
'''
if x<center[0] and x>width_left_quaters:
    #left_quarter:
    if y<center[1]:
        #q3
    if y>center[1] and y<height_quaters:
        #q2

if x>center[0] and x<width_right_quaters:
    #right_quaters:
    if y<center[1]:
        #q4
    if y>center[1] and y<height_quaters:
        #q1
'''

vid = cv2.VideoCapture('AI Assignment video.mp4')
fps = vid.get(cv2.CAP_PROP_FPS)
print(fps)

p_circle = None
#dist = lambda x1,y1,x2,y2: (x1-x2)**2 - (y1-y2)**2
print("Center: ",center)
ctr = 1
qf1 = []
qf2 = []
qf3 = []
qf4 = []

qf = ["Exited","Exited","Exited","Exited"]

with open('res_Method1_usingHoughCircles.txt', 'w') as f:
    t_start = time.time()

    while True:
        _, frame = vid.read()
        if not _: break

        frame = cv2.resize(frame,(x,y))

        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(7,7),0)
        ret,thresh1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
        thresh1=cv2.dilate(thresh1,(5,5))
        circles = cv2.HoughCircles(blur,cv2.HOUGH_GRADIENT,1.2,100,param1 = 100,param2=30,
                                    minRadius= 1,maxRadius=40)
        
        '''if circles is not None:
            circles = np.uint16(np.around(circles))
            cur = None
            for i in circles[0,:]:
                if cur is None: cur =i
                if p_circle is not None:
                    if dist(cur[0],cur[1],p_circle[0],p_circle[1]) <= dist(i[0],i[1],p_circle[0],p_circle[1]): 
                        cur=i
            print(cur)
            cv2.circle(frame,(cur[0],cur[1]),1,(0,100,100),3)
            cv2.circle(frame,(cur[0],cur[1]),cur[2],(255,0,255),3)
            p_circle = cur'''

    
        if circles is not None:
            circles = np.uint16(np.around(circles))
            # Draw the circles
            for i in circles[0,:]:
                # draw the outer circle
                cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)
                (x_c,y_c) = (i[0],i[1])
                #quadrant flags
                #event
                #is in q3:
                if x_c<center[0] and x_c>width_left_quaters and y_c<center[1]:
                    qf3.append("Entered")
                    c3=frame[i[1]+5,i[0]+5]
                else:
                    qf3.append("Exited")
                
                #is in q2
                if x_c<center[0] and x_c>width_left_quaters and y_c>center[1] and y_c<center[1]+height_quaters:
                    qf2.append("Entered")
                    c2=frame[i[1]+5,i[0]+5]
                else:
                    qf2.append("Exited")

                #is in q4
                if x_c>center[0] and x_c<width_right_quaters and y_c<center[1]:
                    qf4.append("Entered")
                    c4=frame[i[1]+5,i[0]+5]
                else:
                    qf4.append("Exited")
                
                #is in q1
                if x_c>center[0] and x_c<width_right_quaters and y_c>center[1] and y_c<center[1]+height_quaters:
                    qf1.append("Entered")
                    c1=frame[i[1]+5,i[0]+5]
                else:
                    qf1.append("Exited")       

                
                ctr=ctr+1
                modulo = int(fps)
                if ctr%modulo==0:
                    num = qf1.count("Entered")
                    prev1 = qf[0]
                    if num>=(modulo/3):
                        qf[0] = "Entered"
                    else: qf[0] = "Exited"
                    if prev1!=qf[0]:
                        print("Ball {} in Quarter 1 at time".format(qf[0]))
                        f.write('{}, Quadrant 1,{},{}\n'.format(time.time()-t_start,c1,qf[0]))
                    qf1.clear()

                    num = qf2.count("Entered")
                    prev2 = qf[1]
                    if num>=(modulo/3):
                        qf[1] = "Entered"
                    else: qf[1] = "Exited"
                    if prev2!=qf[1]:
                        print("Ball {} in Quarter 2 at time".format(qf[1]))
                        f.write('{}, Quadrant 2,{},{}\n'.format(time.time()-t_start,c2,qf[1]))
                    qf2.clear()

                    num = qf3.count("Entered")
                    prev3 = qf[2]
                    if num>=(modulo/3):
                        qf[2] = "Entered"
                    else: qf[2] = "Exited"
                    if prev3!=qf[2]:
                        print("Ball {} in Quarter 3 at time".format(qf[2]))
                        f.write('{}, Quadrant 3,{},{}\n'.format(time.time()-t_start,c3,qf[2]))
                    qf3.clear()

                    num = qf4.count("Entered")
                    prev4 = qf[3]
                    if num>=(modulo/3):
                        qf[3] = "Entered"
                    else: qf[3] = "Exited"
                    if prev4!=qf[3]:
                        print("Ball {} in Quarter 4 at time".format(qf[3]))
                        f.write('{}, Quadrant 4,{},{}\n'.format(time.time()-t_start,c4,qf[3]))
                    qf4.clear()


                cv2.imshow("Circles",frame)
        
        cv2.imshow("Circles",frame)
        #cv2.imshow("Gray",gray)
        #cv2.imshow("Blur",blur)
        #cv2.imshow("Thresh",thresh1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    vid.release()
    cv2.destroyAllWindows()
    elapsed = time.time()-t_start
    f.write("Elapsed time: " + time.strftime("%H:%M:%S.{}".format(str(elapsed % 1)[2:])[:15], time.gmtime(elapsed)))
f.close()


''' if x_c<center[0] and x_c>width_left_quaters:
                #left_quarter:
                if y_c<center[1]:
                    #q3
                    print("Ball of color:{} is in Quater 3".format(frame[i[1]+5,i[0]+5]))
                    #event
                    if qf[2]=="Empty":
                        qf[2] = "Entered"
                        print("Ball Entered in Quater 3")
                    if qf[2]=="Empty":
                        qf[2] = "Entered"
                        print("Ball Entered in Quater 3")
                if y_c>center[1] and y_c<center[1]+height_quaters:
                    #q2
                    print("Ball of color:{} is in Quater 2".format(frame[i[1]+5,i[0]+5]))
            if x_c>center[0] and x_c<width_right_quaters:
                #right_quaters:
                if y_c<center[1]:
                    #q4
                    print("Ball of color:{} is in Quater 4".format(frame[i[1]+5,i[0]+5]))
                if y_c>center[1] and y_c<center[1]+height_quaters:
                    #q1
                    print("Ball of color:{} is in Quater 1".format(frame[i[1]+5,i[0]+5]))'''