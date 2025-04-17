import numpy as np
import datetime
import random
import math

class ItineraryOptimizer:
    def __init__(self):
        # In a real implementation, we would load:
        # - POI (Points of Interest) data for different destinations
        # - Travel time/distance matrices between POIs
        # - User preference models
        self.activities = self._load_sample_activities()
        
    def _load_sample_activities(self):
        """Load sample activity data for demo purposes."""
        sample_data = {
            "Paris": [
                {
                    "id": "p1",
                    "name": "Eiffel Tower",
                    "description": "Iconic iron lattice tower",
                    "category": "sightseeing",
                    "popularity": 9.5,
                    "duration": 180,  # minutes
                    "cost": 25.0,
                    "coordinates": {"lat": 48.8584, "lng": 2.2945},
                    "open_time": "09:00",
                    "close_time": "23:00",
                    "best_time_of_day": "sunset",
                    "crowd_level": {
                        "morning": "medium",
                        "afternoon": "high",
                        "evening": "high"
                    }
                },
                {
                    "id": "p2",
                    "name": "Louvre Museum",
                    "description": "World's largest art museum",
                    "category": "cultural",
                    "popularity": 9.0,
                    "duration": 240,  # minutes
                    "cost": 15.0,
                    "coordinates": {"lat": 48.8606, "lng": 2.3376},
                    "open_time": "09:00",
                    "close_time": "18:00",
                    "best_time_of_day": "morning",
                    "crowd_level": {
                        "morning": "medium",
                        "afternoon": "high",
                        "evening": "low"
                    }
                },
                {
                    "id": "p3",
                    "name": "Notre-Dame Cathedral",
                    "description": "Medieval Catholic cathedral",
                    "category": "cultural",
                    "popularity": 8.5,
                    "duration": 120,  # minutes
                    "cost": 0.0,
                    "coordinates": {"lat": 48.8530, "lng": 2.3499},
                    "open_time": "08:00",
                    "close_time": "19:00",
                    "best_time_of_day": "morning",
                    "crowd_level": {
                        "morning": "low",
                        "afternoon": "medium",
                        "evening": "low"
                    }
                },
                {
                    "id": "p4",
                    "name": "Montmartre",
                    "description": "Bohemian district with Sacré-Cœur Basilica",
                    "category": "cultural",
                    "popularity": 8.0,
                    "duration": 180,  # minutes
                    "cost": 0.0,
                    "coordinates": {"lat": 48.8867, "lng": 2.3431},
                    "open_time": "00:00",
                    "close_time": "23:59",
                    "best_time_of_day": "evening",
                    "crowd_level": {
                        "morning": "low",
                        "afternoon": "medium",
                        "evening": "medium"
                    }
                },
                {
                    "id": "p5",
                    "name": "Seine River Cruise",
                    "description": "Boat tour along the Seine River",
                    "category": "relaxation",
                    "popularity": 7.5,
                    "duration": 120,  # minutes
                    "cost": 15.0,
                    "coordinates": {"lat": 48.8599, "lng": 2.3408},
                    "open_time": "10:00",
                    "close_time": "22:00",
                    "best_time_of_day": "evening",
                    "crowd_level": {
                        "morning": "low",
                        "afternoon": "medium",
                        "evening": "high"
                    }
                }
            ],
            "Bali": [
                {
                    "id": "b1",
                    "name": "Uluwatu Temple",
                    "description": "Ancient sea temple perched on a cliff",
                    "category": "cultural",
                    "popularity": 8.5,
                    "duration": 120,  # minutes
                    "cost": 5.0,
                    "coordinates": {"lat": -8.8291, "lng": 115.0849},
                    "open_time": "09:00",
                    "close_time": "19:00",
                    "best_time_of_day": "sunset",
                    "crowd_level": {
                        "morning": "low",
                        "afternoon": "medium",
                        "evening": "high"
                    }
                },
                {
                    "id": "b2",
                    "name": "Ubud Monkey Forest",
                    "description": "Natural sanctuary with macaques",
                    "category": "nature",
                    "popularity": 8.0,
                    "duration": 120,  # minutes
                    "cost": 8.0,
                    "coordinates": {"lat": -8.5188, "lng": 115.2582},
                    "open_time": "08:30",
                    "close_time": "18:00",
                    "best_time_of_day": "morning",
                    "crowd_level": {
                        "morning": "medium",
                        "afternoon": "high",
                        "evening": "low"
                    }
                },
                {
                    "id": "b3",
                    "name": "Tegallalang Rice Terraces",
                    "description": "Stunning rice paddies",
                    "category": "nature",
                    "popularity": 7.5,
                    "duration": 120,  # minutes
                    "cost": 2.0,
                    "coordinates": {"lat": -8.4310, "lng": 115.2772},
                    "open_time": "07:00",
                    "close_time": "18:00",
                    "best_time_of_day": "morning",
                    "crowd_level": {
                        "morning": "low",
                        "afternoon": "medium",
                        "evening": "low"
                    }
                }
            ]
        }
        return sample_data
    
    def _haversine_distance(self, lat1, lon1, lat2, lon2):
        """Calculate the great-circle distance between two points."""
        # Convert latitude and longitude from degrees to radians
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)
        
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371  # Radius of earth in kilometers
        
        return c * r
    
    def _estimate_travel_time(self, lat1, lon1, lat2, lon2, mode="walking"):
        """Estimate travel time between two points in minutes."""
        distance = self._haversine_distance(lat1, lon1, lat2, lon2)
        
        # Rough estimates of travel speeds
        speeds = {
            "walking": 5,       # km/h
            "public_transit": 20,  # km/h
            "car": 30           # km/h
        }
        
        speed = speeds.get(mode, speeds["walking"])
        time_hours = distance / speed
        return time_hours * 60  # Convert to minutes
    
    def _filter_activities_by_preferences(self, activities, preferences):
        """Filter activities based on user preferences."""
        filtered_activities = []
        
        # Filter by categories
        preferred_categories = preferences.get('categories', [])
        
        for activity in activities:
            # Skip if category doesn't match (if preferences specified)
            if preferred_categories and activity['category'] not in preferred_categories:
                continue
                
            # Calculate a preference score (higher is better match)
            score = activity['popularity']
            
            # Adjust score based on user preferences
            if activity['category'] in preferred_categories:
                score += 2
                
            # Add activity with its score
            filtered_activities.append({
                **activity,
                'preference_score': score
            })
        
        # Sort by preference score
        return sorted(filtered_activities, key=lambda x: x['preference_score'], reverse=True)
    
    def _create_daily_itinerary(self, activities, start_time, end_time, current_location=None):
        """Create a daily itinerary from available activities."""
        schedule = []
        current_time = datetime.datetime.strptime(start_time, "%H:%M")
        end_datetime = datetime.datetime.strptime(end_time, "%H:%M")
        
        # Start with current location or default
        if current_location is None:
            current_location = {"lat": activities[0]["coordinates"]["lat"], 
                                "lng": activities[0]["coordinates"]["lng"]}
        
        # Copy the activities list so we can remove items
        available_activities = activities.copy()
        
        while available_activities and current_time < end_datetime:
            best_activity = None
            best_score = -float('inf')
            
            for activity in available_activities:
                # Skip if activity is closed at current time
                activity_open = datetime.datetime.strptime(activity["open_time"], "%H:%M")
                activity_close = datetime.datetime.strptime(activity["close_time"], "%H:%M")
                
                if not (activity_open.time() <= current_time.time() <= activity_close.time()):
                    continue
                
                # Calculate travel time to this activity
                travel_time = self._estimate_travel_time(
                    current_location["lat"], current_location["lng"],
                    activity["coordinates"]["lat"], activity["coordinates"]["lng"]
                )
                
                # Check if we have enough time for travel + activity + buffer
                total_time_needed = travel_time + activity["duration"] + 30  # 30 min buffer
                activity_end_time = current_time + datetime.timedelta(minutes=total_time_needed)
                
                if activity_end_time.time() > end_datetime.time():
                    continue
                
                # Calculate a score based on preference score and travel time
                time_penalty = travel_time / 30  # Penalty for longer travel
                score = activity["preference_score"] - time_penalty
                
                # Adjust score based on best time of day
                time_of_day = "morning"
                if current_time.hour >= 12 and current_time.hour < 17:
                    time_of_day = "afternoon"
                elif current_time.hour >= 17:
                    time_of_day = "evening"
                
                if activity["best_time_of_day"] == time_of_day:
                    score += 1
                
                # Adjust score based on crowd level (prefer less crowded times)
                crowd_level = activity["crowd_level"][time_of_day]
                if crowd_level == "low":
                    score += 0.5
                elif crowd_level == "high":
                    score -= 0.5
                
                if score > best_score:
                    best_score = score
                    best_activity = {
                        **activity,
                        "travel_time": travel_time,
                        "start_time": current_time.strftime("%H:%M"),
                        "end_time": activity_end_time.strftime("%H:%M")
                    }
            
            if best_activity:
                schedule.append(best_activity)
                
                # Update current location and time
                current_location = best_activity["coordinates"]
                current_time = datetime.datetime.strptime(best_activity["end_time"], "%H:%M")
                
                # Remove activity from available list
                available_activities = [a for a in available_activities if a["id"] != best_activity["id"]]
            else:
                # No suitable activity found, advance time by 30 minutes
                current_time += datetime.timedelta(minutes=30)
        
        return schedule
    
    def optimize(self, destinations, preferences, constraints):
        """Optimize an itinerary based on destinations, preferences, and constraints."""
        itinerary = []
        
        for destination in destinations:
            destination_name = destination.get("location")
            if destination_name not in self.activities:
                continue
                
            # Get activities for this destination
            destination_activities = self.activities[destination_name]
            
            # Filter activities based on preferences
            filtered_activities = self._filter_activities_by_preferences(
                destination_activities, 
                preferences
            )
            
            # Get dates for this destination
            start_date = datetime.datetime.strptime(destination.get("startDate", ""), "%Y-%m-%d")
            end_date = datetime.datetime.strptime(destination.get("endDate", ""), "%Y-%m-%d")
            num_days = (end_date - start_date).days
            
            # Create daily itineraries
            daily_itineraries = []
            for day in range(num_days):
                current_date = start_date + datetime.timedelta(days=day)
                
                # Get start and end times from constraints or use defaults
                start_time = constraints.get("daily_start_time", "09:00")
                end_time = constraints.get("daily_end_time", "20:00")
                
                # Create daily schedule
                daily_schedule = self._create_daily_itinerary(
                    filtered_activities,
                    start_time,
                    end_time
                )
                
                daily_itineraries.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "day_of_week": current_date.strftime("%A"),
                    "activities": daily_schedule
                })
            
            # Add to overall itinerary
            itinerary.append({
                "destination": destination_name,
                "daily_itineraries": daily_itineraries
            })
        
        return {
            "itinerary": itinerary,
            "summary": {
                "total_destinations": len(itinerary),
                "total_days": sum(len(dest["daily_itineraries"]) for dest in itinerary),
                "estimated_cost": sum(
                    sum(activity["cost"] for activity in day["activities"])
                    for dest in itinerary
                    for day in dest["daily_itineraries"]
                )
            }
        } 