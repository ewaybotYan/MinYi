# 笔记: How To Tango With Django 1.7

这是一个学习笔记，来源: 

- http://www.tangowithdjango.com/book17/
- https://github.com/leifos/tango_with_django

## 新增内容

从Django 1.7开始对于数据库的操作有所改变，比如migratesql和migrate。


## 概览

这个教程会学到的内容，同时也是一个django知识点清单:

- 建立开发环境，包括使用终端、pip、git等
- 设置Django项目并创建基本的django应用
- 配置项目以支持静态文件
- 熟悉**模型-视图-模板**设计模式
- 创建数据模型并使用django的ORM
- 创建表单以便动态生成网页
- 使用Django的用户授权服务
- 引入外部服务到应用中
- 加入CSS与JavaScript
- 设计与应用CSS
- Cookie与会员
- AJAX
- 部署应用到PythonAnywhere

这个教程过程以建立一个叫Rango的应用，在这个过程中会涉及web开发需要的各个部分。


## 准备工作

建立环境:

```
$ mkdir Rango
$ cd Rango
$ mkvirtualenv rango
$ workon rango
$ pip install -U django==1.7
$ pip install pillow
$ pip freeze > requirements.txt
```

## Django基础


### 创建项目

```
$ django-admin.py startproject tango_with_django_project
```

运行:

```
$ cd tango_with_django_project
$ python manage.py runserver
$ python manage.py migrate
```

### 创建应用

```
$ python manage.py startapp rango
```

将 **range** 添加到 tango_with_django_project/settings.py:

```
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rango',
    )
```

### 创建View

range/view.py:

```
from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("Rango says hey there world!")
```

### 映射应用的URL

rango/urls.py:

```
from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'))
```

### 映射项目的URL

tango_with_django_project/urls.py:

```
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'tango_with_django_project.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^rango/', include('rango.urls')),
                       )
```


此时可以运行项目。

### 工作流

- 创建项目
- 创建应用
  - 创建应用，将应用添加到项目的settings.py中
  - 为应用添加视图，修改views.py
  - 为应用添加路由，修改urls.py
  - 将应用路由添加到项目路由文件urls.py中
- 测试


## 模板与静态文件

### 使用模板

创建静态文件目录:

```
$ mkdir -p templates/rango/
```

在项目设置文件settings.py中添加静态文件目录配置:

```
TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')
TEMPLATE_DIRS = (
    TEMPLATE_PATH,
    )
```

添加模板文件templates/rango/index.html:

```
<!DOCTYPE html>
<html>

    <head>
            <title>Rango</title>
    </head>
    
    <body>
      <h1>Rango says...</h1>
      hello world! <strong>{{ boldmessage }}</strong><br />
      <a href="/rango/about/">About</a><br />
    </body>
</html>
```

修改rango/views.py以使用模板文件:

```
from django.shortcuts import render

def index(request):
    context_dict = {'boldmessage': "I am bold font from the context"}
    return render(request, 'rango/index.html', context_dict)
```

函数render第二个参数是使用的模板文件，第三个参数是一个字典，用于动态替换模板里面的变量。


### 静态多媒体文件支持

创建静态文件目录:

```
$ mkdir -p static/images
```

配置项目settings.py文件添加静态文件目录:

```
STATIC_PATH = os.path.join(BASE_DIR,'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    STATIC_PATH,
    )
```

其中，STATIC_URL是访问静态文件的URL，而STATICFILES_DIRS是配置的静态文件的路径。


在模板文件中使用静态文件(templates/rango/index.html):

```
<!DOCTYPE html>

{% load staticfiles %}<!-- New line -->

<html>
    <head>
      <title>Rango</title>
    </head>
    <body>
      <h1>Rango says...</h1>
      hello world! <strong>{{ boldmessage }}</strong><br />
      <a href="/rango/about/">About</a><br />
      <img src="{% static "images/rango.jpg" %}" alt="Picture of Rango" /> <!-- New line -->
    </body>
</html>
```


注意，第一行的 **<!DOCTYPE html>** 是不可少的。

在实际生产环境部署时，需要将DEBUG设置为False，同时设置ALLOWED_HOSTS；同时，此时修改urls.py来支持static文件.


**存疑： DEBUG模式与static、media文件的问题？**


## 模型与数据库

修改rango/models.py:

```
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    
    def __unicode__(self):      #For Python 2, use __str__ on Python 3
        return self.name
                
class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
                                
    def __unicode__(self):      #For Python 2, use __str__ on Python 3
        return self.title
```

### 创建模型与数据库

模型发现变化:

```
$ python manage.py makemigrations rango
Migrations for 'rango':
  0001_initial.py:
  - Create model Category
  - Create model Page
  
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, rango, contenttypes, auth, sessions
  Running migrations:
    Applying rango.0001_initial... OK
    
$ python manage.py sqlmigrate rango 0001 # 查看具体执行的SQL语句    
```

创建管理员来管理数据库:

```
$ python manage.py createsuperuser
```

### Django shell

```
$ python manage.py shell
>>> from rango.models import Category
>>> print Category.objects.all()
[]
>>> c = Category(name="Test")
>>> c.save()
>>> print Category.objects.all()
[<Category: Test>]
>>> quit()
```

### 配置管理接口

Django自带了管理界面，访问URL是 **/admin/** :

```
url(r'^admin/', include(admin.site.urls)),
```

要管理新建立的模型，则需要注册到管理接口中, rango/admin.py:

```
from django.contrib import admin

# Register your models here.
from rango.models import Category, Page

admin.site.register(Category)
admin.site.register(Page)
```

这样就可以在管理界面管理模型数据了。


### 脚本化支持

为了测试的方面，使用脚本填充模拟数据 populate_rango.py:

```
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from rango.models import Category, Page


def populate():
    python_cat = add_cat('Python')
    
    add_page(cat=python_cat,
          title="Official Python Tutorial",
          url="http://docs.python.org/2/tutorial/")
                                  
    add_page(cat=python_cat,
          title="How to Think like a Computer Scientist",
          url="http://www.greenteapress.com/thinkpython/")
                                                                
    add_page(cat=python_cat,
          title="Learn Python in 10 Minutes",
          url="http://www.korokithakis.net/tutorials/python/")
                                                                                              
    django_cat = add_cat("Django")
    
    add_page(cat=django_cat,
          title="Official Django Tutorial",
          url="https://docs.djangoproject.com/en/1.5/intro/tutorial01/")
          
    add_page(cat=django_cat,
          title="Django Rocks",
          url="http://www.djangorocks.com/")
          
    add_page(cat=django_cat,
          title="How to Tango with Django",
          url="http://www.tangowithdjango.com/")
          
    frame_cat = add_cat("Other Frameworks")
    
    add_page(cat=frame_cat,
          title="Bottle",
          url="http://bottlepy.org/docs/dev/")
          
    add_page(cat=frame_cat,
         title="Flask",
         url="http://flask.pocoo.org")
         
    # Print out what we have added to the user.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(p))
            
def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p
    
def add_cat(name):
    c = Category.objects.get_or_create(name=name)[0]
    return c
    
# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()
```

通过这个脚本就可以脚本化测试。


### 定制管理界面

改成一行显示所有信息的形式, rango/admin.py:

```
from django.contrib import admin

# Register your models here.
from rango.models import Category, Page

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','views','likes')
    
class PageAdmin(admin.ModelAdmin):
    list_display = ('category', 'title','url','views')
        
admin.site.register(Category,CategoryAdmin)
admin.site.register(Page,PageAdmin)
```

更多定制细节，参考: https://docs.djangoproject.com/en/1.7/intro/tutorial02/


### 基本流程

- 修改应用的models.py，更新或添加模型
- 在应用的admin.py里面注册新模型
- 通知模型的变更，执行 ``python manage.py makemigrations``
- 应用模型的变更，执行 ``python manage.py migrate``
- 建立脚本化测试


## 模型-模板-视图

### 数据驱动页面

在Django中创建数据驱动页面需要5步:

- 将模型导入views.py文件
- 在视图中获取模型的数据
- 将模型数据传给模板
- 在模板文件中使用模型数据
- 在urls.py中为新视图添加映射

### 导入模型，修改视图

```
# Import the Category model
from rango.models import Category

def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    
    # Render the response and send it back!
    return render(request, 'rango/index.html', context_dict)
```

### 更新模板文件

```
<!DOCTYPE html>
<html>
    <head>
      <title>Rango</title>
    </head>
                
    <body>
      <h1>Rango says...hello world!</h1>
      
      {% if categories %}
        <ul>
          {% for category in categories %}
             <li>{{ category.name }}</li>
          {% endfor %}
        </ul>
      {% else %}
        <strong>There are no categories present.</strong>
      {% endif %}
      
      <a href="/rango/about/">About</a>
    </body>
</html>
```

这样，在首页就可以动态显示数据库中前五个标签了。


### URL设计与映射

一般的url可能是 ``/rango/category/1/`` 但这样的url不够友好，数字具体代表什么必须点开之后才知道，改成 ``/rango/category/category-name/`` 的形式。

为了处理name里面包含空格的情况，必须引入 ``slugify`` 函数,可以将 ``how do i create a slug in django`` 转换为 ``how-do-i-create-a-slug-in-django``.


### 增加slug field

```
from django.template.defaultfilters import slugify

class Category(models.Model):
        name = models.CharField(max_length=128, unique=True)
        views = models.IntegerField(default=0)
        likes = models.IntegerField(default=0)
        slug = models.SlugField(unique=True)
                                
        def save(self, *args, **kwargs):
            self.slug = slugify(self.name)
            super(Category, self).save(*args, **kwargs)
            
        def __unicode__(self):
           return self.name
```

更新模型:

```
$ python manage.py makemigrations rango
$ python manage.py migrate
```

由于之前的数据里面没有slug而报错，可以先删掉数据再之后用脚本更新模拟数据。


修改admin.py:

```
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
```


### 新视图

```
def category(request, category_name_slug):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}
        
    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        
        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)
        
        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
     except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass
        
     # Go render the response and return it to the client.
     return render(request, 'rango/category.html', context_dict)
```

通过 ``Category.objects.get(slug=category_name_slug)``来获取需要的数据。


### 新模板文件

```
<!DOCTYPE html>
<html>
    <head>
        <title>Rango</title>
    </head>
    <body>
        <h1>{{ category_name }}</h1>
        {% if category %}
           {% if pages %}
           <ul>
               {% for page in pages %}
                   <li><a href="{{ page.url }}">{{ page.title }}</a></li>
               {% endfor %}
           </ul>
           {% else %}
               <strong>No pages currently in category.</strong>
           {% endif %}
        {% else %}
           The specified category {{ category_name }} does not exist!
        {% endif %}
    </body>
</html>
```


### 增加映射url

```
url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
```

相应更新首页模板则可以了。



## 玩转表单


要增加对表单的支持，基本流程是:

- 为应用添加forms.py
- 为需要的模型尽力ModelForm类
- 在视图、模板增加对表单的处理

### rango/forms.py

```
from django import forms
from rango.models import Page, Category

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
                
    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)
                                                
                                                
class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page
    
        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ('category',)
        #or specify the fields to include (i.e. not include the category field)
        #fields = ('title', 'url', 'views')
```



### 增加表单视图

```
from rango.forms import CategoryForm

def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
                
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            
            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
     else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()
        
     # Bad form (or form details), no form supplied...
     # Render the form with error messages (if any).
     return render(request, 'rango/add_category.html', {'form': form})
```

### 表单模板文件

```
<!DOCTYPE html>
<html>
    <head>
            <title>Rango</title>
    </head>
                
    <body>
      <h1>Add a Category</h1>
      
      <form id="category_form" method="post" action="/rango/add_category/">
      
         {% csrf_token %}
         {% for hidden in form.hidden_fields %}
            {{ hidden }}
         {% endfor %}
         
         {% for field in form.visible_fields %}
            {{ field.errors }}
            {{ field.help_text }}
            {{ field }}
         {% endfor %}
         
         <input type="submit" name="submit" value="Create Category" />
       </form>
     </body>
</html>
```

### 添加url映射

```
url(r'^add_category/$', views.add_category, name='add_category'),
```

### clean()函数对表单数据预处理

ModelForm有一个clean函数，会在将表单数据保存为模型实例前调用，可以覆盖此方法来进行一些预处理，如:

```
def clean(self):
    cleaned_data = self.cleaned_data
    url = cleaned_data.get('url')
                
    # If url is not empty and doesn't start with 'http://', prepend 'http://'.
    if url and not url.startswith('http://'):
       url = 'http://' + url
       cleaned_data['url'] = url
       
    return cleaned_data
```

表单的数据以字典的形式保存在``cleaned_data``中.

### add_page视图

```
from rango.forms import PageForm

def add_page(request, category_name_slug):

    try:
         cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
         cat = None
                                
    if request.method == 'POST':
         form = PageForm(request.POST)
         if form.is_valid():
             if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
          else:
              print form.errors
     else:
          form = PageForm()
          
     context_dict = {'form':form, 'category': cat}
     
     return render(request, 'rango/add_page.html', context_dict)
```

相应的url映射是:

```
url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$',views.add_page,name='add_page'),
```

这样设计的url可以通过url很清晰的得知行为的目的.

### 理解url映射规则

如:

```
url(r'^test/(\d{4})/(\d{2})/$', test_view,name="the_test_view"),
url(r'^test/(?P<year>\d{4})/(?P<month>\d{2})/$', test_view,name="the_test_view"),
```

- 第一个映射为 ``test_view(request,2015,05)``,在模板里面不需要指定参数名
- 第二个映射为 ``test_view(request,year=2015,month=05)``，在模板里面需要指明参数，如``{% url 'the_test_view' year=2015 month=05 %}``
- url配置中的``name``作用是在模板里面使用url的name，即使更新了url映射路径，但只要name没变，就不需要修改模板,如这里的``the_test_view``


## 用户授权


