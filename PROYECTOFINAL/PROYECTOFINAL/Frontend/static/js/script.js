// Validación del formulario de contacto
const form = document.querySelector('.contact form');

form.addEventListener('submit', (event) => {
  event.preventDefault();

  const name = document.querySelector('.contact input[name="nombre"]').value;
  const email = document.querySelector('.contact input[name="email"]').value;
  const subject = document.querySelector('.contact input[name="asunto"]').value;
  const message = document.querySelector('.contact textarea[name="mensaje"]').value;

  // Aquí puedes agregar la lógica para enviar el formulario
  console.log('Nombre:', name);
  console.log('Email:', email);
  console.log('Asunto:', subject);
  console.log('Mensaje:', message);

  // Reiniciar el formulario
  form.reset();
});