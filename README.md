# JSWallPaper

[Release](https://github.com/wswn/JSWallPaper/releases)

![Image text](https://raw.githubusercontent.com/wswn/JSWallPaper/main/UIExamples/wdbyte.jpg)

A WallPaper tool.

This tool is inspired by the effort of [@niumoo](https://github.com/niumoo/bing-wallpaper), and written with python and Javascript.

**_Really appreciate it!!!_**

_Platforms: MacOS, Windows_

It has Very Simple Functions including loading website, injecting js script and then setting backgound. 

**_Traits:_**

* Convenient ...

**_For extension_**, just write a JS file and put it into `./scripts`. 
Make sure specifying the target host url at the first line with the format like: 

`// host_url = https://bing.wdbyte.com, www.baidu.com`

Then, set the obtained pic url and the file to be saved with the format like

``` javascript
new QWebChannel(qt.webChannelTransport, function(channel) {
    var url = ...
    var file = ...
    channel.objects.handler.set_background(url, file);
});
```
All done.
