#!/usr/bin/env python3


# A very basic TurtleBot script that moves TurtleBot forward indefinitely. Press CTRL + C to stop.  To run:
# On TurtleBot:
# roslaunch turtlebot_bringup minimal.launch
# On work station:
# python goforward.py

import sys
import math
import rospy
import tf
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PointStamped


class Turtlebot():
    def __init__(self):

        # Create a publisher which can "talk" to TurtleBot and tell it to move
        # Tip: You may need to change cmd_vel_mux/input/navi to /cmd_vel if you're not using TurtleBot2
        self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)

        self.listener = tf.TransformListener()

    def command(self, gx, gy):
        rospy.loginfo("Command")

        goal = PointStamped();
        base_goal = PointStamped();

        goal.header.frame_id = "odom";

        goal.header.stamp = rospy.Time();

        goal.point.x = gx;
        goal.point.y = gy;
        goal.point.z = 0.0;

        try:
            base_goal = self.listener.transformPoint('base_link', goal)
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            rospy.loginfo("Problem TF")
            return

        # TODO: put the control law here
        angular = 0.0
        linear = 0.0
        rospy.loginfo(angular)

        self.publish(linear, angular)

    def publish(self, lin_vel, ang_vel):
        # Twist is a datatype for velocity
        move_cmd = Twist()
        # let's go forward at 0.2 m/s
        move_cmd.linear.x = lin_vel
        # let's turn at 0 radians/s
        move_cmd.angular.z = ang_vel

        self.cmd_vel.publish(move_cmd)

    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop TurtleBot")
        # a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
        self.cmd_vel.publish(Twist())
        # sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
        rospy.sleep(1)


if __name__ == '__main__':
    try:
        # initiliaze
        rospy.init_node('robotcontrol', anonymous=False)

        # tell user how to stop TurtleBot
        rospy.loginfo("To stop TurtleBot CTRL + C")

        robot = Turtlebot()
        # What function to call when you ctrl + c
        rospy.on_shutdown(robot.shutdown)

        goalx = float(sys.argv[1])
        goaly = float(sys.argv[2])

        # TODO 2: extend it to load more than one goal with base in "path" parameter
        if rospy.has_param('~goal'):
            goalx = rospy.get_param('~goal/x', default=goalx)
            goaly = rospy.get_param('~goal/y', default=goaly)
        # TODO 1: Load more internal parameters such as maximum speed, goal tolerance....

        print(' Goal to reach: ', goalx, ', ', goaly)

        # TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ
        r = rospy.Rate(10);

        # as long as you haven't ctrl + c keeping doing...
        while not rospy.is_shutdown():
            rospy.loginfo("Loop")
            # publish the velocity
            robot.command(goalx, goaly)
            # wait for 0.1 seconds (10 HZ) and publish again
            r.sleep()

    except:
        rospy.loginfo("robotcontrol node terminated.")
