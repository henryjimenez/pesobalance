<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sudoku Matemático</title>
  <style>
    body {
      font-family: 'Arial', sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
      background: linear-gradient(135deg, #ff9a9e, #fad0c4, #fbc2eb, #a6c1ee, #f6d365);
      background-size: 400% 400%;
      animation: gradientBG 10s ease infinite;
    }
    @keyframes gradientBG {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }
    .container {
      text-align: center;
      background: rgba(255, 255, 255, 0.8);
      padding: 20px;
      border-radius: 15px;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    h1 {
      font-size: 24px;
      color: #333;
      margin-bottom: 20px;
    }
    .sudoku {
      display: grid;
      grid-template-columns: repeat(3, 100px);
      grid-template-rows: repeat(3, 100px);
      gap: 5px;
      margin: 20px auto;
    }
    .cell {
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: #fff;
      border: 1px solid #ccc;
      font-size: 18px;
      font-weight: bold;
      cursor: pointer;
    }
    .highlight {
      background-color: #ffcc00;
    }
    .inputs {
      display: flex;
      justify-content: center;
      gap: 10px;
      margin: 20px 0;
    }
    .inputs input {
      width: 60px;
      height: 30px;
      text-align: center;
      font-size: 16px;
      border: 2px solid #ccc;
      border-radius: 5px;
    }
    button {
      padding: 10px 20px;
      font-size: 16px;
      color: #fff;
      background-color: #4caf50;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      transition: background-color 0.3s;
    }
    button:hover {
      background-color: #45a049;
    }
    .message {
      margin-top: 20px;
      font-size: 20px;
      color: #333;
    }
    .counter {
      margin-top: 10px;
      font-size: 18px;
      color: #333;
    }
    .modal {
      display: none;
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: #fff;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
      text-align: center;
      z-index: 1000;
    }
    .modal h2 {
      font-size: 24px;
      margin-bottom: 10px;
    }
    .modal button {
      margin-top: 10px;
    }
    .overlay {
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.5);
      z-index: 999;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Hecho por Noelia Y Maria Jose con Deepseek -
    9C- Colegio Hispanoamericano</h1>
    <div class="sudoku" id="sudoku"></div>
    <div class="inputs" id="inputs">
      <input type="text" id="input1" placeholder="Respuesta 1">
      <input type="text" id="input2" placeholder="Respuesta 2">
      <input type="text" id="input3" placeholder="Respuesta 3">
    </div>
    <button id="submitBtn">Evaluar Respuestas</button>
    <div class="counter" id="counter">Victorias seguidas: 0</div>
    <div class="message" id="message"></div>
  </div>

  <!-- Modal para mensajes -->
  <div class="overlay" id="overlay"></div>
  <div class="modal" id="modal">
    <h2 id="modalTitle"></h2>
    <p id="modalMessage"></p>
    <button id="modalBtn">Cerrar</button>
  </div>

  <!-- Audio de gato -->
  <audio id="catAudio">
    <source src="https://www.soundjay.com/human/family-guy-happy-cat-1.mp3" type="audio/mpeg">
    Tu navegador no soporta el elemento de audio.
  </audio>

  <audio class="music1"
       src="https://www.myinstants.com/media/sounds/happy-happy-happy-cat.mp3">
  </audio>
  <audio class="music2"
       src="https://www.myinstants.com/media/sounds/bocina-air.mp3">
  </audio>

  <script>
    const sudokuContainer = document.getElementById('sudoku');
    const inputsContainer = document.getElementById('inputs');
    const submitBtn = document.getElementById('submitBtn');
    const messageElement = document.getElementById('message');
    const counterElement = document.getElementById('counter');
    const modal = document.getElementById('modal');
    const modalTitle = document.getElementById('modalTitle');
    const modalMessage = document.getElementById('modalMessage');
    const modalBtn = document.getElementById('modalBtn');
    const overlay = document.getElementById('overlay');
    const catAudio = document.getElementById('catAudio');

    let highlightedRow = 0;
    let currentSudoku = [];
    let timer;
    let winStreak = 0;

    // Generar un Sudoku de operaciones matemáticas
    function generateSudoku() {
      const operations = ['+', '-', '*', '/'];
      const sudoku = [];

      for (let i = 0; i < 3; i++) {
        const row = [];
        for (let j = 0; j < 3; j++) {
          const num1 = Math.floor(Math.random() * 10) + 1;
          const num2 = Math.floor(Math.random() * 10) + 1;
          const operation = operations[Math.floor(Math.random() * operations.length)];
          const expression = `${num1} ${operation} ${num2}`;
          const result = eval(expression).toFixed(2);
          row.push({ expression, result });
        }
        sudoku.push(row);
      }

      return sudoku;
    }

    // Mostrar el Sudoku en la página
    function renderSudoku(sudoku) {
      sudokuContainer.innerHTML = '';
      sudoku.forEach((row, rowIndex) => {
        row.forEach((cell, colIndex) => {
          const cellElement = document.createElement('div');
          cellElement.classList.add('cell');
          if (rowIndex === highlightedRow) {
            cellElement.classList.add('highlight');
          }
          cellElement.textContent = cell.expression;
          sudokuContainer.appendChild(cellElement);
        });
      });
    }

    // Resaltar una fila aleatoria
    function highlightRandomRow() {
      highlightedRow = Math.floor(Math.random() * 3);
    }

    // Evaluar las respuestas del usuario
    function evaluateAnswers() {
      const userAnswers = [
        document.getElementById('input1').value,
        document.getElementById('input2').value,
        document.getElementById('input3').value,
      ];
      const correctAnswers = currentSudoku[highlightedRow].map(cell => cell.result);

      if (userAnswers.every((answer, index) => parseFloat(answer).toFixed(2) === correctAnswers[index])) {
        winStreak++;
        counterElement.textContent = `Victorias seguidas: ${winStreak}`;
        if (winStreak === 3) {
          showModal('¡GANASTE!', 'GANASTE, TE MERECES UN BOMBOM');
          //catAudio.play(); // Reproducir audio de gato
          const music1 = document.querySelector(".music1");
          music1.play();// Reproducir audio de gato
          winStreak = 0; // Reiniciar contador
          counterElement.textContent = `Victorias seguidas: ${winStreak}`;
        } else {
          showModal('¡GANASTE!', 'Felicidades, todas las respuestas son correctas.');
        }
      } else {

        showModal('¡LOSER!', 'Al menos una respuesta es incorrecta. ¡Sigue intentando!');
        const music2 = document.querySelector(".music2");
        music2.play();// Reproducir audio de bocina de aire
        winStreak = 0; // Reiniciar contador
        counterElement.textContent = `Victorias seguidas: ${winStreak}`;
      }
      clearTimeout(timer);
    }

    // Mostrar el modal con un mensaje
    function showModal(title, message) {
      modalTitle.textContent = title;
      modalMessage.textContent = message;
      modal.style.display = 'block';
      overlay.style.display = 'block';
    }

    // Cerrar el modal
    modalBtn.addEventListener('click', () => {
      modal.style.display = 'none';
      overlay.style.display = 'none';
      startNewSudoku();
    });

    // Iniciar un nuevo Sudoku
    function startNewSudoku() {
      currentSudoku = generateSudoku();
      highlightRandomRow();
      renderSudoku(currentSudoku);
      document.getElementById('input1').value = '';
      document.getElementById('input2').value = '';
      document.getElementById('input3').value = '';
      messageElement.textContent = '';
      timer = setTimeout(() => {
        showModal('Tiempo agotado', 'Se acabó el tiempo. ¡Inténtalo de nuevo!');
        winStreak = 0; // Reiniciar contador
        counterElement.textContent = `Victorias seguidas: ${winStreak}`;
      }, 30000); // 10 segundos para responder
    }

    // Iniciar el juego
    submitBtn.addEventListener('click', evaluateAnswers);
    startNewSudoku();
  </script>
</body>
</html>
