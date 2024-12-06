import rospy
from std_msgs.msg import String
import time

def talker():
    rospy.init_node('talker', anonymous=True)
    pub = rospy.Publisher('/example_topic', String, queue_size=10)

    while not rospy.is_shutdown():
        for _ in range(10):
            msg = String()
            msg.data = 'hello ROS'
            pub.publish(msg)
            rospy.sleep(0.1)  # 每次发布间隔 0.1 秒
        rospy.sleep(1)  # 每秒发送 10 条消息

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
