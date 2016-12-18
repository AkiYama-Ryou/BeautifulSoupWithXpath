#coding=utf-8
from bs4 import BeautifulSoup
import re
from timeit import Timer
"""
首先用谷歌浏览器的copyXpath功能来生成Xpath，
然后用下面的findBeautifulTagsByXpath()提取html中的标签
"""

def startingPointAnalysis(stringBeforeAnalysis):
    """
    对起点进行解析
    :param stringBeforeAnalysis: 相对xpath的起点字符串
    :return: 元组，第一个成员是起点的标签名,第二个成员是起点的属性名，第三个是起点的属性值
    """
    tagName = stringBeforeAnalysis[:re.search("\[",stringBeforeAnalysis).span()[0]]
    attrName = stringBeforeAnalysis[re.search("\@",stringBeforeAnalysis).span()[0]+1:re.search("=",stringBeforeAnalysis).span()[0]]
    attrValue = re.search("('|\").+('|\")",stringBeforeAnalysis).group().lstrip("'").lstrip('"').rstrip("'").rstrip('"')
    return (tagName, attrName, attrValue)
#OK
def XpathAnalysis(Xpath):
    """
    解析xpath，从而得知从何处起，向何处去
    :param Xpath: 需要解析的Xpath
    :return:startingPoint:相对路径Xpath的起点
            genealogy:Xpath路径列表（家谱）
    """
    startingPoint,relative = None, False
    genealogy = []

    for i, letter in enumerate(Xpath):
        if letter == '/' :
            if i == 0:
                pass
            elif i == 1:
                relative = True
            else:
                if relative:
                    startingPoint = startingPointAnalysis(number)
                    relative = 0
                else:
                    genealogy.append(number)
            number = ''
        else:
            number += letter
            if i == len(Xpath)-1:
                genealogy.append(number)
    return startingPoint, genealogy
#OK
def findStartPoint(soups, startingPoint):
    """
    用startingPoint找出html文档中，xpath搜索的起点(们)
    :param soup: 完整的html文档对应的Beautifulsoup对象
    :param startingPoint: 表示起点的元组，第一个成员是起点的标签名,第二个成员是起点的属性名，第三个是起点的属性值
    :return: 新的soup(们)
    """
    tagName = startingPoint[0]
    attrName = startingPoint[1]
    attrValue = startingPoint[2]
    # 寻找符合条件的标签(们)
    if tagName == "*":
        if attrName == "class":
            soup = soups[0].find_all(class_ = attrValue)
        if attrName == "id":
            soup = soups[0].find_all(id = attrValue)
    else:
        if attrName == "class":
            soup = soups[0].find_all(tagName, class_ = attrValue)
        if attrName == "id":
            soup = soups[0].find_all(tagName, id = attrValue)
    return soup
#OK
def Find(soup, genealogy):
    for tag in genealogy:
        # 从soup中一级一级地取出目标标签
        newList = []
        index = 0
        if re.search("\[\d+]",tag) != None:
            lastLetterPath = re.search("\[\d+]",tag).span()[0]
            index = int(re.search("\[\d+]",tag).group().lstrip("[").rstrip("]"))
            tag = tag[:int(lastLetterPath)]

        for chlidhtml in soup:
            if index == 0:
                for child in chlidhtml.contents:
                    if child == '\n':continue
                    elif child.name == tag:
                        newList.append(child)
            else:
                i = 0
                for child in chlidhtml.contents:
                    if child == '\n':continue
                    elif child.name == tag:
                        i += 1
                        if i == index:
                            newList.append(child)
                            break

        soup = newList
    return soup



# main function:
def findBeautifulTagsByXpath(html, Xpath, htmlIsBS = False):
    """
     # 找出一个html文本中，特定xpath指向的元素们
    :param html:html文本
    :param Xpath:xpath，可以指向文本内的某些元素
    :return:一个列表，包含xpath所指向的标签们，每个成员都是一个Beautifulsoup的tag对象。
    """
    soup = []
    if htmlIsBS:
        soup.append(html)
    else:
        soup.append(BeautifulSoup(html, "html.parser"))  # "html.parser"
    # startingPoint指起点，genealogy译为“家谱”
    startingPoint, genealogy = XpathAnalysis(Xpath)
    if startingPoint != None:
        soup = findStartPoint(soup, startingPoint)
    return Find(soup, genealogy)


if __name__ == '__main__':

    # test ###########################################################
    soup =  """
                <html>
                    <body class='h'>
                        <p>你好<span>1</span><span>2</span></p>
                        <p>holle！</p>
                    </body>
                </html>
            """
    xpath = '//*[@class="h"]/p'
    print(findBeautifulTagsByXpath(soup, xpath))

    soup = """

<!DOCTYPE html>
<html lang="zh-CN" dropEffect="none" class="no-js topic-pages">
<head>
<meta charset="utf-8" />

<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
<meta name="renderer" content="webkit" />
<meta http-equiv="X-ZA-Response-Id" content="00137d6d7beaa5f9">
<meta http-equiv="X-ZA-Experiment" content="default:None">

<title>话题组织 - 「根话题」 - 知乎</title>

<meta name="apple-itunes-app" content="app-id=432274380" />


<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"/>
<meta http-equiv="mobile-agent" content="format=html5;url=https://www.zhihu.com/topic/19776749/organize">
<meta id="znonce" name="znonce" content="19238ed76bc54c329f64218028b82e91">



<link rel="apple-touch-icon" href="https://static.zhihu.com/static/revved/img/ios/touch-icon-152.87c020b9.png" sizes="152x152">
<link rel="apple-touch-icon" href="https://static.zhihu.com/static/revved/img/ios/touch-icon-120.496c913b.png" sizes="120x120">
<link rel="apple-touch-icon" href="https://static.zhihu.com/static/revved/img/ios/touch-icon-76.dcf79352.png" sizes="76x76">
<link rel="apple-touch-icon" href="https://static.zhihu.com/static/revved/img/ios/touch-icon-60.9911cffb.png" sizes="60x60">


<link rel="shortcut icon" href="https://static.zhihu.com/static/favicon.ico" type="image/x-icon">

<link rel="search" type="application/opensearchdescription+xml" href="https://static.zhihu.com/static/search.xml" title="知乎" />
<link rel="stylesheet" href="https://static.zhihu.com/static/revved/-/css/z.ff107350.css">





<!--[if lt IE 9]>
<script src="https://static.zhihu.com/static/components/respond/dest/respond.min.js"></script>
<link href="https://static.zhihu.com/static/components/respond/cross-domain/respond-proxy.html" id="respond-proxy" rel="respond-proxy" />
<link href="/static/components/respond/cross-domain/respond.proxy.gif" id="respond-redirect" rel="respond-redirect" />
<script src="/static/components/respond/cross-domain/respond.proxy.js"></script>
<![endif]-->
<script src="https://static.zhihu.com/static/revved/-/js/instant.14757a4a.js"></script>

<style>
.zm-topic-manage-item ul {
margin-left: 1.6em;
list-style:circle;
}
</style>

</head>

<body class="zhi ">




<div role="navigation" class="zu-top" data-za-module="TopNavBar">
<div class="zg-wrap modal-shifting clearfix" id="zh-top-inner">
<a href="/" class="zu-top-link-logo" id="zh-top-link-logo" data-za-c="view_home" data-za-a="visit_home" data-za-l="top_navigation_zhihu_logo">知乎</a>

<div class="top-nav-profile">
<a href="/people/da-you-zhen" class="zu-top-nav-userinfo ">
<span class="name">若晗</span>
<img class="Avatar" src="https://pic1.zhimg.com/3ff8329cf6c7eb223e29ee2e40cf16cc_s.jpg" srcset="https://pic1.zhimg.com/3ff8329cf6c7eb223e29ee2e40cf16cc_xs.jpg 2x" alt="若晗" />
<span id="zh-top-nav-new-pm" class="zg-noti-number zu-top-nav-pm-count"
style="visibility:hidden" data-count="0">

</span>
</a>
<ul class="top-nav-dropdown" id="top-nav-profile-dropdown">
<li>
<a href="/people/da-you-zhen">
<i class="zg-icon zg-icon-dd-home"></i>我的主页
</a>
</li>

<li>
<a href="/inbox">
<i class="zg-icon zg-icon-dd-pm"></i>私信
<span id="zh-top-nav-pm-count" class="zu-top-nav-pm-count zg-noti-number"
style="visibility:hidden" data-count="0">

</span>
</a>
</li>
<li>
<a href="/settings">
<i class="zg-icon zg-icon-dd-settings"></i>设置
</a>
</li>
<li>
<a href="/logout">
<i class="zg-icon zg-icon-dd-logout"></i>退出
</a>
</li>
</ul>

</div>



<button class="zu-top-add-question" id="zu-top-add-question">提问</button>


<div role="search" id="zh-top-search" class="zu-top-search">
<form method="GET" action="/search" id="zh-top-search-form" class="zu-top-search-form">



<input type="hidden" name="type" value="content">
<label for="q" class="hide-text">知乎搜索</label><input type="text" class="zu-top-search-input" id="q" name="q" autocomplete="off" value="" maxlength="100" placeholder="搜索你感兴趣的内容...">
<button type="submit" class="zu-top-search-button"><span class="hide-text">搜索</span><span class="sprite-global-icon-magnifier-dark"></span></button>
</form>
</div>



<div id="zg-top-nav" class="zu-top-nav">
<ul class="zu-top-nav-ul zg-clear">

<li class="zu-top-nav-li " id="zh-top-nav-home">
<a class="zu-top-nav-link" href="/" id="zh-top-link-home" data-za-c="view_home" data-za-a="visit_home" data-za-l="top_navigation_home">首页</a>
</li>



<li class="top-nav-topic-selector zu-top-nav-li current" id="zh-top-nav-topic">
<a class="zu-top-nav-link" href="/topic" id="top-nav-dd-topic">话题</a>
</li>

<li class="zu-top-nav-li " id="zh-top-nav-explore">
<a class="zu-top-nav-link" href="/explore">发现</a>
</li>

<li class="top-nav-noti zu-top-nav-li ">
<a class="zu-top-nav-link" href="javascript:;" id="zh-top-nav-count-wrap" role="button"><span class="mobi-arrow"></span>消息</a>
</li>



</ul>
<div class="zu-top-nav-live zu-noti7-popup zg-r5px no-hovercard" id="zh-top-nav-live-new" role="popup" tabindex="0">
<div class="zu-top-nav-live-inner zg-r5px">
<div class="zu-top-live-icon">&nbsp;</div>
<div class="zu-home-noti-inner" id="zh-top-nav-live-new-inner">
<div class="zm-noti7-popup-tab-container clearfix" tabindex="0">
<button class="zm-noti7-popup-tab-item message">
<span class="icon">消息</span>
</button>
<button class="zm-noti7-popup-tab-item user">
<span class="icon">用户</span>
</button>
<button class="zm-noti7-popup-tab-item thanks">
<span class="icon">赞同和感谢</span>
</button>
</div>
</div>
<div class="zm-noti7-frame-border top"></div>
<div class="zm-noti7-frame">
<div class="zm-noti7-content message">
<div class="zm-noti7-content-inner">
<div class="zm-noti7-content-body">
<div class="zm-noti7-popup-loading">
<span class="noti-spinner-loading"></span>
</div>
</div>
</div>
</div>
<div class="zm-noti7-content user" style="display:none;">
<div class="zm-noti7-content-inner">
<div class="zm-noti7-content-body">
<div class="zm-noti7-popup-loading">
<span class="noti-spinner-loading"></span>
</div>
</div>
</div>
</div>
<div class="zm-noti7-content thanks" style="display:none;">
<div class="zm-noti7-content-inner">
<div class="zm-noti7-content-body">
<div class="zm-noti7-popup-loading">
<span class="noti-spinner-loading"></span>
</div>
</div>
</div>
</div>
</div>
<div class="zm-noti7-frame-border bottom"></div>
<div class="zm-noti7-popup-footer">
<a href="/notifications" class="zm-noti7-popup-footer-all zg-right">查看全部 &raquo;</a>
<a href="/settings/notification" class="zm-noti7-popup-footer-set" title="通知设置" ><i class="zg-icon zg-icon-settings"></i></a>
</div>
</div>
</div>

</div>

</div>
</div>


<div class="zu-global-notify" id="zh-global-message" style="display:none">
<div class="zg-wrap">
<div class="zu-global-nitify-inner">
<a class="zu-global-notify-close" href="javascript:;" title="关闭" name="close">x</a>
<span class="zu-global-notify-icon"></span>
<span class="zu-global-notify-msg"></span>
</div>
</div>
</div>




<div class="zg-wrap zu-main clearfix "  role="main">
<div class="zu-main-content">
<div class="zu-main-content-inner">


<div id="zh-topic-organize-page-wrap">
<div class="topic-avatar" itemprop="image" itemscope itemtype="http://schema.org/ImageObject">
<div>
<a class="zm-entry-head-avatar-link" href="/topic/19776749" id="zh-avartar-edit-form">
<img alt="「根话题」" src="https://pic4.zhimg.com/7d3842057_m.jpg" class="zm-avatar-editor-preview"></a>
<meta itemprop="image" content="https://pic4.zhimg.com/7d3842057_l.jpg" />
</div>

<span class="zm-entry-head-avatar-edit-button">修改</span>

</div>
<div class="topic-info">
<div class="topic-name" id="zh-topic-title">
<h1 class="zm-editable-content" data-disabled="1">「根话题」</h1>
<div class="zm-editable-editor-wrap" style="display:none">
<input type="text" class="zm-editable-editor-input zg-form-text-input" style="width:150px" />
<span class="zm-command">
<a href="javascript:;" name="save" class="zg-btn-blue" style="margin:0 15px;">完成</a>
<a href="javascript:;" name="cancel" class="zm-command-cancel">取消</a>
</span>
</div>
</div>
<a href="#" class="meta-item share-button zg-right" name="share"><i class="z-icon-share"></i>分享</a>


<div class="zm-topic-topbar">
<div class="zm-topic-topbar-nav clearfix">


<a href="/topic/19776749">「根话题」</a>&nbsp;&nbsp;<span class="zg-gray-normal">»</span>&nbsp;&nbsp;<span>话题组织</span>&nbsp;&nbsp;<span class="zg-gray-normal">»</span>&nbsp;&nbsp;<a href="/topic/19776749/organize/entire">完整话题结构</a>

</div>

</div>
</div>
<div class="zm-topic-manage-item">
<h3 class="zm-topic-manage-item-title">父级话题</h3>
<div class="zm-topic-manage-item-inner">
<div class="zg-section zg-gray-normal">完全包括本话题的更大的话题。例如：「水果」可以是「苹果」的父话题。</div>
<div id="zh-topic-organize-parent-editor" class="zm-tag-editor zg-section" data-disabled="true">
<div class="zm-tag-editor-labels zg-clear">

</div>

<div class="zg-gray"><i class="icon icon-lock"></i>该话题的父话题已锁定</div>

</div>
</div>
</div>
<div class="zm-topic-manage-item">
<h3 class="zm-topic-manage-item-title">子级话题</h3>
<div class="zm-topic-manage-item-inner">
<div class="zg-section zg-gray-normal">完全隶属于本话题的细分话题。例如：「苹果」可以是「水果」的子话题。</div>
<div id="zh-topic-organize-child-editor" class="zm-tag-editor zg-section" data-disabled="true">
<div class="zm-tag-editor-labels zg-clear">


<a class="zm-item-tag" href="/topic/19776751/organize"
data-uneditable="true"
data-token="19776751"
data-topicid="76001">
「未归类」话题
</a>



<a class="zm-item-tag" href="/topic/19618774/organize"

data-token="19618774"
data-topicid="22908">
学科
</a>



<a class="zm-item-tag" href="/topic/19778287/organize"

data-token="19778287"
data-topicid="76518">
实体
</a>



<a class="zm-item-tag" href="/topic/19778298/organize"

data-token="19778298"
data-topicid="76521">
「形而上」话题
</a>



<a class="zm-item-tag" href="/topic/19560891/organize"

data-token="19560891"
data-topicid="3564">
产业
</a>



<a class="zm-item-tag" href="/topic/19778317/organize"

data-token="19778317"
data-topicid="76527">
生活、艺术、文化与活动
</a>


</div>


<div class="zg-gray"><i class="icon icon-lock"></i>该话题的子话题已锁定</div>

</div>
</div>
</div>
<div class="zm-topic-manage-item" id="zh-topic-alias-container">
<h3 class="zm-topic-manage-item-title">话题别名</h3>
<div class="zm-topic-manage-item-inner">
<div class="zg-section">
<div class="zg-gray-normal zg-section">
话题名称的其他表述方式。添加别名可以方便其他人找到本话题。
</div>

<a href="/question/23261456" class="zg-link-gray-normal"><i class="icon-info" style="vertical-align: -3px; margin-right: 6px"></i>如何参与知乎话题的公共编辑？</a>

</div>

<div class="zg-section">

<span>有这些别名：</span>
<ul id="zh-topic-alias-list">


<li data-token="76000_All-topics">All topics



<li data-token="76000_Root-topic">Root topic



<li data-token="76000_大杂烩">大杂烩



<li data-token="76000_所有话题">所有话题


</ul>
</div>
</div>
</div>
<div class="zm-topic-manage-item">
<h3 class="zm-topic-manage-item-title">话题合并</h3>
<div class="zm-topic-manage-item-inner">
<div class="zg-section">
<div class="zg-gray-normal zg-section">
合并本话题至意义相近的其他话题。本话题会被删除，相关内容会自动迁移至目标话题中，同时添加话题别名。请将不常用的话题合并至常用话题。
</div>

<div class="zg-gray"><i class="icon icon-lock"></i>该话题已锁定</div>

</div>

<div style="display: none;" class="zg-section">

</div>
</div>
</div>

</div>

</div>
</div>


<div class="zu-main-sidebar" data-za-module="RightSideBar">

<div class="zm-side-section">
<div class="zm-side-section-inner">

<div class="zm-side-section">
<div class="zm-side-section-inner">
<div class="topic-header-side zm-entry-head-wrap">

<div class="clearfix"><div id="zh-topic-side-head">

<a href="javascript:;" id="tf-76000" name="focus" class="zg-btn-green zu-entry-focus-button zg-mr10">关注话题</a>

<div class="zm-topic-side-followers-info">

<a href="/topic/19776749/followers"><strong>79720</strong></a> 人关注了该话题

</div>
</div></div>
<div style="margin-top: 15px;">

<a class="zg-link-litblue-normal js-may-disable" href="/topic/19776749/organize">组织</a>
<span class="zg-bull">•</span>
<a class="zg-link-litblue-normal js-may-disable" href="/topic/19776749/manage">管理</a>
<span class="zg-bull">•</span>

<a class="zg-link-litblue-normal" href="/topic/19776749/log">日志</a>
</div>

</div>
</div>
</div>

</div>
</div>
<div class="zm-side-section">
<div class="zm-side-section-inner">
<h3 class="zm-topic-side-organize-title">描述
</h3>
<div id="zh-topic-desc" data-resourceid="76000" data-action="/topic-introduction">
<div class="zm-editable-content" data-editable-maxlength="130" >知乎的全部话题通过父子关系构成一个<a href="http://www.zhihu.com/question/21544822" class="internal">有根无循环的有向图</a>。<br>「根话题」即为所有话题的最上层的父话题。<br><a href="http://www.zhihu.com/topic/19776749/top-answers" class="internal">话题精华</a>即为知乎的 Top1000 高票回答。<br>请不要在问题上直接绑定「根话题」。<br>这样会使问题话题过于宽泛。</div>
</div>
</div>
</div>

<div class="zm-side-section" id="zh-topic-side-children-list">
<div class="zm-side-section-inner child-topic">
<h3 class="zm-topic-side-organize-title">子话题
</h3>
<div class="clearfix">

<a class="zm-item-tag"
href="/topic/19778317"
data-hovercard="t$b$19778317" data-token="19778317" data-topicid="76527" data-za-element-name="Title">
生活、艺术、文化与活动
</a>

<a class="zm-item-tag"
href="/topic/19776751"
data-hovercard="t$b$19776751" data-token="19776751" data-topicid="76001" data-za-element-name="Title">
「未归类」话题
</a>

<a class="zm-item-tag"
href="/topic/19778298"
data-hovercard="t$b$19778298" data-token="19778298" data-topicid="76521" data-za-element-name="Title">
「形而上」话题
</a>

<a class="zm-item-tag"
href="/topic/19618774"
data-hovercard="t$b$19618774" data-token="19618774" data-topicid="22908" data-za-element-name="Title">
学科
</a>

<a class="zm-item-tag"
href="/topic/19778287"
data-hovercard="t$b$19778287" data-token="19778287" data-topicid="76518" data-za-element-name="Title">
实体
</a>

<a class="zm-item-tag"
href="/topic/19560891"
data-hovercard="t$b$19560891" data-token="19560891" data-topicid="3564" data-za-element-name="Title">
产业
</a>

</div>

<a class="zg-link-litblue zm-topic-side-title-link" href="/topic/19776749/organize/entire#anchor-children-topic">查看完整话题结构 »</a>

</div>
</div>

</div>


</div>


<div id="zh-footer" class="zh-footer">
<div class="content zg-wrap clearfix">
<ul>

<li><a href="https://liukanshan.zhihu.com" target="_blank">刘看山</a></li>

<li><a href="/question/19581624" target="_blank">知乎指南</a></li>
<li><a href="javascript:;" id="js-feedback-button">建议反馈</a></li>

<li><a href="/app" target="_blank">移动应用</a></li>
<li><a href="/careers">加入知乎</a></li>
<li><a href="/terms" target="_blank">知乎协议</a></li>
<li><a href="/contact">联系我们</a></li>

</ul>

<span class="copy">&copy; 2016 知乎</span>

</div>
</div>

<script type="text/json" class="json-inline" data-name="guiders2">{"exclusive-popover":{},"section":{},"editor":[]}</script>
<script type="text/json" class="json-inline" data-name="current_user">["\u82e5\u6657","da-you-zhen","https:\/\/pic1.zhimg.com\/3ff8329cf6c7eb223e29ee2e40cf16cc_s.jpg","c2bc8adde25c6af3bb16f3fd7dcd81d1","",0,0,true,"827392909@qq.com","http:\/\/mail.qq.com",0,false,false,false,"546753975945322496",false,false,false,true,null]</script>
<script type="text/json" class="json-inline" data-name="user_status">[null,null,false]</script>
<script type="text/json" class="json-inline" data-name="env">["zhihu.com","comet.zhihu.com",false,null,false,false]</script>
<script type="text/json" class="json-inline" data-name="permissions">[]</script>


<script type="text/json" class="json-inline" data-name="ga_vars">{"user_created":1423136305000,"now":1482063842000,"abtest_mask":"---------0--------------------","user_attr":[1,0,0,"-",1],"user_hash":"c2bc8adde25c6af3bb16f3fd7dcd81d1"}</script>

<script type="text/json" class="json-inline" data-name="ra-urls">{"Copyright":"https:\/\/static.zhihu.com\/static\/revved\/-\/apps\/Copyright.a08277db.js","CouponApp":"https:\/\/static.zhihu.com\/static\/revved\/-\/apps\/CouponApp.020ed2f5.js","PaymentApp":"https:\/\/static.zhihu.com\/static\/revved\/-\/apps\/PaymentApp.59fa6542.js","Community":"https:\/\/static.zhihu.com\/static\/revved\/-\/apps\/Community.4e7802b8.js","Report":"https:\/\/static.zhihu.com\/static\/revved\/-\/apps\/Report.66dfcf9c.js","OrgOpHelp":"https:\/\/static.zhihu.com\/static\/revved\/-\/apps\/OrgOpHelp.822ca791.js","common":"https:\/\/static.zhihu.com\/static\/revved\/-\/apps\/common.b8369a70.js","BalanceApp":"https:\/\/static.zhihu.com\/static\/revved\/-\/apps\/BalanceApp.e5268acf.js","AnswerWarrant":"https:\/\/static.zhihu.com\/static\/revved\/-\/apps\/AnswerWarrant.9762e482.js","CommentApp":"https:\/\/static.zhihu.com\/static\/revved\/-\/apps\/CommentApp.acaf0f21.js"}</script>

<script type="text/json" class="json-inline" data-name="current_topic">[["\u300c\u6839\u8bdd\u9898\u300d","19776749","https:\/\/pic4.zhimg.com\/7d3842057_s.jpg",76000],[],0,0,"",0]</script>

<script src="https://static.zhihu.com/static/revved/-/js/vendor.cb14a042.js"></script>
<script src="https://static.zhihu.com/static/revved/-/js/closure/base.34bda779.js"></script>

<script src="https://static.zhihu.com/static/revved/-/js/closure/common.ce42c456.js"></script>


<script src="https://static.zhihu.com/static/revved/-/js/closure/richtexteditor.25c6a511.js" async></script>
<script src="https://static.zhihu.com/static/revved/-/js/closure/page-main.6f2ea2e4.js"></script>
<meta name="entry" content="ZH.entryT" data-module-id="page-main">

<script type="text/zscript" znonce="19238ed76bc54c329f64218028b82e91"></script>

<input type="hidden" name="_xsrf" value="afe7de42cbe077fda8a60a7be8896040"/>
</body>
</html>"""
    xpath = '//*[@id="zh-topic-organize-child-editor"]/div[1]/a[1]'
    print(findBeautifulTagsByXpath(soup,xpath))
    ##################################################################

