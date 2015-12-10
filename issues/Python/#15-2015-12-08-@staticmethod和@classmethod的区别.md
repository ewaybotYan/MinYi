LeslieZhu on 2015-12-08:


- 原文链接: [what-is-the-difference-between-staticmethod-and-classmethod-in-python](http://stackoverflow.com/questions/136097/what-is-the-difference-between-staticmethod-and-classmethod-in-python)

这是**StackOverFlow**上一个讨论，觉得很不错，翻译整理如下。

用户`unutbu`的回答:

或许用一些代码作为例子比较好理解，注意对于class_foo和static_foo的定义:

```python
class A(object):
    def foo(self,x):
        print "executing foo(%s,%s)"%(self,x)

    @classmethod
    def class_foo(cls,x):
        print "executing class_foo(%s,%s)"%(cls,x)

    @staticmethod
    def static_foo(x):
        print "executing static_foo(%s)"%x

a=A()
```

下面是类实例调用普通函数的一般用法，类实例(self)作为第一个参数传递进去:

```python
a.foo(1)
# executing foo(<__main__.A object at 0xb7dbef0c>,1)
```

通过 **classmethod**，函数实例代替**self**作为第一个参数传递给函数:

```
a.class_foo(1)
# executing class_foo(<class '__main__.A'>,1)
```

你也可以直接通过类调用class_foo，实际上如果要调用classmethod，最好用类来调用，而不是类实例:

```python
A.class_foo(1)
# executing class_foo(<class '__main__.A'>,1)
```

有些人通过classmethod来创建可选择性继承构造器。

对于staticmethods，不管是self(类实例)还是cls(类)都可以作为其第一个参数，即可通过类调用，也
可以通过类实例调用:
```
a.static_foo(1)
# executing static_foo(1)

A.static_foo('hi')
# executing static_foo(hi)
```

Staticmethod常常用于将一些和某个类相关的函数包含到类定义中去.

foo是一个函数，但调用a.foo的时候不是直接就调用这个函数，而是调用一个特殊版本的函数，在这个函数
里面第一个参数和实例a绑定了。foo需要2个参数，但a.foo只需要传递1个参数.

a绑定到了foo上，如:

```
print(a.foo)
# <bound method A.foo of <__main__.A object at 0xb7d52f0c>>
```

对于a.class_foo, a并没有绑定到class_foo上，而是将类A直接绑定到class_foo上:

```
print(a.class_foo)
# <bound method type.class_foo of <class '__main__.A'>>
```

相比而言，staticmethod只是一个函数，a.static_foo仅仅返回一个没有绑定任何参数的函数，
static_foo需要一个参数，而a.static_foo也只需要一个参数:

```
print(a.static_foo)
# <function static_foo at 0xb7d479cc>
```

`Alcott` 问:

```
我不明白为什么要是有staticmethod，我们可以直接使用一个在类定义之外的函数啊?
```

`unutbu` 答:

```
Alcott, 当一个函数在逻辑上属于某个类，你可能会把这个函数放到类的定义里面。在Python程序中，
staticmethod以前是作为模块名字空间的私有函数。但只有少部分模块这样做，可能这样的风格不够优雅。
虽然我没有找到具体例子，但@staticmethod应该可以通过子类重载让代码更有条理。如果没有
staticmethod，你就需要在模块名字空间搞出一堆函数来。
```

`MestreLion` 答:

```
Alcott,正如unutbu所言，staticmethod是一个和组织代码/代码风格有关的特性。有时候，一个模块有
多个类，并且有些辅助性函数在逻辑上只适用于特定类，其他类不能使用。这个时候，就不应该在模块中保留
这么多这种函数，最好还是static method的方式来表明这些函数和某个类是有关联的，而不是把他们和其
他一堆函数定义混在一块。
```

`SilentDirge` 答:

```
Python不支持类似C++的名字空间，通过@staticmethod仅仅是将函数从全局名字空间移走，以保持模块
名字空间干净.
```

总结:

- `@classmethod`:
  - 和类关联，可以访问类私有成员，常用于做工厂函数
  - 继承不会破坏这种关系，因为类作为第一个参数传入
- `@staticmethod`:
  - 优化代码组织风格，不和类或类实例关联
  - 是类的辅助性函数



# 评论


MestreLion on 2015-12-08T06:33:43Z:

 What? 

LeslieZhu on 2015-12-08T07:39:46Z:

 Oops... I found [what-is-the-difference-between-staticmethod-and-classmethod-in-python](http://stackoverflow.com/questions/136097/what-is-the-difference-between-staticmethod-and-classmethod-in-python) on stackoverflow, and I translated some answers by keep the author ,like `@someone: balabala`. But i forgot to add quote character before and after the `@someone`, so the GitHub issues notify functional may auto send a message to you, i'm so sorry for that. 

