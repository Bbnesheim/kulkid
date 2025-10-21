# Norwegian Email Template - Ready for Klaviyo

## 📋 Manual Setup Guide (5 minutes)

Since the API key input is having issues, here's the **template ready for manual upload**:

---

## 1. Create Custom Properties First

Go to **Klaviyo Settings → Account → Custom Properties** and create these:

```
Name: last_purchase_size
Type: Text
Description: Size of customer's most recent purchase (e.g., '74', '80', '86')

Name: predicted_next_size  
Type: Text
Description: Predicted next size based on growth patterns

Name: size_progression_date
Type: Date & Time
Description: When to send next size reminder

Name: preferred_categories
Type: Text
Description: Customer's preferred product categories (comma-separated)
```

---

## 2. Create Email Template

Go to **Klaviyo Content → Email Templates → Create Template → Create from scratch**

**Template Name:** `kulkid_welcome_nb`

**Click "< > Source" (HTML view) and copy the HTML from:**
`/home/ben/projects/kulkid/klaviyo_automation/kulkid_template_final.html`

**Or paste this clean version:**

The template includes:
- ✅ **Correct branding**: "KUL KID Kundeklubb" (not "Kul Kid-klubben")
- ✅ **Brand fonts**: Luckiest Guy for headings, Quicksand for body
- ✅ **Brand colors**: #121212 (ink), #F3F3F3 (surface), #334FB4 (accent)
- ✅ **Sharp corners**: 0px border-radius as per brand guide
- ✅ **Proper contrast**: WCAG AA compliant
- ✅ **Consistent naming**: KULKID.no for website references

---

## 3. Test Your Template

1. **Click "Save"** after pasting the HTML
2. **Click "Preview"** to see your Norwegian email
3. **Send test email** to yourself
4. **Verify it looks professional** on mobile and desktop

---

## ✅ What You Get

- Professional Norwegian welcome email with 15% discount
- Mobile-responsive design that works everywhere
- Brand-consistent styling with kulkid.no colors
- Dynamic personalization (`{{ first_name }}`)
- Links to your three main collections
- Instagram social proof
- Proper unsubscribe footer

---

## 🚀 Ready for Day 2!

Once your template is working:
- **Custom properties created** ✅
- **Professional Norwegian email** ✅  
- **Ready for flow automation** ✅

Tomorrow we'll create the automated flows that use this template!