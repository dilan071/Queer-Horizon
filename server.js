const express = require('express');
const multer = require('multer');
const app = express();
const port = 3000;

// Configurar Multer para almacenar archivos en la carpeta 'uploads'
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    cb(null, `${Date.now()}-${file.originalname}`);
  },
});
const upload = multer({ storage });

// Ruta para mostrar el formulario de carga
app.get('/', (req, res) => {
  res.send(`
    <form action="/upload" method="post" enctype="multipart/form-data">
      <label for="video-upload">Adjuntar video:</label>
      <input type="file" id="video-upload" name="video" accept="video/*">
      <button type="submit">Enviar</button>
    </form>
  `);
});

// Ruta para manejar la carga de archivos
app.post('/upload', upload.single('video'), (req, res) => {
  res.send('Video subido y guardado.');
});

// Iniciar el servidor
app.listen(port, () => {
  console.log(`Servidor escuchando en http://localhost:${port}`);
});
