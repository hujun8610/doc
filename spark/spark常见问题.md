# Spark常见问题
## 环境问题
1. windows下运行程序Failed to locate the winutils binary in the hadoop binary path
报错原因：
查看源码发现程序需要根据HADOOP_HOME找到winutils.exe,由于win机器并没有配置该环境变量，所以程序报 null\bin\winutils.exe
解决方案：
在网上下载对应版本的winutils，解压后。配置HADOOP_HOME环境变量。然后在path中添加$HADOOP_HOME\bin即可。



## 参考文档
[winutils问题解决方案](http://www.cnblogs.com/zq-inlook/p/4386216.html)