from django.shortcuts import render
import requests
from django.views.decorators.cache import never_cache

from accounts.decorators import farmer_required
#ML model 
import os
import joblib
import pandas as pd
from .models import PredictionReport


# Load Saved Models
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

model_path = os.path.join(
    BASE_DIR,
    'ml_model/models/crop_model.pkl'
)

encoder_crop_path = os.path.join(
    BASE_DIR,
    'ml_model/models/encoder_crop.pkl'
)

encoder_soil_path = os.path.join(
    BASE_DIR,
    'ml_model/models/encoder_soil.pkl'
)

encoder_season_path = os.path.join(
    BASE_DIR,
    'ml_model/models/encoder_season.pkl'
)

encoder_result_path = os.path.join(
    BASE_DIR,
    'ml_model/models/encoder_result.pkl'
)


# Load Files

model = joblib.load(model_path)

encoder_crop = joblib.load(encoder_crop_path)

encoder_soil = joblib.load(encoder_soil_path)

encoder_season = joblib.load(encoder_season_path)

encoder_result = joblib.load(encoder_result_path)


# Home Page
def about(request):

    return render(request, 'about.html')

def home(request):

    return render(request, 'home.html')

@never_cache
@farmer_required
def soil_scan(request):

    return render(request, 'soil_scan.html')


# Protected Pages

@never_cache
@farmer_required
def prediction(request):

    result = None

    if request.method == "POST":

        crop = request.POST.get('crop')

        soil = request.POST.get('soil')

        season = request.POST.get('season')

        land = request.POST.get('land')


        # Season Weather Mapping

        if season == "June to October":

            temperature = 30

            humidity = 80

            rainfall = 220

        elif season == "October to March":

            temperature = 22

            humidity = 45

            rainfall = 40

        else:

            temperature = 38

            humidity = 30

            rainfall = 20


        # Encode Inputs

        crop_encoded = encoder_crop.transform([crop])[0]

        soil_encoded = encoder_soil.transform([soil])[0]

        season_encoded = encoder_season.transform([season])[0]


        # Create Input Data

        input_data = pd.DataFrame([{

            'crop': crop_encoded,

            'soil': soil_encoded,

            'season': season_encoded,

            'temperature': temperature,

            'humidity': humidity,

            'rainfall': rainfall
        }])


        # ML Prediction

        prediction = model.predict(input_data)[0]


        # Decode Prediction

        final_prediction = encoder_result.inverse_transform(

            [prediction]

        )[0]


        # Irrigation Advice

        if rainfall > 200:

            irrigation = "Low Irrigation Needed"

        elif rainfall > 50:

            irrigation = "Moderate Irrigation Needed"

        else:

            irrigation = "High Irrigation Needed"
        

        PredictionReport.objects.create(

            farmer_phone=request.session.get('farmer_phone'),

            crop=crop,

            soil=soil,

            season=season,

            prediction=final_prediction,

            irrigation=irrigation
        )

        result = {

            'prediction': final_prediction,

            'irrigation': irrigation,

            'temperature': temperature,

            'humidity': humidity,

            'rainfall': rainfall
        }
        

    return render(request, 'prediction.html', {

        'result': result
    })


@never_cache
@farmer_required
def weather(request):
    weather_data = None

    error = None

    if request.method == "POST":

        city = request.POST.get('city')

        api_key = "e039e610e3317fef701ba02bb3d0a256"

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}&units=metric"

        response = requests.get(url)

        data = response.json()

        print(data)

        if response.status_code == 200:

            weather_data = {

                'city': city,

                'temperature': data['main']['temp'],

                'humidity': data['main']['humidity'],

                'wind_speed': data['wind']['speed'],

                'description': data['weather'][0]['description'],
            }

        else:

            error = "City not found or API issue"

    return render(request, 'weather.html', {

        'weather_data': weather_data,

        'error': error
    })

@never_cache
@farmer_required
def irrigation(request):

    result = None

    if request.method == "POST":

        crop = request.POST.get('crop')

        season = request.POST.get('season')


        # Seasonal Weather Mapping

        if season == "June to October":

            temperature = 30

            humidity = 80

            rainfall = 220

        elif season == "October to March":

            temperature = 22

            humidity = 45

            rainfall = 40

        else:

            temperature = 38

            humidity = 30

            rainfall = 20


        # Irrigation Logic

        if rainfall > 200:

            irrigation_days = "Irrigate every 5-6 days"

        elif rainfall > 50:

            irrigation_days = "Irrigate every 3-4 days"

        else:

            irrigation_days = "Irrigate every 1-2 days"


        result = {

            'crop': crop,

            'temperature': temperature,

            'humidity': humidity,

            'rainfall': rainfall,

            'irrigation_days': irrigation_days
        }

    return render(request, 'irrigation.html', {

        'result': result
    })





@never_cache
@farmer_required
def manual_soil(request):

    recommendation = None

    selected_soil = None

    if request.method == "POST":

        selected_soil = request.POST.get('soil')

        soil_data = {

            'Black Soil': {

                'crops': 'Cotton, Soybean, Wheat',

                'fertilizer': 'Nitrogen Rich Fertilizer',

                'irrigation': 'Moderate Water Required'
            },

            'Red Soil': {

                'crops': 'Groundnut, Millets, Potato',

                'fertilizer': 'Compost and Phosphorus',

                'irrigation': 'Regular Irrigation Required'
            },

            'Alluvial Soil': {

                'crops': 'Rice, Sugarcane, Wheat',

                'fertilizer': 'Potassium and Organic Compost',

                'irrigation': 'High Water Requirement'
            },

            'Sandy Soil': {

                'crops': 'Watermelon, Coconut, Groundnut',

                'fertilizer': 'Organic Matter Compost',

                'irrigation': 'Frequent Irrigation Required'
            },

            'Clay Soil': {

                'crops': 'Rice, Lettuce, Chard',

                'fertilizer': 'Organic Compost',

                'irrigation': 'Slow Irrigation Needed'
            },

            'Loamy Soil': {

                'crops': 'Tomato, Wheat, Pulses',

                'fertilizer': 'Balanced Fertilizer',

                'irrigation': 'Moderate Irrigation'
            }
        }

        recommendation = soil_data.get(selected_soil)

    return render(request, 'manual_soil.html', {

        'recommendation': recommendation,

        'selected_soil': selected_soil
    })

@never_cache
@farmer_required
@farmer_required
def reports(request):

    farmer_phone = request.session.get('farmer_phone')

    reports = PredictionReport.objects.filter(

        farmer_phone=farmer_phone

    ).order_by('-created_at')

    return render(request, 'reports.html', {

        'reports': reports
    })