[LeslieZhu](https://github.com/LeslieZhu) on 2015-11-28:


# 笔记: How To Tango With Django 1.7

这是一个学习笔记，来源: 

- http://www.tangowithdjango.com/book17/
- https://github.com/leifos/tango_with_django

## 1. 新增内容

从Django 1.7开始对于数据库的操作有所改变，比如migratesql和migrate。


## 2. 概览

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


## 3. 准备工作

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

## 4. Django基础


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


## 5. 模板与静态文件

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


## 6. 模型与数据库

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


## 7. 模型-模板-视图

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



## 8. 玩转表单


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


## 9. 用户授权


Django的用户授权功能使用``django.contrib.auth``。

### 确保已经安装auth应用

在settings.py中确保在INSTALLED_APPS配置项包含``django.contrib.auth``.

### 增加User模型

User模型包含5个主要属性:

- 用户账号
- 账号密码
- 用户邮箱
- 用户的姓
- 用户的名

其它可选属性:

- **URLField**可以指定用户主页链接
- **ImageField**可以指定用户的头像

建立模型:

```
from django.contrib.auth.models import User
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
        
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
                    
    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
```

不要忘记注册管理接口和更新数据库。

### 用户注册视图与模板

增加表单:

```
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
       model = User
       fields = ('username', 'email', 'password')
                        
class UserProfileForm(forms.ModelForm):
    class Meta:
       model = UserProfile
       fields = ('website', 'picture')
```

增加视图:

```
from rango.forms import UserForm, UserProfileForm

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False
            
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        
        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
            
            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()
            
            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            
            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
                # Now we save the UserProfile model instance.
                profile.save()
                
            # Update our variable to tell the template registration was successful.
            registered = True
                
        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors
                 
         # Not a HTTP POST, so we render our form using two ModelForm instances.
         # These forms will be blank, ready for user input.
         else:
             user_form = UserForm()
             profile_form = UserProfileForm()
             
         # Render the template depending on the context.
         return render(request,
                       'rango/register.html',
                       {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )
```

注册页面模板:

```
<!DOCTYPE html>
<html>
    <head>
      <title>Rango</title>
    </head>
                
    <body>
      <h1>Register with Rango</h1>
      
      {% if registered %}
        Rango says: <strong>thank you for registering!</strong>
        <a href="/rango/">Return to the homepage.</a><br />
      {% else %}
        Rango says: <strong>register here!</strong><br />
        
        <form id="user_form" method="post" action="/rango/register/"
          enctype="multipart/form-data">
          
          {% csrf_token %}
          
          <!-- Display each form. The as_p method wraps each element in a paragraph
          (<p>) element. This ensures each element appears on a new line,
          making everything look neater. -->
          {{ user_form.as_p }}
          {{ profile_form.as_p }}
          
          <!-- Provide a button to click to submit the form. -->
          <input type="submit" name="submit" value="Register" />
        </form>
     {% endif %}
   </body>
</html>
```

如果要通过表单上传文件，则添加 ``enctype='multipart/form-data'``.

添加url映射:

```
url(r'^register/$', views.register, name='register'), 
```

### 登陆视图

```
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse

def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
        # because the request.POST.get('<variable>') returns None, if the value does not exist,
        # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
               # If the account is valid and active, we can log the user in.
               # We'll send the user back to the homepage.
               login(request, user)
               return HttpResponseRedirect('/rango/')
            else:
               # An inactive account was used - no logging in!
               return HttpResponse("Your Rango account is disabled.")
        else:
           # Bad login details were provided. So we can't log the user in.
           print "Invalid login details: {0}, {1}".format(username, password)
           return HttpResponse("Invalid login details supplied.")
           
     # The request is not a HTTP POST, so display the login form.
     # This scenario would most likely be a HTTP GET.
     else:
         # No context variables to pass to the template system, hence the
         # blank dictionary object...
         return render(request, 'rango/login.html', {})
```

函数``authenticate()``可以验证用户的正确性,函数``login()``用于登录。

**注意**: 登录后的网页跳转使用函数``HttpResponseRedirect()``.


### 登录模板

```
<!DOCTYPE html>
<html>
    <head>
      <!-- Is anyone getting tired of repeatedly entering the header over and over?? -->
      <title>Rango</title>
    </head>
    
    <body>
      <h1>Login to Rango</h1>
    
      <form id="login_form" method="post" action="/rango/login/">
        {% csrf_token %}
        Username: <input type="text" name="username" value="" size="50" />
        <br />
        Password: <input type="password" name="password" value="" size="50" />
        <br />
    
        <input type="submit" value="submit" />
      </form>
    
    </body>
</html>
```

不要忘记``{% csrf_token %}``.


可以在模板中查看用户登录验证信息:

```
{% if user.is_authenticated %}

<h1>Rango says... hello {{ user.username }}!</h1>

{% else %}

<h1>Rango says... hello world!</h1>

{% endif %}
```

### 访问控制

一种方法是直接判断:

```
def some_view(request):
    if not request.user.is_authenticated():
            return HttpResponse("You are logged in.")
    else:
            return HttpResponse("You are not logged in.")
```

第二种是使用**装饰器**:

```
from django.contrib.auth.decorators import login_required

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")
```

如果用户访问需要登录授权的页面，则会跳转到登录界面，可以在settings.py中设置默认登陆url:

```
LOGIN_URL = '/rango/login/'
```

### 登出

```
from django.contrib.auth import logout

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
        
    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')
```

修改首页模板:

```
{% if user.is_authenticated %}
  <a href="/rango/restricted/">Restricted Page</a><br />
  <a href="/rango/logout/">Logout</a><br />
{% else %}
  <a href="/rango/register/">Register Here</a><br />
  <a href="/rango/login/">Login</a><br />
{% endif %}

<a href="/rango/about/">About</a><br/>
<a href="/rango/add_category/">Add a New Category</a><br />
```

## 10. 玩转模板

目前的模板有大量重复内容，可以将通用的模板片段独立出来。

创建基础模板 templates/basic.html:

```
<!DOCTYPE html>

<html>
    <head>
      <title>Rango</title>
    </head>
    
    <body>
      <!-- Page specific content goes here -->
    </body>
</html>
```

再次强调第一行必须是``<!DOCTYPE html>``.

### 模板语句块

如:

```
<!DOCTYPE html>

<html>
    <head lang="en">
      <meta charset="UTF-8">
      <title>Rango</title>
    </head>
    
    <body>
      {% block body_block %}{% endblock %}
    </body>
</html>
```

这里定义的body_block可以在后续继承此模板的模板文件里面替换.

修改basic.html:

```
<!DOCTYPE html>

<html>
    <head>
       <title>Rango - {% block title %}How to Tango with Django!{% endblock %}</title>
    </head>
    
    <body>
       <div>
          {% block body_block %}{% endblock %}
       </div>
    
       <hr />
    
       <div>
         <ul>
           {% if user.is_authenticated %}
             <li><a href="/rango/restricted/">Restricted Page</a></li>
             <li><a href="/rango/logout/">Logout</a></li>
             <li><a href="/rango/add_category/">Add a New Category</a></li>
           {% else %}
             <li><a href="/rango/register/">Register Here</a></li>
             <li><a href="/rango/login/">Login</a></li>
           {% endif %}
    
             <li><a href="/rango/about/">About</a></li>
         </ul>
       </div>
    </body>
</html>
```

这里的title_block设置了默认值.

### 模板继承

```
{% extends 'base.html' %}

{% load staticfiles %}

{% block title %}{{ category_name }}{% endblock %}

{% block body_block %}
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
         
         {% if user.is_authenticated %}
            <a href="/rango/category/{{category.slug}}/add_page/">Add a Page</a>
         {% endif %}
        {% else %}
            The specified category {{ category_name }} does not exist!
        {% endif %}
         
{% endblock %}
```

**注意**: 继承模板的时候，路径是从模板根目录开始的，这里面继承的是``templates/basic.html``，而不是``templates/rango/basic.html``.


### 模板中引用URL

如果在urls.py中为URL映射指定了``name='about'``,则可以在模板中这样使用:

```
<li><a href="{% url 'about' %}">About</a></li>
```

否则:

```
<li><a href="{% url 'rango.views.about' %}">About</a></li>
```

这样即使后期urls.py中映射修改了，只要name不变，则不需要在所有模板文件中修改一遍，更好维护.

对于带有参数的url映射，使用方法如:

```
{% for category in categories %}
    <li><a href="{% url 'category'  category.slug %}">{{ category.name }}</a></li>
{% endfor %}
```

## 11. Cookie与Session

- **Cookie**是为了提高用户体验，保存在用户浏览器的数据，每次访问网站时候会把Cookie信息保护在request数据里面，使用``request.COOKIES``
- **Session**是由于HTTP是无状态协议，为了保存用户状态，在服务器端保存了会话信息``request.session``

### 加入会话功能

默认在settings.py中激活了此功能:

```python
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    #...
    )
    
INSTALLED_APPS = (
    'django.contrib.sessions',
    #...
    )
```


### 测试Cookie功能

Django提供了测试Cookie的函数:

- set_test_cookie()
- test_cookie_worked()
- delete_test_cookie()

在index视图:

```
request.session.set_test_cookie()
```

在register视图:

```
if request.session.test_cookie_worked():
    print ">>>> TEST COOKIE WORKED!"
    request.session.delete_test_cookie()
```

通过这个方法可以测试是否支持Cookie。


### 保存在客户端的Cookie数据

- 获取cookie值使用``request.COOKIES['cookie_name']``
- 新建cookie是使用``set_cookie()``,调用者是response对象，即render()返回的对象

### 保存在服务器的Session数据

- 获取session数据，使用``request.session.get()``
- 设置session数据，使用``request.session[]``

```
def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
        
    context_dict = {'categories': category_list, 'pages': page_list}
            
    visits = request.session.get('visits')
    if not visits:
        visits = 1
        
    reset_last_visit_time = False
                                
    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        
        if (datetime.now() - last_visit_time).seconds > 0:
        # ...reassign the value of the cookie to +1 of what it was before...
        visits = visits + 1
        # ...and update the last visit cookie, too.
        reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True
        
    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
        context_dict['visits'] = visits
        
        
    response = render(request,'rango/index.html', context_dict)
    
    return response
```

在使用会话之前，记得删除掉之前加的cookie数据，会发现使用会话之后，cookie里面只保存了``sessionid``一个值.

### 会话超时失效

会话超时失效有2种设置方法：

- 当用户关闭浏览器，则会话数据失效;默认是关闭的，可以在settings.py中添加``SESSION_EXPIRE_AT_BROWSER_CLOSE=True``来激活。
- 会话有一定时间，超过时间则失效;默认是激活的，可以在settings.py中添加``SESSION_COOKIE_AGE=1209600``来设置2周后失效.


### 清除会话数据

应该每天cronjob形式运行:

```
$ python manage.py clearsessions
```

### 注意事项


- 是否真的要把数据以Cookie形式存在客户端?
- 保存在客户端的Cookie的安全性要考虑。
- 如果客户端浏览器安全级别不支持Cookie，会导致程序无法工作。

## 12. 结合Django-Registration-Redux的用户授权管理


大部分应用都有注册、登陆等功能，Django自带的``django-registration-redux``包可以完成这些工作。

### 添加此功能软件包

```
$ pip install django-registration-redux
```

修改settings.py:

```
INSTALLED_APPS = (
     'registration', # add in the registration package
     )
     
REGISTRATION_OPEN = True        # If True, users can register
ACCOUNT_ACTIVATION_DAYS = 7     # One-week activation window; you may, of course, use a different value.
REGISTRATION_AUTO_LOGIN = True  # If True, the user will be automatically logged in.
LOGIN_REDIRECT_URL = '/rango/'  # The page you want users to arrive at after they successful log in
LOGIN_URL = '/accounts/login/'  # The page users are directed to if they are not logged in,
                                # and are trying to access pages requiring authentication
```

修改urls.py:

```
url(r'^accounts/', include('registration.backends.simple.urls')),
```

此软件包提供了多种注册后台，这是最简单的一步验证，还可以有二步验证等发邮件确认。


### URL映射与对应功能

``registration.backend.simple.urls``提供的功能:

- registration -> /accounts/register/
- registration complete -> /accounts/register/complete
- login -> /accounts/login/
- logout -> /accounts/logout/
- password change -> /password/change/
- password reset -> /password/reset/

需要修改模板，参考: https://github.com/macdhuibh/django-registration-templates

### 覆盖软件包的某些方法


```
from registration.backends.simple.views import RegistrationView

# Create a new class that redirects the user to the index page, if successful at logging
class MyRegistrationView(RegistrationView):
    def get_success_url(self,request, user):
        return '/rango/'
            
            
urlpatterns = patterns('',
    #Add in this url pattern to override the default pattern in accounts.
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    (r'^accounts/', include('registration.backends.simple.urls')),
    )
```

### 发送邮件

安装软件包``django-registration-email``或者``django-allauth``.


## 13. 使用Twitter Bootstrap改善前端效果

- http://getbootstrap.com/
- http://getbootstrap.com/getting-started/#examples

参考示例找到比较贴近需求的类型，基于其修改模板文件

### 修改base.html

```
<!DOCTYPE html>
<html lang="en">
  <head>
      <meta charset="utf-8">
      <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <meta name="description" content="">
      <meta name="author" content="">
      <link rel="icon" href="http://getbootstrap.com/favicon.ico">
      
      <title>Rango - {% block title %}How to Tango with Django!{% endblock %}</title>
      
      <link href="http://getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet">
      <link href="http://getbootstrap.com/examples/dashboard/dashboard.css" rel="stylesheet">
      
      <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
      <![endif]-->
   </head>
   
   <body>
   
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container-fluid">
          <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="/rango/">Rango</a>
          </div>
        <div class="navbar-collapse collapse">
        <ul class="nav navbar-nav navbar-right">
          <li><a href="{% url 'index' %}">Home</a></li>
          {% if user.is_authenticated %}
          <li><a href="{% url 'restricted' %}">Restricted Page</a></li>
          <li><a href="{% url 'auth_logout' %}?next=/rango/">Logout</a></li>
          <li><a href="{% url 'add_category' %}">Add a New Category</a></li>
          {% else %}
          <li><a href="{% url 'registration_register' %}">Register Here</a></li>
          <li><a href="{% url 'auth_login' %}">Login</a></li>
          {% endif %}
          <li><a href="{% url 'about' %}">About</a></li>
          
          </ul>
        </div>
      </div>
      </div>
      
      <div class="container-fluid">
        <div class="row">
          <div class="col-sm-3 col-md-2 sidebar">
          {% block side_block %}{% endblock %}
          
          </div>
          <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
            <div>
            {% block body_block %}{% endblock %}
            </div>
          </div>
        </div>
      </div>
      
      <!-- Bootstrap core JavaScript
      ================================================== -->
      <!-- Placed at the end of the document so the pages load faster -->
      <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
      <script src="http://getbootstrap.com/dist/js/bootstrap.min.js"></script>
      <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
      <script src="http://getbootstrap.com/assets/js/ie10-viewport-bug-workaround.js"></script>
   </body>
</html>
```

根据示例给的模板修改的。


### about.html

可以把base.html中加载的静态文件下载好，这样网站加载速度更快。

修改about.html:

```
{% extends 'base.html' %}

{% load staticfiles %}

{% block title %}About{% endblock %}

{% block body_block %}
    <div class="page-header">
      <h1>About</h1>
    </div>
    <div>
      <p></strong>.</p>
      <img  width="90" height="100" src="{% static "images/rango.jpg" %}" alt="Picture of Rango" /> <!-- New line -->
    </div>
{% endblock %}
```

### index.html

```
{% extends 'base.html' %}

{% load staticfiles %}

{% block title %}Index{% endblock %}

        {% block body_block %}
{% if user.is_authenticated %}
    <div class="page-header">

                <h1>Rango says... hello {{ user.username }}!</h1>
            {% else %}
                <h1>Rango says... hello world!</h1>
            {% endif %}
</div>

         <div class="row placeholders">
            <div class="col-xs-12 col-sm-6 placeholder">



               <div class="panel panel-primary">
                 <div class="panel-heading">
                   <h3 class="panel-title">Categories</h3>
                 </div>
               </div>

               {% if categories %}

                    <ul class="list-group">
                        {% for category in categories %}
                         <li class="list-group-item"><a href="{% url 'category'  category.slug %}">{{ category.name }}</a></li>
                        {% endfor %}
                    </ul>
                {% else %}
                    <strong>There are no categories present.</strong>
                {% endif %}

            </div>
            <div class="col-xs-12 col-sm-6 placeholder">
              <div class="panel panel-primary">
                <div class="panel-heading">
                  <h3 class="panel-title">Pages</h3>
                </div>
                    </div>

                {% if pages %}
                    <ul class="list-group">
                        {% for page in pages %}
                         <li class="list-group-item"><a href="{{page.url}}">{{ page.title }}</a></li>
                        {% endfor %}
                    </ul>
                {% else %}
                    <strong>There are no categories present.</strong>
                {% endif %}
            </div>

          </div>


       <p> visits: {{ visits }}</p>
        {% endblock %}
```

### login.html

- 参考: http://getbootstrap.com/examples/signin/

```
{% extends 'base.html' %}

{% block body_block %}

<link href="http://getbootstrap.com/examples/signin/signin.css" rel="stylesheet">

<form class="form-signin" role="form" method="post" action=".">
{% csrf_token %}

<h2 class="form-signin-heading">Please sign in</h2>
<input class="form-control" placeholder="Username" id="id_username" maxlength="254" name="username" type="text" required autofocus=""/>
<input type="password" class="form-control" placeholder="Password" id="id_password" name="password" type="password" required />

<button class="btn btn-lg btn-primary btn-block" type="submit" value="Submit" />Sign in</button>
</form>

{% endblock %}
```


### 使用Django-Bootstrap-Toolkit

- 参考: https://github.com/dyve/django-bootstrap-toolkit

```
$ pip install django-bootstrap-toolkit
```

settings.py:

```
INSTALLED_APPS=(
   #...
   bootstrap_toolkit,
   )
```

category.html:

```
{% extends 'base.html' %}
{% load bootstrap_toolkit %}

{% block title %}Add Category{% endblock %}

{% block body_block %}

<form id="category_form" method="post" action="{% url 'add_category' %}">
  <h2 class="form-signin-heading">Add a Category</a></h2>
  {% csrf_token %}
  
  {{ form|as_bootstrap }}
  
  <br/>
  
  <button class="btn btn-primary" type="submit" name="submit">Create Category</button>
  </form>
  
  {% endblock %}
```

更加简洁.

## 14. 模板标签

想在左边栏添加东西，但又不想对模板大动干戈，则可以创建自己的**模板标签**.


### 使用模板标签
   
创建 ``rango/templatetags``，里面包含空文件 ``__init__.py`` 与 ``rango_extras.py``:

```
from django import template
from rango.models import Category

register = template.Library()

@register.inclusion_tag('rango/cats.html')
def get_category_list():
    return {'cats': Category.objects.all()}
```

创建模板文件**rango/cates.html**:

```
{% if cats %}
    <ul class="nav nav-sidebar">
    {% for c in cats %}
      <li><a href="{% url 'category'  c.slug %}">{{ c.name }}</a></li>
    {% endfor %}
    
{% else %}
    <li> <strong >There are no category present.</strong></li>
    
    </ul>
{% endif %}
```

更新**base.html**:

```
{% load rango_extras %}

<div class="col-sm-3 col-md-2 sidebar">

    {% block side_block %}
    {% get_category_list %}
    {% endblock %}
    
</div>
```

需要重启Web Server以生效。

## 15. 增加搜索功能


- 添加``Bing Search API``

### 注册Bing API Key

- [Windows Azure](https://account.windowsazure.com/Home/Index)
- [Windows Azure Marketplace Bing Search API page](https://datamarket.azure.com/dataset/5BA839F1-12CE-4CCE-BF57-A49D98D29A44)

获取到 **Primary Account Key**


### 增加搜索功能

keys.py:

```
BING_API_KEY = '<Bing Search API Key>'
```

bing_search.py:

```
import json
import urllib, urllib2
from keys import BING_API_KEY

# Add your BING_API_KEY

#BING_API_KEY = '<insert_bing_api_key>'

def run_query(search_terms):
    # Specify the base
    root_url = 'https://api.datamarket.azure.com/Bing/Search/'
    source = 'Web'
    
    # Specify how many results we wish to be returned per page.
    # Offset specifies where in the results list to start from.
    # With results_per_page = 10 and offset = 11, this would start from page 2.
    results_per_page = 10
    offset = 0
    
    # Wrap quotes around our query terms as required by the Bing API.
    # The query we will then use is stored within variable query.
    query = "'{0}'".format(search_terms)
    query = urllib.quote(query)
    
    # Construct the latter part of our request's URL.
    # Sets the format of the response to JSON and sets other properties.
    search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
             root_url,
             source,
             results_per_page,
             offset,
             query)
             
    # Setup authentication with the Bing servers.
    # The username MUST be a blank string, and put in your API key!
    username = ''
    
    
    # Create a 'password manager' which handles authentication for us.
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, search_url, username, BING_API_KEY)
    
    # Create our results list which we'll populate.
    results = []
    
    try:
       # Prepare for connecting to Bing's servers.
       handler = urllib2.HTTPBasicAuthHandler(password_mgr)
       opener = urllib2.build_opener(handler)
       urllib2.install_opener(opener)
       
       # Connect to the server and read the response generated.
       response = urllib2.urlopen(search_url).read()
       
       # Convert the string response to a Python dictionary object.
       json_response = json.loads(response)
       
       # Loop through each page returned, populating out results list.
       for result in json_response['d']['results']:
           results.append({
             'title': result['Title'],
             'link': result['Url'],
             'summary': result['Description']})
             
    # Catch a URLError exception - something went wrong when connecting!
    except urllib2.URLError, e:
        print "Error when querying the Bing API: ", e
        
    # Return the list of results to the calling function.
    return results
```

search.html:

```
{% extends "base.html" %}

{% load staticfiles %}

{% block title %}Search{% endblock %}

{% block body_block %}

    <div class="page-header">
      <h1>Search with Rango</h1>
    </div>
    
    <div class="row">
    
      <div class="panel panel-primary">
      <br/>
      
         <form class="form-inline" id="user_form" method="post" action="{% url 'search' %}">
           {% csrf_token %}
           <!-- Display the search form elements here -->
           <input class="form-control" type="text" size="50" name="query" value="" id="query" />
           <input class="btn btn-primary" type="submit" name="submit" value="Search" />
           <br />
         </form>
         
         <div class="panel">
           {% if result_list %}
             <div class="panel-heading">
               <h3 class="panel-title">Results</h3>
               <!-- Display search results in an ordered list -->
               <div class="panel-body">
                 <div class="list-group">
                   {% for result in result_list %}
                     <div class="list-group-item">
                       <h4 class="list-group-item-heading"><a href="{{ result.link }}">{{ result.title }}</a></h4>
                       <p class="list-group-item-text">{{ result.summary }}</p>
                     </div>
                   {% endfor %}
                 </div>
               </div>
            {% endif %}
          </div>
         </div>
       </div>
{% endblock %}
```

views.py:

```
from rango.bing_search import run_query

def search(request):
    result_list = []
    
    if request.method == 'POST':
       query = request.POST['query'].strip()
       
       if query:
         # Run our Bing function to get the results list!
         result_list = run_query(query)
         
    return render(request, 'rango/search.html', {'result_list': result_list})
```

甚至可以定制一个自己用的搜索网站....


## 21. 部署到PythonAnyWhere


```
# TURN ON THE VIRTUAL ENVIRONMENT FOR YOUR APPLICATION
activate_this = '/home/<username>/.virtualenvs/rango/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import os
import sys

# ADD YOUR PROJECT TO THE PYTHONPATH FOR THE PYTHON INSTANCE
path = '/home/<username>/tango_with_django_17/'
if path not in sys.path:
    sys.path.append(path)
    
# IMPORTANTLY GO TO THE PROJECT DIR
os.chdir(path)

# TELL DJANGO WHERE YOUR SETTINGS MODULE IS LOCATED
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project_17.settings')

# IMPORT THE DJANGO SETUP - NEW TO 1.7
import django
django.setup()

# IMPORT THE DJANGO WSGI HANDLER TO TAKE CARE OF REQUESTS
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
```

### 去掉DEBUG模式

```
ALLOWED_HOSTS = ['<username>.pythonanywhere.com']
```


配置:

```
static/admin: /home/<username>/.virtualenvs/rango/lib/python2.7/site-packages/django/contrib/admin/static/admin
static/: /home/<username>/tango_with_django/tango_with_django_project/static
```

同时取消DEBUG模式：

```
DEBUG =False
ALLOWED_HOSTS = ['<username>.pythonanywhere.com']
```

注意这个URL后面不要有**/**.


## 结语

这个教程算学完了，继续学习.

