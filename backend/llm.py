import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3.8-flash")


def generate_summary(data):
    prompt = f"""
    Create a short neighborhood summary.

    Neighborhood: {data['name']}
    Parks: {data['parks']}
    Libraries: {data['libraries']}
    Community Centers: {data['centers']}
    Transit Score: {data['transit']}
    Population Density: {data['population']}
    Wellness Score: {data['wellness']}

    Keep it under 5 sentences.
    """

    response = model.generate_content(prompt)

    return response.text