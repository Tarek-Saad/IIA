from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# 🔐 Load environment variables from .env
load_dotenv()

token = os.getenv("AI_API_KEY")
endpoint = os.getenv("AI_BASE_URL")
model_name = os.getenv("AI_MODEL_NAME")

# ✅ AI client setup
client = OpenAI(
    base_url=endpoint,
    api_key=token,
)
# comment

# ✅ Your concepts
concepts = [
    "Introduction to Programming", "Data Structures", "Algorithms", "Arrays", "Linked Lists",
    "Stacks", "Queues", "Trees", "Binary Search Trees", "Hash Tables", "Sorting", "Searching",
    "Recursion", "Divide and Conquer", "Dynamic Programming", "Greedy Algorithms", "Big O Notation",
    "Object-Oriented Programming", "Classes & Objects", "Inheritance", "Polymorphism",
    "Functional Programming", "Lambda Calculus", "Databases", "SQL Basics", "NoSQL Concepts",
    "Web Development", "Mobile App Development", "Cloud Computing", "Operating Systems",
    "Memory Management", "Concurrency", "Multithreading", "Networking Basics",
    "Cybersecurity Principles", "Compilers", "Regular Expressions", "Software Design Patterns",
    "Software Testing", "Artificial Intelligence Basics", "Machine Learning Fundamentals",
    "Data Science", "Computer Vision", "Natural Language Processing", "Blockchain Technology",
    "Internet of Things (IoT)", "Embedded Systems", "Quantum Computing", "Automata Theory"
]


def generate_learning_analysis(user_knowledge: str, user_goal: str):
    prompt = f"""
You are an intelligent assistant helping to build a personalized learning path.

The user answered two questions:
1. What do you already know in tech or programming?
"{user_knowledge}"

2. What is your goal or what would you like to achieve by learning tech?
"{user_goal}"

Your task is to:
- Extract a list of **existing knowledge** concepts (only those mentioned or implied).
- Identify the **learning goal** as the **most relevant concept** from the following official concept list only:

{json.dumps(concepts, indent=2)}

Respond with **only raw JSON** in the following format:
{{
  "knowledge_base": ["concept1", "concept2"],
  "learning_goal": ["concept_from_list"]
}}
"""
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        ai_text = response.choices[0].message.content
        cleaned_json = ai_text.replace("```json", "").replace("```", "").strip()

        # Ensure output is in list format as required
        json_response = json.loads(cleaned_json)

        # Ensure "knowledge_base" and "learning_goal" are both lists
        if isinstance(json_response.get("knowledge_base"), list) and isinstance(json_response.get("learning_goal"),
                                                                                list):
            return json_response
        else:
            raise ValueError("The format of the returned data is incorrect.")

    except Exception as e:
        return {"error": str(e)}


# ✅ Manual test
if __name__ == "__main__":
    user_knowledge = input("What do you already know in tech or programming?\n> ")
    user_goal = input("What is your goal or what would you like to achieve by learning tech?\n> ")

    result = generate_learning_analysis(user_knowledge, user_goal)
    print("\n🎯 Analysis Result:")
    print(json.dumps(result, indent=2))