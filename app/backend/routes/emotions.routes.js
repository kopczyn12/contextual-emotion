const express = require('express');
const router = express.Router();

const emotions_controller = require('../controllers/emotions.controller');

router.post('/add-image', emotions_controller.createEmotionsImage);

module.exports = router;
