import os
from airtop import Airtop
import time

def login_to_linkedin(email, password):
    """
    Login to LinkedIn using Airtop AI browser automation
    
    Args:
        email (str): LinkedIn email
        password (str): LinkedIn password
    
    Returns:
        dict: Session information for further operations
    """
    # Initialize Airtop client
    airtop = Airtop(api_key=os.getenv("AIRTOP_API_KEY"))
    
    try:
        # Create a new browser session
        session_response = airtop.sessions.create()
        session_id = session_response.data.id
        print(f"✅ Created Airtop session: {session_id}")
        
        # Store session info for later use
        session_info = {
            'client': airtop,
            'session_id': session_id,
            'session_data': session_response.data
        }
        
        # Navigate to LinkedIn login page using windows API
        print("🌐 Navigating to LinkedIn login page...")
        navigate_response = airtop.windows.create(
            session_id=session_id,
            url="https://www.linkedin.com/login"
        )
        
        window_id = navigate_response.data.window_id
        session_info['window_id'] = window_id
        
        print("📝 Please complete the login manually in the Airtop browser...")
        print("⏳ Waiting 30 seconds for manual login completion...")
        time.sleep(30)  # Give time for manual login
        
        return session_info
        
    except Exception as e:
        print(f"❌ Error creating Airtop session: {e}")
        print("📖 Please check:")
        print("   1. Your AIRTOP_API_KEY is correctly set in .env file")
        print("   2. You have sufficient credits in your Airtop account")
        print("   3. Your internet connection is stable")
        raise