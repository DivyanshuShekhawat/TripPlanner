const mongoose = require('mongoose');

const tripSchema = new mongoose.Schema(
  {
    user: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: true,
    },
    title: {
      type: String,
      required: [true, 'A trip must have a title'],
      trim: true,
    },
    description: {
      type: String,
      trim: true,
    },
    startDate: {
      type: Date,
      required: [true, 'A trip must have a start date'],
    },
    endDate: {
      type: Date,
      required: [true, 'A trip must have an end date'],
      validate: {
        validator: function (value) {
          return value > this.startDate;
        },
        message: 'End date must be after start date',
      },
    },
    destinations: [
      {
        location: {
          type: String,
          required: true,
        },
        coordinates: {
          lat: Number,
          lng: Number,
        },
        startDate: Date,
        endDate: Date,
        accommodations: [
          {
            name: String,
            address: String,
            price: Number,
            bookingUrl: String,
            checkIn: Date,
            checkOut: Date,
          },
        ],
        activities: [
          {
            name: String,
            description: String,
            date: Date,
            duration: Number, // in minutes
            price: Number,
            location: String,
            coordinates: {
              lat: Number,
              lng: Number,
            },
            bookingUrl: String,
          },
        ],
        transportation: [
          {
            type: {
              type: String,
              enum: ['flight', 'train', 'bus', 'car', 'ferry', 'other'],
            },
            departureTime: Date,
            arrivalTime: Date,
            departureLocation: String,
            arrivalLocation: String,
            provider: String,
            price: Number,
            bookingReference: String,
            bookingUrl: String,
          },
        ],
      },
    ],
    budget: {
      currency: {
        type: String,
        default: 'USD',
      },
      total: {
        type: Number,
        default: 0,
      },
      spent: {
        type: Number,
        default: 0,
      },
      categories: {
        accommodation: {
          type: Number,
          default: 0,
        },
        transportation: {
          type: Number,
          default: 0,
        },
        food: {
          type: Number,
          default: 0,
        },
        activities: {
          type: Number,
          default: 0,
        },
        shopping: {
          type: Number,
          default: 0,
        },
        other: {
          type: Number,
          default: 0,
        },
      },
    },
    notes: [
      {
        title: String,
        content: String,
        date: {
          type: Date,
          default: Date.now,
        },
      },
    ],
    isPublic: {
      type: Boolean,
      default: false,
    },
  },
  {
    timestamps: true,
    toJSON: { virtuals: true },
    toObject: { virtuals: true },
  }
);

// Virtual property for trip duration in days
tripSchema.virtual('duration').get(function () {
  return Math.ceil((this.endDate - this.startDate) / (1000 * 60 * 60 * 24));
});

// Pre-save middleware to update budget totals
tripSchema.pre('save', function (next) {
  let accommodationTotal = 0;
  let transportationTotal = 0;
  let activitiesTotal = 0;

  this.destinations.forEach((destination) => {
    // Calculate accommodation costs
    destination.accommodations.forEach((accommodation) => {
      accommodationTotal += accommodation.price || 0;
    });

    // Calculate transportation costs
    destination.transportation.forEach((transport) => {
      transportationTotal += transport.price || 0;
    });

    // Calculate activities costs
    destination.activities.forEach((activity) => {
      activitiesTotal += activity.price || 0;
    });
  });

  // Update budget categories
  this.budget.categories.accommodation = accommodationTotal;
  this.budget.categories.transportation = transportationTotal;
  this.budget.categories.activities = activitiesTotal;

  // Update total spent
  this.budget.spent =
    accommodationTotal +
    transportationTotal +
    activitiesTotal +
    this.budget.categories.food +
    this.budget.categories.shopping +
    this.budget.categories.other;

  next();
});

const Trip = mongoose.model('Trip', tripSchema);

module.exports = Trip; 