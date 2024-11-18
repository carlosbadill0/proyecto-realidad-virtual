// frecuencia_cardiaca.js

let currentStage = 1;
let isEvaluating = false;
let startTime;
let timerInterval;
let chart;
const serverUrlPost = "http://localhost:127/api/frecuencia/"; // Cambiar a localhost
const serverUrlGet = "http://localhost:127/api/ultima_frecuencia/"; // Cambiar a localhost
const evaluacionId = "{{ evaluacion.id }}";
console.log(evaluacionId);

function updateProgressBar() {
  const progressValues = { 1: 33, 2: 66, 3: 100 };
  const stageNames = ["stage-name-1", "stage-name-2", "stage-name-3"];
  const progressBar = document.getElementById("progress-bar");

  // Actualiza el ancho de la barra de progreso
  progressBar.style.width = `${progressValues[currentStage]}%`;
  progressBar.setAttribute("aria-valuenow", progressValues[currentStage]);

  // Resalta el nombre de la etapa actual
  stageNames.forEach((stage, index) => {
    const element = document.getElementById(stage);
    if (index + 1 === currentStage) {
      element.style.fontWeight = "bold";
      element.style.color = "#007bff"; // Color destacado
    } else {
      element.style.fontWeight = "normal";
      element.style.color = "#495057"; // Color normal
    }
  });
}

function showStage(stage) {
  document.querySelectorAll(".stage-container").forEach((container) => {
    container.style.display = "none";
  });
  document.getElementById("stage-" + stage).style.display = "block";
  currentStage = stage; // Actualiza la etapa actual
  updateProgressBar(); // Actualiza la barra de progreso
}

function updateTimer() {
  const now = new Date();
  const elapsedTime = Math.floor((now - startTime) / 1000);
  const minutes = Math.floor(elapsedTime / 60);
  const seconds = elapsedTime % 60;
  document.getElementById("timer").textContent = `${minutes}m ${seconds}s`;
}

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

function iniciarGuardado() {
  axios
    .post("/api/iniciar_guardado/")
    .then((response) => {
      console.log("Guardado iniciado:", response.data);
    })
    .catch((error) => {
      console.error("Error al iniciar guardado:", error);
    });
}

function detenerGuardado() {
  axios
    .post("/api/detener_guardado/")
    .then((response) => {
      console.log("Guardado detenido:", response.data);
    })
    .catch((error) => {
      console.error("Error al detener guardado:", error);
    });
}

function enviarDatosAlServidor(bpm, evaluationId) {
  axios
    .post("/api/frecuencia/", {
      bpm: parseInt(bpm),
      evaluationId: parseInt(evaluationId),
    })
    .then((response) => {
      console.log("Datos enviados correctamente:", response.data);
    })
    .catch((error) => {
      console.error("Error al enviar datos:", error);
      if (error.response) {
        console.error("Detalles del error:", error.response);
      } else if (error.request) {
        console.error("No se recibió respuesta del servidor:", error.request);
      } else {
        console.error("Error al configurar la solicitud:", error.message);
      }
    });
}

function obtenerFrecuencia() {
  axios
    .get(serverUrlGet)
    .then((response) => {
      console.log("Frecuencia obtenida:", response.data);
      if (response.data.status === "success") {
        const frecuencia = response.data.frecuencia;
        const now = new Date();
        chart.data.labels.push(now);
        chart.data.datasets[0].data.push(frecuencia);
        chart.update();
        document.getElementById("frecuencia").textContent = frecuencia;
      }
    })
    .catch((error) => {
      console.error("Error al obtener frecuencia:", error);
      if (error.response) {
        console.error("Detalles del error:", error.response);
      } else if (error.request) {
        console.error("No se recibió respuesta del servidor:", error.request);
      } else {
        console.error("Error al configurar la solicitud:", error.message);
      }
    });
}

document.addEventListener("DOMContentLoaded", function () {
  updateProgressBar();
  showStage(currentStage);

  document
    .getElementById("nextStage1")
    .addEventListener("click", function () {
      currentStage++;
      updateProgressBar();
      showStage(currentStage);
    });

  document
    .getElementById("prevStage2")
    .addEventListener("click", function () {
      currentStage--;
      updateProgressBar();
      showStage(currentStage);
    });

  document
    .getElementById("nextStage2")
    .addEventListener("click", function () {
      currentStage++;
      updateProgressBar();
      showStage(currentStage);
    });
  document
    .getElementById("prevStage3")
    .addEventListener("click", function () {
      currentStage--;
      updateProgressBar();
      showStage(currentStage);
    });

  const ctx = document.getElementById("graficoFrecuencia").getContext("2d");
  chart = new Chart(ctx, {
    type: "line",
    data: {
      labels: [],
      datasets: [
        {
          label: "Frecuencia Cardíaca (BPM)",
          backgroundColor: "rgba(255, 99, 132, 0.2)",
          borderColor: "rgba(255, 99, 132, 1)",
          data: [],
          fill: false,
        },
      ],
    },
    options: {
      scales: {
        x: {
          type: "time",
          time: { unit: "second" },
          title: { display: true, text: "Tiempo" },
        },
        y: {
          beginAtZero: true,
          suggestedMax: 150,
          title: { display: true, text: "BPM" },
        },
      },
    },
  });

  obtenerFrecuencia();
  setInterval(obtenerFrecuencia, 1000);

  // Inicializa el temporizador en 0m 0s
  document.getElementById("timer").textContent = "0m 0s";
});

document.addEventListener("DOMContentLoaded", function () {
  // Inicializa en la primera etapa
  showStage(1);

  // Configura los botones de navegación de etapas
  document
    .getElementById("nextStage1")
    .addEventListener("click", function () {
      showStage(2);
    });

  document
    .getElementById("nextStage2")
    .addEventListener("click", function () {
      showStage(3);
    });

  // Configura el botón de evaluación
  document
    .getElementById("evaluationButton")
    .addEventListener("click", function (event) {
      event.preventDefault();
      const button = this;
      const backButton = document.getElementById("prevStage3");
      if (!isEvaluating) {
        // Iniciar evaluación
        button.textContent = "Finalizar evaluación";
        isEvaluating = true;
        startTime = new Date();
        timerInterval = setInterval(updateTimer, 1000);
        backButton.disabled = true; // Bloquear el botón de volver atrás
      } else {
        // Finalizar evaluación
        button.textContent = "Iniciar evaluación";
        isEvaluating = false;
        clearInterval(timerInterval);
        backButton.disabled = false; // Desbloquear el botón de volver atrás

        // Calcular tiempo total
        const now = new Date();
        const elapsedTime = Math.floor((now - startTime) / 1000);
        document.getElementById("tiempo_total").value = elapsedTime;

        // Enviar el formulario
        document.getElementById("evaluacionForm").submit();
      }
    });

  // Inicializa el gráfico
  const ctx = document.getElementById("graficoFrecuencia").getContext("2d");
  chart = new Chart(ctx, {
    type: "line",
    data: {
      labels: [], // Etiquetas de tiempo
      datasets: [
        {
          label: "Frecuencia Cardíaca (BPM)",
          backgroundColor: "rgba(255, 99, 132, 0.2)",
          borderColor: "rgba(255, 99, 132, 1)",
          data: [], // Datos de frecuencia
          fill: false,
        },
      ],
    },
    options: {
      scales: {
        x: {
          type: "time",
          time: {
            unit: "second",
          },
          title: {
            display: true,
            text: "Tiempo",
          },
        },
        y: {
          beginAtZero: true,
          suggestedMax: 150,
          title: {
            display: true,
            text: "BPM",
          },
        },
      },
    },
  });

  // Obtener y enviar datos de evaluación
  const bpm = document.getElementById("bpm-value").textContent;
  enviarDatosAlServidor(bpm, evaluacionId);

  // Obtener la última frecuencia inicialmente y luego cada 1 segundos
  obtenerFrecuencia();
  setInterval(obtenerFrecuencia, 1000);
});

// Ejemplo de cómo podrías llamar a esta función
document.addEventListener("DOMContentLoaded", function () {
  const bpmElement = document.getElementById("bpm-value");
  if (bpmElement) {
    const frecuencia = bpmElement.textContent;
    enviarDatosAlServidor(frecuencia);
  }
});

document
  .getElementById("startCapture")
  .addEventListener("click", async function () {
    try {
      const stream = await navigator.mediaDevices.getDisplayMedia({
        video: true,
      });
      const videoElement = document.getElementById("liveVideo");
      videoElement.srcObject = stream;
    } catch (err) {
      console.error("Error: " + err);
    }
  });

document
  .getElementById("startCapture2")
  .addEventListener("click", async function () {
    try {
      const stream = await navigator.mediaDevices.getDisplayMedia({
        video: true,
      });
      const videoElement = document.getElementById("liveVideo2");
      videoElement.srcObject = stream;
    } catch (err) {
      console.error("Error: " + err);
    }
  });

// WebSocket para transmisión de video
const videoElement = document.getElementById('player-view');
const signalingServerUrl = "ws://pacheco.chillan.ubiobio.cl:127/"; // Cambiar aca con el del protocolo y nombre del servidor
const pc = new RTCPeerConnection();

const signaling = new WebSocket(signalingServerUrl);

signaling.onopen = () => {
    console.log("WebSocket conectado");
};

signaling.onmessage = async (event) => {
    const message = JSON.parse(event.data);

    if (message.type === 'offer') {
        await pc.setRemoteDescription(new RTCSessionDescription(message));
        const answer = await pc.createAnswer();
        await pc.setLocalDescription(answer);

        signaling.send(JSON.stringify({
            type: 'answer',
            sdp: pc.localDescription.sdp
        }));
    }
};

pc.ontrack = (event) => {
    videoElement.srcObject = event.streams[0];
};

pc.addTransceiver('video', { direction: 'recvonly' });