# <center> TCP笔记
## TCP简介
tcp是一种面向连接的可靠的基于字节流的传输层通信协议。这句话有几个关键的地方，面向连接的、可靠的、基于字节流。同时是传输层的通信协议，其位于IP层之上，在应用层之下。从本质上讲网络是不可靠的，TCP协议实现了在不可靠的网络中可靠的数据传输功能。为了实现这个功能，TCP通过头格式的定义，TCP状态机、重传机制、滑动窗口、拥塞处理等机制保障数据在不可靠网络中可靠传输的功能。下面讲分别介绍这些知识，以便对TCP有一个更深刻的理解。

## TCP头格式
![](http://coolshell.cn//wp-content/uploads/2014/05/TCP-Header-01.jpg)
1. TCP的包没有IP地址，IP地址在IP层，但是有源端口和目的端口.
2. 通常可以使用一个四元组(src_ip,src_port,dst_ip)
3. 图中有四个非常重要的东西：
	- SequenceNumber:包的序列号，用于解决网络包的乱序的问题。
	- AcknowledgementNumber:即ACK，确认收到，用来解决不丢包的问题
	- Advertised-Window，滑动窗口，用于解决流量控制问题的。
	- TCP Flag：包的类型，用于操控TCP的状态机的。

## TCP状态机
网络上的传输是没有连接的，包括TCP也是一样的，一般所谓的TCP连接，其实是通信的两端保持一个通信的状态。因此tcp连接的状态的保持就非常重要了。
### tcp连接的建立与断开
![](http://coolshell.cn//wp-content/uploads/2014/05/tcp_open_close.jpg)

1. 三次握手建立连接
主要是为了初始化SequenceNumber的初始值，也叫SYN，也就是图中的x和y。这个号要作为以后的通信的序号，以保证应用层接收的数据不会因为网络的传输问题而出现乱序的情况。

2. 四次握手断开连接
其实只有两次，由于tcp是全双工的，因此发送方和接收方都需要FIn和ACK，有一行是被动的，看起来像是四次握手。只有两方同时进入closing状态，连接关闭。


## 重传机制
tco为了保证所有的包都可以正常到达，必需要有重传机制。
需要注意的地方：接收端给发送端的Ack确认只会确认最后一个连续的包。举个例子：发送端一共发送了5份数据，接收端收到1,2，因此返回ack3，然后收到了4(此时没有收到3)。我们知道SeqNum和Ack以字节为单位，所以ack的时候，不能跳着确认，只能确认最大的连续收到的包，否则，发送端就会认为之前的都受到了。针对这种情况，tcp设计了几种重传机制。
### 超时重传机制
不回ack，一直等待3，如果发送方发现收不了3的ack的超时后，会重传3，一旦接收方收到3，回复ack4，表示3和4都收到了。但是这种方式存在一个问题：因为死等3，导致4和5即便已经收到了，发送方由于没有收到4和5的ack，也会重传4和5.效率太低。因此一般有两种选择：
 - 仅仅重传timeout的包，也就是第三份数据。节省带宽，但是慢
 - 另一种就是重传超时后的所有数据，也就是3、4、5三份数据。快一点但是浪费带宽。

### 快速重传机制
和超时重传不同，快速重传以**数据驱动，而不以时间驱动**。如果包没有连续到达，就ack最后那个可能被丢的包，如果发送方连续收到三次相同的ack就重传。优点不用等待timeout之后再重传。
例如:还是以上面的例子为例，发送方发出1,2,3,4,5，第一份到达之后ack返回2，第二份数据丢失，3到达了于是ack仍然返回2，4、5到达了，仍然返回ack 2。于是发送方收到了三个ack2，知道需要重传第二份数据，此时由于3/4/5都收到了，因此返回ack6，示意图如下所示:
![](http://coolshell.cn//wp-content/uploads/2014/05/FASTIncast021.png)

但是Retransmit只解决了一个timeout问题，并没有解决需要重传哪几个包的问题。这样发送端有可能需要重传丢失数据之后的所有数据。效率仍然比较低。

### SACK方法
Selective Acknowledgment(SACK)需要在tcp的头中添加sack的东西，SACK汇报收到的数据碎版，如下所示：
![](http://coolshell.cn//wp-content/uploads/2014/05/tcp_sack_example-900x507.jpg)

这样一来，在发送端就可以根据回传的SACK知道有哪些数据收到了，哪些没有收到。在Linux下，通过tcp_sack参数打开这个功能（2.4之后默认打开）

### TCP的RTT算法
从前面的tcp的重传机制知道Timeout的设置对于重传非常重要：
- 设置过长，重发就会变得很慢，没有效率，性能比较差
- 设置过短，导可能没有致没有丢就重发，重发变得很快，增加网络拥塞，导致更多超时，更多的超时导致更多的重发，进入恶性循环。
- 这个超时在不同的网络环境下还都不一样，不能设置成一个常数。只能动态的进行设置。为了能够动态的设置这个值，tcp引入RTT-round trip time，一个数据包发出去到回来的时间。这样发送端就能知道大约需要多长的时间，从而更方便的设置timeout-Retransmission Timeout.让重传机制更高效。

tcp中有一些经典的算法来解决这个问题：包括RFC793中的经典算法，Karn/Partridge算法，Jacobson/Karels算法等。当前tcp协议中使用的就是Jacobson/Karels算法。

## 滑动窗口
tcp必需解决可靠传输以及包的乱序问题，因此tcp必需知道网络实际的处理带宽或者数据处理速度，才不会引起网络拥塞，导致丢包的问题。因此tcp引入一些技术和设计来做网络流控，Sliding window是其中的一个技术。tcp头中有一个字段叫Window，又叫Advertised-Window。**这个字段是接收端告诉发送端自己还有多少缓冲区可以用来接收数据。于是发送端就可以根据这个接收端的处理能力来发送数据，而不会导致接收端处理不过来。**
### tcp缓冲区结构
![](http://coolshell.cn//wp-content/uploads/2014/05/sliding_window-900x358.jpg)

1. 接收端：LastByteRead指向缓冲区中读到的位置，NextByteExpected指向收到的连续包的最后一个位置。LastByteAcked指向收到的包的最后一个位置，中间的称之为数据空白区。
2. 发送端：LastByteAcked指向了被接收端Ack过的位置（表示成功发送确认），LastByteSent表示发出去了，但还没有收到成功确认的Ack，LastByteWritten指向的是上层应用正在写的地方。
3. 接收端在给发送端回ACK中会汇报自己的AdvertisedWindow = MaxRcvBuffer – LastByteRcvd – 1
4. 而发送方会根据这个窗口来控制发送数据的大小，以保证接收方可以处理。

关于滑动窗口，还有其他的一些问题需要解决，比如滑动窗口的大小有可能为0或者会出现Silly Window Syndrome问题.针对这两个问题：
1. ZeroWindow：tcp使用Zero Window Probe技术，如果发送端在窗口大小为0的时候，发送端不发送数据，而是发送zwp包给接收方，希望能直接获取接收方的Windo size，一般会设置3次，如果三次均为0，tcp会断掉这个连接。
2. Silly Window Syndrome，本质上就是频繁的传递小数据量，降低了数据传输速率，浪费带宽，解决这个问题就是避免对小的window size作出相应，直到足够大的window才响应。

## 拥塞处理
由上可知，tcp通过sliding window来做流量控制，但是sliding window依赖于连接的发送端与接收端，并不知道网络中间发生了什么。更具体的tcp通过timer采用rtt并计算rto，但是**如果网络的延时突然增加，tcp就只能重传数据了，但是重传会导致网络负担更重，导致更多的丢包和更大的延时，这个情况会被恶性放大。**因此tcp需要处理网络拥塞以便能够更好的传输数据。

控制拥塞主要是四个算法
1. 慢启动
 - 慢启动的意思是刚刚加入网络的连接，需要一点点的提速，不能一上来就占光所有的带宽。
 - 算法的过程如下所示：
 	- 连接建好的开始先初始化cwnd = 1，表明可以传一个MSS大小的数据。
 	- 每当收到一个ACK，cwnd++; 呈线性上升
 	- 每当过了一个RTT，cwnd = cwnd*2; 呈指数让升
 	- 还有一个ssthresh（slow start threshold），是一个上限，当cwnd >= ssthresh时，就会进入“拥塞避免算法”
 - 启动过程如下所示
![](http://coolshell.cn//wp-content/uploads/2014/05/tcp.slow_.start_.jpg)

2. 拥塞避免
  - 当cwnd >= ssthresh时，就会进入“拥塞避免算法”。一般来说ssthresh的值是65535，单位是字节，当cwnd达到这个值时后，算法如下：
    - 收到一个ACK时，cwnd = cwnd + 1/cwnd
    - 当每过一个RTT时，cwnd = cwnd + 1
    
  - 这样就可以避免增长过快导致网络拥塞，慢慢的增加调整到网络的最佳值。很明显，是一个线性上升的算法
3. 拥塞发生
  - 丢包的时候有两种情况需要处理：
    - RTO超时，重传数据包，sshthresh =  cwnd /2，cwnd 重置为1，进入慢启动过程
    - Fast Retransmit算法，也就是在收到3个duplicate ACK时就开启重传，而不用等到RTO超时。
    	- TCP Tahoe的实现和RTO超时一样
    	- TCP Reno的实现是：cwnd = cwnd /2；sshthresh = cwnd；进入快速恢复算法——Fast Recovery

4. 快速恢复
	- 快速恢复有多个算法实现，包括TCP Reno、TCP New Reno、FACK算法等。这列主要介绍TCP Reno算法。
	- Tcp Reno算法如下：
		- cwnd = sshthresh  + 3 * MSS （3的意思是确认有3个数据包被收到了）
		- 重传Duplicated ACKs指定的数据包
		- 如果再收到 duplicated Acks，那么cwnd = cwnd +1
		- 如果收到了新的Ack，那么，cwnd = sshthresh ，然后就进入了拥塞避免的算法了。


## 参考网址
[TCP 的那些事儿（上）](http://coolshell.cn/articles/11564.html)
[TCP 的那些事儿（下）](http://coolshell.cn/articles/11609.html)
[IP头、TCP头、UDP头详解以及定义](http://blog.csdn.net/mrwangwang/article/details/8537775)

