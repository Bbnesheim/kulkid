# Day 1: Klaviyo Setup & First Norwegian Email Template
## Getting Started with Your Connected Account

---

## ✅ GREAT NEWS - YOU'RE AHEAD!

Since Klaviyo is already connected, let's jump straight into configuration and content creation.

---

## 🎯 TODAY'S TASKS (Day 1)

### Task 1: Configure Basic Settings (15 minutes)

1. **Go to Klaviyo Dashboard** (klaviyo.com)
2. **Navigate to Settings → Account**
3. **Set your business details:**
   - Company name: "kulkid.no"
   - Website: "https://kulkid.no"
   - Industry: "Fashion/Apparel"
   - Country: "Norway"
   - Currency: "NOK"
   - Timezone: "Europe/Oslo"

### Task 2: Set Up Customer Properties (10 minutes)

1. **Go to Settings → Account → Custom Properties**
2. **Create these properties** (click "Create Custom Property"):

```
Property Name: last_purchase_size
Type: Text
Description: Size of customer's most recent purchase (e.g., "74", "80", "86")

Property Name: predicted_next_size  
Type: Text
Description: Predicted next size based on growth patterns

Property Name: size_progression_date
Type: Date & Time
Description: When to send next size reminder

Property Name: preferred_categories
Type: List
Description: Customer's preferred product categories (basics, superhelter, etc.)
```

### Task 3: Create Your First Norwegian Email Template (30 minutes)

I'll provide you with the complete HTML template for your **Welcome Email**:

## 📧 WELCOME EMAIL TEMPLATE (Norwegian)

**Template Name:** `kulkid_welcome_nb`

**Subject Line Options (A/B Test These):**
- A: "Velkommen til Kul Kid-klubben! 🎉 Her er din 15% rabatt"
- B: "15% rabatt venter på deg + eksklusive barneklær-tips"  
- C: "Kul Kid hilser deg velkommen - din personlige rabatt er klar!"

**HTML Template to Copy/Paste:**

```html
<!DOCTYPE html>
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
                                    Gyldig til: {% now "Y-m-d"|add_days:7 %}
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
</html>
```

---

## 📝 HOW TO ADD THIS TEMPLATE TO KLAVIYO

### Step 1: Navigate to Templates
1. In your Klaviyo dashboard, go to **Content → Email Templates**
2. Click **"Create Template"**
3. Choose **"Create from scratch"**

### Step 2: Set Up Template
1. **Template Name:** `kulkid_welcome_nb`
2. **Template Tags:** Add `norwegian`, `welcome`, `discount`
3. Click **"Create Template"**

### Step 3: Add the HTML
1. In the template editor, click **"< > Source"** (HTML view)
2. **Delete all existing code**
3. **Copy and paste** the complete HTML template above
4. Click **"Save"**

### Step 4: Preview & Test
1. Click **"Preview"** to see how it looks
2. Click **"Send Test Email"** and send to your own email
3. Check both desktop and mobile views

---

## 🎯 WHAT YOU'RE LEARNING TODAY

### Email Marketing Concepts:
- **Merge tags** (`{{ first_name|default:"venn" }}`) - Dynamic personalization
- **Responsive design** - Works on all devices
- **Call-to-action** - Clear next steps for customers
- **Brand consistency** - Matches kulkid.no visual style

### Norwegian Marketing Best Practices:
- **Friendly tone** - "Tusen takk" and "venn" for warmth
- **Cultural relevance** - Norwegian expressions and emoji usage
- **Local urgency** - 7-day discount expiry creates action

---

## ✅ TODAY'S SUCCESS CHECKLIST

- [ ] Account settings configured
- [ ] Customer properties created
- [ ] Welcome email template created
- [ ] Template tested and previewed
- [ ] Test email sent to yourself

---

## 🚀 TOMORROW'S PREVIEW (Day 2)

Tomorrow we'll create:
- Cart abandonment email series (3 emails)
- Browse abandonment emails (2 emails) 
- Your first automated flow setup

**Time investment today:** ~1 hour
**Skills gained:** Klaviyo navigation, HTML email creation, Norwegian marketing copy

Ready for Day 2? Let me know when you've completed today's tasks!