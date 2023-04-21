// host_url = https://bing.wdbyte.com, https://www.baidu.com

var downloadLinks = Array.from(document.querySelectorAll('a'))
.filter(el => el.textContent === 'Download 4k');

const isWindows = navigator.platform.startsWith('Win');
const pathSep = isWindows ? '\\' : '/';

downloadLinks.forEach(function(link) {
  var button = document.createElement('button');
  button.innerHTML = 'Set Background';
  button.style.marginLeft = '10px';
  button.style.fontSize = (parseFloat(window.getComputedStyle(link).fontSize) / 4 * 3) + 'px';
  // link.style.fontSize
  button.addEventListener('click', function() {
    fileName = link.parentNode.childNodes[0].textContent.trim() + '.jpg';
    new QWebChannel(qt.webChannelTransport, function(channel) {
        const regex_href = /:\/\/|\./g;
        var folder = self.location.href.replace(regex_href, "_")
        if (!folder.endsWith('/')) {
            folder += '/'
        }
        const regex_ym = /\d{4}-\d{2}/;
        const match = fileName.match(regex_ym);
        const year_mon = match ? match[0] : '';
        console.log(year_mon)
        if (!folder.includes(year_mon)) {
            folder += year_mon + '/'
        }
        // Reformat path with current platform separator
        const regex_pathSep = /\//g;
        let fullPath = (folder+fileName).replace(regex_pathSep, pathSep)
        channel.objects.handler.set_background(link.href, fullPath);
    });
  });
  link.parentNode.insertBefore(button, link.nextSibling);
});
