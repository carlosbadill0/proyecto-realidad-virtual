document.addEventListener("DOMContentLoaded", function () {
  const isPacheco = window.location.host === 'pacheco.chillan.ubiobio.cl';

  document.querySelectorAll(".verEvaluacionBtn").forEach(function (button) {
    button.addEventListener("click", function () {
      var url = this.getAttribute("data-url");

      if (url && isPacheco && !url.startsWith('/easyflow')) {
        url = '/easyflow' + url;
      }

      if (url) {
        fetch(url)
          .then((response) => response.json())
          .then((data) => {
            const verExpositor = document.getElementById("verExpositor");
            if (verExpositor) verExpositor.value = data.expositor;

            const verEvaluador = document.getElementById("verEvaluador");
            if (verEvaluador) verEvaluador.value = data.nombre_evaluador;

            const verFechaEvaluacion = document.getElementById("verFechaEvaluacion");
            if (verFechaEvaluacion) verFechaEvaluacion.value = data.fecha_evaluacion;

            const verEvaluacionAplicada = document.getElementById("verEvaluacionAplicada");
            if (verEvaluacionAplicada) verEvaluacionAplicada.value = data.evaluacion_aplicada;

            const verObservacionInicial = document.getElementById("verObservacionInicial");
            if (verObservacionInicial) verObservacionInicial.value = data.observacion_inicial;

            const verObservacionFinal = document.getElementById("verObservacionFinal");
            if (verObservacionFinal) verObservacionFinal.value = data.observacion_final;

            const verTiempoExposicion = document.getElementById("verTiempoExposicion");
            if (verTiempoExposicion) verTiempoExposicion.value = data.tiempo_exposicion;

            const verVideoEvaluacion = document.getElementById("verVideoEvaluacion");
            if (verVideoEvaluacion) {
              let videoUrl = data.video_evaluacion;

              if (videoUrl) {
                if (isPacheco && !videoUrl.startsWith('/easyflow')) {
                  videoUrl = '/easyflow' + videoUrl;
                }
                verVideoEvaluacion.innerHTML = `<a href="${videoUrl}">Ver Video</a>`;
              } else {
                verVideoEvaluacion.innerHTML = isPacheco ? "No disponible en Pacheco" : "No disponible";
              }
            } else {
              verVideoEvaluacion.innerHTML = isPacheco ? "No disponible en Pacheco" : "No disponible";
            }

            var verEvaluacionModal = new bootstrap.Modal(document.getElementById("verEvaluacionModal"));
            verEvaluacionModal.show();
          })
          .catch((error) => {
            console.error("Error al obtener los detalles de la evaluación:", error);
            var verEvaluacionModal = new bootstrap.Modal(document.getElementById("verEvaluacionModal"));
            verEvaluacionModal.show();
          });
      } else {
        console.error("URL no válida:", url);
      }
    });
  });

  document.querySelectorAll(".editarEvaluacionBtn").forEach(function (button) {
    button.addEventListener("click", function () {
      var url = this.getAttribute("data-url");
      var id = this.getAttribute("data-id");

      if (isPacheco && !url.startsWith('/easyflow')) {
        url = '/easyflow' + url;
      }

      fetch(url)
        .then((response) => {
          if (!response.ok) {
            throw new Error("La respuesta de la red no fue satisfactoria.");
          }
          return response.json();
        })
        .then((data) => {
          const editarExpositorNombre = document.getElementById("editarExpositorNombre");
          const editarExpositor = document.getElementById("editarExpositor");
          const editarEvaluador = document.getElementById("editarEvaluador");
          const editarFechaEvaluacion = document.getElementById("editarFechaEvaluacion");
          const editarObservacionInicial = document.getElementById("editarObservacionInicial");
          const editarObservacionFinal = document.getElementById("editarObservacionFinal");
          const editarTiempoExposicion = document.getElementById("editarTiempoExposicion");
          const editarVideoEvaluacion = document.getElementById("editarVideoEvaluacion");
          const editarEvaluacionAplicadaNombre = document.getElementById("editarEvaluacionAplicadaNombre");
          const editarEvaluacionAplicada = document.getElementById("editarEvaluacionAplicada");

          if (editarExpositorNombre) editarExpositorNombre.value = data.expositor_nombre;
          if (editarExpositor) editarExpositor.value = data.expositor_id;
          if (editarEvaluador) editarEvaluador.value = data.nombre_evaluador;
          if (editarFechaEvaluacion) editarFechaEvaluacion.value = data.fecha_evaluacion;
          if (editarObservacionInicial) editarObservacionInicial.value = data.observacion_inicial;
          if (editarObservacionFinal) editarObservacionFinal.value = data.observacion_final;
          if (editarTiempoExposicion) editarTiempoExposicion.value = data.tiempo_exposicion;
          if (editarVideoEvaluacion) editarVideoEvaluacion.value = data.video_evaluacion;
          if (editarEvaluacionAplicadaNombre) editarEvaluacionAplicadaNombre.value = data.evaluacion_aplicada_nombre;
          if (editarEvaluacionAplicada) editarEvaluacionAplicada.value = data.evaluacion_aplicada_id;

          document.getElementById("guardarCambiosBtn").setAttribute("data-id", id);

          var editarEvaluacionModal = new bootstrap.Modal(document.getElementById("editarEvaluacionModal"));
          editarEvaluacionModal.show();
        })
        .catch((error) => {
          console.error("Error al obtener los detalles de la evaluación:", error);
        });
    });
  });

  document.getElementById("guardarCambiosBtn").addEventListener("click", function () {
    var id = this.getAttribute("data-id");
    var url = `/evaluaciones_realizadas/${id}/editar/`;
    if (isPacheco && !url.startsWith('/easyflow')) {
      url = '/easyflow' + url;
    }

    var expositor = document.getElementById("editarExpositor").value;
    var nombre_evaluador = document.getElementById("editarEvaluador").value;
    var fecha_evaluacion = document.getElementById("editarFechaEvaluacion").value;
    var observacion_inicial = document.getElementById("editarObservacionInicial").value;
    var observacion_final = document.getElementById("editarObservacionFinal").value;
    var tiempo_exposicion = document.getElementById("editarTiempoExposicion").value;
    var video_evaluacion = document.getElementById("editarVideoEvaluacion").value;
    var evaluacion_aplicada = document.getElementById("editarEvaluacionAplicada").value;

    var formData = new FormData();
    formData.append('expositor', expositor);
    formData.append('nombre_evaluador', nombre_evaluador);
    formData.append('fecha_evaluacion', fecha_evaluacion);
    formData.append('observacion_inicial', observacion_inicial);
    formData.append('observacion_final', observacion_final);
    formData.append('tiempo_exposicion', tiempo_exposicion);
    formData.append('video_evaluacion', video_evaluacion);
    formData.append('evaluacion_aplicada', evaluacion_aplicada);
    formData.append('csrfmiddlewaretoken', document.querySelector("[name=csrfmiddlewaretoken]").value);

    fetch(url, {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        if (data.success) {
          // Cerrar el modal
          var editarEvaluacionModal = bootstrap.Modal.getInstance(document.getElementById("editarEvaluacionModal"));
          editarEvaluacionModal.hide();
          // Opcional: Actualizar la página o la tabla de evaluaciones
          location.reload();
        } else {
          console.error("Error al guardar los cambios:", data.errors);
        }
      })
      .catch((error) => {
        console.error("Error al guardar los cambios:", error);
      });
  });

  // borrar evaluación
  document.querySelectorAll(".borrarEvaluacionBtn").forEach(function (button) {
    button.addEventListener("click", function () {
      var id = this.getAttribute("data-id");
      var url = this.getAttribute("data-url");
      if (isPacheco && !url.startsWith('/easyflow')) {
        url = '/easyflow' + url;
      }

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
    if (isPacheco && !url.startsWith('/easyflow')) {
      url = '/easyflow' + url;
    }

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

document.addEventListener('DOMContentLoaded', function () {
  const searchInput = document.getElementById('searchInput');
  const table = document.getElementById('evaluationTable');
  const noResultsMessage = document.getElementById('noResultsMessage');

  if (searchInput && table && noResultsMessage) {
    const rows = table.getElementsByTagName('tr');

    searchInput.addEventListener('input', function () {
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