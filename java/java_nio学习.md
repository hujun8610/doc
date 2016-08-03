# Java NIO学习
## 基本概念
Java nio是JDK1.4引入的新特性，与传统的io不同，nio是一种**高速面向块的io**，而传统的io是面向流的io，面向流的io一次一个字节的处理数据，因此效率比较低，不适用于性能要求比较高的场景。nio使用块I/O的方式来处理数据，每一个操作在每一步都产生或者消费一个数据块。**因此其性能要远超传统I/O。**	

### 缓冲区Buffer
Buffer本质上就是一个容器，也是nio和传统io的一个非常重要的区别。在nio中数据都是通过Buffer进行读写的。缓冲区的实质是一个数组，提供了对存储在其中的数据的结构化访问，同时还可以跟踪系统的读写进程。
在java中除了boolean类型之外，其他基本数据类型都有对应的Buffer类型，如LongBuffer、IntBuffer等。每种Buffer类型都包括如下属性：
<li> capacity：Buffer能存放的最大数据量，Buffer创建的时候指定。
<li>  limit：Buffer上读写不能超过的最大**下标**，写数据的时候limit==capacity，读数据的时候表示当前buffer中有效的数据量。
<li> position：跟踪buffer中写入多少数据或从buffer中读取了多少数据。
<li> mark：临时存放的位置下标，mark()会将mark设置为当前position的值，后面调用reset会position设置为mark的值。
<li> 这些属性满足：0 <= mark <= position <= limit <= capacity

Buffer的方法
<li> get方法

```
byte get();  //读取单个字节
ByteBuffer get( byte dst[] );  //将一组字节读入数组中  
ByteBuffer get( byte dst[], int offset, int length ); //同上  
byte get( int index );  //从缓冲区特定位置读取
```

注意buffer.get(myArray)等价于buffer.get(myArray,0,myArray.length);当传入一个数组没有指定长度的时候就必须填满数组否则会出现`BufferUnderflowException` 异常。

<li> put方法
put方法与get方法类似：

```
    ByteBuffer put( byte b );  
    ByteBuffer put( byte src[] );  
    ByteBuffer put( byte src[], int offset, int length );  
    ByteBuffer put( ByteBuffer src );  
    ByteBuffer put( int index, byte b );
```

### Channel
Java nio中的通道类似于流，但是和流存在一些区别:
<li>既可以从通道中读取数据也可写入数据，但是**读写数据是单向的**
<li>通道可以异步的读写
<li>通道中的数据总是从buffer中读入或者从buffer写到数据通道。

Java nio中包含四种通道，分别如下所示：

- FileChannel:从文件中读写：

   - FileChannel无法设置为非阻塞模式，一直在阻塞模式。在使用FileChannel的时候必须从InputStream、OutputStream或者RandomAccessFile中获取一个FileChannel的实例。
注意**通道使用完成后必须调用close方法来关闭通道**

- DatagramChannel：从UDP中读写网络数据,接收数据调用receive方法，发送数据调用send方法。

	- 打开通道的方式如下所示：
	
	```
		DatagramChannel channel = DatagramChannel.open();
		channel.socket().bind(new InetSocketAddress(9999));
	```
	
- SocketChannel:通过TCP读写网络数据

	- 打开SocketChannel两种方式，创建一个SocketChannel并连接到网络服务器，或者当一个新的连接到达ServerSocketChannel的时候，创建SocketChannel。代码如下所示：
	
	```
	SocketChannel socketChannel = SocketChannel.open();
socketChannel.connect(new InetSocketAddress("http://jenkov.com", 80));
	```
	注意**可以设置SocketChannel为异步工作模式，设置之后就可以以异步的方式调用connect、read和write方法来访问网络**

- ServerSocketChannel：监听新的TCP连接，对每一个进来的TCP连接创建一个SocketChannel。两种工作模式，阻塞模式和非阻塞模式
	- 阻塞模式
	
	```
	ServerSocketChannel serverSocketChannel = ServerSocketChannel.open(); 
   serverSocketChannel.socket().bind(new InetSocketAddress(9999));
 
    while(true){
    	SocketChannel socketChannel =
            serverSocketChannel.accept();
 		}
	```
	
	- 非阻塞模式
	
	```
	ServerSocketChannel serverSocketChannel = ServerSocketChannel.open();
 
	serverSocketChannel.socket().bind(new InetSocketAddress(9999));
	serverSocketChannel.configureBlocking(false);
 
	while(true){
    SocketChannel socketChannel =
            serverSocketChannel.accept();
    //在非阻塞模式下，accept() 方法会立刻返回，如果还没有新进来的连接,返回的将是null。 因此，需要检查返回的SocketChannel是否是null
    if(socketChannel != null){
        //do something with socketChannel...
    	}
	}
	```

### Scatter/Gather
- scatter:从Channel中读取是指在读操作时将读取的数据写入多个buffer中。因此，Channel将从Channel中读取的数据“分散（scatter）”到多个Buffer中。

![scatter](http://ifeve.com/wp-content/uploads/2013/06/scatter.png)

代码如下所示：

```
ByteBuffer header = ByteBuffer.allocate(128);
ByteBuffer body   = ByteBuffer.allocate(1024);
 
ByteBuffer[] bufferArray = { header, body };
 
channel.read(bufferArray);
```


- 聚集（gather）写入Channel是指在写操作时将多个buffer的数据写入同一个Channel，因此，Channel 将多个Buffer中的数据“聚集（gather）”后发送到Channel。

![gather](http://ifeve.com/wp-content/uploads/2013/06/gather.png)

代码如下所示：

```
ByteBuffer header = ByteBuffer.allocate(128);
ByteBuffer body   = ByteBuffer.allocate(1024);
 
//write data into buffers
 
ByteBuffer[] bufferArray = { header, body };
 
channel.write(bufferArray);
```
### 通道之间的数据传输
<li> transformFrom方法：将数据从源通道传入FileChannel中。代码如下所示：

```
RandomAccessFile fromFile = new RandomAccessFile("fromFile.txt", "rw");
FileChannel      fromChannel = fromFile.getChannel();
 
RandomAccessFile toFile = new RandomAccessFile("toFile.txt", "rw");
FileChannel      toChannel = toFile.getChannel();
 
long position = 0;
long count = fromChannel.size();
 
toChannel.transferFrom(position, count, fromChannel);
```

<li>transformTo方法从FileChannel传输到其他Channel，代码如下所示：

```
RandomAccessFile fromFile = new RandomAccessFile("fromFile.txt", "rw");
FileChannel      fromChannel = fromFile.getChannel();
 
RandomAccessFile toFile = new RandomAccessFile("toFile.txt", "rw");
FileChannel      toChannel = toFile.getChannel();
 
long position = 0;
long count = fromChannel.size();
 
fromChannel.transferTo(position, count, toChannel);
```


## 参考
[核心概念和基本读写](http://www.importnew.com/20784.html)

[Java NIO系列教程（2）：Channel](http://www.importnew.com/18827.html)