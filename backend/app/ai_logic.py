import requests

def get_environmental_insight(greenery_percent, area):
    # Sarvam AI ka sahi endpoint aur structure
    url = "https://api.sarvam.ai/v1/chat/completions"
    
    headers = {
        "api-subscription-key": "sk_pi6eg7ws_bHq9Cz6UxP9Rw9jh8lFYpP6m",
        "Content-Type": "application/json"
    }
    
    # Prompt refine kiya hai taaki AI sahi format mein answer de
    prompt = f"The area {area} has {greenery_percent}% greenery. Analyze the environmental impact based on this data and suggest if there is a risk of urban heat island effect or need for reforestation. Keep the response concise."
    
    payload = {
        "model": "sarvam-30b", 
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers,timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # AI ka output yahan se nikalega
            return data['choices'][0]['message']['content']
        else:
            return f"Error {response.status_code}: {response.text}"
            
    except Exception as e:
        return f"Error: {str(e)}"