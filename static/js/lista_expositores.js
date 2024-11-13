$(document).ready(function () {
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  const csrftoken = getCookie("csrftoken");

  function csrfSafeMethod(method) {
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  }

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
  });

  $("#verExpositorModal").on("show.bs.modal", function (event) {
    var button = $(event.relatedTarget);
    var id = button.data("id");
    var url = "{% url 'detalle_expositor' 0 %}".replace("0", id);

    $.ajax({
      url: url,
      method: "GET",
      success: function (data) {
        $("#verNombre").val(data.nombre);
        $("#verFechaIngreso").val(data.fecha_ingreso);
        $("#verFechaNacimiento").val(data.fecha_nacimiento);
        $("#verEdad").val(data.edad);
        $("#verGenero").val(data.genero);
        $("#verSemestreAcademico").val(data.semestre_academico);
        $("#verCarrera").val(data.carrera);
        $("#verObservacionInicial").val(data.observacion_inicial);
        $("#verObservacionFinal").val(data.observacion_final);
      },
    });
  });

  $("#crearExpositorModal").on("show.bs.modal", function () {
    const today = new Date();
    const day = String(today.getDate()).padStart(2, "0"); // Obtener el día
    const month = String(today.getMonth() + 1).padStart(2, "0"); // Obtener el mes (0-11)
    const year = today.getFullYear(); // Obtener el año
    const formattedDate = `${year}-${month}-${day}`; // Formato 'YYYY-MM-DD'
    $("#fecha_ingreso").val(formattedDate); // Asignar la fecha actual
  });

  $("#crearExpositorBtn").click(function () {
    $.ajax({
      url: '{% url "crear_expositor" %}',
      method: "POST",
      data: $("#crearExpositorForm").serialize(),
      success: function (response) {
        if (response.success) {
          location.reload();
        } else {
          console.log(response);
          alert("Error al crear el expositor.");
        }
      },
    });
  });

  $("#editarExpositorModal").on("show.bs.modal", function (event) {
    var button = $(event.relatedTarget);
    var id = button.data("id");
    var url = "{% url 'detalle_expositor' 0 %}".replace("0", id);
    $.ajax({
      url: url,
      method: "GET",
      success: function (data) {
        $("#editarId").val(id);
        $("#editarNombre").val(data.nombre);
        $("#editarFechaIngreso").val(data.fecha_ingreso);
        $("#editarFecha_nacimiento").val(data.fecha_nacimiento);
        $("#EditarEdad").val(data.edad);
        $("#editarGenero").val(data.genero);
        $("#editarCarrera").val(data.carrera);
        $("#editarSemestre_academico").val(data.semestre_academico);
        $("#editarObservacion_inicial").val(data.observacion_inicial);
        $("#editarObservacion_final").val(data.observacion_final);
      },
    });
  });

  $("#editarExpositorBtn").click(function () {
    var id = $("#editarId").val();
    var url = "{% url 'editar_expositor' 0 %}".replace("0", id);
    $.ajax({
      url: url,
      method: "POST",
      data: $("#editarExpositorForm").serialize(),
      success: function (response) {
        if (response.success) {
          location.reload();
        } else {
          alert("Error al editar el expositor.");
        }
      },
    });
  });

  $("#borrarExpositorModal").on("show.bs.modal", function (event) {
    var button = $(event.relatedTarget);
    var nombreExpositor = button.data("nombre"); // Obtener el nombre del expositor
    var id = button.data("id");
    var url = "{% url 'borrar_expositor' 0 %}".replace("0", id);

    // Establecer el nombre del expositor en el modal
    $("#nombreExpositorBorrar").text(nombreExpositor);

    $("#borrarExpositorBtn")
      .off("click")
      .on("click", function () {
        $.ajax({
          url: url,
          method: "POST",
          success: function (response) {
            if (response.success) {
              location.reload();
            } else {
              alert("Error al borrar el expositor.");
            }
          },
        });
      });
  });

  $(".evaluarExpositorBtn").click(function () {
    var expositorId = $(this).data("id");
    var evaluacionId = $("#evaluacion").val();
    if (evaluacionId) {
      var url = "{% url 'evaluar_expositor' 0 0 %}".replace(
        "0/0",
        expositorId + "/" + evaluacionId
      );
      window.location.href = url;
    } else {
      alert("Por favor, selecciona una evaluación.");
    }
  });

  $(".evaluacionPantallaBtn").click(function () {
    var id = $(this).data("id");
    var url = "{% url 'elegir_evaluacion' 0 %}".replace("0", id);
    window.location.href = url;
  });
});
