import streamlit as st
import numpy as np
import joblib

# Set page configuration for better accessibility and a cleaner look
st.set_page_config(
    page_title="Smart Sprinkler System Predictor",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Load the trained model
try:
    model = joblib.load("C:\\Users\\anush\\Downloads\\AICTE\\Farm_Irrigation_System.pkl")
except FileNotFoundError:
    st.error("Error: The model file 'Farm_Irrigation_System.pkl' was not found. Please make sure it's in the same directory.")
    st.stop()

# ---
# Title and description
# ---
st.title("Smart Sprinkler System Predictor")
st.markdown("""
Welcome to the Smart Sprinkler System! This application uses a machine learning model to predict the optimal status of farm sprinklers based on sensor data.
Please adjust the slider for each sensor to simulate the current soil moisture and environmental conditions.
""")
st.info("Instructions: Adjust the sliders for each of the 20 sensors (from 0.0 to 1.0) and then click the 'Predict Sprinklers' button.")

# ---
# User input section
# ---
st.subheader("Sensor Inputs")
st.markdown("Use the sliders below to input the scaled sensor values.")

# Revert to a single column for sliders as per user request
sensor_values = []
for i in range(20):
    val = st.slider(
        f"Sensor {i+1}",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.01,
        help=f"Scaled value for sensor {i+1}"
    )
    sensor_values.append(val)

# ---
# Prediction section
# ---
st.markdown("---")
st.subheader("Prediction")
if st.button("Predict Sprinklers", type="primary"):
    # Reshape the sensor values for the model
    input_array = np.array(sensor_values).reshape(1, -1)
    
    # Make a prediction
    try:
        prediction = model.predict(input_array)[0]
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
        st.stop()

    st.success("Prediction complete!")
    
    # Display the results in a structured way
    results_container = st.container()
    with results_container:
        st.write("---")
        st.markdown("### Sprinkler Status Prediction:")
        
        # Display the results without using columns
        for i, status in enumerate(prediction):
            sprinkler_name = f"Sprinkler {i+1}"
            status_text = "ON" if status == 1 else "OFF"
            st.metric(label=sprinkler_name, value=status_text)

st.markdown("---")
# ---
# Footer
# ---
st.markdown("""
<div style='text-align: center; padding: 20px; border-top: 1px solid #ddd;'>
    <p style='font-size: 1.2em;'>This is an AICTE PROJECT by Anushka Agarwal.</p>
</div>
""", unsafe_allow_html=True)