# Cloze-Tests-Automatic-Generation
一个完形填空自动生成算法，在给定一个单词时可以自动生成该单词的完形填空问题。

### 1. 简介

我们以**副词**为研究对象。选择副词主要有三点原因：
1. 副词被认为是开放类词(如动词、名词)和封闭类词(如连词、介词)之间的词性，对副词的研究很容易扩展到其他词性；
2. 副词在句子中很容易被同类的其他副词替换，因此需要考虑如何避免副词在完形填空问题中的多解现象；
3. 学习者有时会根据词性判断作为解题技巧，选择副词能够避免这种现象。

我们使用**剑桥高级学习词典**(**CALD**)语料库作为例句的来源，在选择句子时，我们采取以下标准：
1. 复杂性和语法性：通过**Stanford解析器**评估。**Stanford**解析器是一个开源句法分析器，通过生成句子的成分分析树来评估句子的复杂性和语法性；
2. 上下文关联性：计算目标单词与句子中其他词之间组成单词对的出现频率似然比作为关联性得分；
3. 句子长度：大多数情况下较短的句子被认为质量较低。

通过将上述得分归一化后相乘作为句子选择的标准。在选择错误选项即干扰词时首先使用**WordNet**选择同义词，再根据两个标准进行筛选：选择在语法和搭配上得分较高的干扰词；选择与目标单词在语义上“足够远”的干扰词。算法的整体流程如下。

![](https://github.com/0809zheng/Cloze-Tests-Automatic-Generation/blob/main/images/pipeline.png)

一个简单的**GUI**展示如下。当输入单词**regularly**时，会自动生成该单词的完形填空问题。

![](https://github.com/0809zheng/Cloze-Tests-Automatic-Generation/blob/main/images/gui.png)

### 2. 调试环境

使用 **Python3.6** 作为编程语言；

其中核心算法使用了 **nltk** 平台，编译之前需要下载其中的**gutenberg, genesis, inaugural, nps_chat, webtext, treebank, wordnet** 等语料库；

需要自行下载 **stanford parser** 并修改相关参数；

还需要使用剑桥高级学习词典(**CALD**)语料库作为例句的来源，此库不在 **nltk** 上，需要自行下载并处理。


### 3. 代码说明

核心算法都在 `generator.py` 文件中，该文件函数结构：

```
generator.py
|-- get_synonym(w)  # 得到 w 的同义词序列
|-- get_sentences(w)  # 得到含有单词 w 的句子序列
|-- get_complexity_score(sens)  # 计算句子序列中每一个句子的复杂性得分
|-- get_context_score(sens)  # 计算句子序列中每一个句子的上下文得分
|
|-- get_grammar_score(sens, w)  # 计算句子序列中每一个句子的语法得分
|-- get_length_score(sens)  # 计算句子序列中每一个句子的长度得分
|
|-- get_distracts(sen, w)  # 得到针对句子 sen 和单词 w 的干扰项序列
|
|-- main  # 一个运行函数，可以在终端运行并输出找到的句子序列、
		  # 每个句子的得分、干扰项排序、生成的题目等
```

一个简单的 **GUI** 代码在 `gui.py` 中。
