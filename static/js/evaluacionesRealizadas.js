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
        });
    });
  });

  document.querySelectorAll(".editarEvaluacionBtn").forEach(function (button) {
    button.addEventListener("click", function () {
      var url = this.getAttribute("data-url");
      fetch(url)
        .then((response) => response.json())
        .then((data) => {
          const editarEvaluacionId =
            document.getElementById("editarEvaluacionId");
          if (editarEvaluacionId) editarEvaluacionId.value = data.id;

          const editarExpositor = document.getElementById("editarExpositor");
          if (editarExpositor) editarExpositor.value = data.expositor;

          const editarEvaluador = document.getElementById("editarEvaluador");
          if (editarEvaluador) editarEvaluador.value = data.nombre_evaluador;

          const editarFechaEvaluacion = document.getElementById(
            "editarFechaEvaluacion"
          );
          if (editarFechaEvaluacion)
            editarFechaEvaluacion.value = data.fecha_evaluacion;

          const editarObservacionInicial = document.getElementById(
            "editarObservacionInicial"
          );
          if (editarObservacionInicial)
            editarObservacionInicial.value = data.observacion_inicial;

          const editarObservacionFinal = document.getElementById(
            "editarObservacionFinal"
          );
          if (editarObservacionFinal)
            editarObservacionFinal.value = data.observacion_final;

          const editarTiempoExposicion = document.getElementById(
            "editarTiempoExposicion"
          );
          if (editarTiempoExposicion)
            editarTiempoExposicion.value = data.tiempo_exposicion;

          const editarVideoEvaluacion = document.getElementById(
            "editarVideoEvaluacion"
          );
          if (editarVideoEvaluacion)
            editarVideoEvaluacion.value = data.video_evaluacion;

          var editarEvaluacionModal = new bootstrap.Modal(
            document.getElementById("editarEvaluacionModal")
          );
          editarEvaluacionModal.show();
        });
    });
  });
  document.addEventListener("DOMContentLoaded", function () {
    const confirmarBorrarBtn = document.getElementById("confirmarBorrarBtn");
    if (confirmarBorrarBtn) {
      confirmarBorrarBtn.onclick = function () {
        const csrfTokenElement = document.querySelector("[name=csrfmiddlewaretoken]");
        if (csrfTokenElement) {
          fetch(url, {
            method: "POST",
            headers: {
              "X-CSRFToken": csrfTokenElement.value,
            },
          })
            .then((response) => response.json())
            .then((data) => {
              if (data.success) {
                location.reload();
              } else {
                alert("Error al borrar la evaluación.");
              }
            });
        } else {
          console.error("El token CSRF no se encontró en el DOM.");
        }
      };
    } else {
      console.error("El botón confirmarBorrarBtn no se encontró en el DOM.");
    }
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

