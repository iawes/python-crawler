#/bin/bash

source  /home/iawes/Envs/python-crawler/bin/activate

cd /home/iawes/python-crawler

ps ax|grep weibo|grep -v grep| awk '{print $1}' |xargs kill -9
nohup python weibo_sc.py --schedule_on True > /dev/null 2>&1 &

cd -
