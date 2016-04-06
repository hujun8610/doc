#<center> scala常见问题
## scala类型
scala的类型系统只能保证不合理的程序不能编译通过，并不能保证每一个合理的的程序都可以编译通过。而且需要注意的是**所有的类型信息在编译的时候都会被删去，称之为类型擦除。**
scala中的类型系统具有非常强大的表现力，主要特性如下：
1. 支持泛型
2. 支持类型推断
3. 对没有名称的类型进行定义

下面将从这三个方面来介绍scala的类型系统

### 泛型
泛型一般用于给不同类型的值来编写通用代码。泛型的使用也非常简单，如下所示：
```
//定义了一个泛型A
scala> def drop1[A](l: List[A]) = l.tail
drop1: [A](l: List[A])List[A]
//传入了一个Int类型的list
scala> drop1(List(1,2,3))
res1: List[Int] = List(2, 3)
```
注意scala并不支持过于泛化的泛型，如下所示：
```
def foo[A, B](f: A => List[A], b: B) = f(b)   //scala无法同时支持两个类型的泛型
```

### 类型推断
与java不同，scala有着非常强大的类型推断能力。其所有的类型推断都是局部的，也就是说一次只能分析一个表达式。如下所示：
```
scala> def id[T](x: T) = x
id: [T](x: T)T

scala> val x = id(322   //推断出类型为Int
x: Int = 322

scala> val x = id("hey")   //推断出类型为String
x: java.lang.String = hey
```

### 协变与逆变
#### 定义
如果B是A的一个子类，那么Container[A]与Container[B]之间的关系可以用协变和逆变来定义

|  | 含义 | scala标记 |
|--------|--------|
|协变|C[B]是C[A]的子类 | [+T]|
|逆变|C[B]是C[A]的父类 |[-T] |
|不变|C[B]和C[A]无关  |[T]  |
子类型的真正含义：对于一个给定的类型T，如果T'是其子类型，则T'可以替代T
协变的使用：
```
 //class定义了+T，而func的返回值定义的T，T是+T的子类，此处是协变的使用，协变使用了更具体的子类，增强了处理能力
 class A[+T] {
    def func(): T = {
      null.asInstanceOf[T]
    }
  }
```
逆变的使用
```
//class 定义-T，而func中参数定义了T，-T是T的父类，因此接受的参数的范围更加广泛，为逆变的使用场景
   class A[-T] {
    def func(x: T) {}
  }
```

#### 优点
参数逆变：正是因为需要符合里氏替换法则，方法中的参数类型声明时必须符合逆变（或不变），以让子类方法可以接收更大的范围的参数(处理能力增强)；而不能声明为协变，子类方法可接收的范围是父类中参数类型的子集(处理能力减弱)。这样对于一些子类的公共方法，可以上升到基类中去，增强了调用的灵活性，同时避免了一些列的类型判断。
返回值协变：如果结果类型是逆变的，那子类方法的处理能力是减弱的，不符合里氏替换。
一句话：**函数参数中只能使用不变或者逆变（能够接受更大范围的参数），返回值只能选择协变或者不变（具体的子类处理的能力更强）**

### 边界
与java相同，scala也可以通过边界来限定泛型：
1：上限
```
[T<:A]或者[_ <:A]表示T是A的一个子类型
```
2: 下限
```
[T>:A]或者[_ >:A]表示T是A的父类型
```

### 通配符
当不太关心类型变量的名称的时候可以使用`_`来代替，如下：
```
scala> def count[A](l: List[A]) = l.size
等价于：
def count(l: List[_]) = l.size
```

## 集合框架
### 可变集合与不可变集合
Scala集合系统的区分了可变和不可变集合。可变集合可以在适当的时候进行扩展，而不可变集合永远不会发生改变，但是也可以模拟添加、删除操作，只是会返回一个新的集合。可变集合几种`scala.collection.mutable`中，不可变集合集中中`scala.collection.immutable`中，scala默认使用不可变集合。可变集合与不可变集合的区别是不可变集合类的客户端可以确保不会被修改，**但是仅能保证集合本身不会被修改，并不能保证集合中内容也不会被修改。**
一个有用的约定，如果希望同时使用可变集合和不可变集合只需要导入`collection.mutable`即可。

### 不可变集合继承图
![](http://docs.scala-lang.org/resources/images/collections.png)

上图的集合类都是抽象类或者特质，可以看到所有的集合类都继承了`Traversable`特质，表示可遍历。
下面的图是多有不可变集合的类图：
![](http://docs.scala-lang.org/resources/images/collections.immutable.png)

可以看到`Array`,`String`都是·Seq·的子类，`TreeMap`是SortedMap的实现。由于这些集合都是不可变的，他们可以很容易的直接应用在多线程环境中，并不需要特殊的同步操作。

### 可变集合
可变集合类图如下所示：
![](http://docs.scala-lang.org/resources/images/collections.mutable.png)

可变集合最大的特点是为了使用多线程环境，添加了一些同步的集合类。




## option[T]、Any、Nothing、Null和Nil
1. option[T]主要是用来避免NullPointerException异常的(Option本身是一个容器),可以使用`getOrElse` 方法

```
val option1: Option[Int] = Some(123)
val option2: Option[Int] = None  

val value1 = option1.getOrElse(0) //返回123
val value2 = option2.getOrElse(0)  //返回0
```
2. Any是abstract类，它是Scala类继承结构中最底层的。所有运行环境中的Scala类都是直接或间接继承自Any这个类，它就是其它语言（.Net，Java等）中的Object。
3. Nothing是所有类型的子类，Nothing没有对象，但是可以用来定义类型。
4. Null是所有AnyRef的子类，在scala的类型系统中，AnyRef是Any的子类，同时Any子类的还有AnyVal。
5. Nil是一个空的List，定义为List[Nothing]，根据List的定义List[+A]，所有Nil是所有List[T]的子类。


## 参考文件
[类型与多态基础](https://twitter.github.io/scala_school/zh_cn/type-basics.html)
[scala逆变有什么用](https://www.zhihu.com/question/35339328)
[协变点与逆变点](http://hongjiang.info/scala-pitfalls-10/)
[Null, null, Nil, Nothing, None, and Unit in Scala](http://sanaulla.info/2009/07/12/nothingness-2/)
[scala集合性能比较](http://docs.scala-lang.org/zh-cn/overviews/collections/performance-characteristics)
[mutable和immutable集合](http://docs.scala-lang.org/zh-cn/overviews/collections/overview)