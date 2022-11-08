# **Week 6**
## *Last weeks problem addressed*
Download the zip file from github.  
<img src=https://pic1.imgdb.cn/item/636a310916f2c2beb1255b46.png  width=80% />  
Note: Modify the file path when running cmd line.  
<img src=https://pic1.imgdb.cn/item/636a31d716f2c2beb1264660.png width=65% />  

## **Capture CSI**
### Capture only CSI of those packets from Wi-Fi dongle
```
./side_ch_ctl wh1h4001
./side_ch_ctl wh7h27d2c2e4
./side_ch_ctl g
```
### Problem occurred
Question 1  
No CSI captured when applying MAC filter.  
<img src=https://pic1.imgdb.cn/item/636adb0816f2c2beb14e32f7.png width=80% />  

Question 2  
No image displayed when running side_info_display.py file, already keep zedboard working, and CSI is going to the computer.  

### Problem description
* can capture CSI samples without a MAC address filter (evidence shown in last week's blog)
* can NOT capture CSI sample from the PC which is connected to the wifi dongle  
<img src=https://pic1.imgdb.cn/item/636adc5016f2c2beb14eeafb.jpg width=80% />