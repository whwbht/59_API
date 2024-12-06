#!/usr/bin/env python
from flask import Flask, Response
import rospy
from std_msgs.msg import String
from multiprocessing import Process, Queue

app = Flask(__name__)

# 使用队列来存储 ROS 话题接收到的消息
message_queue = Queue()

# 回调函数，处理从 ROS 话题接收到的数据
def callback(msg):
    print(f"Received: {msg.data}")
    message_queue.put(msg.data)  # 将消息放入队列中

# ROS 话题监听函数
def listener():
    rospy.init_node('topic_listener', anonymous=True)
    rospy.Subscriber('/example_topic', String, callback) # change topic to RTK: robot pose
    rospy.spin()

# Flask 路由，返回简单的响应
@app.route('/location_gps') 
def location_gps():
    if not message_queue.empty():
        # 从队列中取出最新的消息
        msg = message_queue.get()
        return Response(f"Received: {msg}", mimetype='text/plain')
    else:
        return Response("No GPS data received yet.", mimetype='text/plain')

if __name__ == '__main__':
    # 启动一个子进程来运行 ROS 话题订阅
    p = Process(target=listener)
    p.start()
    print("ROS topic listener is running in a subprocess.")

    # 启动 Flask 服务器
    app.run(host='192.168.67.187', port=8080, debug=True)  # 服务器绑定的 IP 地址
    
    # 等待子进程结束
    p.join()
