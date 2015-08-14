# Python游戏编程入门

买的《Python游戏编程入门》书籍到了，准备记录点学习Pygame开发2D游戏的笔记。


## 建立开发环境

由于书籍例子使用python3.2+pygame1.9,因此保持一致。其实，如果使用python2.7的话，应该更多软件包可以使用。

我使用的Mac，而pygame编译好的安装包只有windows版本，需要自己源码安装.


建立虚拟python环境:

```
$ python -m venv venv
$ source venv/bin/active
```

下载源码文件后，安装:

```
$ brew install sdl sdl_image sdl_mixer sdl_ttf portmidi
$ pip install hg+http://bitbucket.org/pygame/pygame
```

经过测试，发现使用python2.7完成可以运行所有的例子，因此使用python2.7，省去很多麻烦.

```
$ virtualenv envpygame
$ source envpygame/bin/activate
$ python --version
Python 2.7.6
 
$ pip install hg+http://bitbucket.org/pygame/pygame
  
$ pip list
 
pip (1.5.6)
pygame (1.9.2a0)
setuptools (3.6)
wsgiref (0.1.2)
```

## 简单示例

```python
import pygame
from pygame.locals import *
import sys

# 初始化Pygame资源
pygame.init()                      

screen = pygame.display.set_mode((600,500))

pygame.display.set_caption("Hello Pygame")

myfont = pygame.font.Font(None,60)

white = 255,255,255
blue = 0,0,255

textImage = myfont.render("Hello Pygame",True,white)


screen.fill(blue)
screen.blit(textImage,(100,100))   # 绘制图形

pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type in (QUIT,KEYDOWN):
            sys.exit()
                        
    screen.fill(blue)
    screen.blit(textImage,(100,100))
    pygame.display.update()
```
