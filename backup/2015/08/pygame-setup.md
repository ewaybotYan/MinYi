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


## 绘制不同形状

使用`pygame.draw`来绘制图形，如:

- `pygame.draw.circle()`
- `pygame.draw.rect()`
- `pygame.draw.line()`
- `pygame.draw.arc()`

画弧线举例:

```python
start_angle = math.radians(0)
end_angle = math.radians(90)
pygame.draw.arc(screen, color, position, start_angle, end_angle, width)
```

## 事件监听举例


```python
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYUP:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_1:
                piece1 = True
            elif event.key == pygame.K_2:
                piece2 = True
            elif event.key == pygame.K_3:
                piece3 = True
            elif event.key == pygame.K_4:
                piece4 = True
                
     #.....
```

在监听事件的时候一般只设置变量，然后再根据变量进行后续操作。

## 用pygame打印文本


以图片的形式绘制文本:

```python
myfont = pygame.font.Font("Arial",30)
image = myfont.render(text,True,(255,255,255))
screen.blit(image,(100,100))
```

## 键盘事件

一般按键事件分为`KEYDOWN`,`KEYUP`，如果要在按键持续按住的情况下持续产生事件，需要设置:

```python
pygame.key.set_repeat(10)  # 表示每个10毫秒一个事件
```

## 鼠标事件

Pygame支持的鼠标事件包括:`MOUSEMOTION`,`MOUSEBUTTONUP`,`MOUSEBUTTONDOWN`.

```python
for event in pygame.event.get():
    if event.type == MOUSEMOTION:
        mous_x,mouse_y = event.pos
        move_x,move_y = event.rel
    elif event.type == MOUSEBUTTONDOWN:
        mouse_down = event.button
        mouse_down_x,mouse_down_y = event.pos
    elif event.type == MOUSEBUTTONUP:
        mouse_up = event.button
        mouse_up_x,mouse_up_y = event.pos
```

## 轮询键盘

通过轮询键盘接口，可以一次性获取按键列表，不需要遍历事件系统:

```python
keys = pygame.keys.get_pressed()
if keys[K_ESCAPE]:
    sys.exit()
```

## 轮询鼠标

```python
pos_x,pos_y = pygame.mouse.get_pos()
rel_x,rel_y = pygame.mouse.get_rel()
button1,button2,button3 = pygame.mouse.get_pressed()
```






