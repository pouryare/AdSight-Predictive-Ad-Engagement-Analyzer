import streamlit as st
import requests

# Hard-coded variables
API_KEY = "<Enter your API Key>"
API_ENDPOINT = "https://eu-de.ml.cloud.ibm.com/ml/v4/deployments/xxxx"
IAM_URL = "https://iam.cloud.ibm.com/identity/token"

def get_ibm_token(api_key: str) -> str:
    """Retrieve IBM Cloud authentication token."""
    token_response = requests.post(IAM_URL, data={
        "apikey": api_key,
        "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'
    })
    token_response.raise_for_status()
    return token_response.json()["access_token"]

def predict_ad_view(input_features: list, token: str) -> float:
    """Make a prediction using the IBM Watson API."""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    payload = {
        "input_data": [{
            "fields": [
                "daily_time", "age", "areaincome", "dailyinternetuse", 
                "adtopicline", "city", "gender", "country", "timestamp"
            ],
            "values": input_features
        }]
    }
    response = requests.post(API_ENDPOINT, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()['predictions'][0]['values'][0][1][0]

def main():
    st.title('Advertisement Success Prediction')

    # Input fields
    daily_time = st.number_input('Enter Your Daily Time (minutes)', min_value=0.0)
    age = st.number_input('Enter Your Age', min_value=0, max_value=120)
    areaincome = st.number_input('Enter Your Area Income', min_value=0.0)
    dailyinternetuse = st.number_input('Enter Your Daily Internet Use (minutes)', min_value=0.0)
    adtopicline = st.text_input('Enter Advertisement Topic Line')
    city = st.text_input('Enter City')
    gender = st.selectbox('Enter Gender', ['Male', 'Female'])
    country = st.text_input('Enter Country Name')
    timestamp = st.text_input('Enter Timestamp (YYYY-MM-DD HH:MM:SS)')

    if st.button('Predict'):
        try:
            token = get_ibm_token(API_KEY)
            input_features = [[
                daily_time, age, areaincome, dailyinternetuse, 
                adtopicline, city, gender, country, timestamp
            ]]
            probability = predict_ad_view(input_features, token)
            
            if probability > 0.5:
                st.success("Based on the above factors, the user is likely to view the advertisement.")
            else:
                st.info("Based on the above factors, the user is unlikely to view the advertisement.")
            
            st.write(f"Probability of viewing: {probability:.2%}")

        except requests.RequestException as e:
            st.error(f"An error occurred while making the prediction: {str(e)}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()