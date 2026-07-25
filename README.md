# NutriGen AI

AI-Powered Personalized Nutrition, Fitness and Wellness Assistant

NutriGen AI is an AI-powered web application that provides personalized nutrition, fitness, and wellness recommendations. Built using Python, Streamlit, and Google Gemini AI, the application generates customized meal plans, workout routines, health insights, food image analysis, and budget-friendly nutrition plans based on the user's health profile, dietary preferences, fitness goals, and lifestyle.

## Features

- Personalized user profile management
- BMI, BMR, and TDEE calculation
- AI-generated meal plans
- Personalized workout planner
- Food image analysis using AI
- Personalized health insights
- Budget-friendly nutrition planning
- Wellness tracking dashboard
- AI-powered health chatbot

## Tech Stack

- Python
- Streamlit
- Google Gemini 2.0 Flash
- Google GenAI SDK
- Pandas
- Plotly
- Pillow
- Git
- GitHub

## Project Structure

```text
NutriGen-AI/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── config.toml
```

## Installation

Clone the repository.

```bash
git clone https://github.com/your-username/NutriGen-AI.git
cd NutriGen-AI
```

Create a virtual environment.

```bash
python -m venv venv
```

Activate the environment.

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

Install the required packages.

```bash
pip install -r requirements.txt
```

Configure your Gemini API key.

**Windows**

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

**Linux/macOS**

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

Run the application.

```bash
streamlit run app.py
```

## Application Modules

- User Profile
- Meal Planner
- Workout Planner
- Food Image Analysis
- Health Insights
- Budget Nutrition
- Wellness Tracker
- AI Chat Assistant

## How It Works

1. Create your health profile.
2. Enter your fitness goals and dietary preferences.
3. Select a module such as Meal Planner, Workout Planner, Food Analysis, or Wellness Tracker.
4. Google Gemini AI processes the request and generates personalized recommendations.
5. View and interact with the results through the Streamlit interface.

## Future Enhancements

- User authentication
- Cloud database integration
- Mobile application
- Barcode scanner
- Wearable device integration
- Voice assistant
- Multi-language support
- Advanced health analytics

## Author

**Ravi Kumar Kushwaha**

B.Tech Computer Science Engineering  
Symbiosis Institute of Technology, Nagpur

## License

This project was developed for educational purposes as part of the **Edunet Foundation – IBM SkillsBuild AICTE Artificial Intelligence Internship**.

## Acknowledgements

- Edunet Foundation
- IBM SkillsBuild
- Google Gemini AI
- Streamlit
- Plotly
- Open Source Community
