#!/usr/bin/env python3
"""
Klaviyo Template Upload Automation
Uploads all Norwegian email templates via Klaviyo API
"""

import requests
import json
import os
from typing import Dict, List

class KlaviyoAutomation:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://a.klaviyo.com/api"
        self.headers = {
            "Authorization": f"Klaviyo-API-Key {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "revision": "2024-10-15"
        }
    
    def create_template(self, name: str, subject: str, html_content: str, tags: List[str] = None) -> Dict:
        """Create email template in Klaviyo"""
        
        data = {
            "data": {
                "type": "template",
                "attributes": {
                    "name": name,
                    "editor_type": "CODE",
                    "html": html_content,
                    "text": self._html_to_text(html_content)
                }
            }
        }
            
        response = requests.post(
            f"{self.base_url}/templates/",
            headers=self.headers,
            json=data
        )
        
        if response.status_code in [200, 201]:
            print(f"✅ Template '{name}' created successfully!")
            return response.json()
        else:
            print(f"❌ Error creating template '{name}': {response.text}")
            return None
    
    def _html_to_text(self, html_content: str) -> str:
        """Convert HTML to plain text for email clients that don't support HTML"""
        # Simple text conversion - removes HTML tags
        import re
        text = re.sub('<[^<]+?>', '', html_content)
        text = text.replace('&nbsp;', ' ')
        return text.strip()
    
    def create_custom_property(self, name: str, property_type: str, description: str = "") -> Dict:
        """Create custom customer property using profile update"""
        # Klaviyo automatically creates properties when they're first used
        # We'll create a test profile with these properties to initialize them
        
        test_data = {
            "data": {
                "type": "profile",
                "attributes": {
                    "email": f"test_{name}@kulkid.no",
                    "properties": {
                        name: self._get_default_value(property_type)
                    }
                }
            }
        }
        
        response = requests.post(
            f"{self.base_url}/profiles/",
            headers=self.headers,
            json=test_data
        )
        
        if response.status_code in [200, 201]:
            print(f"✅ Custom property '{name}' initialized successfully!")
            # Clean up test profile
            self._cleanup_test_profile(f"test_{name}@kulkid.no")
            return response.json()
        else:
            print(f"⚠️  Property '{name}' setup - will be created on first use")
            print(f"   Description: {description}")
            return None
    
    def _get_default_value(self, property_type: str):
        """Get default value for property type"""
        if property_type.lower() == "datetime":
            return "2024-01-01T00:00:00Z"
        else:
            return "default_value"
    
    def _cleanup_test_profile(self, email: str):
        """Clean up test profile after property creation"""
        try:
            # Get profile ID
            response = requests.get(
                f"{self.base_url}/profiles/?filter=equals(email,\"{email}\")",
                headers=self.headers
            )
            if response.status_code == 200:
                profiles = response.json().get('data', [])
                if profiles:
                    profile_id = profiles[0]['id']
                    # Delete test profile
                    requests.delete(
                        f"{self.base_url}/profiles/{profile_id}/",
                        headers=self.headers
                    )
                    print(f"🧹 Cleaned up test profile for {email}")
        except Exception as e:
            print(f"Note: Test profile cleanup skipped ({str(e)})")

# Email Templates Dictionary
TEMPLATES = {
    "kulkid_welcome_nb": {
        "subject": "Velkommen til Kul Kid-klubben! 🎉 Her er din 15% rabatt",
        "tags": ["norwegian", "welcome", "discount"],
        "html": """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Velkommen til Kul Kid!</title>
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f8f9fa;">
    <table width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: #f8f9fa;">
        <tr>
            <td align="center">
                <table width="600" cellspacing="0" cellpadding="0" border="0" style="background-color: #ffffff; margin: 20px 0;">
                    <!-- Header -->
                    <tr>
                        <td align="center" style="padding: 40px 20px 20px; background-color: #ffffff;">
                            <h1 style="color: #2c3e50; font-size: 28px; margin: 0; font-weight: bold;">
                                Velkommen til Kul Kid-klubben, {{ first_name|default:"venn" }}! 🌟
                            </h1>
                        </td>
                    </tr>
                    <!-- Main Content -->
                    <tr>
                        <td style="padding: 0 40px 20px;">
                            <p style="font-size: 16px; line-height: 1.6; color: #555; margin-bottom: 20px;">
                                Tusen takk for at du ble med i Kul Kid-klubben!
                            </p>
                            <!-- Discount Code -->
                            <div style="background-color: #e8f5e8; border: 2px dashed #27ae60; padding: 20px; text-align: center; margin: 20px 0; border-radius: 8px;">
                                <p style="margin: 0; font-size: 14px; color: #555;">Din personlige rabattkode:</p>
                                <h2 style="color: #27ae60; font-size: 24px; margin: 10px 0; font-weight: bold; letter-spacing: 2px;">
                                    KULKID15
                                </h2>
                                <p style="margin: 0; font-size: 14px; color: #555;">
                                    Gyldig i 7 dager
                                </p>
                            </div>
                            <p style="font-size: 16px; line-height: 1.6; color: #555; margin-bottom: 20px;">
                                Vi ser frem til å hjelpe deg finne de perfekte klærne! Start gjerne med å se våre mest populære kolleksjoner:
                            </p>
                        </td>
                    </tr>
                    <!-- Collections -->
                    <tr>
                        <td style="padding: 0 40px;">
                            <table width="100%" cellspacing="0" cellpadding="10">
                                <tr>
                                    <td style="width: 33.33%; text-align: center; padding: 10px;">
                                        <a href="https://kulkid.no/collections/basics" style="text-decoration: none; color: #2c3e50;">
                                            <div style="border: 2px solid #ecf0f1; padding: 15px; border-radius: 8px; background-color: #f8f9fa;">
                                                <h3 style="margin: 0; font-size: 16px; font-weight: bold;">BASICS</h3>
                                                <p style="margin: 5px 0 0; font-size: 12px; color: #7f8c8d;">Tidløse favoritter</p>
                                            </div>
                                        </a>
                                    </td>
                                    <td style="width: 33.33%; text-align: center; padding: 10px;">
                                        <a href="https://kulkid.no/collections/superhelter" style="text-decoration: none; color: #2c3e50;">
                                            <div style="border: 2px solid #ecf0f1; padding: 15px; border-radius: 8px; background-color: #f8f9fa;">
                                                <h3 style="margin: 0; font-size: 16px; font-weight: bold;">SUPERHELTER</h3>
                                                <p style="margin: 5px 0 0; font-size: 12px; color: #7f8c8d;">For de tøffeste</p>
                                            </div>
                                        </a>
                                    </td>
                                    <td style="width: 33.33%; text-align: center; padding: 10px;">
                                        <a href="https://kulkid.no/collections/gymtime" style="text-decoration: none; color: #2c3e50;">
                                            <div style="border: 2px solid #ecf0f1; padding: 15px; border-radius: 8px; background-color: #f8f9fa;">
                                                <h3 style="margin: 0; font-size: 16px; font-weight: bold;">GYMTIME</h3>
                                                <p style="margin: 5px 0 0; font-size: 12px; color: #7f8c8d;">Komfort i hverdagen</p>
                                            </div>
                                        </a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- CTA Button -->
                    <tr>
                        <td align="center" style="padding: 30px 40px;">
                            <a href="https://kulkid.no" style="background-color: #27ae60; color: #ffffff; padding: 15px 30px; text-decoration: none; border-radius: 25px; font-weight: bold; font-size: 16px; display: inline-block;">
                                Kul shopping! 👕✨
                            </a>
                        </td>
                    </tr>
                    <!-- Social Media -->
                    <tr>
                        <td align="center" style="padding: 20px 40px 40px; border-top: 1px solid #ecf0f1;">
                            <p style="font-size: 14px; color: #7f8c8d; margin-bottom: 15px;">
                                P.S. Følg oss på Instagram for daglig inspirasjon!
                            </p>
                            <a href="https://instagram.com/kulkid.no" style="background-color: #e1306c; color: white; padding: 10px 20px; text-decoration: none; border-radius: 20px; font-size: 14px;">
                                @kulkid.no
                            </a>
                        </td>
                    </tr>
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f8f9fa; padding: 20px; text-align: center;">
                            <p style="font-size: 12px; color: #95a5a6; margin: 0;">
                                Teamet på kulkid.no<br>
                                <a href="{% unsubscribe_url %}" style="color: #95a5a6;">Avmeld deg her</a>
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""
    }
}

# Customer Properties to Create
CUSTOM_PROPERTIES = [
    {
        "name": "last_purchase_size",
        "type": "string",
        "description": "Size of customer's most recent purchase (e.g., '74', '80', '86')"
    },
    {
        "name": "predicted_next_size",
        "type": "string", 
        "description": "Predicted next size based on growth patterns"
    },
    {
        "name": "size_progression_date",
        "type": "datetime",
        "description": "When to send next size reminder"
    },
    {
        "name": "preferred_categories",
        "type": "string",
        "description": "Customer's preferred product categories (comma-separated)"
    }
]

def main():
    print("🚀 Klaviyo Automation Setup Starting...")
    
    # Get API key from environment or user input
    api_key = os.getenv('KLAVIYO_API_KEY')
    if not api_key:
        api_key = input("Enter your Klaviyo Private API Key: ").strip()
    
    if not api_key:
        print("❌ API key required. Get it from Klaviyo Settings → Account → API Keys")
        return
    
    klaviyo = KlaviyoAutomation(api_key)
    
    # Create custom properties
    print("\n📊 Creating custom customer properties...")
    for prop in CUSTOM_PROPERTIES:
        klaviyo.create_custom_property(
            prop["name"], 
            prop["type"], 
            prop["description"]
        )
    
    # Create email templates  
    print("\n📧 Creating Norwegian email templates...")
    for template_name, template_data in TEMPLATES.items():
        klaviyo.create_template(
            name=template_name,
            subject=template_data["subject"],
            html_content=template_data["html"],
            tags=template_data.get("tags", [])
        )
    
    print("\n✅ Klaviyo automation setup complete!")
    print("\nNext steps:")
    print("1. Check your Klaviyo dashboard for the new template")
    print("2. Test the welcome email template")
    print("3. Ready for Day 2 - Flow creation!")

if __name__ == "__main__":
    main()