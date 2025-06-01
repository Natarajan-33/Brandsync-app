from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints import influencers, outreach

app = FastAPI(title="BrandSync API", description="API for BrandSync influencer marketing platform")

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(influencers.router)
app.include_router(outreach.router)

@app.get("/")
async def root():
    return {"message": "Welcome to BrandSync API. Visit /docs for API documentation."}
