#/bin/bash

source  /home/iawes/Envs/python-crawler/bin/activate

cd /home/iawes/python-crawler

nohup python weibo_sc.py --schedule_on True > /dev/null 2>&1 &
