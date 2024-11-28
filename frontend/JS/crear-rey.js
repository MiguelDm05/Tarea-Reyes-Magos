document.addEventListener("DOMContentLoaded", () => {
  // Función que encapsula toda la lógica
  (function () {
    // Los nombres válidos de los Reyes Magos
    const nombresValidos = ["Melchor", "Gaspar", "Baltasar"];
    // URL de la API
    const apiUrl = "http://127.0.0.1:8000/reyes_magos/";

    // Obtener los Reyes Magos de la API
    const obtenerReyesMagos = async () => {
      try {
        const response = await fetch(apiUrl);
        console.log("Respuesta de la API:", response);
        if (!response.ok) {
          console.error(
            "Error en la respuesta de la API:",
            response.statusText
          );
          throw new Error("Error al obtener los Reyes Magos");
        }
        const reyes = await response.json();
        return reyes;
      } catch (error) {
        console.error("Error en la API:", error);
        return []; // Devuelve un array vacío si hay error en la API
      }
    };

    // Mostrar listado de Reyes Magos
    const mostrarListadoReyes = async () => {
      const listadoReyes = document.getElementById("listado-reyes");
      const reyes = await obtenerReyesMagos();
      listadoReyes.innerHTML = ""; // Limpiar el listado antes de mostrarlo

      if (reyes.length > 0) {
        const ul = document.createElement("ul");
        reyes.forEach((rey) => {
          const li = document.createElement("li");
          li.textContent = rey.nombre;

          // Crear botón de eliminar para cada Rey Mago
          const btnEliminar = document.createElement("button");
          btnEliminar.textContent = "Eliminar";
          btnEliminar.setAttribute("data-id", rey.id); // Establecer el ID en el botón

          // Agregar el evento de eliminar al botón
          btnEliminar.addEventListener("click", () => eliminarReyMago(rey.id));

          li.appendChild(btnEliminar); // Añadir el botón al elemento de la lista
          ul.appendChild(li);
        });
        listadoReyes.appendChild(ul);
        listadoReyes.style.display = "block"; // Mostrar el listado
      } else {
        listadoReyes.innerHTML = "<p>No hay Reyes Magos registrados.</p>";
        listadoReyes.style.display = "block"; // Mostrar el listado
      }
    };

    // Función para eliminar un Rey Mago
    const eliminarReyMago = async (id) => {
      try {
        const response = await fetch(`${apiUrl}${id}`, {
          method: "DELETE",
        });

        if (!response.ok) {
          throw new Error("Error al eliminar el Rey Mago");
        }

        // Mostrar un mensaje de éxito y actualizar el listado
        alert("Rey Mago eliminado correctamente");
        mostrarListadoReyes(); // Recargar el listado de Reyes Magos
      } catch (error) {
        console.error("Error en la API:", error);
        alert("No se pudo eliminar el Rey Mago.");
      }
    };

    // Validar el nombre ingresado
    const validarNombreRey = (nombre) => {
      return nombresValidos.includes(nombre);
    };

    // Agregar un Rey Mago a la API
    const agregarReyMago = async (nombreRey) => {
      try {
        const response = await fetch(apiUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ nombre: nombreRey }),
        });

        if (!response.ok) {
          console.error("Error al agregar Rey Mago:", response.statusText);
          throw new Error("Error al añadir el Rey Mago");
        }

        const rey = await response.json();
        console.log("Rey Mago agregado:", rey);
        alert("Rey Mago agregado correctamente");

        // Llamamos a mostrarListadoReyes solo después de que el Rey Mago haya sido agregado
        mostrarListadoReyes(); // Actualizar listado después de agregar
      } catch (error) {
        console.error("Error en la API:", error);
        alert("No se pudo agregar el Rey Mago.");
      }
    };

    // Eventos de interacción con el formulario
    const formReyMago = document.getElementById("form-rey-mago");
    const inputNombreRey = document.getElementById("nombre-rey");

    formReyMago.addEventListener("submit", (e) => {
      e.preventDefault();
      const nombreRey = inputNombreRey.value.trim();

      if (!validarNombreRey(nombreRey)) {
        // Si el nombre no es válido, mostrar un mensaje de error
        alert(
          "El nombre debe ser uno de los siguientes: Melchor, Gaspar o Baltasar."
        );
        return;
      }

      // Agregar el Rey Mago a la API
      agregarReyMago(nombreRey);

      // Limpiar el campo de entrada
      inputNombreRey.value = "";
    });

    // Mostrar listado de Reyes Magos al hacer clic en el botón
    const btnVerListado = document.getElementById("ver-listado-reyes");
    btnVerListado.addEventListener("click", mostrarListadoReyes);
  })();
});
