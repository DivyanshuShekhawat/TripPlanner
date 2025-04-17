import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import os
import json

class RecommendationModel:
    def __init__(self):
        # In a real implementation, we would load:
        # - A pre-trained recommendation model
        # - Dataset of destinations with features
        # - User similarity matrix
        self.destinations = self._load_sample_destinations()
        self.feature_columns = [
            'adventure', 'beach', 'cultural', 'eco_friendly', 
            'family', 'luxury', 'budget', 
            'spring', 'summer', 'fall', 'winter'
        ]
        
    def _load_sample_destinations(self):
        """Load sample destination data for demo purposes."""
        # In a real scenario, this would load from a database or CSV file
        sample_data = [
            {
                "id": 1,
                "name": "Paris",
                "country": "France",
                "description": "The City of Light",
                "adventure": 0.3,
                "beach": 0.0,
                "cultural": 0.9,
                "eco_friendly": 0.4,
                "family": 0.6,
                "luxury": 0.8,
                "budget": 0.3,
                "spring": 0.8,
                "summer": 0.7,
                "fall": 0.8,
                "winter": 0.5,
                "cost_index": 8,
                "image_url": "https://example.com/paris.jpg"
            },
            {
                "id": 2,
                "name": "Bali",
                "country": "Indonesia",
                "description": "Island of the Gods",
                "adventure": 0.7,
                "beach": 0.9,
                "cultural": 0.7,
                "eco_friendly": 0.6,
                "family": 0.7,
                "luxury": 0.7,
                "budget": 0.6,
                "spring": 0.6,
                "summer": 0.9,
                "fall": 0.7,
                "winter": 0.8,
                "cost_index": 5,
                "image_url": "https://example.com/bali.jpg"
            },
            {
                "id": 3,
                "name": "New York City",
                "country": "USA",
                "description": "The Big Apple",
                "adventure": 0.5,
                "beach": 0.2,
                "cultural": 0.9,
                "eco_friendly": 0.3,
                "family": 0.6,
                "luxury": 0.9,
                "budget": 0.2,
                "spring": 0.7,
                "summer": 0.8,
                "fall": 0.9,
                "winter": 0.6,
                "cost_index": 9,
                "image_url": "https://example.com/nyc.jpg"
            },
            {
                "id": 4,
                "name": "Tokyo",
                "country": "Japan",
                "description": "Where tradition meets future",
                "adventure": 0.6,
                "beach": 0.1,
                "cultural": 0.9,
                "eco_friendly": 0.5,
                "family": 0.7,
                "luxury": 0.8,
                "budget": 0.4,
                "spring": 0.9,
                "summer": 0.6,
                "fall": 0.8,
                "winter": 0.5,
                "cost_index": 8,
                "image_url": "https://example.com/tokyo.jpg"
            },
            {
                "id": 5,
                "name": "Santorini",
                "country": "Greece",
                "description": "Stunning island with white architecture",
                "adventure": 0.4,
                "beach": 0.9,
                "cultural": 0.7,
                "eco_friendly": 0.6,
                "family": 0.5,
                "luxury": 0.9,
                "budget": 0.3,
                "spring": 0.7,
                "summer": 0.9,
                "fall": 0.7,
                "winter": 0.3,
                "cost_index": 7,
                "image_url": "https://example.com/santorini.jpg"
            }
        ]
        return pd.DataFrame(sample_data)
    
    def _create_user_vector(self, user_preferences):
        """Create a feature vector from user preferences."""
        user_vector = np.zeros(len(self.feature_columns))
        
        # Convert user preferences to vector representation
        if 'travelStyles' in user_preferences:
            for style in user_preferences['travelStyles']:
                if style == 'adventure':
                    user_vector[0] = 1
                elif style == 'beach':
                    user_vector[1] = 1
                elif style == 'cultural':
                    user_vector[2] = 1
                elif style == 'eco-friendly':
                    user_vector[3] = 1
                elif style == 'family':
                    user_vector[4] = 1
                elif style == 'luxury':
                    user_vector[5] = 1
                elif style == 'budget':
                    user_vector[6] = 1
        
        # Add seasonal preferences
        if 'seasonalPreferences' in user_preferences:
            for season in user_preferences['seasonalPreferences']:
                if season == 'spring':
                    user_vector[7] = 1
                elif season == 'summer':
                    user_vector[8] = 1
                elif season == 'fall':
                    user_vector[9] = 1
                elif season == 'winter':
                    user_vector[10] = 1
                    
        return user_vector
    
    def _incorporate_travel_history(self, user_vector, travel_history):
        """Incorporate past travel history into user preferences."""
        # This is a simplified implementation
        # In a real model, we would use a more sophisticated approach
        if not travel_history:
            return user_vector
        
        # Get names of previously visited destinations
        visited_destinations = [item['destination'] for item in travel_history]
        
        # Find these destinations in our dataset
        visited_df = self.destinations[self.destinations['name'].isin(visited_destinations)]
        
        if not visited_df.empty:
            # Calculate average feature values from visited destinations
            history_vector = visited_df[self.feature_columns].mean().values
            
            # Blend current preferences with history (with more weight to explicit preferences)
            return 0.7 * user_vector + 0.3 * history_vector
        
        return user_vector
    
    def predict(self, user_preferences, travel_history=None):
        """Predict destination recommendations based on user preferences and history."""
        # Create user preference vector
        user_vector = self._create_user_vector(user_preferences)
        
        # Incorporate travel history if available
        if travel_history:
            user_vector = self._incorporate_travel_history(user_vector, travel_history)
        
        # Extract destination features
        destination_features = self.destinations[self.feature_columns].values
        
        # Calculate similarity between user preferences and destinations
        user_vector = user_vector.reshape(1, -1)
        similarities = cosine_similarity(user_vector, destination_features)[0]
        
        # Get budget constraints if provided
        min_budget = user_preferences.get('budgetRange', {}).get('min', 0)
        max_budget = user_preferences.get('budgetRange', {}).get('max', 10)
        
        # Filter by budget constraints
        budget_mask = (self.destinations['cost_index'] >= min_budget / 10 * 10) & \
                      (self.destinations['cost_index'] <= max_budget / 10 * 10)
        
        # Get top recommendations
        self.destinations['similarity'] = similarities
        filtered_destinations = self.destinations[budget_mask].sort_values('similarity', ascending=False)
        
        # Return top 5 recommendations
        top_recommendations = filtered_destinations.head(5)
        
        # Format results
        recommendations = []
        for _, row in top_recommendations.iterrows():
            recommendations.append({
                'id': int(row['id']),
                'name': row['name'],
                'country': row['country'],
                'description': row['description'],
                'similarity_score': float(row['similarity']),
                'cost_index': int(row['cost_index']),
                'image_url': row['image_url']
            })
        
        return recommendations 