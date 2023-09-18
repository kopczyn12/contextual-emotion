const express = require('express');
const router = express.Router();

const stable_controller = require('../controllers/stable.controller');

router.post('/generate-image', stable_controller.generate_image);

module.exports = router;
