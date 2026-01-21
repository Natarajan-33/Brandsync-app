# BrandSync - AI-Powered Influencer Marketing Platform

<div align="center">

**An intelligent platform that helps brands discover, connect with, and negotiate with influencers using advanced AI technologies**

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a98f?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3-61dafb?style=flat&logo=react)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.5-3178c6?style=flat&logo=typescript)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=flat&logo=python)](https://www.python.org/)

</div>

---

## 🎯 Overview

BrandSync is a full-stack AI-powered influencer marketing platform that revolutionizes how brands discover and engage with influencers. The platform leverages semantic search, conversational AI, and voice agents to automate and personalize influencer outreach at scale.

### Key Features

- 🔍 **Semantic Search** - Natural language search powered by vector embeddings to find influencers based on meaning, not just keywords
- 🤖 **AI Voice Agent** - Automated voice calls using ElevenLabs Conversational AI for personalized outreach
- 📧 **Email Automation** - Automated email campaigns via SendGrid integration
- 🎨 **Modern UI** - Beautiful, responsive interface built with React, TypeScript, and Tailwind CSS
- ⚡ **Real-time Audio Streaming** - Bidirectional WebSocket streaming for live voice conversations
- 📊 **Influencer Discovery** - Advanced search and filtering capabilities

---

## 🏗️ Architecture

### Tech Stack

**Backend:**
- **FastAPI** - Modern Python web framework for building APIs
- **Python 3.8+** - Backend programming language
- **Uvicorn** - ASGI server for running FastAPI
- **ChromaDB** - Vector database for semantic search
- **Sentence Transformers** - For generating embeddings (`all-MiniLM-L6-v2`)
- **ElevenLabs** - Conversational AI and voice synthesis
- **Twilio** - Telephony integration for phone calls
- **SendGrid** - Email delivery service

**Frontend:**
- **React 18** with **TypeScript** - Modern UI framework
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - High-quality React component library
- **React Router** - Client-side routing
- **TanStack Query** - Data fetching and state management

### System Architecture

```
┌─────────────┐
│   Frontend  │ (React + TypeScript)
│  (React UI) │
└──────┬──────┘
       │ HTTP/REST API
       ▼
┌─────────────────────────────────────┐
│      FastAPI Backend                │
│  ┌───────────────────────────────┐  │
│  │  Influencer Search Endpoint   │  │
│  │  - Vector Search (ChromaDB)  │  │
│  │  - Sentence Transformers     │  │
│  └──────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │  Outreach Endpoints          │  │
│  │  - Email (SendGrid)          │  │
│  │  - Voice (ElevenLabs)        │  │
│  └──────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │  Twilio Integration          │  │
│  │  - WebSocket Audio Stream    │  │
│  │  - TwiML Generation          │  │
│  └──────────────────────────────┘  │
└──────┬──────────────────────────────┘
       │
       ├───► ChromaDB (Vector DB)
       ├───► ElevenLabs API (Voice AI)
       ├───► Twilio API (Telephony)
       └───► SendGrid API (Email)
```

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** 18+ and npm (or yarn)
- **Python** 3.8 or higher
- **pip** (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <YOUR_GIT_URL>
   cd Brandsync-app
   ```

2. **Install Frontend Dependencies**
   ```bash
   npm install
   ```

3. **Install Backend Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

### Environment Variables

Create a `.env` file in the `backend` directory with the following variables:

```bash
# ElevenLabs Configuration
ELEVENLABS_API_KEY=your_elevenlabs_api_key
ELEVENLABS_AGENT_ID=your_agent_id
ELEVENLABS_PHONE_NUMBER_ID=your_phone_number_id

# SendGrid Configuration
SENDGRID_API_KEY=your_sendgrid_api_key
DEFAULT_SENDER_EMAIL=your_email@domain.com

# Twilio Configuration (if using direct integration)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token

# Development
PUBLIC_URL=http://localhost:8000  # For local development
# Use ngrok URL for Twilio callbacks: PUBLIC_URL=https://your-ngrok-url.ngrok.io
```

### Running the Application

1. **Start the Backend Server**
   ```bash
   cd backend
   python server.py
   ```
   The API will be available at `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`
   - Alternative docs: `http://localhost:8000/redoc`

2. **Start the Frontend Development Server**
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

---

## 📁 Project Structure

```
Brandsync-app/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI app initialization
│   │   ├── endpoints/
│   │   │   ├── influencers.py         # Influencer search API
│   │   │   ├── outreach.py            # Email & voice outreach
│   │   │   └── twilio_integration.py  # Twilio WebSocket handling
│   │   └── utils/
│   │       ├── vector_search.py       # Vector search utility
│   │       ├── twilio_audio_interface.py  # Audio streaming
│   │       └── twilio_config.py       # Twilio configuration
│   ├── tests/                         # Backend tests
│   ├── requirements.txt               # Python dependencies
│   └── server.py                     # Server entry point
│
├── src/                               # Frontend (React)
│   ├── pages/
│   │   ├── Index.tsx                 # Main dashboard
│   │   ├── Influencers.tsx           # Influencer listing
│   │   └── NotFound.tsx              # 404 page
│   ├── components/                    # React components
│   │   ├── InfluencerCard.tsx        # Influencer card component
│   │   ├── StatsCard.tsx             # Statistics card
│   │   └── ui/                       # shadcn/ui components
│   ├── hooks/                        # Custom React hooks
│   └── lib/                          # Utility functions
│
├── public/                            # Static assets
├── package.json                       # Frontend dependencies
└── README.md                         # This file
```

---

## 🔌 API Endpoints

### Influencer Search

- `GET /influencers/` - Get all influencers
- `GET /influencers/search?q=<query>` - Semantic search using vector embeddings

### Outreach

- `POST /outreach/email` - Send email to influencer
  ```json
  {
    "to_email": "influencer@example.com",
    "influencer_name": "John Doe",
    "brand_name": "Brand Name",
    "campaign_name": "Campaign Name",
    "deliverables": "3 Instagram posts",
    "timeline": "4 weeks",
    "budget_range": "$5,000 - $10,000"
  }
  ```

- `POST /outreach/direct-call` - Initiate voice call via ElevenLabs
  ```json
  {
    "phone_number": "+1234567890",
    "influencer_name": "John Doe",
    "brand_name": "Brand Name",
    "campaign_name": "Campaign Name",
    "deliverables": "3 Instagram posts",
    "timeline": "4 weeks",
    "budget_range": "$5,000 - $10,000"
  }
  ```

- `POST /outreach/negotiation/summary` - Log negotiation results

### Twilio Integration

- `POST /twilio/outbound-call` - Initiate outbound call
- `POST /twilio/inbound-call` - Handle inbound call
- `WebSocket /twilio/stream` - Audio streaming endpoint

---

## 🤖 AI Features Explained

### 1. Semantic Search with Vector Embeddings

**How it works:**
- Influencer profiles are converted to rich text descriptions
- `SentenceTransformer` model (`all-MiniLM-L6-v2`) encodes descriptions into 384-dimensional vectors
- Vectors capture semantic meaning (e.g., "fashion influencer from India" vs "tech reviewer")
- User queries are encoded and matched using cosine similarity in ChromaDB
- Returns top-k most similar influencers with similarity scores

**Why it's powerful:**
- Natural language queries: "Find me a tech influencer in India"
- Understands meaning, not just keywords
- Handles synonyms and related concepts

**Code Location:**
- `backend/app/utils/vector_search.py` - Reusable vector search utility
- `backend/app/endpoints/influencers.py` - API endpoint for influencer search

### 2. Conversational AI Voice Agent

**How it works:**
- Uses ElevenLabs Conversational AI agent for natural voice conversations
- Dynamic variables (brand name, campaign details) are injected for personalization
- Real-time bidirectional audio streaming via WebSocket
- Backend acts as a bridge between Twilio (telephony) and ElevenLabs (AI)

**Architecture Flow:**
```
Frontend → FastAPI Backend → ElevenLabs API → Twilio → Phone Call
```

**Key Components:**
- WebSocket connections for real-time audio streaming
- Audio format conversion (μ-law ↔ base64 JSON)
- Parallel async tasks for bidirectional audio flow

**Code Location:**
- `backend/app/endpoints/outreach.py` - Voice agent API endpoints
- `backend/app/endpoints/twilio_integration.py` - Twilio WebSocket handling
- `backend/app/utils/twilio_audio_interface.py` - Audio streaming interface

### 3. Email Outreach Automation

**How it works:**
- Personalized HTML email templates
- SendGrid API integration for reliable delivery
- SMTP fallback for development/testing
- Mock mode support for testing without sending emails

**Code Location:**
- `backend/app/endpoints/outreach.py` - Email endpoint

---

## 🧪 Testing

### Backend Tests

Run backend tests using pytest:

```bash
cd backend
pip install pytest
pytest
```

Test files are located in `backend/tests/`:
- `test_influencers.py` - Influencer search tests
- `test_outreach.py` - Outreach endpoint tests
- `test_vector_search.py` - Vector search utility tests
- `test_main.py` - Main application tests

### Frontend Tests

```bash
npm run lint  # Run ESLint
```

---

## 🛠️ Development

### Building for Production

**Frontend:**
```bash
npm run build
```

**Backend:**
The FastAPI application runs directly with uvicorn. For production, use:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Development Tips

1. **Local Development with Twilio:**
   - Use [ngrok](https://ngrok.com/) to expose your local server
   - Set `PUBLIC_URL` environment variable to your ngrok URL
   - Configure Twilio webhook URLs to point to your ngrok URL

2. **Testing Voice Calls:**
   - Ensure ElevenLabs agent is configured in ElevenLabs dashboard
   - Verify Twilio credentials are correctly set
   - Check WebSocket connections in browser DevTools

3. **Vector Search:**
   - ChromaDB data persists in `backend/chroma_db/` directory
   - To reset embeddings, delete the directory and restart the server

---

## 📊 Performance Metrics

- **Vector Search:** <100ms for query encoding + similarity search
- **Embedding Generation:** ~50ms per influencer (batch processing)
- **Voice Call Initiation:** ~2-3 seconds (API call + Twilio setup)
- **Audio Latency:** <500ms (WebSocket streaming)

---

## 🔮 Future Enhancements

- [ ] **Database Persistence** - Supabase integration for storing campaigns and negotiations
- [ ] **Advanced Filtering** - Multi-criteria search (followers, engagement rate, region)
- [ ] **Analytics Dashboard** - Campaign performance tracking and insights
- [ ] **Multi-language Support** - Extend embeddings to support multiple languages
- [ ] **Fine-tuning** - Custom embedding model trained on influencer data
- [ ] **Authentication & Authorization** - User authentication and role-based access
- [ ] **Campaign Management** - Full campaign lifecycle management
- [ ] **Real-time Notifications** - WebSocket-based notifications for campaign updates

---

## 📚 Additional Documentation

- [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md) - Detailed project overview and architecture
- [VOICE_AGENT_DETAILED_EXPLANATION.md](./VOICE_AGENT_DETAILED_EXPLANATION.md) - Comprehensive guide to voice agent implementation
- [VOICE_AGENT_VISUAL_FLOW.md](./VOICE_AGENT_VISUAL_FLOW.md) - Visual flow diagrams for voice agent
- [INTERVIEW_QUICK_REFERENCE.md](./INTERVIEW_QUICK_REFERENCE.md) - Quick reference for technical interviews

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is private and proprietary.

---

## 🆘 Support

For issues, questions, or contributions, please open an issue in the repository.

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - UI library
- [shadcn/ui](https://ui.shadcn.com/) - Component library
- [ElevenLabs](https://elevenlabs.io/) - Voice AI platform
- [Twilio](https://www.twilio.com/) - Communications platform
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [Sentence Transformers](https://www.sbert.net/) - Semantic embeddings

---

<div align="center">

**Built with ❤️ using AI-powered technologies**

</div>
