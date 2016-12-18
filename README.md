# BeautifulSoupWithXpath
Use this Python function you can find tags in your BeautifulSoup object by Xpath.

But the Xpath must be smiple like:

//*[@id="xxx"]/div[1]/a[1]  
Maybe your xpath havn't tagname.it will be ok

//div[@class="xxx"]/div[1]/a   
Have tagname?no problem.  
Point to tags，not only one？no problem too.

/html/body/p  
Absolute path will be OK

So I mean that, I want to use this function to find tags in my BeautifulSoup object by Xpath.And the Xpath usully come from my Chrome's "cpoyXpath".


我们写python爬虫的时候，往往希望使用beautifulsoup模块，而不希望使用lxml模块，但是beautifulsoup不支持xpath定位元素。
这个函数帮助你在beautifulsoup中使用xpath定位元素。
但是并不能完美的支持任何形势的xpath，而是只支持比较常见的xpath（就像上面的例子那样）。
你可以从谷歌浏览器的开发者工具提取xpath，然后拿来用，都是没问题的。

