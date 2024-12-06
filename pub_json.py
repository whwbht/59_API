import rospy
import json
from std_msgs.msg import String

pub = None

###############################读取extracted_data文件 进行ros发送##########################
# 初始化 ROS 节点
def init_ros():
    global pub
    rospy.init_node('flask_ros_node', anonymous=True)
    pub = rospy.Publisher('extracted_data_topic', String, queue_size=10)
    print("ROS publisher initialized successfully")

# 发布 ros 话题
def publish_ros_topic():
    rate = rospy.Rate(1)  # 设定发布频率为 1 Hz
    while not rospy.is_shutdown():
        with open('extracted_data.json', 'r', encoding='utf-8') as f:
            json_data = json.dumps(json.load(f))
            if pub is not None:
                pub.publish(json_data)
                print("Data published successfully")
        rate.sleep()  # 休眠以维持发布频率

if __name__ == '__main__':
    init_ros()
    publish_ros_topic()
    rospy.spin()  # 保持节点运行
