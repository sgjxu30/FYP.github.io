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
6. Change the IP address of the PC used to connect the zedboard <!--ip add-->
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

Problem occurred:  the above operations would work given that you have openssh-serve installed, however, duo to the Java Runtime issue, the problem cannot be solved.   
<img src=https://pic1.imgdb.cn/item/635a6a0616f2c2beb141decc.png width=65% />

So, guanxiong offered me another way, that is to ping the IP address instead of using ssh.  
<!--ping 192.168.10.122-->

*to be continued...*