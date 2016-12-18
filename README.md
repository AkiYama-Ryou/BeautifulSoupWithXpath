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
