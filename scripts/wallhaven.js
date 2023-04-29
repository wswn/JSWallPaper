// host_url = https://wallhaven.cc

var figures = Array.from(document.querySelectorAll('figure'));

const isWindows = navigator.platform.startsWith('Win');
const pathSep = isWindows ? '\\' : '/';
const folder = 'wallhaven' + pathSep;

add_buttons_for_figures(figures)

function add_buttons_for_figures(figures) {
  figures.forEach(function(figure) {
    const img = figure.getElementsByTagName("img")[0];
    const a = figure.getElementsByTagName("a")[0];

    var button = document.createElement('button');
    button.innerHTML = 'Set Background';

    button.addEventListener('click', function() {
      fetch(a.href)
        .then(response => {
          if (!response.ok) {
            throw new Error("Request failed：" + response.status);
          }
          return response.text();
        })
        .then(text => {
          const parser = new DOMParser();
          const doc = parser.parseFromString(text, "text/html");

          const origin_img = Array.from(doc.querySelectorAll("img")).filter(el => el.id === 'wallpaper')[0];
          const url = origin_img.src
          const filename = folder + url.substring(url.lastIndexOf("/") + 1);

          new QWebChannel(qt.webChannelTransport, function(channel) {
            channel.objects.handler.set_background(url, filename);
          });
        })
        .catch(error => console.error(error));
    });

    figure.appendChild(button);

    const imgRect = img.getBoundingClientRect();
    button.style = 'background-color: #0d6efd; color: #fff; border-radius: 5px; padding: 0px 5px; opacity: 0.5; height: auto;'
    button.style.position = "absolute";
    button.style.top = "0"
    button.style.right = "0"
    button.style.zIndex = "9999";

    button.addEventListener("mouseover", function() {
      this.style.opacity = 1
    });

    button.addEventListener("mouseleave", function() {
      button.style.opacity = 0.5
    });

    button.addEventListener("focus", function() {
      button.style.outline = "none";
    });

  });
}

// Monitoring changes
const observer = new MutationObserver(function(mutations_list) {
	mutations_list.forEach(function(mutation) {
		mutation.addedNodes.forEach(function(added_node) {
            let added_figures = Array.from(added_node.querySelectorAll('figure'));
            add_buttons_for_figures(added_figures)
		});
	});
});

// Notify me of everything!
var observerConfig = {
	childList: true,
};

var target = Array.from(document.querySelectorAll('div')).filter(el => el.id === 'thumbs')[0];
observer.observe(target, observerConfig);