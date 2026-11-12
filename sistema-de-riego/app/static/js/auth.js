function mostrarPassword(inputId, iconId) {
  const password = document.getElementById(inputId);
  const icono = document.getElementById(iconId);

  if (password.type === "password") {
    password.type = "text";
    icono.setAttribute("data-lucide", "eye-off");
  } else {
    password.type = "password";
    icono.setAttribute("data-lucide", "eye");
  }

  lucide.createIcons();
}
