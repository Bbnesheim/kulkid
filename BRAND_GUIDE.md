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
Based on current theme color schemes (settings_data.json):

- Primary (Ink): #121212 — headings, primary text, primary button bg on light.
- Background (Base): #FFFFFF — default page background.
- Surface (Subtle): #F3F3F3 — cards/alternate backgrounds.
- Dark Surface: #242833 — dark sections, overlays.
- Inverse Text: #FFFFFF — text on dark surfaces and on primary buttons.
- Accent (Cobalt): #334FB4 — highlight/accent sections (scheme-5).
- Shadow: #121212 (used for shadows/borders via opacity).

Accessibility guidance:
- On #FFFFFF, body text #121212 meets WCAG AA/AAA.
- On #242833, use #FFFFFF for text/buttons.
- Maintain minimum 4.5:1 contrast for body text and 3:1 for large text/icons.

Mapping to theme CSS variables:
- Button: background rgb(var(--color-button)), label rgb(var(--color-button-text))
- Link: rgb(var(--color-link))
- Foreground: rgb(var(--color-foreground))
- Background: rgb(var(--color-background))

Recommended usage:
- Primary buttons: #121212 background with #FFFFFF label.
- Secondary buttons: outline/ghost on #FFFFFF backgrounds.
- Badges: follow scheme text/background pairings for contrast.

## 4) Typography
Primary display (headings):
- Luckiest Guy (Google) — fun, chunky display for H1–H4 and hero text.
- Weight: 400 (family offers regular only); use tighter line-height and small positive letter-spacing.

Secondary/body:
- Quicksand — for body copy, UI, captions. Friendly geometric sans.
- Weights: 400/500/700. Default body ~400–500.

Implemented in theme (brand-overrides.css):
- Headings use Luckiest Guy; body remains Quicksand.
- CSS variables override heading family/weight while preserving Dawn type scale.

Editorial rules:
- Title case for H1/H2 in hero/section titles.
- Sentence case for H3–H6 and UI labels.
- Avoid all-caps in body copy; keep letter-spacing comfortable for readability.

## 5) Sizing & Scale
- Base font size: 16px (1.6rem at >=750px per theme).
- Heading scale (relative): as per Dawn defaults; adjust in Theme Editor if needed.
- Recommended practical sizes:
  - H1: ~40–52px desktop; ~30–40px mobile.
  - H2: ~24–32px.
  - Body: 16–18px; captions 12–14px.

## 6) Buttons & Corners
- Corners: 0 radius across buttons/cards/inputs (current settings). Keep sharp, confident edges.
- Shadows: minimal or none; rely on contrast and spacing rather than elevation.
- Variant pills: rounded (radius ~40) for playful selectors.

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
- Add new accent surfaces with scheme-5 (#334FB4) when highlighting promos.

CSS reference (tokens):
- Headings: font-family var(--font-heading-family), weight var(--font-heading-weight)
- Body: font-family var(--font-body-family)
- Colors: var(--color-foreground), var(--color-background), var(--color-button), var(--color-button-text), var(--color-link)

## 11) Do & Don’t
Do
- Use Luckiest Guy only for headings/hero and short labels.
- Keep high contrast and generous spacing.
- Use #334FB4 sparingly as accent, not for long text blocks.

Don’t
- Set body text in Luckiest Guy.
- Reduce contrast below WCAG AA.
- Over-animate or stack multiple strong effects.

## 12) Checklist
- [x] Luckiest Guy applied to headings.
- [x] Quicksand retained for body.
- [x] Color tokens aligned with theme schemes.
- [ ] Final approval on logo usage and any alternate colorways (brand/seasonal).

---
Generated from current repository theme settings and CSS. Update this guide when theme settings (colors, type scale) change.