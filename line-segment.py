import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
import math
import time
from sklearn.cluster import MeanShift, estimate_bandwidth



def getLins(img, center_points,number_windows,window_half_width):
    img_h, img_w = img.shape[:2]
    
    window_height = math.floor(img_h / number_windows)
    
    #所有白色的点的位置
    nonzero = img.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])
        
    lane_lines = []

    
    start = 0
    #按行循环所有行
    for row in range(number_windows):
        lane_lines_points_x = 0
        lane_lines_points_y = 0
        last_offset = 0
        
        points = []

        for c_points in center_points:
            if len(c_points) > 0:
                if c_points[0][0] == row:
                    points = c_points
                    break

        #点存在并且是第一次
        if len(points)>0:
            
            if len(lane_lines) == 0:
                for i_point in range(len(points)):
                    lane_lines.append([])
                    lane_lines[i_point].append([points[i_point][1],points[i_point][2]])
            else:
                #有点的行
                for line_index in range(len(lane_lines)):
                    lane_len = len(lane_lines[line_index])
                    if lane_len > 1:
                        last_offset = lane_lines[line_index][lane_len-1][0] - lane_lines[line_index][lane_len-2][0]
                        
                        window_y_low = img_h - (row + 1) * window_height
                        window_y_high = img_h - row * window_height
                        window_x_low = int(lane_lines[line_index][lane_len-1][0] - window_half_width  + last_offset)
                        window_x_high = int(lane_lines[line_index][lane_len-1][0] + window_half_width + last_offset)
                        
                        # cv2.rectangle(img, (window_x_low, window_y_low), (window_x_high, window_y_high),
                        #                           (0, 255, 0), 2);

                        for point in points:
                            point_x = point[1]
                            point_y = point[2]
                            if point_x > window_x_low and point_x < window_x_high and point_y > window_y_low and point_y < window_y_high:
                                lane_lines[line_index].append([point_x,point_y])
                                points.remove(point)
                                continue
                    else:
                        window_y_low = img_h - (row + 1) * window_height
                        window_y_high = img_h - row * window_height
                        window_x_low = int(lane_lines[line_index][lane_len-1][0] - window_half_width + last_offset)
                        window_x_high = int(lane_lines[line_index][lane_len-1][0] + window_half_width + last_offset)

                        # cv2.rectangle(img, (window_x_low, window_y_low), (window_x_high, window_y_high),
                        #               (0, 255, 0), 2);

                        for point in points:
                            point_x = point[1]
                            point_y = point[2]
                            if int(point_x) > window_x_low and int(point_x) < window_x_high and int(point_y) > window_y_low and int(point_y) < window_y_high:
                                lane_lines[line_index].append([point_x,point_y])
                                points.remove(point)
                                continue

                #如果有单独的点
                for point in points:
                    lane_lines.append([])
                    lane_lines[len(lane_lines)-1].append([point[1],point[2]])
                                
        else:
            #已经有线，没有点的行，预估点
            for line in lane_lines:

                lane_len = len(line)
                last_offset = 0
                
                if lane_len > 1:
                    last_offset = line[lane_len-1][0] - line[lane_len-2][0]
                    lane_lines_points_x = line[lane_len - 1][0] + last_offset
                    lane_lines_points_y = img_h - row * window_height - window_height / 2

                    line.append([lane_lines_points_x, lane_lines_points_y])





                else:
                    lane_lines_points_x = line[lane_len-1][0]
                    lane_lines_points_y = img_h - row  * window_height - window_height/2
                    
                    lane_lines[line_index].append([lane_lines_points_x,lane_lines_points_y])
                    
    print (lane_lines)

    for linee in lane_lines[0]:
        cv2.circle(img,
                   (int(linee[0]),
                    int(linee[1]))
                   , 5, (255, 200 + line_index, line_index), -1)
    plt.figure("dog")
    plt.imshow(img)
    plt.show()

# points =  [
#     [[3., 2.15384615, 212]],
#     [[4., 4,   202],[  4.,590,   3.204]],
#     [[ 5.  ,  15,   193], [  5. , 582,   195]]
#     ]

points = [[[3.        , 2.15384615, 212.76923077]],
 [[  4.        , 591.66071429,   202.98214286],
       [  4.        ,   9.20915033,   203.67320261]],
 [[  5.        ,  15.82026144,   194.04575163],
       [  5.        , 582.61454545,   194.47272727]],
 [[  6.        ,  28.99232737,   184.56777494],
       [  6.        , 572.96629213,   184.55805243]],
 [[  7.        ,  47.96031746,   174.54497354],
       [  7.        , 563.2481203 ,   174.45864662]],
 [[  8.        ,  63.26344086,   164.5       ],
       [  8.        , 554.10810811,   164.61003861]],
 [[  9.        ,  83.19512195,   154.44173442],
       [  9.        , 543.42023346,   154.54474708]],
 [[ 10.        , 101.65317919,   144.5       ],
       [ 10.        , 533.40392157,   144.45098039]],
 [[ 11.        , 118.89285714,   134.6875    ],
       [ 11.        , 525.60986547,   134.74887892]],
 [[ 12.        , 136.7124183 ,   124.58496732],
       [ 12.        , 517.375     ,   124.495     ]],
 [[ 13.        , 157.50328947,   114.50657895],
       [ 13.        , 509.73305085,   114.51271186]],
 [[ 14.        , 175.19708029,   104.62408759],
       [ 14.        , 500.36563877,   104.49339207],
       [ 14.        , 795.17647059,   101.52941176]],
 [[ 15.        , 325.08130081,   94.40243902]],
 [[ 16.        , 308.83632287,  84.81390135],
       [ 16.        , 656.88941176,   84.72470588]],
 [[ 17.        , 229.28846154,   74.59615385],
       [ 17.        , 725.19230769,   74.55128205]],
 [[ 18.        , 685.61864407,   64.45762712],
       [ 18.        , 246.51271186,   64.60169492]],
 [[ 19.        , 647.52136752,   54.38888889],
       [ 19.        , 265.63181818,   54.59090909]],
 [[ 20.        , 568.41836735,  44.09183673],
       [ 20.        , 322.5261324 ,   44.14982578]],
 [[ 21.        , 526.79878049,   34.60365854],
       [ 21.        , 352.35825545,   34.62305296]],
 [[ 22.        , 356.69721116,   24.98406375],
       [ 22.        , 496.51086957,   25.33152174]],
 [[ 23.        , 348.71942446,   14.71223022],
       [ 23.        , 427.60465116,  14.81395349],
       [ 23.        , 523.94736842,   17.73684211]]]


img = cv2.imread("3.jpeg")
getLins(img, points,25,50)
