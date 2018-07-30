# 美女写真图爬虫 trio 版

*其他版本*

* [photo-asyncio 版](https://github.com/chenjiandongx/photo-asyncio)
* [photo-go 版](https://github.com/chenjiandongx/photo-go)
* [photo-gevent 版](https://github.com/chenjiandongx/photo-gevent)

### trio/asks
> 忘了 requests 吧，asks 就足以满足你。 -- 沃·兹基硕德

[Trio](https://github.com/python-trio/trio) 是一个基于 asyncio 的封装库，旨在使异步代码更容易编写，而 [asks](https://github.com/theelous3/asks) 则是 Trio 界的 requests，目前来看除了不支持代理其他都好像很 ok。


### 如何运行

#### 图片数据
图片地址数据保存在了 `data.txt`，共 17w+ 张照片，图片的数据是我从 [mmjpg](https://github.com/chenjiandongx/mmjpg) 和 [mzitu](https://github.com/chenjiandongx/mzitu) 里提取出来的。
```bash
$ wc -l data.txt
178075 data.txt
```

#### 运行代码
```bash
$ git clone https://github.com/chenjiandongx/photo-trio.git
$ cd photo-trio
$ pip install -r requirements.txt # 安装依赖
$ python core.py
```

#### 运行效果
![](https://user-images.githubusercontent.com/19553554/43399082-7987068e-943c-11e8-9224-af550b4a09d9.gif)


## License

MIT [©chenjiandongx](https://github.com/chenjiandongx)
