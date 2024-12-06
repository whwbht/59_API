from flask import Flask, Response
import rospy
from std_msgs.msg import String
from multiprocessing import Process, Queue
import time

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
    rospy.Subscriber('/example_topic', String, callback)  # 订阅 ROS 话题
    rospy.spin()

# SSE 流式响应
def generate():
    while True:
        if not message_queue.empty():
            msg = message_queue.get()  # 从队列中取出消息
            yield f"data: {msg}\n\n"  # SSE 格式的数据流
        else:
            yield "data: No GPS data received yet.\n\n"  # 如果队列为空，返回提示信息
        time.sleep(1)  # 每隔一秒检查一次队列

# Flask 路由，返回流式数据
@app.route('/location_gps')
def location_gps():
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    # 启动一个子进程来运行 ROS 话题订阅
    p = Process(target=listener)
    p.start()
    print("ROS topic listener is running in a subprocess.")

    # 启动 Flask 服务器
    app.run(host='127.0.0.1', port=8081, debug=True)  # 服务器绑定的 IP 地址

    # 等待子进程结束
    p.join()

##目前问题：发送还是不能快速。没有那种数据流的效果。1s中更新一次位姿信息还是可以的。