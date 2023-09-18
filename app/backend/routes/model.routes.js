const express = require('express');
const router = express.Router();

const model_controller = require('../services/model_detecting');

router.post('/detect-emotion', model_controller.detecting_emotions);

module.exports = router;
