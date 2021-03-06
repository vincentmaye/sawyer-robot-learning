import rospy

import intera_interface

from intera_interface import CHECK_VERSION

from std_msgs.msg import String
from std_msgs.msg import Bool
from sensor_msgs.msg import Image
from gazebo_msgs.msg import ModelStates
from cv_bridge import CvBridge, CvBridgeError
import cv2
import os

from sawyer_demonstration.srv import *

class DataRecorder(object):
    def __init__(self, rate, side="right"):
        """
        Records joint data to a file at a specified rate.
        """
        self._raw_rate = rate
        self._rate = rospy.Rate(rate)
        self._start_time = rospy.get_time()
        self._done = True
        self.counter = 0
        self.is_recording = False
        self.filename = str(self.counter)+'.csv'
        self.cv2_img = None
        self.img_counter = 0
        # self.cube_pose_x = 0.0
        # self.cube_pose_y = 0.0

        self.last_eef_pose_x = 0.0

        self._limb_right = intera_interface.Limb(side)

        data_path = 'data_pose_2/'
        if not os.path.exists(data_path):
            os.makedirs(data_path)

        image_path = 'data_pose_2/'
        if not os.path.exists(image_path):
            os.makedirs(image_path)

        with open('data_pose_2/'+self.filename, 'w') as f:
            f.write('counter,')
            f.write('time,')
            # f.write('cube_pose_x,')
            # f.write('cube_pose_y,')
            f.write('eef_pose_x,')
            f.write('eef_pose_y,')
            f.write('eef_pose_z,')
            f.write('eef_vel_x,')
            f.write('eef_vel_y,')
            f.write('eef_vel_z,')
            
            f.write('\n')

    def _time_stamp(self):
        return rospy.get_time() - self._start_time

    def start(self):
        self._done =  False

    def stop(self):
        self._done = True  

    def record(self):
        """
        Records the current joint positions to a csv file if outputFilename was
        provided at construction this function will record the latest set of
        joint angles in a csv format.

        """
        joints_right = self._limb_right.joint_names()
        
        data_path = 'data/'
        if not os.path.exists(data_path):
            os.makedirs(data_path)

        image_path = 'data/'+str(self.counter) 
        if not os.path.exists(image_path):
            os.makedirs(image_path)

        with open('data/'+self.filename, 'w') as f:
            f.write('time,')
            temp_str = '' if self._gripper else '\n'
            f.write(','.join([j for j in joints_right]) + ',' + temp_str)
            f.write('joint_trajectory_id ,')
            if self._gripper:
                f.write(self.gripper_name+'\n')
            while not dr._done:
                if self._gripper:
                    if self._cuff.upper_button():
                        self._gripper.open()
                    elif self._cuff.lower_button():
                        self._gripper.close()
                angles_right = [self._limb_right.joint_angle(j)
                                for j in joints_right]
                f.write("%f," % (self._time_stamp(),))
                f.write(','.join([str(x) for x in angles_right]) + ',' + temp_str)
                
                # save current snapshot
                cv2.imwrite('data/'+str(dr.counter)+'/image_'+str(self.img_counter)+'.jpeg', dr.cv2_img)

                f.write('data_jt_'+str(self.img_counter)+',')
                self.img_counter += 1

                if self._gripper:
                    f.write(str(self._gripper.get_position()) + '\n')

                self._rate.sleep()

            self.img_counter = 0

    # def record(self):
    #     ## for recording images and corresponding
    #     ## position labels. Supposed to be a very
    #     ## simple task

    #     joints_right = self._limb_right.joint_names()

    #     with open('data_pose_2/'+self.filename, 'a') as f:
    #         # f.write('time,')
    #         # temp_str = '' if self._gripper else '\n'
    #         # f.write(','.join([j for j in joints_right]) + ',' + temp_str)
    #         # if self._gripper:
    #         #     f.write(self.gripper_name+'\n')
    #         while not dr._done:


                # eef_pose = self._limb_right.endpoint_pose()['position']

                # if eef_pose.x != self.last_eef_pose_x: #to avoid redundant data when starting new demo

                #     eef_pose_x = eef_pose.x
                #     eef_pose_y = eef_pose.y
                #     eef_pose_z = eef_pose.z

                #     eef_vel = self._limb_right.endpoint_velocity()['linear']
                #     eef_vel_x = eef_vel.x
                #     eef_vel_y = eef_vel.y
                #     eef_vel_z = eef_vel.z

                #     f.write(str(self.img_counter)+',')
                #     f.write("%f," % (self._time_stamp(),))

                #     f.write(str(self.cube_pose_x)+',')
                #     f.write(str(self.cube_pose_y)+',')
                    
                #     f.write(str(eef_pose_x)+',')
                #     f.write(str(eef_pose_y)+',')
                #     f.write(str(eef_pose_z)+',')

                #     f.write(str(eef_vel_x)+',')
                #     f.write(str(eef_vel_y)+',')
                #     f.write(str(eef_vel_z)+',')

                #     f.write('\n')

                #     # save current snapshot
                #     cv2.imwrite('data_pose/'+str(self.img_counter)+'.jpeg', dr.cv2_img)

                #     self.img_counter += 1

                #     self.last_eef_pose_x = eef_pose_x


                # self._rate.sleep()

                eef_pose = self._limb_right.endpoint_pose()['position']


                eef_pose_x = eef_pose.x
                eef_pose_y = eef_pose.y
                eef_pose_z = eef_pose.z

                eef_vel = self._limb_right.endpoint_velocity()['linear']
                eef_vel_x = eef_vel.x
                eef_vel_y = eef_vel.y
                eef_vel_z = eef_vel.z

                f.write(str(self.img_counter)+',')
                f.write("%f," % (self._time_stamp(),))

                # f.write(str(self.cube_pose_x)+',')
                # f.write(str(self.cube_pose_y)+',')
                
                f.write(str(eef_pose_x)+',')
                f.write(str(eef_pose_y)+',')
                f.write(str(eef_pose_z)+',')

                f.write(str(eef_vel_x)+',')
                f.write(str(eef_vel_y)+',')
                f.write(str(eef_vel_z)+',')

                f.write('\n')

                # save current snapshot
                cv2.imwrite('data_pose_2/'+str(self.img_counter)+'.jpeg', dr.cv2_img)

                self.img_counter += 1

                self.last_eef_pose_x = eef_pose_x


                self._rate.sleep()
                


def handle_start_recording(req):
    # print "returning start"
    dr.start()
    return StartRecordingResponse()

def handle_stop_recording(req):
    # print "returning stop"
    dr.stop()
    # dr.counter += 1
    # dr.filename = str(dr.counter)+'.csv'
    return StopRecordingResponse()

def handle_image_cb(msg):
    try:
        # Convert your ROS Image message to OpenCV2
        dr.cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
    except CvBridgeError, e:
        print(e)

# def handle_model_states_cb(msg):
#     if "block" in msg.name:
#         dr.cube_pose_x = round(msg.pose[4].position.x, 2)
#         dr.cube_pose_y = round(msg.pose[4].position.y, 2)


rospy.init_node('joint_recorder_node')

# Instantiate CvBridge
bridge = CvBridge()

dr = DataRecorder(10)
s_start = rospy.Service('start_recording', StartRecording, handle_start_recording)
s_stop = rospy.Service('stop_recording', StopRecording, handle_stop_recording)
camera_sub = rospy.Subscriber('/top_camera/camera/image_raw', Image, handle_image_cb)
# cube_pose_sub = rospy.Subscriber('/gazebo/model_states', ModelStates, handle_model_states_cb)

while not rospy.is_shutdown():
    dr.record()