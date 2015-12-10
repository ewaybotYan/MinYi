acoada on 2015-12-09:


[cnbeta](http://www.cnbeta.com)页面是动态刷新的。爬取其主页需要获取真实的`URL`，下拉页面至底部时查看`firebug`可以发现一个`XHR`，具体是：

    Request URL:http://www.cnbeta.com/more?jsoncallback=jQuery18005619053719565272_1449674708584&type=all&page=3&csrf_token=767438b0585779df6c1ef0c580d18a3cde81fb52&_=1449680413534

关键是`jsoncallback`，`csrf_token`和`&_`参数，其中应该有时间戳。

查看`JS`源码，发现一个涉及上面的`jsoncallback`参数的`getJSON`方法：1. [paging.js](http://www.cnbeta.com/assets/js/pages/paging.js?v=2014) 2. [index.js](http://www.cnbeta.com/assets/js/pages/index.js?v=2014) ，继而发现一个名为`real_url`的变量，其有一个可能值是`GV.URL.INDEX.ALLNEWS`，继续追踪到`url`变量，发现如下代码：

    if(url){
        $.extend(param, settings.param);
        if(url.indexOf("?") == -1 ){
            url += '?jsoncallback=?';
        }else{
            url += '&jsoncallback=?';
        }
        for(var el in param){
            url += '&'+el+'='+param[el];
        }
    }else{
        return;
    }

其中的`el`来自：

    for(var el in data){
        if(el > 5) break;
        if(data[el]){
            items += CB.tmpl(op.template, data[el]);
        }
    }

而`data`：

    $.ajax({
        async:true,
        timeout:2000,
        type:"get",
        url:op.url,
        data:op.param,
        dataType:"jsonp",

依旧没有什么头绪，请赐教！


# 评论


LeslieZhu on 2015-12-10T02:52:25Z:

 http://blog.chedushi.com/archives/8645 你看看这个对你有没有帮助 

LeslieZhu on 2015-12-10T02:54:31Z:

 还有这个 http://www.pythonclub.org/python-network-application/observer-spider  

acoada on 2015-12-10T02:59:32Z:

 这两篇都看过的，都没有讲怎么获取 AJAX 参数。 

LeslieZhu on 2015-12-10T04:26:06Z:

 
我照着你的方法，用Firebug找到这个json请求，拷贝为cURL的形式，如下:

```
curl 'http://www.cnbeta.com/more?jsoncallback=jQuery18007695096260749249_1449720320965&type=all&page=2&csrf_token=a6e20533b07adb18018e89bc6c90eb6df3c25f33&_=1449720329349' -H 'Accept: text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-cn,en-us;q=0.7,en;q=0.3' -H 'Connection: keep-alive' -H 'Cookie: Hm_lvt_4216c57ef1855492a9281acd553f8a6e=1449671129,1449719052; _ga=GA1.2.738214413.1449671129; tma=208385984.3330358.1449671129113.1449671129113.1449671129113.1; tmd=7.208385984.3330358.1449671129113.; bfd_g=882eecf4bbc243d000005c9e0009d461566839da; Hm_lpvt_4216c57ef1855492a9281acd553f8a6e=1449720326; bfd_s=208385984.5513774.1449719052707; tmc=3.208385984.76674402.1449719052709.1449719187960.1449720327022; csrf_token=ece1347ef5d958a6bd8f402f9c056b1304925e5d; _gat=1' -H 'DNT: 1' -H 'Host: www.cnbeta.com' -H 'Referer: http://www.cnbeta.com/' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:30.0) Gecko/20100101 Firefox/30.0' -H 'X-Requested-With: XMLHttpRequest' |gzip -d > cnbeta.txt
```

这种方式拿到这个JSON文件是不会失效的（或许），因为我反复运行，总是能够获取数据的；但看后面。


将cnbeta.txt前后一个括号去掉，就是你在上面所说的JSON格式文件了，我挑取其中一篇文章内容:

```python
>>> print b["hometext"],b["title"],b["url_show"]
<p>谷歌今年9月发布了Google
Play音乐音乐播放家庭计划，如今这项计划终于落实。和苹果音乐一样，用户只需每月支付14.99美元，就可以与五位家庭成员共享谷歌流媒体音乐库。其
中包括3500万首歌曲的无广告播放服务，同时每位家庭成员都可以在自己的播放器上随意播放音乐。</p> Google Play音乐家庭计划本周上线 /articles/455725.htm
```

可见，即使拿到JSON数据文件，里面的数据无非是该网站首页40篇文章的一个列表，每篇文章仅仅包含了标题、简介、文章链接，对于你的爬虫爬取所有内容感觉帮助不是很大啊。

不知道这些信息是否对你有所帮助？ 

