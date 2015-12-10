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

