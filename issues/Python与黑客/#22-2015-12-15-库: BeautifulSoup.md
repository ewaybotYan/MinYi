[LeslieZhu](https://github.com/LeslieZhu) on 2015-12-15:


# 库: BeautifulSoup

![](http://www.crummy.com/software/BeautifulSoup/10.1.jpg)

[Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/) 是一个可以从HTML或XML文件中提取数据的Python库，它可以高效的将文档解析成树结构，然后提供方法进行提取、搜索、修改等操作，结合爬虫一起使用效果更佳。

安装:

```
$ pip install beautifulsoup4
$ pip install lxml
```

基本使用:

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(open("index.html"))

soup = BeautifulSoup("<html>data</html>")
```

详细文档: http://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/

