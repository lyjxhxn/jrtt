# jrtt
今日头条视频解析
解析原理：
破解原理：
那么接下来的问题就是探究上面的第2个请求http://i.snssdk.com/video/urls/v/1/toutiao/mp4/9583cca5fceb4c6b9ca749c214fd1f90?r=18723666135963302&s=3807690062&callback=tt_playerzfndr 是如何构造的。

在用Chrome的开发者工具监视网络请求的时候可以看到该请求是js脚本发出的，该js脚本是 http://s3.pstatp.com/tt_player/player/tt2-player.js?r=customer1
把该js下载下来，prettify一下，使用你最爱的编辑器看看该js到底做了些什么。

通过研究该js脚本，发现请求http://i.snssdk.com/video/urls/v/1/toutiao/mp4/9583cca5fceb4c6b9ca749c214fd1f90?r=18723666135963302&s=3807690062&callback=tt_playerzfndr 中的一些参数的含义如下：

9583cca5fceb4c6b9ca749c214fd1f90：这是视频的唯一ID
18723666135963302：这是一个随机数
3807690062：这是CRC32校验值
视频的唯一ID可以在播放页HTML源码中找到，即id为video的元素的tt-videoid属性值。
