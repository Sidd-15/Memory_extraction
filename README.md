# AI Companion Memory & Personality Engine

A production-ready AI companion system that extracts user memories from conversations and generates personalized responses using different personality styles.

## 🎯 Features

- **Memory Extraction Module**: Identifies user preferences, emotional patterns, and facts from 30 chat messages
- **Personality Engine**: Transforms responses using 3 distinct personalities:
  - 🧘 Calm Mentor (thoughtful, patient, guiding)
  - 😄 Witty Friend (humorous, casual, playful)
  - 💚 Therapist Style (empathetic, validating, supportive)
- **Before/After Comparison**: See personality differences side-by-side
- **Advanced Prompt Engineering**: Chain-of-thought reasoning and structured output parsing

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Groq API Key (free, no credit card required)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Sidd-15/Memory_extraction.git
cd Memory_extraction
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key from: https://console.groq.com/keys

5. **Run the application**
```bash
python app.py
```

6. **Open in browser**
```
http://localhost:5000
```

## 📁 Project Structure

```
Memory_extraction/
├── app.py                  # Main Flask application with AI logic
├── templates/
│   └── index.html         # Frontend interface
├── .env                   # Environment variables (create this)
├── .gitignore            # Git ignore rules
├── requirements.txt      # Python dependencies
├── vercel.json           # Vercel deployment configuration
├── README.md            # This file
├── IMPROVEMENTS.md      # Technical documentation
└── DEPLOYMENT.md        # Deployment guide
```

## 🌐 Live Demo

**Deployed on Vercel**: [Your Live URL Here]

## 🚀 Deployment

This project is deployed on **Vercel** for free hosting.

### Deploy Your Own (Free)

1. **Fork/Clone this repository**

2. **Push to your GitHub**

3. **Deploy to Vercel**:
   - Go to https://vercel.com
   - Sign up with GitHub
   - Click "Import Project"
   - Select your repository
   - Add environment variable: `GROQ_API_KEY` = `your_key_here`
   - Click "Deploy"
   - Done! You'll get a live URL in 1-2 minutes

See `DEPLOYMENT.md` for detailed instructions.

## 🧪 How to Use

1. **Load Example Messages** (or paste your own 30 messages)
2. **Click "Extract Memory"** - AI analyzes and extracts user profile
3. **Enter a test message** (e.g., "How should I handle stress?")
4. **Click "Generate Personality Responses"** - See 3 different personality responses side-by-side

## 🛠️ Technical Details

### Key Technologies
- **Backend**: Flask (Python)
- **AI Model**: Llama 3.3 70B via Groq API
- **Frontend**: Vanilla JavaScript + HTML/CSS
- **Deployment**: Vercel (Serverless)

### AI Engineering Highlights
- **Chain-of-Thought Prompting**: Structured reasoning steps for better analysis
- **Temperature Optimization**: 0.3 for structured output, 0.8 for creative responses
- **Robust JSON Parsing**: Handles multiple markdown formats
- **Error Handling**: Comprehensive validation and error messages
- **Modular Design**: Separated memory extraction and personality generation


## 📊 API Endpoints

### `POST /extract_memory`
Extract user memory from messages.

**Request**:
```json
{
  "messages": ["User: message1", "AI: response1", ...]
}
```

**Response**:
```json
{
  "preferences": ["preference1", "preference2", ...],
  "emotional_patterns": ["pattern1", "pattern2", ...],
  "facts": ["fact1", "fact2", ...]
}
```

### `POST /generate_responses`
Generate personality-based responses.

**Request**:
```json
{
  "message": "user query",
  "memory": { /* memory object */ }
}
```

**Response**:
```json
{
  "calm_mentor": "response text",
  "witty_friend": "response text",
  "therapist_style": "response text"
}
```

## 🔒 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Groq API key for AI model access | Yes |

## 📝 License

MIT License - feel free to use for learning and projects.

## 🤝 Contributing

This is an assignment submission, but suggestions are welcome!

## 📧 Contact

For questions about this project, please open an issue on GitHub.

---

**Built with ❤️ for AI Engineer Assignment**