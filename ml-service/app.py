import os
from flask import Flask, request, jsonify
from flask_cors import CORS # type: ignore
from dotenv import load_dotenv # type: ignore

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# We're creating a simplified version without actual ML models
# but with dummy responses

@app.route('/')
def home():
    return jsonify({
        'status': 'success',
        'message': 'Trip Planner ML API is running (Simplified Version)'
    })

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    try:
        data = request.json
        user_preferences = data.get('preferences', {})
        travel_history = data.get('travelHistory', [])
        
        # Return dummy recommendations
        dummy_recommendations = [
            {
                'id': 1,
                'name': 'Paris',
                'country': 'France',
                'description': 'The City of Light',
                'similarity_score': 0.92,
                'cost_index': 8,
                'image_url': 'https://example.com/paris.jpg'
            },
            {
                'id': 2,
                'name': 'Bali',
                'country': 'Indonesia',
                'description': 'Island of the Gods',
                'similarity_score': 0.87,
                'cost_index': 5,
                'image_url': 'https://example.com/bali.jpg'
            },
            {
                'id': 3,
                'name': 'Tokyo',
                'country': 'Japan',
                'description': 'Where tradition meets future',
                'similarity_score': 0.81,
                'cost_index': 8,
                'image_url': 'https://example.com/tokyo.jpg'
            }
        ]
        
        return jsonify({
            'status': 'success',
            'data': dummy_recommendations
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/price-prediction', methods=['POST'])
def predict_prices():
    try:
        data = request.json
        destination = data.get('destination')
        dates = data.get('dates', {})
        accommodation_type = data.get('accommodationType', 'hotel')
        
        # Return dummy price prediction
        dummy_price_prediction = {
            "destination": destination or "Paris",
            "accommodation_type": accommodation_type,
            "check_in": dates.get("check_in", "2023-06-01"),
            "check_out": dates.get("check_out", "2023-06-05"),
            "num_nights": 4,
            "daily_prices": [
                {"date": "2023-06-01", "price": 185.50},
                {"date": "2023-06-02", "price": 185.50},
                {"date": "2023-06-03", "price": 225.75},
                {"date": "2023-06-04", "price": 225.75}
            ],
            "total_price": 822.50,
            "average_price": 205.63,
            "currency": "USD"
        }
        
        return jsonify({
            'status': 'success',
            'data': dummy_price_prediction
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/optimize-itinerary', methods=['POST'])
def optimize_itinerary():
    try:
        data = request.json
        destinations = data.get('destinations', [])
        preferences = data.get('preferences', {})
        constraints = data.get('constraints', {})
        
        # Return dummy itinerary optimization
        dummy_optimization = {
            "itinerary": [
                {
                    "destination": "Paris",
                    "daily_itineraries": [
                        {
                            "date": "2023-06-01",
                            "day_of_week": "Thursday",
                            "activities": [
                                {
                                    "id": "p1",
                                    "name": "Eiffel Tower",
                                    "description": "Iconic iron lattice tower",
                                    "category": "sightseeing",
                                    "start_time": "10:00",
                                    "end_time": "13:30",
                                    "cost": 25.0
                                },
                                {
                                    "id": "p2",
                                    "name": "Louvre Museum",
                                    "description": "World's largest art museum",
                                    "category": "cultural",
                                    "start_time": "14:30",
                                    "end_time": "18:30",
                                    "cost": 15.0
                                }
                            ]
                        }
                    ]
                }
            ],
            "summary": {
                "total_destinations": 1,
                "total_days": 1,
                "estimated_cost": 40.0
            }
        }
        
        return jsonify({
            'status': 'success',
            'data': dummy_optimization
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/weather-forecast', methods=['POST'])
def get_weather_forecast():
    try:
        data = request.json
        destination = data.get('destination')
        dates = data.get('dates', {})
        
        # Return dummy weather forecast
        forecast = {
            'destination': destination or "Paris",
            'forecast': [
                {
                    'date': '2023-06-01',
                    'temperature': {'min': 20, 'max': 28},
                    'precipitation': 10,
                    'weather_condition': 'sunny'
                },
                {
                    'date': '2023-06-02',
                    'temperature': {'min': 18, 'max': 25},
                    'precipitation': 30,
                    'weather_condition': 'partly_cloudy'
                }
            ]
        }
        
        return jsonify({
            'status': 'success',
            'data': forecast
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True) 