#!/bin/bash

# 捕获 SIGINT，并在退出时关闭所有子进程
trap "kill 0" SIGINT

roscore &
sleep 5
# 启动第一个 Python 脚本
python3 robot_server.py &

sleep 1

# 启动第二个 Python 脚本
python3 pub_json.py &
sleep 1

# 等待所有后台进程完成
wait

echo "所有脚本已完成执行."
