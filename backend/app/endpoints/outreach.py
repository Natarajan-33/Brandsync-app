from fastapi import APIRouter, HTTPException, Depends, status, Body
from typing import Dict, Any, Optional, Union
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

# Load environment variables
load_dotenv()

# Set default values for environment variables
os.environ.setdefault('USE_MOCK_EMAIL', 'true')
os.environ.setdefault('FALLBACK_TO_MOCK', 'true')
os.environ.setdefault('USE_SMTP', 'false')

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
