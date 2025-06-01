from fastapi import APIRouter, Query
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/influencers", tags=["influencers"])

# Initialize the sentence transformer model with explicit parameters
try:
    logger.info("Loading sentence transformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    # Fallback to a simpler model if the first one fails
    try:
        model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
        logger.info("Fallback model loaded successfully")
    except Exception as e2:
        logger.error(f"Error loading fallback model: {e2}")
        raise

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

# Generate comprehensive descriptions for embedding
def generate_influencer_description(influencer: Dict[str, Any]) -> str:
    """Generate a rich text description of an influencer for embedding"""
    # Create a detailed description that captures all important aspects
    desc = f"{influencer['name']} is a {influencer['category']} influencer from {influencer['region']} "
    desc += f"with {influencer['followers']:,} followers "
    desc += f"on {', '.join(influencer['platforms'])} "
    desc += f"with an engagement rate of {influencer['engagement_rate']}%. "
    
    # Add specific details that might be searched for
    if influencer['followers'] >= 1000000:
        desc += f"They are a mega influencer with over {influencer['followers']/1000000:.1f} million followers. "
    elif influencer['followers'] >= 100000:
        desc += f"They are a macro influencer with {influencer['followers']/1000:.0f}K followers. "
    else:
        desc += f"They are a micro influencer with {influencer['followers']/1000:.0f}K followers. "
        
    # Add rate card information
    desc += f"Their rate card is {influencer['rate_card']}. "
    
    # Add description if available
    if 'description' in influencer and influencer['description']:
        desc += influencer['description']
        
    return desc

# Initialize the vector database with influencer data
def initialize_vector_db():
    try:
        # First check if collection already has data
        existing_count = len(influencer_collection.get(include=[])['ids'])
        if existing_count > 0:
            logger.info(f"Collection already contains {existing_count} items, skipping initialization")
            return
    except Exception as e:
        logger.warning(f"Error checking collection: {e}, will proceed with initialization")
    
    logger.info("Initializing vector database with influencer data...")
    
    # Generate IDs and descriptions
    ids = [str(influencer["id"]) for influencer in influencers]
    
    # Create rich descriptions for better semantic search
    descriptions = [generate_influencer_description(inf) for inf in influencers]
    logger.info(f"Generated {len(descriptions)} descriptions for embedding")
    
    # Generate embeddings
    logger.info("Encoding descriptions with the model...")
    embeddings = model.encode(descriptions).tolist()
    logger.info("Encoding complete")
    
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
    logger.info("Adding data to ChromaDB collection...")
    try:
        influencer_collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas
        )
        logger.info(f"Successfully added {len(ids)} influencers to the vector database")
    except Exception as e:
        logger.error(f"Error adding data to collection: {e}")
        raise

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
    """Search influencers using natural language and vector embeddings with cosine similarity"""
    logger.info(f"Received search query: {q}")
    
    # Encode the query
    logger.info("Encoding search query...")
    query_embedding = model.encode(q).tolist()
    
    # Search in the collection with cosine similarity
    try:
        results = influencer_collection.query(
            query_embeddings=[query_embedding],
            n_results=10,  # Get more results initially to calculate similarity scores
            include=["metadatas", "distances"]  # Include distances for similarity calculation
        )
        logger.info(f"Vector search completed with {len(results['ids'][0])} results")
    except Exception as e:
        logger.error(f"Error during vector search: {e}")
        # Return empty list as fallback
        return []
    
    if not results['ids'][0]:
        logger.info("No results found in vector search")
        return []
    
    # Extract results
    matched_ids = results["ids"][0]  # First query results
    distances = results["distances"][0]  # Distances for first query
    
    # Convert distances to cosine similarity scores (ChromaDB uses L2 distance by default)
    # Cosine similarity = 1 - (distance^2 / 2)
    # This is an approximation for normalized vectors
    similarity_scores = [1 - (distance**2 / 2) for distance in distances]
    
    # Create a list of (id, similarity_score) tuples
    id_score_pairs = list(zip(matched_ids, similarity_scores))
    
    # Sort by similarity score (highest first)
    id_score_pairs.sort(key=lambda x: x[1], reverse=True)
    
    logger.info(f"Top similarity scores: {[f'{id}:{score:.4f}' for id, score in id_score_pairs[:5]]}")
    
    # Get all matching influencers with their scores
    matched_influencers = []
    for id_str, score in id_score_pairs:
        try:
            influencer_id = int(id_str)
            for influencer in influencers:
                if influencer["id"] == influencer_id:
                    # Add a copy of the influencer with the similarity score
                    influencer_copy = influencer.copy()
                    influencer_copy["similarity_score"] = score
                    matched_influencers.append(influencer_copy)
                    logger.info(f"Vector match: {influencer['name']} with similarity score {score:.4f}")
                    break
        except (ValueError, TypeError):
            # Skip if ID can't be converted to int
            continue
    
    # Return the top 2 results based on similarity score
    top_results = matched_influencers[:2] if matched_influencers else []
    
    if top_results:
        logger.info(f"Returning top {len(top_results)} results:")
        for result in top_results:
            logger.info(f"  {result['name']} (score: {result['similarity_score']:.4f})")
    else:
        logger.info("No results found")
    
    return top_results
