# Rightly - Your AI Legal Assistant

Rightly is a multi-modal desktop AI assistant designed to democratize legal knowledge. It transforms complex legal jargon into simple, conversational, and even visual explanations that anyone can understand, all through an intuitive voice-controlled interface.

***

### Inspiration
My inspiration for Rightly came from a simple, personal observation: legal information is intimidating. Whether you're a student, an entrepreneur, or just a curious citizen, trying to understand legal concepts is often a stressful and expensive process.

The release of powerful AI models proved to be a turning point. I was inspired to build a bridge across this information gap—a tool that could act as a friendly, knowledgeable expert on your desktop. The goal is to make learning about the law faster, more engaging, and completely free.

***

### Key Features
- **Voice-Activated Q&A**: Simply ask legal questions using your voice. Rightly listens, processes the query, and responds with a spoken answer.  
- **Real-time Web Search**: When answers aren't in its base knowledge, Rightly can search Google in real-time for up-to-the-minute information.  
- **AI Image Generation**: Generates unique images to simplify abstract legal concepts.  
- **System Automation**: Open applications, play YouTube videos, or run system commands directly with voice commands.  
- **Conversation Logging**: Automatically saves chat history in `Chatlog.json` for future reference.  
- **Intuitive Desktop GUI**: Built with PyQt5, ensuring a clean and responsive desktop interface.  

***

### Tech Stack

#### AI & Machine Learning
- **Groq**: High-speed LLM-based chat  
- **Cohere**: Natural language processing  
- **Pillow**: Image processing  
- **model**: openai/gpt-oss-120b

#### GUI  
- **PyQt5**: Native desktop interface  

#### Speech & Audio  
- **SpeechRecognition**: Speech-to-Text  
- **win32com.client**: Windows SAPI Text-to-Speech  

#### Web & Automation  
- **Requests**, **BeautifulSoup**  
- **Pywhatkit**, **googlesearch-python**  
- **AppOpener**, **keyboard**  

#### Core Utilities  
- **python-dotenv**, **threading**, **asyncio**  
- **Rich** (styled console output), **subprocess**  

***

### Project Structure

```
RIGHTLY/
│
├── Backend/
│   ├── Model.py               # Core AI decision-making logic
│   ├── Chatbot.py             # Handles conversational AI
│   ├── RealtimeSearchEngine.py# Manages live web searches
│   ├── ImageGeneration.py     # Creates images from text
│   ├── SpeechToText.py        # Converts speech to text
│   ├── TextToSpeech.py        # Converts text to speech
│   └── Automation.py          # Executes system tasks
│
├── Data/
│   └── Chatlog.json           # Stores conversation history
│
├── Frontend/
│   ├── GUI.py                 # Builds and runs the PyQt5 interface
│   ├── Graphics/              # UI images, icons, GIFs
│   └── Files/                 # Temporary UI data storage
│
├── .env                       # API keys and user configurations
├── Main.py                    # Main script to launch the application
├── Requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

***

### Getting Started

#### Prerequisites
- Python 3.8+
- pip (Python package installer)

#### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Rightly.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Rightly
   ```
3. Install dependencies:
   ```bash
   pip install -r Requirements.txt
   ```

#### Environment Setup
Create a `.env` file at the root of the project and add your credentials:

```bash
CohereAPIKey="your_cohere_api_key_here"
Username="YourName"
Assistantname=Rightly
GroqAPIKey="your_groq_api_key_here"
InputLanguage=en
HuggingFaceAPIKey="your_huggingface_api_key_here"
```

#### Running the Application
To start Rightly, run:

```bash
python Main.py
```

***

### Disclaimer
Rightly is an educational tool and is **not a substitute for professional legal advice**.  
The information provided by the AI is for **informational purposes only** and should not be used as a basis for making legal decisions. Always consult with a qualified legal professional for advice on your specific situation.  

***