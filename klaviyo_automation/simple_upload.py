#!/usr/bin/env python3
"""
Simple Klaviyo Template Upload
Uploads Norwegian email template via Klaviyo API
"""

import requests
import json

def upload_template(api_key):
    """Upload the Norwegian welcome template to Klaviyo"""
    
    headers = {
        "Authorization": f"Klaviyo-API-Key {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "revision": "2024-10-15"
    }
    
    # Norwegian Welcome Email Template
    html_template = """<!DOCTYPE html>
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

    # Simple text version
    text_version = """
Velkommen til Kul Kid-klubben!

Tusen takk for at du ble med i Kul Kid-klubben!

Din personlige rabattkode: KULKID15
Gyldig i 7 dager

Vi ser frem til å hjelpe deg finne de perfekte klærne!

Besøk våre kolleksjoner:
- BASICS: Tidløse favoritter
- SUPERHELTER: For de tøffeste  
- GYMTIME: Komfort i hverdagen

Kul shopping!
Teamet på kulkid.no

Følg oss på Instagram: @kulkid.no
    """

    data = {
        "data": {
            "type": "template",
            "attributes": {
                "name": "kulkid_welcome_nb_v2",
                "editor_type": "CODE",
                "html": html_template,
                "text": text_version.strip()
            }
        }
    }
    
    response = requests.post(
        "https://a.klaviyo.com/api/templates/",
        headers=headers,
        json=data
    )
    
    if response.status_code in [200, 201]:
        print("✅ Norwegian welcome template created successfully!")
        print("📧 Template name: kulkid_welcome_nb_v2")
        print("🎯 Ready to use in welcome flows!")
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Details: {response.text}")
        return False

def main():
    print("🚀 Simple Klaviyo Template Upload")
    print("=" * 40)
    
    api_key = input("Enter your Klaviyo Private API Key: ").strip()
    
    if not api_key:
        print("❌ API key required!")
        return
    
    print("\n📧 Uploading Norwegian welcome email template...")
    
    success = upload_template(api_key)
    
    if success:
        print("\n✅ SUCCESS!")
        print("\nNext steps:")
        print("1. Go to Klaviyo → Content → Email Templates")
        print("2. Find 'kulkid_welcome_nb_v2'")
        print("3. Send a test email to yourself")
        print("4. Ready to create welcome flow!")
        
        print("\n📋 Custom properties to create manually:")
        print("• last_purchase_size (Text)")
        print("• predicted_next_size (Text)")  
        print("• size_progression_date (Date/Time)")
        print("• preferred_categories (Text)")
        print("\nGo to Settings → Account → Custom Properties")
    else:
        print("\n❌ Upload failed. Check your API key and try again.")

if __name__ == "__main__":
    main()