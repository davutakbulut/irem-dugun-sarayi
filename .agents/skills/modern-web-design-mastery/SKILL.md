---
name: modern-web-design-mastery
description: World-class modern web design & UI/UX mastery skill built from top-starred GitHub repositories (awesome-claude-design, awesome-web-prompts, awesome-openclaw-skills). Enforces high-end aesthetics, glassmorphism, micro-animations, curated HSL color palettes, responsive typography, and mobile-first layout design. Use when building or redesigning front-end landing pages, hero sections, and public web applications to achieve a WOW effect.
---

# 🎨 Modern Web Design & UI/UX Mastery Skill

This skill incorporates proven design system rules and visual guidelines distilled from top-starred GitHub UI/UX repositories (`awesome-claude-design`, `awesome-web-prompts`, `awesome-ai-coding-prompts`, and `awesome-openclaw-skills`).

---

## 💎 Core Design Principles

### 1. Visual Excellence & "WOW" Factor
- **Never default to basic browser colors** (plain red, plain blue, plain white). Use curated, high-contrast HSL color systems.
- **Dark Luxury Aesthetics**: Deep obsidian/slate backdrops (`#0B0C0E`, `#0F172A`, `#020617`) with rich champagne gold (`#F59E0B`, `#D97706`, `#FCD34D`) and sapphire accents.
- **Glassmorphism**: Subtle translucent panels with backdrop blur (`backdrop-blur-md`, `bg-slate-900/80`, `border-amber-500/30`).
- **Depth & Elevation**: Layering with soft multi-tier box shadows (`shadow-2xl`, `shadow-[0_20px_50px_rgba(217,119,6,0.25)]`).

### 2. Modern Typography Hierarchy
- **Primary Serif/Heading Font**: *Playfair Display* or *Outfit* for regal, high-end titles.
- **Body Font**: *Inter* or *Plus Jakarta Sans* for clean, legible text.
- **Monospace/Accent Font**: *Space Grotesk* for numbers, dates, capacity badges, and price tags.
- **Dynamic Gradient Text**: `.gold-gradient-text` (`bg-gradient-to-r from-amber-200 via-amber-400 to-amber-600 bg-clip-text text-transparent`).

### 3. Motion & Micro-Animations
- **Hover Transitions**: Smooth scale-up and glow (`transition-all duration-300 hover:scale-105 hover:shadow-amber-500/20`).
- **Interactive Badges**: Glowing pulses (`animate-pulse`, `border-amber-500/40 bg-amber-500/20`).
- **Smooth Page Scrolling**: `scroll-behavior: smooth`.

---

## 🏛️ Public Front-End Component System Standards

### A. Hero Section (First Impression)
- Full-viewport immersive layout (`min-h-[85vh]` or `min-h-screen`).
- Background: HD video overlay or high-res imagery with gradient backdrop overlay (`bg-gradient-to-b from-slate-950 via-slate-900/90 to-slate-950`).
- Prominent Call-to-Action (CTA): Primary gold button + Secondary 360° Virtual Tour trigger.

### B. Interactive Venue Showcase (Salonlarımız)
- Multi-column responsive grid (`grid-cols-1 md:grid-cols-2 lg:grid-cols-3`).
- Cards featuring cover image, capacity pill badge, feature list, and direct quote request button.

### C. 360° Matterport Virtual Tour Viewer
- Full-bleed embedded 3D viewer container (`iframe` with rounded glass border).

### D. Direct Communication Floating Action
- Floating WhatsApp button with pulse glow (`bg-emerald-500 hover:bg-emerald-600 text-white rounded-full shadow-2xl`).

---

## 🚀 Execution Workflow
1. **Inspect existing styles**: Verify CSS variables, Tailwind classes, and typography tokens.
2. **Apply Design Tokens**: Ensure no plain unstyled elements remain.
3. **Validate Responsiveness**: Mobile (<640px), Tablet (640px-1024px), Desktop (>1024px).
4. **Audit SEO & ARIA**: Single `<h1>`, descriptive `alt` tags, semantic `<header>`, `<main>`, `<footer>` tags.
