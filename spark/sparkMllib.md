#<center> Spark Mllib总结
## 概述

## 常见问题
### mllib包与ml包区别
按照spark1.6官网上的描述：
1. mllib中的算法接口是基于RDD实现的
2. ml中的算法接口基于DataFrame实现的。

这两个包会并行发展下去，实际使用中推荐ml，建立在DataFrames基础上的ml中一系列算法更适合创建包含从数据清洗到特征工程再到模型训练等一系列工作的ML pipeline。

### mllib.linalg中的Vector与breeze.linalg中向量区别
scala的breeze库是一个用于数值计算的开源库，类似python中的numpy。
mllib.linalg：mllib机器学习用到的数据结构路向量、矩阵等。

## 参考