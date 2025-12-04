import os
from flask import Flask, render_template, request, jsonify
import json
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

def extract_memory(messages):
    # Enhanced prompt with chain-of-thought reasoning
    prompt = f"""You are an expert psychologist and companion AI analyzing user conversations.

TASK: Analyze these 30 chat messages to build a comprehensive user profile.

MESSAGES:
{json.dumps(messages, indent=2)}

ANALYSIS STEPS (Think through this):
1. First, identify explicit preferences (what they say they like/dislike)
2. Then, infer implicit preferences from context (what they talk about frequently)
3. Analyze emotional language to detect patterns (anxious, happy, stressed, etc.)
4. Look for triggers that cause emotional responses
5. Extract concrete facts (names, places, relationships, goals, habits)
6. Prioritize actionable and specific information over generic statements

EXTRACTION RULES:
- Preferences: Include hobbies, interests, likes, dislikes, work preferences, communication style
- Emotional Patterns: Include recurring emotions, triggers, coping mechanisms, stress responses, mood tendencies
- Facts: Include personal details (names, relationships), professional info (job, skills), goals, challenges, locations

OUTPUT FORMAT:
Return ONLY a valid JSON object (no markdown, no explanations) with this structure:
{{
  "preferences": ["specific preference 1", "specific preference 2", ...],
  "emotional_patterns": ["specific pattern 1", "specific pattern 2", ...],
  "facts": ["specific fact 1", "specific fact 2", ...]
}}

Each array should contain 5-10 items. Be specific and actionable."""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,  # Lower temperature for more consistent structured output
            "max_tokens": 1500
        }
    )
    
    result = response.json()
    
    if "error" in result:
        raise Exception(f"API Error: {result['error'].get('message', 'Unknown error')}")
    
    if "choices" not in result:
        raise Exception(f"Invalid API response. Make sure GROQ_API_KEY is set correctly. Response: {result}")
    
    text = result["choices"][0]["message"]["content"].strip()
    
    # Robust parsing to handle markdown code blocks
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    
    text = text.strip()
    
    # Parse and validate the JSON structure
    try:
        memory_data = json.loads(text)
        
        # Validate required keys
        required_keys = ["preferences", "emotional_patterns", "facts"]
        for key in required_keys:
            if key not in memory_data:
                memory_data[key] = []
        
        return memory_data
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse JSON response: {e}. Response was: {text[:200]}")

def generate_response(user_message, memory, personality):
    # Enhanced personality definitions with specific behavioral instructions
    personalities = {
        "calm_mentor": {
            "role": "You are a calm, wise mentor with years of life experience.",
            "tone": "thoughtful, patient, encouraging, and supportive",
            "approach": "Guide through questions, share wisdom gently, validate feelings, offer perspective",
            "style": "Use metaphors and life lessons. Speak in measured, reassuring language. Focus on growth and learning."
        },
        "witty_friend": {
            "role": "You are a witty, playful best friend who loves humor and keeping things light.",
            "tone": "casual, humorous, energetic, and relatable",
            "approach": "Use jokes and lighthearted observations, be encouraging through humor, show you care while keeping it fun",
            "style": "Use casual language, emojis occasionally, pop culture references, and friendly banter. Make them smile."
        },
        "therapist_style": {
            "role": "You are a compassionate, professional therapist trained in cognitive behavioral therapy.",
            "tone": "empathetic, validating, non-judgmental, and supportive",
            "approach": "Validate emotions, ask reflective questions, help identify patterns, offer coping strategies",
            "style": "Use active listening techniques. Reflect feelings back. Ask open-ended questions. Normalize experiences."
        }
    }
    
    personality_config = personalities[personality]
    
    # Build rich memory context
    memory_context = f"""USER PROFILE (Use this to personalize your response):

PREFERENCES & INTERESTS:
{chr(10).join(f'- {p}' for p in memory['preferences'])}

EMOTIONAL PATTERNS & TRIGGERS:
{chr(10).join(f'- {p}' for p in memory['emotional_patterns'])}

KEY FACTS TO REMEMBER:
{chr(10).join(f'- {f}' for f in memory['facts'])}"""

    # Enhanced system prompt with reasoning structure
    system_prompt = f"""{personality_config['role']}

YOUR PERSONALITY:
- Tone: {personality_config['tone']}
- Approach: {personality_config['approach']}
- Style: {personality_config['style']}

{memory_context}

INSTRUCTIONS:
1. Read the user's message carefully and understand their emotional state
2. Reference relevant information from their profile naturally (don't just list facts)
3. Respond in character - your personality should be clear and consistent
4. Make your response feel personal and tailored to them specifically
5. Keep responses 2-4 sentences unless more depth is needed
6. Show genuine care and understanding

Remember: You know this person. Use their profile to connect authentically."""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.8,  # Higher temperature for more creative, varied responses
            "max_tokens": 800,
            "top_p": 0.9
        }
    )
    
    result = response.json()
    
    if "error" in result:
        raise Exception(f"API Error: {result['error'].get('message', 'Unknown error')}")
    
    if "choices" not in result:
        raise Exception(f"Invalid API response. Make sure GROQ_API_KEY is set correctly.")
    
    return result["choices"][0]["message"]["content"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract_memory', methods=['POST'])
def extract_memory_endpoint():
    data = request.json
    messages = data.get('messages', [])
    memory = extract_memory(messages)
    return jsonify(memory)

@app.route('/generate_responses', methods=['POST'])
def generate_responses():
    data = request.json
    user_message = data.get('message', '')
    memory = data.get('memory', {})
    
    responses = {}
    for personality in ['calm_mentor', 'witty_friend', 'therapist_style']:
        responses[personality] = generate_response(user_message, memory, personality)
    
    return jsonify(responses)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)