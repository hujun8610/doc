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
 

## 参考
[核心概念和基本读写](http://www.importnew.com/20784.html)