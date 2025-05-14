import requests
import json
import sys

def get_best_learning_path(api_url, learner_email, learning_goals, knowledge_base):
    """
    Call the API to get the best learning path and transform the response
    to use simplified lo_id values (just the numerical part at the end).
    """
    url = f"{api_url.rstrip('/')}/api/selection/best-path"
    
    payload = {
        "learner_email": learner_email,
        "learning_goals": learning_goals,
        "knowledge_base": knowledge_base
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print(f"Sending request to: {url}")
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        
        data = response.json()
        
        # Transform the lo_id values to just use the numerical part
        for lo in data.get("learning_objects", []):
            if "lo_id" in lo and ":" in lo["lo_id"]:
                lo["lo_id"] = lo["lo_id"].split(":")[-1]
                
        return data
    
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
        return None

def main():
    # Default values
    api_url = "https://iia-git-master-tarek-saads-projects.vercel.app"
    learner_email = "kareem@example.com"
    learning_goals = ["Searching"]
    knowledge_base = ["Introduction to Programming"]
    
    # Get the result from the API and transform it
    result = get_best_learning_path(api_url, learner_email, learning_goals, knowledge_base)
    
    if result:
        print("\nAPI Response with Simplified IDs:")
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main() 