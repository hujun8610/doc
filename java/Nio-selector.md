#<center> NIO-Selector
Selector是Nio中能够检测一个到多个的NIO通道，并且能够知道通道是否做好了读写的准备，通过这种机制一个单独的线程就可以管理多个Channel，从而管理多个网路。Selector具有很多优点，通过当个线程来处理多个Channel，可以使用更少的线程来管理更多的网络。如下是使用一个Selector处理三个Channel的示意图。
![Selector处理Channel示意图](http://tutorials.jenkov.com/images/java-nio/overview-selectors.png)

## Selector使用
1. 通过调用Selector.open()方法创建一个Selector。
2. 注册通道：为了将Channel和Selector配合一起使用，必须将Channel注册到Selector，通过SelectableChannel.register()方法来实现。

	```
channel.configureBlocking(false);
SelectionKey key = channel.register(selector,
    Selectionkey.OP_READ);
	```
方法的第二个参数是一个“interest集合”，意思是在通过Selector监听Channel时对什么事件感兴趣。可以监听四种不同类型的事件：

	```
	SelectionKey.OP_CONNECT
	SelectionKey.OP_ACCEPT
	SelectionKey.OP_READ
	SelectionKey.OP_WRITE
	```	

	注意**Selector一起使用时，Channel必须处于非阻塞模式下**，因此FileChannel是不能喝Selector一起使用的。

3. register方法返回SelectionKey对象，这个对象包含：
	
	- interest集合，你所选择的感兴趣的事件集合，可以通过集合的&来确定某个事件是否在interest集合中。`int interestSet = selectionKey.interestOps();`
	- ready 集合是通道已经准备就绪的操作的集合。在一次选择(Selection)之后，你会首先访问这个ready set。`int readySet = selectionKey.readyOps();`
	- Channel和Selector，`Channel  channel  = selectionKey.channel();
Selector selector = selectionKey.selector();`
	- 附加对象，可以将一个对象或者更多信息附着到SelectionKey上，这样就能方便的识别某个给定的通道。
	
## 通过Selector选择通道
1. Selector注册了一或多个通道，就可以调用几个重载的select()方法。这些方法返回你所感兴趣的事件（如连接、接受、读或写）已经准备就绪的那些通道。有三种select方法可以选择使用

	- int select()：阻塞到至少有一个通道在你注册的事件上就绪了。
	- int select(long timeout)：与select相同，最长会阻塞timeout毫秒(参数)
	- int selectNow()：不会阻塞，不管什么通道就绪都立刻返回

2. **select()方法返回的int值表示有多少通道已经就绪。**
3. SelectKeys方法，通过调用selector的selectedKeys()方法，访问“已选择键集（selected key set）”中的就绪通道。使用如下所示`Set selectedKeys = selector.selectedKeys();`
4. wakeUp方法：某个线程调用select()方法后阻塞了，即使没有通道已经就绪，也有办法让其从select()方法返回。只要让其它线程在第一个线程调用select()方法的那个对象上调用Selector.wakeup()方法即可。阻塞在select()方法上的线程会立马返回。如果有其它线程调用了wakeup()方法，但当前没有线程阻塞在select()方法上，下个调用select()方法的线程会立即“醒来（wake up）”。
5. close方法：用完Selector后调用其close()方法会关闭该Selector，且使注册到该Selector上的所有SelectionKey实例无效。**通道本身并不会关闭。**

	```
	Selector selector = Selector.open();
channel.configureBlocking(false);
SelectionKey key = channel.register(selector, SelectionKey.OP_READ);
while(true) {
  int readyChannels = selector.select();
  if(readyChannels == 0) continue;
  Set selectedKeys = selector.selectedKeys();
  Iterator keyIterator = selectedKeys.iterator();
  while(keyIterator.hasNext()) {
    SelectionKey key = keyIterator.next();
    if(key.isAcceptable()) {
        // a connection was accepted by a ServerSocketChannel.
    } else if (key.isConnectable()) {
        // a connection was established with a remote server.
    } else if (key.isReadable()) {
        // a channel is ready for reading
    } else if (key.isWritable()) {
        // a channel is ready for writing
    }
    //必须调用remove方法，移除已经处理的SelectionKey
    keyIterator.remove();
  }
}
	```



## 参考

[Selector](http://www.importnew.com/18927.html)
