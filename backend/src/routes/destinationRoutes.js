const express = require('express');
const router = express.Router();
const destinationController = require('../controllers/destinationController');
const authController = require('../controllers/authController');

// Public routes
router.get('/', destinationController.getAllDestinations);
router.get('/:id', destinationController.getDestination);
router.get('/search', destinationController.searchDestinations);
router.get('/nearby', destinationController.getNearbyDestinations);
router.get('/popular', destinationController.getPopularDestinations);
router.get('/recommended', destinationController.getRecommendedDestinations);

// Protected routes
router.use(authController.protect);

router.get('/personalized-recommendations', destinationController.getPersonalizedRecommendations);

// Admin routes
router.use(authController.restrictTo('admin'));

router.post('/', destinationController.createDestination);
router.patch('/:id', destinationController.updateDestination);
router.delete('/:id', destinationController.deleteDestination);

module.exports = router; 