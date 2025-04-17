const mongoose = require('mongoose');

const destinationSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, 'A destination must have a name'],
      unique: true,
      trim: true,
    },
    country: {
      type: String,
      required: [true, 'A destination must have a country'],
    },
    description: {
      type: String,
      trim: true,
    },
    coordinates: {
      lat: {
        type: Number,
        required: [true, 'A destination must have latitude coordinates'],
      },
      lng: {
        type: Number,
        required: [true, 'A destination must have longitude coordinates'],
      },
    },
    images: [String],
    popularActivities: [
      {
        name: String,
        description: String,
        category: {
          type: String,
          enum: [
            'sightseeing',
            'adventure',
            'cultural',
            'food',
            'nightlife',
            'shopping',
            'relaxation',
            'nature',
            'sport',
            'family',
          ],
        },
        averagePrice: Number,
        popularity: {
          type: Number,
          min: 1,
          max: 10,
          default: 5,
        },
      },
    ],
    bestTimeToVisit: [
      {
        month: {
          type: String,
          enum: [
            'January',
            'February',
            'March',
            'April',
            'May',
            'June',
            'July',
            'August',
            'September',
            'October',
            'November',
            'December',
          ],
        },
        reason: String,
        weatherSummary: String,
        temperature: {
          min: Number,
          max: Number,
          unit: {
            type: String,
            enum: ['C', 'F'],
            default: 'C',
          },
        },
        precipitation: {
          type: Number, // in mm
          default: 0,
        },
      },
    ],
    costIndex: {
      type: Number,
      min: 1,
      max: 10,
      default: 5,
      description: '1 is very cheap, 10 is very expensive',
    },
    safetyIndex: {
      type: Number,
      min: 1,
      max: 10,
      default: 5,
      description: '1 is very unsafe, 10 is very safe',
    },
    languages: [String],
    currency: String,
    timeZone: String,
    visaRequirements: {
      type: String,
      enum: ['not_required', 'on_arrival', 'required', 'electronic'],
      default: 'required',
    },
    ratings: {
      overall: {
        type: Number,
        min: 1,
        max: 5,
        default: 4,
      },
      food: {
        type: Number,
        min: 1,
        max: 5,
        default: 4,
      },
      accommodation: {
        type: Number,
        min: 1,
        max: 5,
        default: 4,
      },
      transportation: {
        type: Number,
        min: 1,
        max: 5,
        default: 4,
      },
      activities: {
        type: Number,
        min: 1,
        max: 5,
        default: 4,
      },
      safety: {
        type: Number,
        min: 1,
        max: 5,
        default: 4,
      },
    },
    travelTips: [String],
    averageCosts: {
      hotel: Number, // per night
      hostel: Number, // per night
      meal: {
        budget: Number,
        midRange: Number,
        luxury: Number,
      },
      transportation: {
        publicTransport: Number, // per trip
        taxi: Number, // per km
        rentalCar: Number, // per day
      },
    },
  },
  {
    timestamps: true,
    toJSON: { virtuals: true },
    toObject: { virtuals: true },
  }
);

// Index for geospatial queries
destinationSchema.index({ coordinates: '2dsphere' });

// Index for text search
destinationSchema.index({ name: 'text', description: 'text', country: 'text' });

const Destination = mongoose.model('Destination', destinationSchema);

module.exports = Destination; 