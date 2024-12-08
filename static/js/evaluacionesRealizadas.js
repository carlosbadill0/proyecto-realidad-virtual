document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".verEvaluacionBtn").forEach(function (button) {
    button.addEventListener("click", function () {
      var url = this.getAttribute("data-url");
      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          const verExpositor = document.getElementById("verExpositor");
          if (verExpositor) verExpositor.value = data.expositor;

          const verEvaluador = document.getElementById("verEvaluador");
          if (verEvaluador) verEvaluador.value = data.nombre_evaluador;

          const verFechaEvaluacion =
            document.getElementById("verFechaEvaluacion");
          if (verFechaEvaluacion)
            verFechaEvaluacion.value = data.fecha_evaluacion;

          const verEvaluacionAplicada = document.getElementById(
            "verEvaluacionAplicada"
          );
          if (verEvaluacionAplicada)
            verEvaluacionAplicada.value = data.evaluacion_aplicada;

          const verObservacionInicial = document.getElementById(
            "verObservacionInicial"
          );
          if (verObservacionInicial)
            verObservacionInicial.value = data.observacion_inicial;

          const verObservacionFinal = document.getElementById(
            "verObservacionFinal"
          );
          if (verObservacionFinal)
            verObservacionFinal.value = data.observacion_final;

          const verTiempoExposicion = document.getElementById(
            "verTiempoExposicion"
          );
          if (verTiempoExposicion)
            verTiempoExposicion.value = data.tiempo_exposicion;

          const verVideoEvaluacion =
            document.getElementById("verVideoEvaluacion");
          if (verVideoEvaluacion) {
            verVideoEvaluacion.innerHTML = data.video_evaluacion
              ? `<a href="${data.video_evaluacion}">Ver Video</a>`
              : "No disponible";
          }

          var verEvaluacionModal = new bootstrap.Modal(
            document.getElementById("verEvaluacionModal")
          );
          verEvaluacionModal.show();
        })
        .catch((error) => {
          console.error("Error al obtener los detalles de la evaluación:", error);
        });
    });
  });

  document.querySelectorAll(".editarEvaluacionBtn").forEach(function (button) {
    button.addEventListener("click", function () {
      var url = this.getAttribute("data-url");
      fetch(url)
        .then((response) => {
          if (!response.ok) {
            throw new Error("La respuesta de la red no fue satisfactoria.");
          }
          return response.json();
        })
        .then((data) => {
          const editarExpositor = document.getElementById("editarExpositor");
          const editarEvaluador = document.getElementById("editarEvaluador");
          const editarFechaEvaluacion = document.getElementById("editarFechaEvaluacion");
          const editarObservacionInicial = document.getElementById("editarObservacionInicial");
          const editarObservacionFinal = document.getElementById("editarObservacionFinal");
          const editarTiempoExposicion = document.getElementById("editarTiempoExposicion");
          const editarVideoEvaluacion = document.getElementById("editarVideoEvaluacion");
          const editarEvaluacionAplicada = document.getElementById("editarEvaluacionAplicada");

          if (editarExpositor) editarExpositor.value = data.expositor;
          if (editarEvaluador) editarEvaluador.value = data.nombre_evaluador;
          if (editarFechaEvaluacion) editarFechaEvaluacion.value = data.fecha_evaluacion;
          if (editarObservacionInicial) editarObservacionInicial.value = data.observacion_inicial;
          if (editarObservacionFinal) editarObservacionFinal.value = data.observacion_final;
          if (editarTiempoExposicion) editarTiempoExposicion.value = data.tiempo_exposicion;
          if (editarVideoEvaluacion) editarVideoEvaluacion.value = data.video_evaluacion;
          if (editarEvaluacionAplicada) editarEvaluacionAplicada.value = data.evaluacion_aplicada;

          var editarEvaluacionModal = new bootstrap.Modal(document.getElementById("editarEvaluacionModal"));
          editarEvaluacionModal.show();
        })
        .catch((error) => {
          console.error("Error al obtener los detalles de la evaluación:", error);
        });
    });
  });

  // guardar cambios
  document.getElementById("guardarCambiosBtn").addEventListener("click", function () {
    var id = document.querySelector(".editarEvaluacionBtn").getAttribute("data-id");
    var url = `/evaluaciones_realizadas/${id}/editar/`;
    var expositor = document.getElementById("editarExpositor");
    var nombre_evaluador = document.getElementById("editarEvaluador");
    var fecha_evaluacion = document.getElementById("editarFechaEvaluacion");
    var observacion_inicial = document.getElementById("editarObservacionInicial");
    var observacion_final = document.getElementById("editarObservacionFinal");
    var tiempo_exposicion = document.getElementById("editarTiempoExposicion");
    var video_evaluacion = document.getElementById("editarVideoEvaluacion");
    var evaluacion_aplicada = document.getElementById("editarEvaluacionAplicada");

  
    if (expositor && nombre_evaluador && fecha_evaluacion && observacion_inicial && observacion_final && tiempo_exposicion && video_evaluacion && evaluacion_aplicada) {
      var formData = new FormData();
      formData.append('expositor', expositor.value);
      formData.append('nombre_evaluador', nombre_evaluador.value);
      formData.append('fecha_evaluacion', fecha_evaluacion.value);
      formData.append('observacion_inicial', observacion_inicial.value);
      formData.append('observacion_final', observacion_final.value);
      formData.append('tiempo_exposicion', tiempo_exposicion.value);
      formData.append('video_evaluacion', video_evaluacion.value);
      formData.append('evaluacion_aplicada', evaluacion_aplicada.value);
      formData.append('csrfmiddlewaretoken', document.querySelector("[name=csrfmiddlewaretoken]").value);

      fetch(url, {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            location.reload();
          } else {
            alert("Error al guardar los cambios.");
            console.error(data.errors); // Log the errors for debugging
          }
        })
        .catch((error) => {
          console.error("Error al guardar los cambios:", error);
        });
    } else {
      console.error("Falta uno o más elementos.");
    }
  });

  // borrar evaluación
  document.querySelectorAll(".borrarEvaluacionBtn").forEach(function (button) {
    button.addEventListener("click", function () {
      var id = this.getAttribute("data-id");
      var url = this.getAttribute("data-url");
      document.getElementById("confirmarBorrarBtn").setAttribute("data-id", id);
      document.getElementById("confirmarBorrarBtn").setAttribute("data-url", url);

      var borrarEvaluacionModal = new bootstrap.Modal(document.getElementById("borrarEvaluacionModal"));
      borrarEvaluacionModal.show();
    });
  });

  // Handle confirm delete button click
  document.getElementById("confirmarBorrarBtn").addEventListener("click", function () {
    var id = this.getAttribute("data-id");
    var url = this.getAttribute("data-url");
    var csrfmiddlewaretoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    fetch(url, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfmiddlewaretoken,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          location.reload();
        } else {
          alert("Error al borrar la evaluación.");
        }
      })
      .catch((error) => {
        console.error("Error al borrar la evaluación:", error);
      });
  });
});
  

function parseDate(dateString) {
  // Intenta convertir cadenas comunes (como DD/MM/YYYY o YYYY-MM-DD) en objetos Date
  const parts = dateString.split(/[-/]/); // Admite '-' o '/' como separador
  if (parts.length === 3) {
      if (parts[0].length === 4) {
          // Formato: YYYY-MM-DD
          return new Date(parts[0], parts[1] - 1, parts[2]);
      } else {
          // Formato: DD/MM/YYYY
          return new Date(parts[2], parts[1] - 1, parts[0]);
      }
  }
  return new Date(dateString); // Último recurso: confiar en el constructor Date
}

function sortTable(column, order) {
const table = document.querySelector('table tbody');
const rows = Array.from(table.rows);

rows.sort((a, b) => {
    let aText = a.querySelector(`td[data-column="${column}"]`).textContent.trim();
    let bText = b.querySelector(`td[data-column="${column}"]`).textContent.trim();

    if (column === 'date') {
        aText = parseDate(aText);
        bText = parseDate(bText);
    }

    if (order === 'asc') {
        return aText > bText ? 1 : -1;
    } else {
        return aText < bText ? 1 : -1;
    }
});

rows.forEach(row => table.appendChild(row));
}

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const table = document.getElementById('evaluationTable');
    const noResultsMessage = document.getElementById('noResultsMessage');

    if (searchInput && table && noResultsMessage) {
        const rows = table.getElementsByTagName('tr');

        searchInput.addEventListener('input', function() {
            const filter = searchInput.value.toLowerCase();
            let hasResults = false;

            for (let i = 1; i < rows.length; i++) { // Start from 1 to skip table header
                let cells = rows[i].getElementsByTagName('td');
                let match = false;

                for (let j = 0; j < cells.length; j++) {
                    if (cells[j] && cells[j].getAttribute('data-column') === 'expositor') {
                        if (cells[j].innerText.toLowerCase().indexOf(filter) > -1) {
                            match = true;
                            break;
                        }
                    }
                }

                if (match) {
                    rows[i].style.display = '';
                    hasResults = true;
                } else {
                    rows[i].style.display = 'none';
                }
            }

            if (hasResults) {
                noResultsMessage.style.display = 'none';
            } else {
                noResultsMessage.style.display = 'block';
            }
        });
    }
});

