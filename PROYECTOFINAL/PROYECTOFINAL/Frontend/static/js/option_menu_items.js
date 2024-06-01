document.addEventListener("DOMContentLoaded", function() {
  const navLinks = document.querySelectorAll(".nav-link");

  navLinks.forEach(function(navLink) {
    navLink.addEventListener("click", function(event) {
      event.preventDefault();
      const menuOption = event.target.textContent.trim();
      redirectToUrl(menuOption);
    });
  });
});

function redirectToUrl(menuOption) {
  // Define un objeto que mapea nombres de menú a URLs
  const menuOptions = {
    "Castracion": "/Castracion_datos",
    "Registrar": "/Registrar_datos",
    "Adopciones": "/Catalogo_datos"
  };

  // Obtiene la URL correspondiente a la opción del menú seleccionada
  const url = menuOptions[menuOption];

  // Redirige al usuario a la URL correspondiente
  if (url) {
    window.location.href = url;
  } else {
    console.error(`No se encontró una URL para la opción del menú: ${menuOption}`);
  }
}