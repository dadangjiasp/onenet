# onenet
树莓派将传感器数据（AM2320&MPU6050，连接sda0/scl0,需要树莓派开启iic功能）上传至ONENET平台


#需要启动定时脚本，每隔一分钟将数据上传至onenet
#开启crontab定时任务
#sudo crontab -e 
#在最后一行输入如下代码，每一分钟将数据上传至onenet平台，如不需要log可去掉。onenet.py 启动的路径下
#   */1 * * * * python /home/pi/onenet.py >> /home/pi/onenet.log
#重启cron ，任务有效执行  
#sudo service cron restart
