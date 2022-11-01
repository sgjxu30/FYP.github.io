# **Week 5**
## **openwifi**  
> <https://github.com/open-sdr/openwifi>

<img src=https://pic1.imgdb.cn/item/635a591916f2c2beb11d2a33.png width=80% />

sdr platform chosen for the project: zed_fmcs2, with board combination Xinlinx ZC706 + FMCOMMS2/3/4.  

1. Restore the img file into a SD card;
2. Confog the corresponding file in the BOOT partition;
<!--pic.BOOT根目录文件-->
3. 2 antennas are connected to RXA/TXA port on FMC radio board;
4. Config the board to SD card boot mode <!--(check the board manual)-->;
5. Connect the zedboard with PC usinga ethernet cable; <!--pic.连接图片-->
6. Change the IP address of the PC used to connect the zedboard 
<img src=https://pic1.imgdb.cn/item/6361169c16f2c2beb15ee6f5.png width=80% />
7. Login to the board from PC
```
ssh root@192.168.10.122
```
However, the above step is not successfully completed, since the authencication of 'PermitRootLogin' is negative. The following operations refer the following link, 

> 'How to allow the root user to log in to Linux using SSH' 
> <https://blog.csdn.net/allway2/article/details/108815503>

It can be checked using cmd
```
grep -i "rootlogin" /etc/ssh/sshd_config
```
<img src=https://pic1.imgdb.cn/item/635a635316f2c2beb13404e5.png width=65%/>

If there is a hash # before PermitRootLogin, this means you should edit the corresponding file using cmd
```
vim /etc/ssh/sshd_config
```
Notice: for Linux users, you can comfirm the changes by restart the ssh server using cmd 
```
sudo /etc/init.d/ssh restart
```
however, for Mac user, you should use the following cmd to operate as an administrator.
``` 
sudo su vim /etc/ssh/sshd_config
```
The configuration after modification is as follows:  
<img src=https://pic1.imgdb.cn/item/635a663d16f2c2beb13a67eb.png width=65% />

### *Problem occurred*  
*The above operations would work given that you have openssh-serve installed, however, duo to the Java Runtime issue, the problem cannot be solved.*   
<img src=https://pic1.imgdb.cn/item/635a6a0616f2c2beb141decc.png width=65% />

So, I chose another way, ping the IP address instead of using ssh. (This method is suggested by Guanxiong Shen, PhD student of my project supervisior, Junqing Zhang)  
<img src=https://pic1.imgdb.cn/item/6360fc4d16f2c2beb10037a5.jpg width=65% />  

The following figure is the result of using ssh which I tried another day. The above problem would occur is due to the mistake when settig the IP of my computer.  
"Confifure IPv4" should set to Manually instead of "Using DHCP with manual address". And the "Subnet Mask" should set to 255.255.255.0

<img src=https://pic1.imgdb.cn/item/6361000716f2c2beb10dce4c.jpg width=65% />


## **CSI**
> https://github.com/open-sdr/openwifi/blob/master/doc/app_notes/csi.md

Run the following cmd in Ternimal
```
ssh root@192.168.10.122
(password: openwifi)
cd openwifi
./wgd.sh
(Wait for the script completed)
./monitor_ch.sh sdr0 11
(Monitor on channel 11. You can change 11 to other channel that is busy)
insmod side_ch.ko
./side_ch_ctl g
```

The board outputs:  
<img src=https://pic1.imgdb.cn/item/63611ac716f2c2beb171fb2c.jpg width=48% />
<img src=https://pic1.imgdb.cn/item/63611ac716f2c2beb171fb42.jpg width=48% />

CSI (Chip State Information) is going to the computer smoothly.  

However, when following the guide, this problem occurs, so I dicide to learn CSI first, and deal with this problem later in Week 6.
<img src=https://pic1.imgdb.cn/item/63611a2316f2c2beb16ee660.jpg width=80% />
