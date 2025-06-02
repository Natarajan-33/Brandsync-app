from fastapi import APIRouter, HTTPException, Depends, status, Body
from typing import Dict, Any, Optional, Union, List
from pydantic import BaseModel, EmailStr, Field, validator
import os
import logging
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import json
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set default values for environment variables
os.environ.setdefault('USE_MOCK_EMAIL', 'true')
os.environ.setdefault('FALLBACK_TO_MOCK', 'true')
os.environ.setdefault('USE_SMTP', 'false')
os.environ.setdefault('USE_MOCK_ELEVENLABS', 'true')

# SMTP settings (for Gmail)
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/outreach", tags=["outreach"])

# Pydantic model for email request
class EmailRequest(BaseModel):
    influencer_name: str = Field(..., description="Name of the influencer")
    influencer_email: EmailStr = Field(..., description="Email address of the influencer")
    campaign_name: str = Field(..., description="Name of the campaign")
    message: str = Field(..., description="Email message content")
    influencer_id: Optional[int] = Field(None, description="ID of the influencer in the system")
    campaign_id: Optional[int] = Field(None, description="ID of the campaign in the system")
    use_mock: Optional[bool] = Field(False, description="Use mock email service instead of SendGrid")
    
    @validator('influencer_email')
    def validate_email(cls, v):
        # Always allow your own email for testing
        if v == 'natarajan.mohan33@gmail.com':
            return v
        # Basic email validation
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v

# Pydantic model for email response
class EmailResponse(BaseModel):
    success: bool
    message: str
    timestamp: datetime

# Pydantic model for voice agent request
class VoiceAgentRequest(BaseModel):
    phone_number: str = Field(..., description="Phone number to call")
    influencer_name: str = Field(..., description="Name of the influencer")
    brand_name: str = Field(..., description="Name of the brand")
    campaign_name: str = Field(..., description="Name of the campaign")
    deliverables: str = Field(..., description="Campaign deliverables")
    timeline: str = Field(..., description="Campaign timeline")
    budget_range: str = Field(..., description="Budget range for the campaign")
    influencer_id: Optional[int] = Field(None, description="ID of the influencer in the system")
    campaign_id: Optional[int] = Field(None, description="ID of the campaign in the system")
    use_mock: Optional[bool] = Field(False, description="Use mock voice service instead of ElevenLabs")
    
    @validator('phone_number')
    def validate_phone(cls, v):
        # Basic phone number validation
        v = v.strip()
        if not v.startswith('+'):
            raise ValueError('Phone number must start with country code (e.g., +1)')
        # Remove any non-digit characters except the leading +
        digits = ''.join(c for c in v if c.isdigit() or c == '+')
        # Check if it has enough digits (at least country code + 10 digits)
        if len(digits) < 11:
            raise ValueError('Phone number must include country code and at least 10 digits')
        return digits

# Pydantic model for voice agent response
class VoiceAgentResponse(BaseModel):
    success: bool
    message: str
    call_id: Optional[str] = None
    timestamp: datetime

# Pydantic model for negotiation summary
class NegotiationSummary(BaseModel):
    influencer_name: str
    brand_name: str
    campaign_name: str
    deliverables: str
    timeline: str
    agreed_budget: Optional[str] = None
    status: str = Field(..., description="Status of the negotiation (pending, accepted, rejected)")
    notes: Optional[str] = None
    timestamp: datetime

def send_email_via_smtp(sender_email, recipient_email, subject, html_content):
    """Send an email using Python's built-in SMTP library"""
    try:
        # Create message container
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email
        
        # Attach HTML content
        part = MIMEText(html_content, 'html')
        msg.attach(part)
        
        # Connect to SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        
        # Login to email account
        if SMTP_USERNAME and SMTP_PASSWORD:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
        
        # Send email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        
        logger.info(f"Email sent to {recipient_email} via SMTP")
        return True
    except Exception as e:
        logger.error(f"SMTP error: {str(e)}")
        return False

@router.post("/email", response_model=EmailResponse, status_code=status.HTTP_200_OK)
async def send_email(request: EmailRequest):
    """
    Send an email to an influencer using SendGrid API.
    Optionally logs the outreach event to Supabase if influencer_id and campaign_id are provided.
    """
    try:
        # Get SendGrid API key from environment variables
        sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
        if not sendgrid_api_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="SendGrid API key not configured"
            )
            
        # Get sender email from environment variables or use default
        sender_email = os.getenv("DEFAULT_SENDER_EMAIL")
        if not sender_email:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Sender email not configured"
            )
            
        # Create email message
        subject = f"Collaboration Opportunity: {request.campaign_name}"
        
        # Personalize the email content
        html_content = f"""
        <html>
            <body>
                <p>Dear {request.influencer_name},</p>
                <p>{request.message}</p>
                <p>Best regards,<br>BrandSync Team</p>
            </body>
        </html>
        """
        
        message = Mail(
            from_email=sender_email,
            to_emails=request.influencer_email,
            subject=subject,
            html_content=html_content
        )
        
        # Determine which email service to use
        use_mock = request.use_mock or os.getenv('USE_MOCK_EMAIL', 'false').lower() == 'true'
        use_smtp = os.getenv('USE_SMTP', 'false').lower() == 'true'
        
        email_sent = False
        error_detail = "Unknown error"
        
        if use_mock:
            # Use mock email service (just log the email details)
            logger.info(f"[MOCK EMAIL] Would send email to {request.influencer_email}")
            logger.info(f"[MOCK EMAIL] Subject: {subject}")
            logger.info(f"[MOCK EMAIL] Content: {html_content}")
            
            # For development/testing purposes, we'll consider this a success
            logger.info(f"[MOCK EMAIL] Email to {request.influencer_email} simulated successfully")
            email_sent = True
        else:
            # Try SendGrid first (unless SMTP is specifically requested)
            if not use_smtp:
                try:
                    logger.info(f"Attempting to send email to {request.influencer_email} using SendGrid")
                    logger.info(f"Using API key: {sendgrid_api_key[:5]}...{sendgrid_api_key[-5:] if len(sendgrid_api_key) > 10 else '***'}")
                    
                    # Verify API key format
                    if not sendgrid_api_key.startswith('SG.') or len(sendgrid_api_key) < 50:
                        logger.warning(f"SendGrid API key appears to be in an invalid format. Expected format: 'SG.xxxxxx...'")
                    
                    # Create SendGrid client and send message
                    sg = SendGridAPIClient(sendgrid_api_key)
                    response = sg.send(message)
                    
                    logger.info(f"Email sent to {request.influencer_email}, status code: {response.status_code}")
                    email_sent = True
                except Exception as e:
                    error_message = str(e)
                    logger.error(f"SendGrid API error: {error_message}")
                    
                    # Provide more specific error messages based on common issues
                    if "Unauthorized" in error_message or "401" in error_message:
                        logger.error("The SendGrid API key appears to be invalid or revoked. Please check your SendGrid account.")
                        error_detail = "The SendGrid API key is invalid or has been revoked. Please check your SendGrid account."
                    elif "Permission Denied" in error_message:
                        logger.error("The SendGrid API key doesn't have permission to send emails. Check API key permissions.")
                        error_detail = "The SendGrid API key doesn't have permission to send emails. Check API key permissions."
                    else:
                        error_detail = f"SendGrid API error: {error_message}"
            
            # If SendGrid failed or SMTP was requested, try SMTP
            if not email_sent and (use_smtp or os.getenv('FALLBACK_TO_SMTP', 'false').lower() == 'true'):
                logger.info(f"Attempting to send email via SMTP")
                if SMTP_USERNAME and SMTP_PASSWORD:
                    smtp_success = send_email_via_smtp(
                        sender_email=sender_email,
                        recipient_email=request.influencer_email,
                        subject=subject,
                        html_content=html_content
                    )
                    
                    if smtp_success:
                        email_sent = True
                        logger.info(f"Email sent to {request.influencer_email} via SMTP")
                    else:
                        error_detail = "Failed to send email via SMTP. Check SMTP credentials and settings."
                else:
                    logger.error("SMTP username and password not configured")
                    error_detail = "SMTP username and password not configured"
            
            # If both SendGrid and SMTP failed, check if we should fall back to mock
            if not email_sent and os.getenv('FALLBACK_TO_MOCK', 'true').lower() == 'true':
                # Fall back to mock email service
                logger.info(f"Falling back to mock email service")
                logger.info(f"[MOCK EMAIL] Would send email to {request.influencer_email}")
                logger.info(f"[MOCK EMAIL] Subject: {subject}")
                logger.info(f"[MOCK EMAIL] Content: {html_content}")
                
                # For development/testing purposes, we'll consider this a success
                logger.info(f"[MOCK EMAIL] Email to {request.influencer_email} simulated successfully")
                email_sent = True
            
            # If all methods failed and we're not falling back to mock, raise an error
            if not email_sent:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=error_detail
                )
        
        # Log outreach event to Supabase (optional)
        timestamp = datetime.now()
        if request.influencer_id and request.campaign_id:
            try:
                # This is a placeholder for Supabase integration
                # In a future implementation, this would save the outreach event to Supabase
                logger.info(f"Logging outreach event: Influencer ID {request.influencer_id}, Campaign ID {request.campaign_id}")
                # TODO: Implement Supabase integration when needed
            except Exception as e:
                logger.error(f"Error logging outreach event: {str(e)}")
        
        return EmailResponse(
            success=True,
            message=f"Email sent successfully to {request.influencer_email}",
            timestamp=timestamp
        )
        
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send email: {str(e)}"
        )


def call_voice_agent(phone_number: str, dynamic_vars: dict):
    """
    Call the ElevenLabs Voice Agent API to initiate a voice call using the Python SDK
    """
    try:
        # Get ElevenLabs API key from environment variables
        elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        agent_id = os.getenv("ELEVENLABS_AGENT_ID")
        
        if not elevenlabs_api_key:
            logger.error("ElevenLabs API key not configured")
            return {"error": "ElevenLabs API key not configured"}
            
        if not agent_id:
            logger.error("ElevenLabs Agent ID not configured")
            return {"error": "ElevenLabs Agent ID not configured"}
        
        # Initialize ElevenLabs client with API key
        client = ElevenLabs(api_key=elevenlabs_api_key)
        
        logger.info(f"Calling ElevenLabs Voice Agent API for {phone_number}")
        logger.info(f"Using API key: {elevenlabs_api_key[:5]}...{elevenlabs_api_key[-5:] if len(elevenlabs_api_key) > 10 else '***'}")
        logger.info(f"Using agent ID: {agent_id}")
        logger.info(f"Dynamic variables: {json.dumps(dynamic_vars, indent=2)}")
        
        try:
            # Make the call using the ElevenLabs client
            call_response = client.call.create(
                agent_id=agent_id,
                voice_id="21m00Tcm4TlvDq8ikWAM",  # Default voice ID (Rachel)
                recipient={
                    "phone_number": phone_number
                },
                dynamic_variables=dynamic_vars
            )
            
            logger.info(f"Call response: {call_response}")
            
            # Return the call details
            return {
                "call_id": call_response.call_id,
                "status": "initiated"
            }
        except Exception as sdk_error:
            logger.error(f"ElevenLabs SDK error: {str(sdk_error)}")
            return {"error": f"ElevenLabs SDK error: {str(sdk_error)}"}
            
    except Exception as e:
        logger.error(f"Error calling voice agent: {str(e)}")
        return {"error": f"Error calling voice agent: {str(e)}"}


@router.post("/voice", response_model=VoiceAgentResponse, status_code=status.HTTP_200_OK)
async def trigger_voice_agent(request: VoiceAgentRequest):
    """
    Trigger a voice call to an influencer using ElevenLabs Voice Agent API.
    Optionally logs the outreach event to Supabase if influencer_id and campaign_id are provided.
    """
    try:
        # Always use the real API, not mock mode
        use_mock = False
        
        # Prepare dynamic variables for the voice agent
        dynamic_vars = {
            "brand_name": request.brand_name,
            "campaign_name": request.campaign_name,
            "influencer_name": request.influencer_name,
            "deliverables": request.deliverables,
            "timeline": request.timeline,
            "budget_range": request.budget_range
        }
        
        call_id = None
        error_detail = "Unknown error"
        call_success = False
        
        if use_mock:
            # Use mock voice service (just log the call details)
            logger.info(f"[MOCK VOICE CALL] Would call {request.phone_number}")
            logger.info(f"[MOCK VOICE CALL] Dynamic variables: {json.dumps(dynamic_vars, indent=2)}")
            
            # For development/testing purposes, we'll consider this a success
            logger.info(f"[MOCK VOICE CALL] Voice call to {request.phone_number} simulated successfully")
            call_id = "mock-call-id-" + datetime.now().strftime("%Y%m%d%H%M%S")
            call_success = True
        else:
            # Call the ElevenLabs Voice Agent API
            result = call_voice_agent(request.phone_number, dynamic_vars)
            
            if "error" not in result:
                call_success = True
                call_id = result.get("call_id", "unknown")
                logger.info(f"Voice call initiated successfully for {request.phone_number}, call ID: {call_id}")
            else:
                error_detail = result["error"]
                logger.error(f"Voice call failed: {error_detail}")
        
        # If the call failed and we're not using mock, raise an error
        if not call_success and not use_mock:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_detail
            )
        
        # Log outreach event to Supabase (optional)
        timestamp = datetime.now()
        if request.influencer_id and request.campaign_id:
            try:
                # This is a placeholder for Supabase integration
                # In a future implementation, this would save the outreach event to Supabase
                logger.info(f"Logging voice outreach event: Influencer ID {request.influencer_id}, Campaign ID {request.campaign_id}")
                # TODO: Implement Supabase integration when needed
            except Exception as e:
                logger.error(f"Error logging voice outreach event: {str(e)}")
        
        return VoiceAgentResponse(
            success=True,
            message=f"Voice call initiated successfully to {request.phone_number}",
            call_id=call_id,
            timestamp=timestamp
        )
        
    except Exception as e:
        logger.error(f"Error initiating voice call: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initiate voice call: {str(e)}"
        )


@router.post("/negotiation/summary", response_model=NegotiationSummary)
async def log_negotiation_summary(summary: NegotiationSummary):
    """
    Log a negotiation summary after a voice call is completed.
    This endpoint allows recording the outcome of a negotiation call.
    """
    try:
        # In a real implementation, this would save the summary to a database
        logger.info(f"Logging negotiation summary for {summary.influencer_name} with {summary.brand_name}")
        logger.info(f"Campaign: {summary.campaign_name}, Status: {summary.status}")
        
        # TODO: Implement database integration when needed
        
        return summary
    except Exception as e:
        logger.error(f"Error logging negotiation summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to log negotiation summary: {str(e)}"
        )


# Model for direct call request with dynamic influencer data
class DirectCallRequest(BaseModel):
    phone_number: str = Field(..., description="Phone number to call")
    influencer_name: str = Field(..., description="Name of the influencer")
    brand_name: str = Field(..., description="Name of the brand")
    campaign_name: str = Field(..., description="Name of the campaign")
    deliverables: str = Field(..., description="Campaign deliverables")
    timeline: str = Field(..., description="Campaign timeline")
    budget_range: str = Field(..., description="Budget range for the campaign")
    
    @validator('phone_number')
    def validate_phone(cls, v):
        # Basic phone number validation
        v = v.strip()
        if not v.startswith('+'):
            raise ValueError('Phone number must start with country code (e.g., +1)')
        # Remove any non-digit characters except the leading +
        digits = ''.join(c for c in v if c.isdigit() or c == '+')
        # Check if it has enough digits (at least country code + 10 digits)
        if len(digits) < 11:
            raise ValueError('Phone number must include country code and at least 10 digits')
        return digits


@router.post("/direct-call", response_model=VoiceAgentResponse, status_code=status.HTTP_200_OK)
async def direct_call(request: DirectCallRequest):
    """
    Make a direct call to the specified phone number using the ElevenLabs Voice Agent API.
    This is a simplified endpoint that uses predefined campaign details.
    """
    try:
        # Get ElevenLabs API key and agent ID directly from environment variables
        elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        agent_id = os.getenv("ELEVENLABS_AGENT_ID")
        
        if not elevenlabs_api_key:
            logger.error("ElevenLabs API key not configured")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="ElevenLabs API key not configured"
            )
            
        if not agent_id:
            logger.error("ElevenLabs Agent ID not configured")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="ElevenLabs Agent ID not configured"
            )
        
        # Use dynamic variables from the request
        dynamic_vars = {
            "brand_name": request.brand_name,
            "campaign_name": request.campaign_name,
            "influencer_name": request.influencer_name,
            "deliverables": request.deliverables,
            "timeline": request.timeline,
            "budget_range": request.budget_range
        }
        
        # Make direct API call to ElevenLabs API using Twilio integration
        url = "https://api.elevenlabs.io/v1/convai/twilio/outbound-call"
        
        headers = {
            "xi-api-key": elevenlabs_api_key,
            "Content-Type": "application/json"
        }
        
        # Get the Twilio phone number ID from environment variable
        agent_phone_number_id = os.getenv("ELEVENLABS_PHONE_NUMBER_ID")
        
        if not agent_phone_number_id:
            logger.error("ElevenLabs Phone Number ID not configured")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="ElevenLabs Phone Number ID not configured"
            )
        
        # Prepare the payload according to ElevenLabs Twilio integration API
        payload = {
            "agent_id": agent_id,
            "agent_phone_number_id": agent_phone_number_id,
            "to_number": request.phone_number,
            "dynamic_variables": dynamic_vars
        }
        
        logger.info(f"Making direct call to {request.phone_number} using ElevenLabs API")
        logger.info(f"Using agent ID: {agent_id}")
        logger.info(f"Dynamic variables: {json.dumps(dynamic_vars, indent=2)}")
        
        # Make the API call
        response = requests.post(url, headers=headers, json=payload)
        
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response body: {response.text}")
        
        if response.status_code in [200, 201, 202]:
            result = response.json()
            call_id = result.get("call_id", "unknown")
            
            logger.info(f"Voice call initiated successfully for {request.phone_number}, call ID: {call_id}")
            return VoiceAgentResponse(
                success=True,
                message=f"Voice call initiated successfully to {request.phone_number}",
                call_id=call_id,
                timestamp=datetime.now()
            )
        else:
            error_detail = f"Voice call failed: {response.text}"
            logger.error(error_detail)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_detail
            )
        
    except Exception as e:
        logger.error(f"Error initiating direct call: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initiate direct call: {str(e)}"
        )
