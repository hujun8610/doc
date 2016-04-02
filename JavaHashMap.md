#<center> Java集合框架概述-HashMap
## 概述
![](http://img.blog.csdn.net/20160317124151998)

类图中，实现的边框是实现类比如ArrayList、HashMap、LinkList，折线边框代表抽象类比如AbstractCollection、AbstractList等，而点线边框代表的是接口，比如Collection，Iterator、List等。
1. 所有的集合类实现了Iterator接口，该接口用于遍历集合中元素。包含hasNext()、next、remove三种方法。Iterator接口只允许往后遍历，已经遍历的元素不会被继续访问。无序集合的遍历一般使用这个接口。
2. 子接口LinkedIterator又添加了add、previous、hasPrevious方法，有序集合可以通过该接口访问。

## HashMap
### 工作原理
1. 定义如下所示
```
public class HashMap<K,V>
    extends AbstractMap<K,V>
    implements Map<K,V>, Cloneable, Serializable{
}
```
1. 通过hash方法以及put和get存储和获取对象。存储对象的时候，kv值传给put方法的时候，调用hashCode计算hash值得到bucket的位置，更进一步根据当前bucket的存储情况动态调整容量。获取对象的时候，通过key值计算hashCode值获取对应的bucket，然后根据equals方法确定键值对。
2. 基于Map接口实现，允许null键/值，非同步，不保证存储顺序，也不保证顺序发生变化。HashMap存储着**Entry(hash, key, value, next)**对象，当key==null的时候，存储在table[0]中hash值为0.HashMap对key==null的情况单独处理。
3. Capacity的默认值为16，Capacity就是bucket的大小
4. 负载因子的默认值为0.75，就是bucket填满程度的最大比例，当填充程度大于负载因子的时候，容量会扩大二倍。
5. HashMap中有一个modCount，实现了`fast-fail`机制（快速失败），在并发的集合中，进行迭代操作的时候，若其他线程对HashMap进行结构性改变，会立即抛出`ConcurrentModificationException`异常，而不用等遍历结束的时候才能知道。

### 自定义对象作为Key
1. 可以使用任何对象作为键，只要它遵守了equals()和hashCode()方法的定义规则，并且当对象插入到Map中之后将不会再改变了。
2. 重写hashCode和equals方法需要注意：
```
    //方法签名
    @Override
    public int hashCode(){
    
    }
    //方法签名
    @Override
    public boolean equals(Object obj){
    
    }
```
在每个覆盖了equals方法的类中也必须覆盖hashCode方法，如果不这样做的话，就会违反Object.hashCode的通用约定，从而导致该类无法结合所有基于散列的集合一起正常运转，这样的集合包括HashMap, HashSet和Hashtable.

### 序列化
#### 问题
HashMap实现了Serializable接口，但是对table的定义（transient Entry<K,V>[] table = (Entry<K,V>[]) EMPTY_TABLE;）却是transient的。然后又自己实现了writeObject()和readObject()两个方法，而我们知道声明为transient的变量不再是对象持久化的一部分。那为什么要做么做呢?这么实现的原因有两点
1. HashMap的put与get基于hashCode的实现，但是hashCode方法是native方法，因此对每个不同的java环境，hashCode的值是不一样的。而反序列化后的table的index也会发生变化，无法还原。
2. HashMap的默认值达到阈值后进行扩容，很明显HashMap布恩保证每个bucket都有数据，很多都为null，对这部分数据进行序列化会浪费很多资源。

### 与HashTable的区别
两者的相同点是都实现了Map接口。他们之间的区别主要有以下四点：
1. HashMap是**非synchronized**的，而HashTable是**synchronized**，因此HashTable可以直接用于多线程环境中，而HashMap必需使用同步或者锁操作。
2. HashMap可以接受null作为key和value，而HashTable不能接受null作为key和value，会抛出空指针异常。
3. HashMap的迭代器(Iterator)是fail-fast迭代器，而Hashtable的enumerator迭代器不是fail-fast的。
4. Hashtable和HashMap它们两个内部实现方式的数组的初始大小和扩容的方式。HashTable中hash数组默认大小是11，增加的方式是 old*2+1。HashMap中hash数组的默认大小是16，而且一定是2的指数。

##参考
[Java集合框架：HashMap](http://www.importnew.com/18604.html)











