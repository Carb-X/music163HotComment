# music163HotComment
这是一个基于Scrapy的爬虫项目，爬取[网易云音乐](https://music.163.com/#)所有歌曲的热门评论，并导入MongoDB，每条数据包含：
- id: 歌曲在网易云中的id
- music: 歌名
- artist: 歌手
- comment: 热评列表

爬取结果部分信息预览：

<img src='https://github.com/Carb-X/music163HotComment/blob/master/images/Capture_0.JPG?raw=true' width="500" height="650" />

![](https://github.com/Carb-X/music163HotComment/blob/master/images/Capture_1.JPG?raw=true)

---
备注：
- 网易云音乐相关信息需要登陆才能爬取，在请求头中加入登陆后的cookie即可
- 在模拟ajax请求获取评论时也要提供适当参数

请打开Chrome Developer Tools将相关参数加入代码中相应部位



