# KULKID Brand Guide

Status: Draft v1 (derived from current live theme configuration and codebase)

## 1) Brand Essence
- Personality: Playful, bold, kid-first; approachable with simple shapes and high contrast.
- Values: Creativity, inclusivity, everyday fun.
- Voice & tone: Short, punchy, encouraging. Active verbs, few exclamation points. Avoid sarcasm; be clear and upbeat.

## 2) Logo
- Primary logo: shop image “Kul_Kid_Logo.svg” (theme setting points to Shopify file). Use on light backgrounds whenever possible.
- Minimum size: 24px height on mobile, 32px+ on desktop.
- Clear space: At least the height of the “K” around the mark.
- Don’ts: Do not skew, recolor outside the palette, or place on low-contrast backgrounds.

## 3) Color System
Brand colors are strictly two-tone:

- Black: #121212 — headings, body text, default CTA background.
- White: #FFFFFF — page background, inverse CTA text/background when needed.

Guidance:
- Maintain WCAG AA: use #121212 text on #FFFFFF backgrounds; use #FFFFFF text only on true-black (#121212) surfaces.
- Rainbow gradients are effect-only and do not constitute brand colors; always pair them with #121212 text.

Mapping tokens (keep minimal):
- Button bg: #121212; Button text: #FFFFFF (invert on dark surfaces only).
- Foreground text: #121212; Background: #FFFFFF.

## 3a) Rainbow Gradient Effects
Use sparingly (max 2–3 per page) and only in approved spots. Always use #121212 text on rainbow.

- Background rainbow (footer-only):
  - Animated linear-gradient background with keyframes shifting background-position.
  - Implemented in `sections/main-footer.liquid` with `animation: rainbowGradient {speed}s ease infinite; background-size: 1200% 1200%`.
  - Text and links within the footer must use #121212.

- Outline rainbow (component borders):
  - Pseudo-element (::before) creates an outer, blurred animated gradient border around a card/form.
  - Supports directions: diagonal (45deg), horizontal (90deg), vertical (180deg), or radial; patterns: smooth, wave, pulse.
  - Recommended for product cards, forms, and newsletter boxes; do not use on full-width sections.
  - Inside content must remain on solid background with #121212 text.

## 4) Typography
Primary display (headings):
- Luckiest Guy (Google) — fun, chunky display for H1–H4 and hero text.
- Weight: 400 (family offers regular only); use tighter line-height and small positive letter-spacing.
- Locking rule: Title headings must always use "Luckiest Guy"; do not override in sections/snippets.

Secondary/body:
- Quicksand — primary body font and secondary fallback for headings.
- Weights: 400/500/700. Default body ~400–500.

Implemented in theme (brand-overrides.css):
- Headings use Luckiest Guy with Quicksand fallback; body remains Quicksand.
- CSS variables override heading family/weight while preserving Dawn type scale.

Editorial rules:
- Title case for H1/H2 in hero/section titles.
- Sentence case for H3–H6 and UI labels.
- Avoid all-caps in body copy; keep letter-spacing comfortable for readability.

Example CSS:
```css path=null start=null
:root {
  --color-black: #121212;
  --color-white: #FFFFFF;
}
/* Headings */
h1, h2, h3, h4, h5, h6 {
  font-family: "Luckiest Guy", "Quicksand", system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
}
/* Body */
body, p, li, input, button {
  font-family: "Quicksand", system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
}
```

## 5) Sizing & Scale
- Base font size: 16px (1.6rem at >=750px per theme).
- Heading scale (relative): as per Dawn defaults; adjust in Theme Editor if needed.
- Recommended practical sizes:
  - H1: ~40–52px desktop; ~30–40px mobile.
  - H2: ~24–32px.
  - Body: 16–18px; captions 12–14px.

## 6) Buttons & Corners
- CTA default: black buttons with white text.
  - Background: `#121212`
  - Text: `#FFFFFF`
- On dark/black (`#121212`) page backgrounds: invert CTA for contrast.
  - Background: `#FFFFFF`
  - Text: `#121212`
- Border radius: always `2px` for buttons (cards/inputs may follow theme style).
- Shadows: minimal or none; rely on contrast and spacing rather than elevation.
- Variant pills: rounded (radius ~40) for playful selectors.

Example CSS:
```css path=null start=null
.btn, .button, button[type="submit"] {
  border-radius: 2px;
  background: var(--color-black);
  color: var(--color-white);
}
.on-dark .btn, .on-dark .button {
  background: var(--color-white);
  color: var(--color-black);
}
.btn:disabled { opacity: 0.6; cursor: not-allowed; }
```

## 7) Imagery
- Art direction: Bright, joyful, kid-centered. Simple backgrounds; focus on expression and color.
- Composition: Clear subject, generous whitespace; avoid clutter and heavy filters.
- Iconography: Line icons; maintain stroke consistency; avoid overly detailed pictograms.

## 8) Motion
- Subtle, swift (100–300ms). Favor fades/slide-ins over large parallax.
- Disable non-essential animations for reduced motion preference.

## 9) Copy Guidelines
- Use simple, concrete words. Short sentences.
- Speak to kids and caretakers; avoid jargon.
- Examples:
  - Do: “Build your bundle.” “Pick your colors.”
  - Don’t: “Leverage customizable multi-variant configurations.”

## 10) Asset Implementation Notes
- Fonts loaded via head preconnect + lazy CSS; headings forced to Luckiest Guy via CSS variables in assets/brand-overrides.css.
- Body remains Quicksand via theme settings.
- Footer rainbow background: implement animated gradient in `sections/main-footer.liquid` (`@keyframes rainbowGradient`, large background-size, animated position).
- Outline rainbow: implement via container `::before` with negative insets, gradient background, optional blur/hover speed changes.
- Product cards may use either static rainbow background or outline rainbow; in both cases, set text to #121212 and keep inner surface solid.

CSS reference (tokens):
- Headings: font-family var(--font-heading-family), weight var(--font-heading-weight)
- Body: font-family var(--font-body-family)
- Colors: var(--color-foreground), var(--color-background), var(--color-button), var(--color-button-text), var(--color-link)

## 11) Do & Don’t
Do
- Use Luckiest Guy only for headings/hero and short labels (locked); Quicksand for body and as heading fallback.
- Keep high contrast: #121212 on #FFFFFF; invert only on true-black backgrounds.
- Use rainbow background only in the footer; use outline or static rainbow on product cards as needed (max 2–3 total per page).
- Always use #121212 text on rainbow surfaces and keep inner content on a solid background.

Don’t
- Introduce additional brand colors beyond #121212 and #FFFFFF.
- Set body text in Luckiest Guy.
- Reduce contrast below WCAG AA or place light text on rainbow gradients.
- Over-animate or apply rainbow to full-width sections beyond the footer.

## 12) Checklist
- [x] Luckiest Guy applied to headings (locked) with Quicksand fallback.
- [x] Quicksand retained for body.
- [x] CTA rules implemented (black/white default, inverted on dark, 2px radius).
- [x] Rainbow usage: footer animated background; product cards outline/static; text #121212.
- [x] Brand colors restricted to #121212 and #FFFFFF only.
- [ ] Final approval on logo usage.

---
Generated from current repository theme settings and CSS. Update this guide when theme settings (colors, type scale) change.
