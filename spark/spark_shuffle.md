# <center>spark shuffle
## shuffle过程划分
1. shuffle write:map端划分数据、持久化数据的过程
2. shuffle read：reduce端读入数据、aggregate数据的过程

## Hash shuffle
### shuffle write
不要求数据有序：将数据partition好并持久化.持久化的原因：减少内存存储空间压力以及fault-tolerance
。实现方式也比较简单：将shuffle write的处理逻辑加入ShuffleMapStage的最后，该stage的finalRdd每输出一个record就将其partition并持久化。
