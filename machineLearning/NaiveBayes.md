#<center> Navie Bayes
## 基本原理



## spark实现
### 准备数据
本实验的数据来自[数据堂](http://www.datatang.com/datares/go.aspx?dataid=617586)，其数据格式如下所示：
```
data format
1. author.txt: "author_id"
2. conf.txt: "conf_id"
3. term.txt: "term_id"
4. paper.txt: "paper_id"
5. paper_author: "paper_id	author_id"
6. paper_conf: "paper_id	conf_id"
7. paper_term: "paper_id	term_id"
8. ground_truth: "paper_id	true_classification"
```
考虑使用Bayes实现这样一个需求：
根据论文(paper)中出现的关键字(term)来对文章进行分类，并计算分类的准确率、召回率以及AOC值。使用的数据是paper_term。

### 算法执行流程
1: 将原始数据转换为词向量
2：使用部分词向量训练来训练模型，得到bayes模型的参数(一个向量)
3：使用剩余的词向量验证模型，计算准确率、召回率以及AOC的值
4：调整训练数据和测试数据的比例，再次计算准确率和召回率，汇总得到一个折线图。

#### 词向量

