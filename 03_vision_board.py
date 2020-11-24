import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

class Vision():
    def __init__(self):
        # square width 55.9mm
        #self.SW = .0559
        self.SW = .3750

        # Red
        ##self.lower_range_red = np.array([0,173,156])
        ##self.self.upper_range_red = np.array([180,255,255])
        # Blue
        ##self.lower_range_blue = np.array([65,0,0])
        ##self.upper_range_blue = np.array([180,255,255])

        # Kept default colors red and blue, but actual colors are light green and light purple
        # Light green
        self.lower_range_blue = np.array([95,136,78])
        self.upper_range_blue = np.array([140,255,255])
        # Light purple
        self.lower_range_red = np.array([118,30,39])
        self.upper_range_red = np.array([180,255,255])

        # Minimum contour for recognizing blobs
        self.min_contour = 50

        # Define self.axis to display origin of board
        self.axis = np.float32([[1,0,0], [0,1,0], [0,0,-1]]).reshape(-1,3)

        # Termination self.criteria
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # Values found from camera_calibration.py in scripts directory
        self.mtx = np.float32([[833.40232692,   0,         819.7971566 ],
                          [  0,         797.82472818, 418.71156851],
                          [  0,           0,           1        ]])
        self.dist = np.float32([[ 0.17707474, -0.23145481,  0.00875303, -0.01869425,  0.12936391]])

        # Object points to create board cordinates
        self.objp = np.zeros((7*7,3), np.float32)
        self.objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)

        # Dictionary to convert index to board position from top left inner corner
        self.board_dict = {0 : [self.SW*-0.5,self.SW*-0.5], 1 : [self.SW*0.5,self.SW*-0.5], 2 : [self.SW*1.5,self.SW*-0.5], 3 : [self.SW*2.5,self.SW*-0.5], 4 : [self.SW*3.5,self.SW*-0.5], 5 : [self.SW*4.5,self.SW*-0.5], 6 : [self.SW*5.5,self.SW*-0.5], 7 : [self.SW*6.5,self.SW*-0.5],
                      8 : [self.SW*-0.5,self.SW*0.5], 9 : [self.SW*0.5,self.SW*0.5], 10: [self.SW*1.5,self.SW*0.5], 11: [self.SW*2.5,self.SW*0.5], 12: [self.SW*3.5,self.SW*0.5], 13: [self.SW*4.5,self.SW*0.5], 14: [self.SW*5.5,self.SW*0.5], 15: [self.SW*6.5,self.SW*0.5],
                      16: [self.SW*-0.5,self.SW*1.5], 17: [self.SW*0.5,self.SW*1.5], 18: [self.SW*1.5,self.SW*1.5], 19: [self.SW*2.5,self.SW*1.5], 20: [self.SW*3.5,self.SW*1.5], 21: [self.SW*4.5,self.SW*1.5], 22: [self.SW*5.5,self.SW*1.5], 23: [self.SW*6.5,self.SW*1.5],
                      24: [self.SW*-0.5,self.SW*2.5], 25: [self.SW*0.5,self.SW*2.5], 26: [self.SW*1.5,self.SW*2.5], 27: [self.SW*2.5,self.SW*2.5], 28: [self.SW*3.5,self.SW*2.5], 29: [self.SW*4.5,self.SW*2.5], 30: [self.SW*5.5,self.SW*2.5], 31: [self.SW*6.5,self.SW*2.5],
                      32: [self.SW*-0.5,self.SW*3.5], 33: [self.SW*0.5,self.SW*3.5], 34: [self.SW*1.5,self.SW*3.5], 35: [self.SW*2.5,self.SW*3.5], 36: [self.SW*3.5,self.SW*3.5], 37: [self.SW*4.5,self.SW*3.5], 38: [self.SW*5.5,self.SW*3.5], 39: [self.SW*6.5,self.SW*3.5],
                      40: [self.SW*-0.5,self.SW*4.5], 41: [self.SW*0.5,self.SW*4.5], 42: [self.SW*1.5,self.SW*4.5], 43: [self.SW*2.5,self.SW*4.5], 44: [self.SW*3.5,self.SW*4.5], 45: [self.SW*4.5,self.SW*4.5], 46: [self.SW*5.5,self.SW*4.5], 47: [self.SW*6.5,self.SW*4.5],
                      48: [self.SW*-0.5,self.SW*5.5], 49: [self.SW*0.5,self.SW*5.5], 50: [self.SW*1.5,self.SW*5.5], 51: [self.SW*2.5,self.SW*5.5], 52: [self.SW*3.5,self.SW*5.5], 53: [self.SW*4.5,self.SW*5.5], 54: [self.SW*5.5,self.SW*5.5], 55: [self.SW*6.5,self.SW*5.5],
                      56: [self.SW*-0.5,self.SW*6.5], 57: [self.SW*0.5,self.SW*6.5], 58: [self.SW*1.5,self.SW*6.5], 59: [self.SW*2.5,self.SW*6.5], 60: [self.SW*3.5,self.SW*6.5], 61: [self.SW*4.5,self.SW*6.5], 62: [self.SW*5.5,self.SW*6.5], 63: [self.SW*6.5,self.SW*6.5]}

        #print(self.board_dict)
        # Made top left inside corner the origin based on cv2.findChessboardCorners().
        # All spaces are listed going left to right and top to bottom.  (A8 first, H1 last)
        self.board_pts = np.float32([[-0.5,-0.5,0],[.5,-0.5,0],[1.5,-0.5,0],[2.5,-0.5,0],[3.5,-0.5,0],[4.5,-0.5,0],[5.5,-0.5,0],[6.5,-0.5,0],
                                [-0.5,0.5,0],[.5,0.5,0],[1.5,0.5,0],[2.5,0.5,0],[3.5,0.5,0],[4.5,0.5,0],[5.5,0.5,0],[6.5,0.5,0],
                                [-0.5,1.5,0],[.5,1.5,0],[1.5,1.5,0],[2.5,1.5,0],[3.5,1.5,0],[4.5,1.5,0],[5.5,1.5,0],[6.5,1.5,0],
                                [-0.5,2.5,0],[.5,2.5,0],[1.5,2.5,0],[2.5,2.5,0],[3.5,2.5,0],[4.5,2.5,0],[5.5,2.5,0],[6.5,2.5,0],
                                [-0.5,3.5,0],[.5,3.5,0],[1.5,3.5,0],[2.5,3.5,0],[3.5,3.5,0],[4.5,3.5,0],[5.5,3.5,0],[6.5,3.5,0],
                                [-0.5,4.5,0],[.5,4.5,0],[1.5,4.5,0],[2.5,4.5,0],[3.5,4.5,0],[4.5,4.5,0],[5.5,4.5,0],[6.5,4.5,0],
                                [-0.5,5.5,0],[.5,5.5,0],[1.5,5.5,0],[2.5,5.5,0],[3.5,5.5,0],[4.5,5.5,0],[5.5,5.5,0],[6.5,5.5,0],
                                [-0.5,6.5,0],[.5,6.5,0],[1.5,6.5,0],[2.5,6.5,0],[3.5,6.5,0],[4.5,6.5,0],[5.5,6.5,0],[6.5,6.5,0]]).reshape(-1,3)

        self.board_pts_1 = self.board_pts
        self.board_pts_2 = self.rotate_matrix(self.board_pts_1)
        self.board_pts_3 = self.rotate_matrix(self.board_pts_2)
        self.board_pts_4 = self.rotate_matrix(self.board_pts_3)
        K = self.image_callback()

    def rotate_matrix(self, mtx):
        # Outputs a new 64x1 vector but rotated by 90 degrees clockwise as if it
        # were an 8x8 matrix
        mtx2 = []
        for i in range(8):
            line  = [mtx[i],mtx[i+8],mtx[i+16],mtx[i+24],mtx[i+32],mtx[i+40],mtx[i+48],mtx[i+56]]
            line= line[::-1]
            for j in line:
                mtx2.append(j)
        return(np.array(mtx2))

    def draw_origin(self, img, corners, imgpts):
        # Draws each self.axis based on the corners found from findChessboardCorners
        corner = tuple(corners[0].ravel())
        img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
        img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
        img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
        return img

    def image_callback(self):
            # Convert received image message to OpenCv image
            frame = cv2.imread('C:\Checkers Playing Robot\AI\images\Board.jpg')
            ##cv2.imshow('frame', frame)
            ##cv2.waitKey(0)

            #  Initialize board state
            board_state =[]

            # Gray image for findChessboardCorners
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (7,7),None)

            # Initialize board image points
            board_imgpts = []

            if ret == True:
            # If chessboard corners were found

                # Output new board state in order from top left to bottom right outputing
                #   a list of strings with either "empty" or piece_color
                board_state2 = []
                for i in range(64):
                    board_state2.append('empty')

                corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),self.criteria)
                corners3 = []
                for i in corners2:
                        corners3.append(list(i.ravel()))

                # Find the rotation and translation vectors.
                _, rvecs, tvecs, inliers = cv2.solvePnPRansac(self.objp, corners2, self.mtx, self.dist)

                # Rotate order of square points to stay consistant with changing origin
                if corners3[0][0] < corners3[-1][0] and corners3[0][1] < corners3[-1][1]:
                    self.board_pts = self.board_pts_1
                    """
                    # Use if you want to output the pose relative to board cordinates
                    R,_ = cv2.Rodrigues(rvecs)
                    Rt = np.zeros((4,4))
                    Rt[0:2, 0:2] = R[0:2, 0:2]
                    Rt[3,3] = 1
                    quat = tf.transformations.quaternion_from_matrix(Rt)
                    # Populate Tranformation Matrix
                    Tcb = Pose()
                    Tcb.orientation.x = quat[0]
                    Tcb.orientation.y = quat[1]
                    Tcb.orientation.z = quat[2]
                    Tcb.orientation.w = quat[3]
                    Tcb.position.x = self.SW*tvecs[0][0]
                    Tcb.position.y = self.SW*tvecs[1][0]
                    Tcb.position.z = self.SW*tvecs[2][0]
                    print(Tcb)
                    # Now Publish Transformation Matrix
                    self.pub.publish(Tcb)
                    """
                if corners3[0][0] > corners3[-1][0] and corners3[0][1] < corners3[-1][1]:
                    self.board_pts = self.board_pts_2

                if corners3[0][0] > corners3[-1][0] and corners3[0][1] > corners3[-1][1]:
                    self.board_pts = self.board_pts_3

                if corners3[0][0] < corners3[-1][0] and corners3[0][1] > corners3[-1][1]:
                    self.board_pts = self.board_pts_4


                # Project board and self.axis points from board cord to image cord
                board_imgpts, jac2 = cv2.projectPoints(self.board_pts,rvecs,tvecs,self.mtx,self.dist)
                axis_imgpts, jac = cv2.projectPoints(self.axis,rvecs,tvecs,self.mtx,self.dist)

                # Show square centers
                for point in board_imgpts:
                    point = (point[0][0], point[0][1])
                    frame = cv2.circle(frame, point, 2, (255,0,0),2)

                # Calculate maximum distance a contour can be from a square center
                #  based on the diagonal distance of the board in the image
                board_imgpts_s = np.squeeze(board_imgpts)
                board_diag_dist = math.sqrt( ((board_imgpts_s[0][0] - board_imgpts_s[-1][0])**2) + ((board_imgpts_s[0][1] - board_imgpts_s[-1][1])**2))
                MIN_IMGPNT_DIST = board_diag_dist / 22.7

                # Find Red blobs
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                hsv = cv2.medianBlur(hsv, 5)

                hsv_red = cv2.inRange(hsv, self.lower_range_red, self.upper_range_red)

                # convert the grayscale image to binary image
                ret,thresh = cv2.threshold(hsv_red,127,255,0)
                rows = hsv.shape[0]

                # find contours in the thresholded image
                circles_red, _ = cv2.findContours(hsv_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                circle_count_red = 0
                checkers_impgpts_red = []
                for c in circles_red:
                    # compute the center of the contour
                    M = cv2.moments(c)
                    if cv2.contourArea(c) > self.min_contour:
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                        cv2.circle(frame, (cX, cY), 5, (0, 255, 255),-1)
                        circle_count_red += 1
                        checkers_impgpts_red.append([cX,cY,'red'])

                # Find blue blobs
                hsv_blue = cv2.inRange(hsv, self.lower_range_blue, self.upper_range_blue)

                # convert the grayscale image to binary image
                ret,thresh = cv2.threshold(hsv_blue,127,255,0)
                rows = hsv.shape[0]

                # find contours in the thresholded image
                circles_blue, hierarchy = cv2.findContours(hsv_blue, cv2.RETR_TREE,
                    cv2.CHAIN_APPROX_SIMPLE)
                #circles = imutils.grab_contours(circles)

                circle_count_blue = 0
                checkers_impgpts_blue = []
                for c in circles_blue:
                    # compute the center of the contour
                    M = cv2.moments(c)
                    if cv2.contourArea(c) > self.min_contour:
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                        cv2.circle(frame, (cX, cY), 5, (255, 255, 255),-1)
                        circle_count_blue += 1
                        checkers_impgpts_blue.append([cX,cY,'blue'])

                # Calculate distance to available board squares
                min_distance_list_blue = []
                for point in checkers_impgpts_blue:
                    ##distance_list = []
                    for point2 in board_imgpts:
                        point3 = point2[0]
                        distance = math.sqrt( ((point[0] - point3[0])**2) + ((point[1] - point3[1])**2))
                        ##distance_list.append(distance)
                        if distance < MIN_IMGPNT_DIST:
                            index = np.where(board_imgpts == point2)

                            ##if not [self.board_dict[index[0][0]], 'blue'] in board_state:
                            # Output index of board position to board state lists
                            ##board_state.append([self.board_dict[index[0][0]], 'blue'])
                            board_state2[index[0][0]] = 'green'
                            break
                    ##min_distance_list_blue.append(min(distance_list))

                # Calculate distance to available board squares
                ##min_distance_list_red = []
                for point in checkers_impgpts_red:
                    ##distance_list = []
                    for point2 in board_imgpts:
                        point2 = point2[0]
                        distance = math.sqrt( ((point[0] - point2[0])**2) + ((point[1] - point2[1])**2))
                        ##distance_list.append(distance)
                        if distance < MIN_IMGPNT_DIST:
                            index = np.where(board_imgpts == point2)

                            # Output index of board position to board state lists
                            ##board_state.append([self.board_dict[index[0][0]], 'red'])
                            board_state2[index[0][0]] = 'purple'
                            break
                    ##min_distance_list_red.append(min(distance_list))

                # Draw the origin
                frame = self.draw_origin(frame,corners2,axis_imgpts)

                board_state3 = ''
                for i in range(64):
                    if i == 0:
                        board_state3 = board_state2[i]
                    else:
                        board_state3 = board_state3 + ' ' + board_state2[i]
                print('boardstate3')
                print(board_state3)
                # self.pub2.publish(board_state3)

                # Crop and process frame to publish to baxter's monitor
                cropframe = frame[300:650, 350:945]
                cropframe = cv2.resize(cropframe, (1024, 600))
                # pubframe = self.bridge.cv2_to_imgmsg(cropframe, encoding="passthrough")
                num_com = 0
                # while num_com < 1:
                #     num_com = self.pub3.get_num_connections()
                # self.pub3.publish(pubframe)

            cv2.imshow('frame', frame)
            cv2.waitKey(0)

if __name__ == '__main__':
    vision = Vision()
    cv2.destroyAllWindows()  # Destroy CV image window on shut_down