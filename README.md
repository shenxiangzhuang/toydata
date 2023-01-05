
<p align="center" style="font-size:40px; margin:0px 10px 0px 10px">
    <em>ToyData</em>
</p>
<p align="center">
    <em>Learning Data Structures with toy code</em>
</p>

<p align="center">
<a href="https://codecov.io/gh/shenxiangzhuang/toydata" target="_blank">
    <img src="https://codecov.io/gh/shenxiangzhuang/toydata/branch/master/graph/badge.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/toydata" target="_blank">
    <img src="https://badge.fury.io/py/toydata.svg" alt="PyPI Package">
</a>
</p>


![](https://github.com/shenxiangzhuang/toydata/raw/master/toydata.png)


There are some simple implementations of classic data structures.

I am trying to do this with an easy-to-read style.

And, I add some extra functions beyond the ADTs, which are used mostly for printing and testing purposes.

# Installation
`pip install toydata`

>Note that: If you had change the default mirror of pip to another one,
>such as *https://pypi.tuna.tsinghua.edu.cn/simple* or *http://pypi.douban.com/simple* , you may have to install with `pip install toydata -i https://pypi.org/simple`


# Documentation
- [http://datahonor.com/toydata/](http://datahonor.com/toydata/)


# Data Structures

- [x] Stack: ArrayStack, LinkedStack
- [x] Queue: ArrayQueue, ArrayDeque
- [x] Deque: LinkedDeque
- [x] Positional List: PositionalList
- [x] Priority Queues: UnsortedPriorityQueue, SortedPriorityQueue, HeapPriorityQueue
- [x] LinkedLists: Singlellist, Doublellist
- [x] Hash Tables: ChainHashMap, ProbeHashMap, SortedTableMap
- [x] Trees: LinkedBinaryTree
- [x] Search Trees: AVLTreeMap, SplayTreeMap, RedBlackTreeMap
- [x] Graph: Adjacency Map, DFS/BFS, Floyd-Warshall



# References

## Books

[*Data Structures and Algorithms in Python, Michael T. Goodrich*](https://www.amazon.com/Structures-Algorithms-Python-Michael-Goodrich/dp/1118290275/ref=sr_1_4?qid=1580122939&refinements=p_27%3AMichael+T.+Goodrich&s=books&sr=1-4&text=Michael+T.+Goodrich)
is the **main reference** of the implementations.

Note that there is a book named [*Data Structures and Algorithms in C++, Michael T. Goodrich*](https://www.amazon.com/Data-Structures-Algorithms-Michael-Goodrich/dp/0470383275/ref=sr_1_2?qid=1580122957&refinements=p_27%3AMichael+T.+Goodrich&s=books&sr=1-2&text=Michael+T.+Goodrich) which use C++ to implement these data structures.

And [*Data Structures Using C, Reema Thareja*](https://www.amazon.in/Data-Structures-Using-Reema-Thareja/dp/0198099304/ref=sr_1_1?qid=1580122713&refinements=p_27%3AReema+Thareja&s=books&sr=1-1) is also a great book that implement these data structures using C.


## Courses
There some courses that use the book(*Data Structures and Algorithms in Python*) as textbook.(Tell me please, if you know other courses use it:-)

1. [数据结构与算法-Python (2019秋季)，武汉大学](http://xpzhang.me/)
   >Great lecture notes.

2. [Jenny's lectures CS/IT NET&JRF](https://www.youtube.com/channel/UCM-yUTYGmrNvKOCcAl21g3w/playlists)
   >Jenny makes everything clear！
