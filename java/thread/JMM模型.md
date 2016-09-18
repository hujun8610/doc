#<center> Java Memory Model
## 简介
Java内存模型主要用于多线程之间的通信。对于线程内的局部变量的访问与JMM无关，JMM决定一个线程对共享变量的写入对另一个线程何时可见，抽象的来看：JMM定义了线程和主内存之间的抽象关系。其关系如下所示：
![](http://cdn2.infoqstatic.com/statics_s1_20160914-0333/resource/articles/java-memory-model-1/zh/resources/11.png)

因此线程A与线程B之间的通信将有两步：
1. 线程A把本地内存A中更新过的共享变量刷新到主内存中去。
2. 线程B到主内存中去读取线程A之前已更新过的共享变量。

## 指令重排序
指令重排序指的是在执行程序时为了提高性能，编译器和处理器常常会对指令做重排序。由于Java程序在执行过程中会出现指令重排序的问题。所谓重排序就是指在Java执行的时候后面的语句有可能会在前面的语句中执行，如下：
```java
	int a = 10;
    int b = 11;
```
两条语句在执行的时候完全有可能出现先赋值b再赋值a的可能，在单线程中出现指令重排序不会导致结果出现问题。但是在多线程中指令重排序会出现严重的问题，且问题有时候很难重现。
在多线程中由于线程交互执行，此时在访问共享变量的时候由于指令重排序有可能导致共享变量错误的状态，导致程序出现严重的bug。因此必须用引入同步和互斥来避免该问题。
多线程指令重排序问题：详细可参考[代码](https://github.com/hujun8610/sparkProject/blob/master/commonAlgorithm/src/main/java/com/bupt/javalearning/mutithread/memorymodel/InstructionReorderDemo.java)


## happens-before
用于描述两个操作之间的内存可见性。两个操作既可以是同一个进程内部也可以是在不同的进程之间。一句话两个操作存在happens-before关系，在前一个操作的结果对后一个操作可见。需要注意的是：**两个操作之间具有happens-before关系，并不意味着前一个操作必须要在后一个操作之前执行！happens-before仅仅要求前一个操作（执行的结果）对后一个操作可见，且前一个操作按顺序排在第二个操作之前**


## 参考
[深入理解Java内存模型](http://www.infoq.com/cn/articles/java-memory-model-1)


