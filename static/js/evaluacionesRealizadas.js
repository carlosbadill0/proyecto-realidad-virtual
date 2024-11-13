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

  // Borrar evaluación
  document.querySelectorAll(".borrarEvaluacionBtn").forEach(function (button) {
    button.addEventListener("click", function () {
      var url = this.getAttribute("data-url");
      var borrarEvaluacionModal = new bootstrap.Modal(document.getElementById("borrarEvaluacionModal"));
      document.getElementById("confirmarBorrarBtn").onclick = function () {
        fetch(url, {
          method: "POST",
          headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
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
      };
      borrarEvaluacionModal.show();
    });
  });
});
