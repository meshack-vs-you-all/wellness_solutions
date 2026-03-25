# 🎯 Wellness Solutions - Demo Master Guide
**Last Updated:** March 13, 2026 (Demo Ready)

This document serves as your single source of truth for the live demo. It covers the narrative, user personas, and a step-by-step walkthrough.

---

## 🛠️ Pre-Demo Setup Checklist (One-Click)
1. [ ] **Launch the System:** Open a terminal in the project root and run:
   ```bash
   bash LAUNCH_DEMO.sh
   ```
   *This starts both the backend and frontend in the background and clears old ports.*

2. [ ] **Wait for the "DEMO IS LIVE!" message.**
3. [ ] **Open Browser Tabs:**
   - Landing Page: `http://localhost:5173/`
   - Login Page: `http://localhost:5173/login`
   - Admin Panel: `http://localhost:8000/admin` (Optional backup)

---

## 👤 The 9 Demo Personas (Password: `demo123`)
*Note: These are already pre-seeded into your `db.sqlite3` file. You do NOT need to re-seed unless you intentionally want to wipe all history.*

| Persona | Email | Purpose |
| :--- | :--- | :--- |
| **Admin Alex** | `alex@jpf.com` | Show Analytics, Growth, and Master Schedule. |
| **Staff Steve** | `steve@jpf.com` | Show Instructor Dashboard & AI "✨ Prep Notes". |
| **David Desk** | `david@jpf.com` | Show "Smart Rebook" (suggests his usual Monday 10AM slot). |
| **Elena Exec** | `elena@jpf.com` | Show Upcoming Booking & Cancellation flow. |
| **Marcus Medic** | `marcus@jpf.com` | Show Loyalty history & Buying a 10-Session Package. |
| **Chloe Core** | `chloe@jpf.com` | Show Product Purchasing (Foam Rollers/Recovery Gear). |
| **Sarah Swift** | `sarah@jpf.com` | Show New User Welcome & Notifications. |
| **James Joy** | `james@jpf.com` | Show Gifting/Bundles. |
| **Tom Tracker** | `tom@jpf.com` | Show Window Shopping & High-value clinical items. |

---

## 🎭 The 15-Minute Demo Script

### **Act I: Conversion (0-4 Min)**
*   **Scene:** Landing Page.
*   **Narrative:** *"Sarah has back pain from sitting all day. She finds us online. Instead of a boring contact form, she uses our AI Therapist Matcher."*
*   **Action:** Go to `Landing Page`, type: *"My lower back is killing me after 10 hours at my desk."*
*   **The Wow:** Show the instant recommendation for Dr. Sarah Jenkins and the Spinal Decompression service.

### **Act II: Retention & AI (4-8 Min)**
*   **Scene:** Client Dashboard (Login as **David Desk**).
*   **Narrative:** *"David is a regular. We don't want him searching. Our Smart Rebook knows his routine."*
*   **Action:** Log in as `david@jpf.com`. Point to the **Smart Rebook** widget.
*   **The Wow:** *"It's already suggesting his usual Monday 10:00 AM slot. Frictionless."*
*   **Action 2:** Go to /bookings. Show his 2-month history we consolidated.

### **Act III: The Practice Store (8-12 Min)**
*   **Scene:** Wellness Essentials Page.
*   **Narrative:** *"The practice is now a commerce powerhouse. We sell clinical-grade recovery gear and session packages 24/7."*
*   **Action:** Click **Shop** (Wellness Essentials). Show the **10-Session Performance Pack**.
*   **Action 2:** Click on a "Clinical Grade Foam Roller."
*   **The Wow:** Explain how this increases the Average Order Value (AOV) without adding staff labor.

### **Act IV: Staff Efficiency (12-14 Min)**
*   **Scene:** Instructor Dashboard (Login as **Staff Steve**).
*   **Narrative:** *"Steve needs to prep for a busy day. He doesn't have time to dig through files."*
*   **Action:** Log in as `steve@jpf.com`. Click **"✨ Prep Notes"** next to David Desk's name.
*   **The Wow:** Show the AI-generated insight: *"VIP Client... historical tightness in right hip flexor."*

### **Act V: Business Intelligence (14-15 Min)**
*   **Scene:** Admin Dashboard (Login as **Admin Alex**).
*   **Narrative:** *"Finally, the practice owner sees it all: revenue growth, new user trends, and the true health of the business."*
*   **Action:** Log in as `alex@jpf.com`. Show the **Studio Analytics** charts.
*   **The Wow:** Point to the **Growth Rate** and **Total Revenue** (powered by the 40+ seeded bookings).

---

## 🆘 Backup Plans ("In Case of Fire")
*   **If AI Fails:** *"We're currently updating the model with fresh clinical data; the heuristic backup ensures the logic remains sound."*
*   **If Payment Fails:** *"Today's demo is in 'Clinic Bill' mode to bypass sensitive credit card data entry."*
*   **If Analytics are Empty:** *"We've just cleared the cache to start a fresh tracking cycle for this demo."*

---

## 🎯 Pro Tip: The "Mic Drop" Moment
At the very end, mention: **"This isn't just a booking tool. It's a revenue-generating ecosystem that learns from your patients to grow your practice."**
