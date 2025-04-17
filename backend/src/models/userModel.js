const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const validator = require('validator');

const userSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, 'Please provide your name'],
      trim: true,
    },
    email: {
      type: String,
      required: [true, 'Please provide your email'],
      unique: true,
      lowercase: true,
      validate: [validator.isEmail, 'Please provide a valid email'],
    },
    password: {
      type: String,
      required: [true, 'Please provide a password'],
      minlength: 8,
      select: false,
    },
    preferences: {
      travelStyles: {
        type: [String],
        enum: ['adventure', 'beach', 'cultural', 'eco-friendly', 'family', 'luxury', 'budget'],
        default: [],
      },
      activities: {
        type: [String],
        default: [],
      },
      accommodationTypes: {
        type: [String],
        enum: ['hotel', 'hostel', 'apartment', 'resort', 'camping', 'villa'],
        default: [],
      },
      budgetRange: {
        min: {
          type: Number,
          default: 0,
        },
        max: {
          type: Number,
          default: 10000,
        },
      },
      seasonalPreferences: {
        type: [String],
        enum: ['spring', 'summer', 'fall', 'winter'],
        default: [],
      },
    },
    travelHistory: [
      {
        destination: {
          type: String,
          required: true,
        },
        startDate: Date,
        endDate: Date,
        rating: {
          type: Number,
          min: 1,
          max: 5,
        },
      },
    ],
  },
  {
    timestamps: true,
  }
);

// Hash the password before saving
userSchema.pre('save', async function (next) {
  if (!this.isModified('password')) return next();

  this.password = await bcrypt.hash(this.password, 12);
  next();
});

// Check if password is correct
userSchema.methods.correctPassword = async function (candidatePassword, userPassword) {
  return await bcrypt.compare(candidatePassword, userPassword);
};

const User = mongoose.model('User', userSchema);

module.exports = User; 