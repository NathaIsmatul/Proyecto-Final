document.addEventListener('DOMContentLoaded', function () {
    var nombreInput = document.getElementById("nombreInput");
    var userTypeElement = document.getElementById('userType');

    nombreInput.addEventListener('input', function () {
        var nombre = nombreInput.value;
        var userType = "";

        if (nombre === "Oliver") {
            userType = "Admin";
            userTypeElement.style.color = "black"; // Color negro para "Admin"
        } else if (nombre === "Natanael") {
            userType = "User";
            userTypeElement.style.color = "blue"; // Color azul para "User"
        } else {
            userType = "Strange";
            userTypeElement.style.color = "red"; // Color rojo para "Strange"
        }

        userTypeElement.textContent = "-- " + userType + " --";

        if (nombre === "") {
            userTypeElement.classList.remove('fade-in'); // Oculta el elemento si el campo está vacío
        } else {
            userTypeElement.classList.add('fade-in'); // Agrega la clase para mostrar con desvanecimiento
        }
    });
});
