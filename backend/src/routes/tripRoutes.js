const express = require('express');
const router = express.Router();
const tripController = require('../controllers/tripController');
const authController = require('../controllers/authController');

// Protect all routes after this middleware
router.use(authController.protect);

// Routes for trips
router.route('/')
  .get(tripController.getAllTrips)
  .post(tripController.createTrip);

router.route('/:id')
  .get(tripController.getTrip)
  .patch(tripController.updateTrip)
  .delete(tripController.deleteTrip);

// Budget routes
router.route('/:id/budget')
  .get(tripController.getTripBudget)
  .patch(tripController.updateTripBudget);

// Destination routes within a trip
router.route('/:id/destinations')
  .get(tripController.getTripDestinations)
  .post(tripController.addDestination);

router.route('/:id/destinations/:destinationId')
  .get(tripController.getDestination)
  .patch(tripController.updateDestination)
  .delete(tripController.removeDestination);

// Activities routes within a trip destination
router.route('/:id/destinations/:destinationId/activities')
  .get(tripController.getActivities)
  .post(tripController.addActivity);

router.route('/:id/destinations/:destinationId/activities/:activityId')
  .patch(tripController.updateActivity)
  .delete(tripController.removeActivity);

// Accommodation routes within a trip destination
router.route('/:id/destinations/:destinationId/accommodations')
  .get(tripController.getAccommodations)
  .post(tripController.addAccommodation);

router.route('/:id/destinations/:destinationId/accommodations/:accommodationId')
  .patch(tripController.updateAccommodation)
  .delete(tripController.removeAccommodation);

// Transportation routes within a trip destination
router.route('/:id/destinations/:destinationId/transportation')
  .get(tripController.getTransportation)
  .post(tripController.addTransportation);

router.route('/:id/destinations/:destinationId/transportation/:transportationId')
  .patch(tripController.updateTransportation)
  .delete(tripController.removeTransportation);

// Notes routes
router.route('/:id/notes')
  .get(tripController.getNotes)
  .post(tripController.addNote);

router.route('/:id/notes/:noteId')
  .patch(tripController.updateNote)
  .delete(tripController.removeNote);

// Share trip route
router.patch('/:id/share', tripController.shareTrip);

// Export itinerary route
router.get('/:id/export', tripController.exportTrip);

module.exports = router; 