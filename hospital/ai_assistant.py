def analyze_health_data(patient_data):
    advice = []
    
    # Blood Pressure Analysis
    if patient_data.get('blood_pressure'):
        try:
            systolic, diastolic = map(int, patient_data['blood_pressure'].split('/'))
            if systolic > 140 or diastolic > 90:
                advice.append("Your blood pressure is high. Consider consulting a doctor and reducing salt intake.")
            elif systolic < 90 or diastolic < 60:
                advice.append("Your blood pressure is low. Stay hydrated and consider a check-up.")
        except ValueError:
            advice.append("Invalid blood pressure format. Please enter in '120/80' format.")

    # Heart Rate Analysis
    if patient_data.get('heart_rate'):
        heart_rate = int(patient_data['heart_rate'])
        if heart_rate > 100:
            advice.append("Your heart rate is high. Avoid caffeine and stress, and consult a doctor if persistent.")
        elif heart_rate < 60:
            advice.append("Your heart rate is low. Ensure you're eating properly and not over-exercising.")

    # Medical History-Based Suggestions
    if patient_data.get('medical_history'):
        advice.append(f"Since you have a history of {patient_data['medical_history']}, consider regular check-ups.")

    # Allergy-Based Recommendations
    if patient_data.get('allergies'):
        advice.append(f"Avoid known allergens like {patient_data['allergies']}, and always carry necessary medication.")

    if not advice:
        advice.append("Your health data seems normal, but regular check-ups are important.")

    return advice
