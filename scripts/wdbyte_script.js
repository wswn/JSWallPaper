// host_url = https://bing.wdbyte.com

var downloadLinks = Array.from(document.querySelectorAll('a'))
.filter(el => el.textContent === 'Download 4k');

const isWindows = navigator.platform.startsWith('Win');
const pathSep = isWindows ? '\\' : '/';

downloadLinks.forEach(function(link) {
    var button = document.createElement('button');
    button.innerHTML = 'Set Background';
    button.style.marginLeft = '10px';
    button.style.fontSize = (parseFloat(window.getComputedStyle(link).fontSize) / 4 * 3) + 'px';

    // Onclick callback.
    button.addEventListener('click', function() {
        // Transform the url as a valid directory.
        const regexHref = /:\/\/|\./g;
        let folder = self.location.href.replace(regexHref, "_");
        folder += folder.endsWith('/')? '' : '/';

        // Add date as sub-directory.
        let fileName = link.parentNode.childNodes[0].textContent.trim() + '.jpg';
        const regexDate = /\d{4}-\d{2}/;
        const match = fileName.match(regexDate);
        const date = match ? match[0] : '';
        folder += folder.includes(date)? '' : date + '/';

        // Reformat path with the separator of current platform.
        const regexPathSep = /\//g;
        let fullPath = (folder+fileName).replace(regexPathSep, pathSep)

        // API: Set Desktop Background.
        if (typeof QWebChannel === "function") {
          new QWebChannel(qt.webChannelTransport, function(channel) {
            channel.objects.handler.set_background(link.href, fullPath);
          });
        }
        if (window.webkit) {
          window.webkit.messageHandlers.callbackHandler.postMessage({'href': link.href, 'file': fullPath})
        }
    });
    link.parentNode.insertBefore(button, link.nextSibling);
});
