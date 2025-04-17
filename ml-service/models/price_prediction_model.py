import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

class PricePredictionModel:
    def __init__(self):
        # In a real implementation, we would load:
        # - A pre-trained price prediction model
        # - Historical price data for different destinations
        self.destinations = self._load_sample_destinations()
        
    def _load_sample_destinations(self):
        """Load sample destination data with price information for demo purposes."""
        sample_data = {
            "Paris": {
                "base_hotel_price": 200,
                "base_hostel_price": 50,
                "base_apartment_price": 150,
                "seasonal_multipliers": {
                    "spring": 1.2,  # Higher in spring
                    "summer": 1.5,  # Peak in summer
                    "fall": 1.0,    # Normal in fall
                    "winter": 0.8   # Lower in winter (except holidays)
                },
                "weekend_multiplier": 1.3,
                "holiday_multiplier": 1.7
            },
            "Bali": {
                "base_hotel_price": 100,
                "base_hostel_price": 20,
                "base_apartment_price": 80,
                "seasonal_multipliers": {
                    "spring": 1.0,
                    "summer": 1.2,
                    "fall": 0.8,
                    "winter": 1.3  # Higher in winter (northern hemisphere winter)
                },
                "weekend_multiplier": 1.2,
                "holiday_multiplier": 1.5
            },
            "New York City": {
                "base_hotel_price": 300,
                "base_hostel_price": 80,
                "base_apartment_price": 250,
                "seasonal_multipliers": {
                    "spring": 1.2,
                    "summer": 1.0,
                    "fall": 1.4,  # Peak in fall
                    "winter": 0.9  # Except during holidays
                },
                "weekend_multiplier": 1.1,
                "holiday_multiplier": 1.6
            },
            "Tokyo": {
                "base_hotel_price": 180,
                "base_hostel_price": 40,
                "base_apartment_price": 120,
                "seasonal_multipliers": {
                    "spring": 1.5,  # Cherry blossom season
                    "summer": 1.0,
                    "fall": 1.3,  # Autumn colors
                    "winter": 0.8
                },
                "weekend_multiplier": 1.1,
                "holiday_multiplier": 1.4
            },
            "Santorini": {
                "base_hotel_price": 220,
                "base_hostel_price": 60,
                "base_apartment_price": 180,
                "seasonal_multipliers": {
                    "spring": 1.0,
                    "summer": 1.8,  # Very high in summer
                    "fall": 1.0,
                    "winter": 0.6  # Low season
                },
                "weekend_multiplier": 1.2,
                "holiday_multiplier": 1.5
            }
        }
        return sample_data
    
    def _get_season(self, date):
        """Determine the season based on the date."""
        month = date.month
        if 3 <= month <= 5:
            return "spring"
        elif 6 <= month <= 8:
            return "summer"
        elif 9 <= month <= 11:
            return "fall"
        else:
            return "winter"
    
    def _is_weekend(self, date):
        """Check if the date is a weekend."""
        return date.weekday() >= 5  # 5 and 6 are Saturday and Sunday
    
    def _is_holiday(self, date):
        """Check if the date is a holiday (simplified)."""
        # This is a simplified implementation
        # In a real model, we would use a holiday API or database
        holidays = [
            (1, 1),   # New Year's Day
            (7, 4),   # Independence Day (US)
            (12, 25), # Christmas
            # Add more holidays as needed
        ]
        return (date.month, date.day) in holidays
    
    def _add_noise(self, price, variance_percent=5):
        """Add some random noise to the price to simulate real-world variability."""
        noise_factor = 1 + (random.random() * 2 - 1) * (variance_percent / 100)
        return price * noise_factor
    
    def _calculate_price_trend(self, base_date, target_date):
        """Calculate price trend based on proximity to the target date."""
        # Prices typically increase as the date approaches
        days_difference = (target_date - base_date).days
        if days_difference <= 7:
            return 1.2  # Last minute bookings
        elif days_difference <= 30:
            return 1.1  # One month ahead
        elif days_difference <= 90:
            return 0.9  # Three months ahead (good deals)
        else:
            return 1.0  # Far ahead
    
    def predict(self, destination, dates, accommodation_type='hotel'):
        """Predict accommodation prices for a destination on given dates."""
        if destination not in self.destinations:
            return {
                "error": f"Destination '{destination}' not found in the database."
            }
        
        dest_data = self.destinations[destination]
        
        # Get base price according to accommodation type
        if accommodation_type == 'hotel':
            base_price = dest_data["base_hotel_price"]
        elif accommodation_type == 'hostel':
            base_price = dest_data["base_hostel_price"]
        elif accommodation_type == 'apartment':
            base_price = dest_data["base_apartment_price"]
        else:
            base_price = dest_data["base_hotel_price"]  # Default to hotel
        
        # Parse dates
        try:
            check_in = datetime.strptime(dates.get("check_in", ""), "%Y-%m-%d")
            check_out = datetime.strptime(dates.get("check_out", ""), "%Y-%m-%d")
        except ValueError:
            return {
                "error": "Invalid date format. Please use YYYY-MM-DD."
            }
        
        if check_out <= check_in:
            return {
                "error": "Check-out date must be after check-in date."
            }
        
        # Calculate number of nights
        num_nights = (check_out - check_in).days
        
        # Get today's date for price trend calculation
        today = datetime.now().date()
        
        # Calculate prices for each day
        daily_prices = []
        current_date = check_in
        while current_date < check_out:
            season = self._get_season(current_date)
            seasonal_multiplier = dest_data["seasonal_multipliers"][season]
            
            # Apply weekend multiplier if applicable
            weekend_multiplier = dest_data["weekend_multiplier"] if self._is_weekend(current_date) else 1.0
            
            # Apply holiday multiplier if applicable
            holiday_multiplier = dest_data["holiday_multiplier"] if self._is_holiday(current_date) else 1.0
            
            # Apply price trend based on how far in advance the booking is
            trend_multiplier = self._calculate_price_trend(today, current_date.date())
            
            # Calculate daily price
            daily_price = base_price * seasonal_multiplier * weekend_multiplier * holiday_multiplier * trend_multiplier
            
            # Add some random noise to simulate real-world variability
            daily_price = self._add_noise(daily_price)
            
            daily_prices.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "price": round(daily_price, 2)
            })
            
            current_date += timedelta(days=1)
        
        # Calculate total and average prices
        total_price = sum(item["price"] for item in daily_prices)
        average_price = total_price / num_nights
        
        return {
            "destination": destination,
            "accommodation_type": accommodation_type,
            "check_in": dates.get("check_in"),
            "check_out": dates.get("check_out"),
            "num_nights": num_nights,
            "daily_prices": daily_prices,
            "total_price": round(total_price, 2),
            "average_price": round(average_price, 2),
            "currency": "USD"
        } 