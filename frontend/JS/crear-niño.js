// Función de inicialización
function init() {
  // Obtener los elementos del DOM
  const form = document.getElementById("form-nino");
  const errorMsg = document.getElementById("error-msg");
  const verListadoBtn = document.getElementById("ver-listado");
  const listadoNinosDiv = document.getElementById("listado-ninos");

  // Manejar la creación del niño
  form.addEventListener("submit", async function (event) {
    event.preventDefault(); // Evita que el formulario se envíe de manera normal

    // Limpiar mensajes de error
    errorMsg.textContent = "";

    // Obtener los valores del formulario
    const nombre = document.getElementById("nombre").value.trim();
    const edad = document.getElementById("edad").value.trim();

    // Validación de los datos
    if (!nombre) {
      errorMsg.textContent = "Por favor, ingresa un nombre válido.";
      return;
    }
    if (nombre.length > 20) {
      errorMsg.textContent = "El nombre no puede tener más de 20 caracteres.";
      return;
    }
    if (!edad || edad < 0 || edad > 15) {
      errorMsg.textContent = "La edad debe estar entre 0 y 15 años.";
      return;
    }

    // Crear objeto con los datos del niño
    const ninoData = {
      nombre: nombre,
      edad: edad,
    };

    try {
      // Realizar la solicitud POST a la API
      const response = await fetch("http://127.0.0.1:8000/usuarios/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(ninoData),
      });

      const data = await response.json();

      if (response.ok) {
        // Si la respuesta es exitosa, mostrar un mensaje
        alert(`Niño añadido con éxito: ${data.nombre}, Edad: ${data.edad}`);
      } else {
        // Si hubo un error con la respuesta
        errorMsg.textContent = `Error: ${
          data.message || "Hubo un problema al agregar al niño."
        }`;
      }
    } catch (error) {
      // En caso de error de red
      errorMsg.textContent = "Hubo un error al intentar conectar con la API.";
      console.error("Error:", error);
    }
  });

  // Función para ver el listado de niños
  verListadoBtn.addEventListener("click", async function () {
    try {
      // Realizar la solicitud GET a la API para obtener el listado
      const response = await fetch("http://127.0.0.1:8000/usuarios/");
      const data = await response.json();

      if (response.ok) {
        // Limpiar el contenedor de listado
        listadoNinosDiv.innerHTML = "<h2>Listado de Niños</h2>";

        // Crear lista de niños
        const ul = document.createElement("ul");
        data.forEach((nino) => {
          const li = document.createElement("li");
          li.innerHTML = `${nino.nombre} - Edad: ${nino.edad} 
                        <button data-id="${nino.id}" class="eliminar-btn">Eliminar</button>`;
          ul.appendChild(li);
        });

        listadoNinosDiv.appendChild(ul);

        // Añadir evento de eliminación a los botones
        const eliminarBtns = document.querySelectorAll(".eliminar-btn");
        eliminarBtns.forEach((btn) => {
          btn.addEventListener("click", async function () {
            const id = this.getAttribute("data-id");

            try {
              const response = await fetch(
                `http://127.0.0.1:8000/usuarios/${id}`,
                {
                  method: "DELETE",
                }
              );

              const data = await response.json();

              if (response.ok) {
                // Si la eliminación fue exitosa
                alert(`Niño eliminado con éxito.`);
                // Refrescar listado
                verListadoBtn.click();
              } else {
                // Si hubo un error en la respuesta
                alert(
                  `Error al eliminar niño: ${
                    data.message || "Hubo un problema al eliminar al niño."
                  }`
                );
              }
            } catch (error) {
              console.error("Error al eliminar niño:", error);
              alert("Hubo un error al intentar eliminar al niño.");
            }
          });
        });
      } else {
        listadoNinosDiv.innerHTML = `<p class="error">Error al obtener el listado de niños.</p>`;
      }
    } catch (error) {
      // En caso de error de red
      listadoNinosDiv.innerHTML = `<p class="error">Hubo un error al intentar conectar con la API.</p>`;
      console.error("Error:", error);
    }
  });
}

// Llamamos a la función init para inicializar el código cuando cargue la página
init();
