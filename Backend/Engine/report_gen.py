import openai
from config import OPENAI_API_KEY, MODEL_NAME
openai.api_key = OPENAI_API_KEY

def generate_threat_report(anomalies_df):
    prompt = (
        "You are a cybersecurity analyst. Based on the following anomalies, "
        "generate a concise summary and recommendations:\n\n"
        + anomalies_df.to_string(index=False)
    )
    resp = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a cybersecurity threat analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return resp['choices'][0]['message']['content']
