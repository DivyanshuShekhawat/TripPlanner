const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');
const authController = require('../controllers/authController');

// Public routes
router.post('/signup', authController.signup);
router.post('/login', authController.login);
router.post('/forgot-password', authController.forgotPassword);
router.patch('/reset-password/:token', authController.resetPassword);

// Protected routes (require authentication)
router.use(authController.protect);

router.get('/me', userController.getMe, userController.getUser);
router.patch('/update-me', userController.updateMe);
router.patch('/update-password', authController.updatePassword);
router.delete('/delete-me', userController.deleteMe);

// Routes for user preferences
router.get('/preferences', userController.getUserPreferences);
router.patch('/preferences', userController.updatePreferences);

// Routes for travel history
router.get('/travel-history', userController.getTravelHistory);
router.post('/travel-history', userController.addTravelHistory);
router.patch('/travel-history/:id', userController.updateTravelHistory);
router.delete('/travel-history/:id', userController.removeTravelHistory);

// Admin routes
router.use(authController.restrictTo('admin'));

router.route('/')
  .get(userController.getAllUsers)
  .post(userController.createUser);

router.route('/:id')
  .get(userController.getUser)
  .patch(userController.updateUser)
  .delete(userController.deleteUser);

module.exports = router; 