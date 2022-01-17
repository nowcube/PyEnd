# 利用Scrapy实现微博热搜榜的爬取,并在Web端实现数据展示
## 请注意，此项目只学习交流使用，请于24h后删除
## 若想使用请在hot_weibo文件夹内的settings.py文件内设置成 ROBOTSTXT_OBEY = ，并且 自行设置BOT_NAME = '' 
## 项目总体介绍

在互联网的时代，互联网拉近了人与人之间的距离，玩微博也成了当下互联网风潮中年轻人的生活的一部分，那么对于实时更新的每天微博热搜排行榜肯定不陌生，那么本项目于是在这种情况下诞生了，来更快的获取微博热搜信息进行二次开发，并在Web端展示！
<!-- 
由于大部分的桌面操作系统是Windows，本项目运行基于Windows环境（`其实是本人的Linux又坏了`），只需运行.bat文件即可，可自动安装所需要的依赖，并展示最新微博热搜的信息。

我自己问自己为什么不用Python自带的GUI展示，我想Web还是未来，所以固然用Web展示 -->

## 功能模块介绍
功能其实很简单，运行`run.bat`文件，即可自动打开浏览器，展示今日微博热搜信息。

<!-- ![image-20210622123013801](C:\Users\任逍遥\AppData\Roaming\Typora\typora-user-images\image-20210622123013801.png)

控制台信息。

![image-20210622123032397](C:\Users\任逍遥\AppData\Roaming\Typora\typora-user-images\image-20210622123032397.png)

浏览器展示。

![image-20210622123055078](C:\Users\任逍遥\AppData\Roaming\Typora\typora-user-images\image-20210622123055078.png)

点击链接自动跳转

![image-20210622114940273](C:\Users\任逍遥\AppData\Roaming\Typora\typora-user-images\image-20210622114940273.png) -->

## 代码实现过程

标题说明，本项目需要Scrapy框架在此我们来看一下Scrapy的原理图（其实这种简单的项目是不需要太过复杂的原理理解的，只需了解即可）

<!-- ![image-20210622112452054](C:\Users\任逍遥\AppData\Roaming\Typora\typora-user-images\image-20210622112452054.png) -->

首先呢，先在工作空间文件夹输入

``` bash
pip install scrapy
scrapy startproject hot_weibo
```

然后，在工作空间文件夹内会出现文件（创建时是不出现 `index.html , result.json , run.bat , run.py` , 请熟知）
<!-- 
![image-20210622123334828](C:\Users\任逍遥\AppData\Roaming\Typora\typora-user-images\image-20210622123334828.png) -->

然后在`VScode`里打开此文件夹，需要创建爬虫程序，如下图，爬虫程序名为 `hot.py`
<!-- 
![image-20210622123350456](C:\Users\任逍遥\AppData\Roaming\Typora\typora-user-images\image-20210622123350456.png) -->

即可在`hot.py`文件里写具体的爬虫了

<!-- ![image-20210622123423620](C:\Users\任逍遥\AppData\Roaming\Typora\typora-user-images\image-20210622123423620.png) -->

`hot.py`的代码如下

```python
# -*- coding:utf-8 -*-  
import scrapy
from scrapy.http.request import Request

class HotWeibo(scrapy.Spider):
    name="hot"
    start_urls = [
        'https://s.weibo.com/top/summary'
    ]

    def parse(self, response):
        for title in response.xpath('//div[@class="data"]//tbody//td[@class="td-02"]/a/text()').extract():
            if title:
                yield {
                    "title": title,
                    "url": 'https://s.weibo.com' + response.xpath('//div[@class="data"]//tbody//td[@class="td-02"]/a/@href').extract_first()
                }
```

过程中也使用了名为Xpath的查询语言，让我们来看一下，如何利用Xpath在浏览器里查询所需要的信息

<!-- ![image-20210622115156119](C:\Users\任逍遥\AppData\Roaming\Typora\typora-user-images\image-20210622115156119.png) -->

在Edeg浏览器控制台里按下`Ctrl + F`，并输入

```Xpath
//div[@class="data"]//tbody//td[@class="td-02"]
```

即可定位自己所需要的信息

然后在`hot.py`的上级目录创建`run.py`为了更方便的运行，代码如下

```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-
from scrapy import cmdline
# import uuid
import os

# id = str(uuid.uuid4()).replace('-', '')
# cmdline.execute("scrapy crawl hot -o result_{0}.json".format(id).split())

if os.path.exists('result.json'):
    os.remove('result.json')
    cmdline.execute("scrapy crawl hot -o result.json".split())
else:
    cmdline.execute("scrapy crawl hot -o result.json".split())
```

`Scrapy 自带的 cmdline` 很好的解决了每次运行都要输入指令的问题，并且通过`Python内置的OS模块`，很好的解决了程序第二次运行，文件无处安放的问题，希望读者也看到了，本可爱是本想通过`uuid`来实现每次生成文件都重名的问题，现在直接每次运行程序直接删除`旧有的json文件`。

为何需要用到`json`文件呢？`hot.py` 的`yield`完美的展示了如何格式化输出`json`文件

```python
yield {
		"title": title,
        "url": 'https://s.weibo.com' + response.xpath('//div[@class="data"]//tbody//td[@class="td-02"]/a/@href').extract_first()
		}
```

本次程序的`json`文件如下图所示

<!-- ![image-20210622122924104](C:\Users\任逍遥\AppData\Roaming\Typora\typora-user-images\image-20210622122924104.png) -->

好了程序到了这一步接下来就到`JavaScript HTML还有可爱的CSS时间了`

首先在控制台`CMD`里输入

```bash
python -m http.server 8888
```

然后在浏览器里输入

```
http://localhost:8888/
```

然后在此路径下编写HTML，在这里我先展示HTML部分

```HTML
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.bootcdn.net/ajax/libs/font-awesome/5.15.3/css/all.css" rel="stylesheet">
    <title>Weibo Top 10</title>
    <style>
    </style>
</head>
<body>
    <div class="header">
        <i class="fab fa-weibo icon"></i>
        <p class="icon-title">热搜榜</p>
    </div>
    <div class="show-box">
        <div class="show">
            <a id="1" class="show-title"></a>
            <a id="2" class="show-title"></a>
            <a id="3" class="show-title"></a>
            <a id="4" class="show-title"></a>
            <a id="5" class="show-title"></a>
            <a id="6" class="show-title"></a>
            <a id="7" class="show-title"></a>
            <a id="8" class="show-title"></a>
            <a id="9" class="show-title"></a>
            <a id="10" class="show-title"></a>    
        </div>
    </div>
    <script>
    </script>
</body>
</html>
```

然后在此展示CSS部分

```css
        *{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        html{
            background-color: rgb(238,212,169);
        }
        .header{
            background-color: rgb(114,96,84);
            height: 80px;
            width: 100vw;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0 30px;
        }
        .icon{
            color: rgb(251,251,251);
            font-size: 30px;
        }
        .icon-title{
            margin: 0 10px;
            font-weight: 500;
            font-size: 20px;
            color: rgb(251,251,251);
        }
        .show-box{
            width: 100vw;
            height: calc(100vh - 80px);
            display: flex;
         
            align-items: center;
            flex-direction: column;
        }
        .show-title{
            background-color: rgb(251,247,237);
            border-left: 50px solid rgb(249,242,236);
            align-items: center;
            padding: 15px;
            display: flex;
            width: 50vw;
            height: 80px;
            font-size: 20px;
            margin-top: 20px;
            text-decoration: none;
        }
```

<!-- 其实本次CSS写的并不是很好，不过设计一个好看的要耗费太大的精力，所以在此致敬一下老罗，模仿的锤子便签的样式，本身每一条左边也有回形针的，不过找不到好看的回形针的位图(其实是懒)

![image-20210622132705178](C:\Users\任逍遥\AppData\Roaming\Typora\typora-user-images\image-20210622132705178.png) -->

到了重头戏的`JavaScript`环节了，这个是最头大的，因为我不会`JS`，勉强写了一下

```javascript
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                myData = JSON.parse(this.responseText);
                document.getElementById("1").innerHTML=myData[0].title;
                document.getElementById("1").href=myData[0].url;

                document.getElementById("2").innerHTML=myData[1].title;
                document.getElementById("2").href=myData[0].url;

                document.getElementById("3").innerHTML=myData[2].title;
                document.getElementById("3").href=myData[0].url;

                document.getElementById("4").innerHTML=myData[3].title;
                document.getElementById("4").href=myData[0].url;

                document.getElementById("5").innerHTML=myData[4].title;
                document.getElementById("5").href=myData[0].url;

                document.getElementById("6").innerHTML=myData[5].title;
                document.getElementById("6").href=myData[0].url;

                document.getElementById("7").innerHTML=myData[6].title;
                document.getElementById("7").href=myData[0].url;

                document.getElementById("8").innerHTML=myData[7].title;
                document.getElementById("8").href=myData[0].url;

                document.getElementById("9").innerHTML=myData[8].title;
                document.getElementById("9").href=myData[0].url;

                document.getElementById("10").innerHTML=myData[9].title;
                document.getElementById("10").href=myData[0].url;

            }
        };
        xmlhttp.open("GET", "result.json", true);
        xmlhttp.send();
```

其实此`JS`难的地方在于`XMLHttpRequest`这东西涉及到了很多服务器通信还有传输数据在这就不多展示了。程序到此就截至了，花了些时间，也终于知道`json`文件的一个简单的利用

为了让别人运行不装依赖，所以写了个`bat`，没写`bash`希望没人把程序跑在Linux上面

```bash
pip install scrapy
python run.py
start http://localhost:8888/
python -m http.server 8888
```

<!-- 下图是程序目录

![image-20210622135136616](C:\Users\任逍遥\AppData\Roaming\Typora\typora-user-images\image-20210622135136616.png)





## 过程经验总结

这个项目不难，也算是学了Python并进行期末总结了吧，说起来好玩本程序用了5种语言，两种编程语言`Python JavaScript`，一种查询语言`Xpath` ，标记语言`HTML`，还有一个样式表`CSS`，我觉得本程序的优点就是在能生成`JSON`文件，进行二次开发，缺点就是用了框架，因为本人觉得依赖越少程序可移植性越强，代码越简洁优雅。 -->

