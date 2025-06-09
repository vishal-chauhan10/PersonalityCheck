# Numerology Personality Viewer

A modern web application that provides personality insights based on numerological principles. Built with Next.js and Python FastAPI.

## Features

- Beautiful, responsive UI with smooth animations
- Numerological calculations based on name and birth date
- Detailed personality analysis using AI
- Google AdSense integration for monetization
- No authentication required

## Tech Stack

- Frontend: Next.js, TypeScript, Tailwind CSS, Framer Motion
- Backend: Python FastAPI, Anthropic Claude API
- Styling: Tailwind CSS with Typography plugin

## Setup Instructions

### Frontend Setup

1. Install dependencies:

```bash
cd personality-viewer
yarn install
```

2. Create a Google AdSense account and replace the placeholder values in `src/app/page.tsx`:

- Replace `YOUR_CLIENT_ID` with your Google AdSense client ID
- Replace `YOUR_AD_SLOT` with your ad slot ID

3. Start the development server:

```bash
yarn dev
```

### Backend Setup

1. Create a Python virtual environment and install dependencies:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

2. Create a `.env` file in the `backend` directory with your Anthropic API key:

```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

3. Start the backend server:

```bash
cd backend
uvicorn api.main:app --reload
```

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Enter your full name and birth date
3. Click "Reveal My Personality" to get your numerological analysis

## Development

- The frontend runs on port 3000
- The backend API runs on port 8000
- The backend provides numerological calculations and AI-powered personality analysis
- The frontend features a responsive design with smooth animations and transitions

## Monetization

The application includes Google AdSense integration. To start earning:

1. Sign up for a Google AdSense account
2. Replace the placeholder values in the code with your actual AdSense client ID and ad slot
3. Wait for Google's approval
4. Start earning from ad impressions and clicks

## License

MIT License
# PersonalityCheck
