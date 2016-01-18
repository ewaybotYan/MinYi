[LeslieZhu](https://github.com/LeslieZhu) on 2016-01-18:


# 基于Gitolite自建Git服务

- https://github.com/sitaramc/gitolite

添加git用户，用于提供git服务:

```
$ sudo useradd git -m -s /bin/bash
$ sudo passwd git
$ su git
```

获取gitolite:

```
$ git clone git://github.com/sitaramc/gitolite
$ mkdir ~/bin/
$ ./gitolite/install -ln
```

将自己本地机器的公钥文件复制过来, 然后设置:

```
$ ./bin/gitolite setup -pk /path/to/lesliezhu.pub
```

则会建立一个叫`gitolite-admin`的git repo,后续的管理都是基于此仓库进行的.


在本地机器获取git服务器上的repo代码:

```
$ git clone git@192.168.1.109:gitolite-admin

$ tree gitolite-admin
gitolite-admin
├── conf
│   └── gitolite.conf
└── keydir
    └── lesliezhu.pub
```

其中`keydir`目录保存各个客户端机器的公钥文件，从而进行访问权控制；而文件`conf/gitolite.conf`就是配置整个git服务器repo情况:

```
$ cat conf/gitolite.conf

@test = user1 user2 user3
@dev  = user4  user4 user6
@admin = lesliezhu

repo gitolite-admin
    RW+    = lesliezhu

repo testing
    R      = @test
    RW+    = user6
    RW+    = lesliezhu
```

新添加一个repo，需要在`gitolite.conf`中添加:

```
repo new-repo
    RW+     = @all
```

然后在本地进行一次提交:

```
$ git clone git@192.168.1.109:new-repo
$ cd new-repo
$ touch .gitignore
$ git add .gitignore
$ git commit -m "init"
$ git push origin master
```

则此新的repo建立好了，更多配置参考[gitolite on github](https://github.com/sitaramc/gitolite)

新添加用户以访问git服务器，只需要将其SSH公钥以文件保存于`keydir`，在`gitolite.conf`中对相应repo添加权限，提交即可。

## Gitolite工作原理

对于每一个repo，都有钩子文件`hooks/update`:

```perl
#!/usr/bin/perl

use strict;
use warnings;

use lib $ENV{GL_LIBDIR};
use Gitolite::Hooks::Update;

# gitolite update hook
# ----------------------------------------------------------------------

update();               # is not expected to return
exit 1;                 # so if it does, something is wrong
```

只要repo有更新，则通过这个钩子自动进行一些更新操作，在`gitolite-admin.git`还有另一个钩子`hooks/post-update`

```
$ tree ~/.gitolite

.gitolite
├── conf
│   ├── gitolite.conf
│   ├── gitolite.conf-compiled.pm
│   └── rule_info
├── hooks
│   ├── common
│   │   └── update
│   └── gitolite-admin
│       └── post-update
├── keydir
│   └── lesliezhu.pub
└── logs
    └── gitolite-2016-01.log
```


# 资源

- [GitLab](https://about.gitlab.com/downloads/#debian8)
- [Gitolite](http://git-scm.com/book/zh/v1/%E6%9C%8D%E5%8A%A1%E5%99%A8%E4%B8%8A%E7%9A%84-Git-Gitolite)

