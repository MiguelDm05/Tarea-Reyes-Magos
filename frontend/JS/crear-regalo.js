document.addEventListener("DOMContentLoaded", () => {
  const apiUrl = "http://127.0.0.1:8000/juguetes/";

  // Función para obtener el nombre de la imagen
  const obtenerNombreImagen = (inputFile) => {
    const archivo = inputFile.files[0];
    if (archivo) {
      return archivo.name; // Retorna el nombre del archivo
    }
    return null;
  };

  // Validar que el nombre del regalo no esté vacío y no supere los 20 caracteres
  const validarNombreRegalo = (nombre) => {
    if (!nombre || nombre.trim() === "") {
      alert("El nombre del regalo no puede estar vacío.");
      return false;
    }
    if (nombre.length > 20) {
      alert("El nombre del regalo no puede tener más de 20 caracteres.");
      return false;
    }
    return true;
  };

  // Validar que la imagen esté seleccionada
  const validarImagen = (inputFile) => {
    if (!inputFile.files.length) {
      alert("Debes seleccionar una imagen para el regalo.");
      return false;
    }
    return true;
  };

  // Función para agregar un regalo a la API
  const agregarRegalo = async (nombreRegalo, nombreImagen) => {
    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          nombre: nombreRegalo,
          imagen: nombreImagen,
        }),
      });

      if (!response.ok) {
        console.error("Error al agregar el regalo:", response.statusText);
        throw new Error("Error al añadir el regalo");
      }

      const regalo = await response.json();
      console.log("Regalo agregado:", regalo);
      alert("Regalo agregado correctamente");

      // Esperamos a que se actualice el listado después de agregar el regalo
      await mostrarListadoRegalos();
    } catch (error) {
      console.error("Error en la API:", error);
      alert("No se pudo agregar el regalo.");
    }
  };

  // Función para mostrar el listado de regalos
  const mostrarListadoRegalos = async () => {
    const listadoRegalos = document.getElementById("listado-regalos");
    try {
      const response = await fetch(apiUrl);
      if (!response.ok) {
        console.error(
          "Error al obtener el listado de regalos:",
          response.statusText
        );
        throw new Error("Error al obtener el listado de regalos");
      }

      const regalos = await response.json();
      listadoRegalos.innerHTML = ""; // Limpiar el listado antes de mostrarlo

      if (regalos.length > 0) {
        const ul = document.createElement("ul");
        regalos.forEach((regalo) => {
          const li = document.createElement("li");
          li.textContent = regalo.nombre;

          const img = document.createElement("img");
          img.src = `../IMG/${regalo.imagen}`;
          img.alt = regalo.nombre;
          img.style.maxWidth = "100px";
          img.style.height = "auto";
          li.appendChild(img);

          const btnEliminar = document.createElement("button");
          btnEliminar.textContent = "Eliminar";
          btnEliminar.setAttribute("data-id", regalo.id);
          btnEliminar.addEventListener("click", () =>
            eliminarRegalo(regalo.id)
          );

          li.appendChild(btnEliminar);
          ul.appendChild(li);
        });
        listadoRegalos.appendChild(ul);
        listadoRegalos.style.display = "block";
      } else {
        listadoRegalos.innerHTML = "<p>No hay regalos registrados.</p>";
        listadoRegalos.style.display = "block";
      }
    } catch (error) {
      console.error("Error al obtener el listado de regalos:", error);
    }
  };

  // Función para eliminar un regalo
  const eliminarRegalo = async (id) => {
    try {
      const response = await fetch(`${apiUrl}${id}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        console.error("Error al eliminar el regalo");
        throw new Error("Error al eliminar el regalo");
      }

      alert("Regalo eliminado correctamente");
      await mostrarListadoRegalos(); // Recargar el listado después de eliminar el regalo
    } catch (error) {
      console.error("Error en la API:", error);
    }
  };

  // Manejo del formulario de regalo
  const formRegalo = document.getElementById("form-regalo");
  const inputNombreRegalo = document.getElementById("nombre-regalo");
  const inputImagenRegalo = document.getElementById("imagen-regalo");

  formRegalo.addEventListener("submit", (e) => {
    e.preventDefault();

    const nombreRegalo = inputNombreRegalo.value.trim();
    const nombreImagen = obtenerNombreImagen(inputImagenRegalo);

    // Validaciones
    if (!validarImagen(inputImagenRegalo)) {
      return; // Si no hay imagen seleccionada, no continuamos
    }

    if (!validarNombreRegalo(nombreRegalo)) {
      return; // Si el nombre no es válido, no continúa
    }

    // Agregar el regalo a la API
    agregarRegalo(nombreRegalo, nombreImagen);

    // Limpiar el formulario
    inputNombreRegalo.value = "";
    inputImagenRegalo.value = ""; // Limpiar el input de archivo
  });

  // Mostrar listado de regalos al hacer clic en el botón
  const btnVerListado = document.getElementById("ver-listado-regalos");
  btnVerListado.addEventListener("click", mostrarListadoRegalos);
});
