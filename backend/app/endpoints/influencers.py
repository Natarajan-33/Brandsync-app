from fastapi import APIRouter, Query
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np

router = APIRouter(prefix="/influencers", tags=["influencers"])

# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Mock influencer data
influencers = [
    {
        "id": 1,
        "name": "Priya Sharma",
        "platforms": ["Instagram", "YouTube"],
        "category": "fashion",
        "followers": 1200000,
        "engagement_rate": 3.5,
        "region": "India",
        "rate_card": "₹50,000 per post, ₹150,000 per video",
        "contact": "priya.sharma@influencer.com",
        "description": "Fashion influencer specializing in sustainable fashion and Indian traditional wear"
    },
    {
        "id": 2,
        "name": "Alex Johnson",
        "platforms": ["TikTok", "Instagram"],
        "category": "fitness",
        "followers": 850000,
        "engagement_rate": 4.2,
        "region": "USA",
        "rate_card": "$3,000 per post, $8,000 per video",
        "contact": "alex@fitnesswithaj.com",
        "description": "Fitness trainer sharing workout routines and nutrition tips"
    },
    {
        "id": 3,
        "name": "Raj Patel",
        "platforms": ["YouTube", "Twitter"],
        "category": "tech",
        "followers": 2000000,
        "engagement_rate": 2.8,
        "region": "India",
        "rate_card": "₹100,000 per video, ₹30,000 per tweet",
        "contact": "raj@techreviews.in",
        "description": "Tech reviewer covering smartphones, laptops, and gadgets with focus on Indian market"
    },
    {
        "id": 4,
        "name": "Emma Wilson",
        "platforms": ["Instagram", "Blog"],
        "category": "beauty",
        "followers": 1500000,
        "engagement_rate": 5.1,
        "region": "UK",
        "rate_card": "£2,500 per post, £5,000 for sponsored blog",
        "contact": "emma@beautyblog.uk",
        "description": "Beauty blogger specializing in skincare routines and makeup tutorials"
    },
    {
        "id": 5,
        "name": "Vikram Singh",
        "platforms": ["Instagram", "YouTube"],
        "category": "travel",
        "followers": 950000,
        "engagement_rate": 3.9,
        "region": "India",
        "rate_card": "₹40,000 per post, ₹120,000 per video",
        "contact": "vikram@traveldiaries.in",
        "description": "Travel vlogger showcasing hidden gems across India and Southeast Asia"
    },
    {
        "id": 6,
        "name": "Sarah Chen",
        "platforms": ["YouTube", "Instagram", "Twitch"],
        "category": "gaming",
        "followers": 3000000,
        "engagement_rate": 4.5,
        "region": "USA",
        "rate_card": "$5,000 per post, $10,000 per stream",
        "contact": "sarah@gamingwithsarah.com",
        "description": "Gaming streamer and content creator focusing on RPGs and strategy games"
    },
    {
        "id": 7,
        "name": "Aditya Mehta",
        "platforms": ["Instagram", "LinkedIn"],
        "category": "business",
        "followers": 500000,
        "engagement_rate": 2.3,
        "region": "India",
        "rate_card": "₹80,000 per post, ₹200,000 per webinar",
        "contact": "aditya@startupmentor.in",
        "description": "Entrepreneur and business coach sharing startup advice and market insights"
    },
    {
        "id": 8,
        "name": "Maria Rodriguez",
        "platforms": ["Instagram", "TikTok", "YouTube"],
        "category": "food",
        "followers": 1800000,
        "engagement_rate": 6.2,
        "region": "Mexico",
        "rate_card": "$4,000 per post, $7,500 per video",
        "contact": "maria@deliciosorecipes.com",
        "description": "Chef and food influencer sharing authentic Mexican recipes and cooking techniques"
    }
]

# Initialize ChromaDB for vector search
chroma_client = chromadb.Client()

# Try to get the collection if it exists, otherwise create it
try:
    influencer_collection = chroma_client.get_collection(name="influencers")
except Exception:
    influencer_collection = chroma_client.create_collection(name="influencers")

# Generate descriptions for embedding
def generate_influencer_description(influencer: Dict[str, Any]) -> str:
    return f"{influencer['name']} is a {influencer['category']} influencer from {influencer['region']} \
            with {influencer['followers']} followers on {', '.join(influencer['platforms'])} \
            with an engagement rate of {influencer['engagement_rate']}%. {influencer['description']}"

# Initialize the vector database with influencer data
def initialize_vector_db():
    ids = [str(influencer["id"]) for influencer in influencers]
    descriptions = [generate_influencer_description(influencer) for influencer in influencers]
    embeddings = model.encode(descriptions).tolist()
    
    # Convert complex data types to strings for ChromaDB compatibility
    metadatas = []
    for influencer in influencers:
        # Create a copy of the influencer data with platform list converted to string
        metadata = influencer.copy()
        metadata["platforms"] = ", ".join(metadata["platforms"])
        # Convert all values to strings to ensure compatibility
        for key, value in metadata.items():
            if not isinstance(value, str):
                metadata[key] = str(value)
        metadatas.append(metadata)
    
    # Add documents to the collection
    influencer_collection.add(
        ids=ids,
        embeddings=embeddings,
        metadatas=metadatas
    )

# Initialize the vector database on module import
# Only run this in production, not during testing
if __name__ != "__main__":
    initialize_vector_db()

@router.get("/", response_model=List[Dict[str, Any]])
async def get_influencers():
    """Get all influencers"""
    return influencers

@router.get("/search")
async def search_influencers(q: str = Query(..., description="Natural language search query")):
    """Search influencers using natural language"""
    # Encode the query
    query_embedding = model.encode(q).tolist()
    
    # Search in the collection
    results = influencer_collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )
    
    # Extract and return the matched influencers
    matched_ids = results["ids"][0]  # First query results
    matched_influencers = []
    
    for id_str in matched_ids:
        influencer_id = int(id_str)
        for influencer in influencers:
            if influencer["id"] == influencer_id:
                matched_influencers.append(influencer)
                break
    
    return matched_influencers
