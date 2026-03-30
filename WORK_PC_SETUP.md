# Work PC Setup

## Required Tools

- Git with HTTPS access to the private GitHub repo
- Docker Desktop with WSL2 enabled
- Node.js

## Clone And Start

```bash
git clone https://github.com/meshack-vs-you-all/wellness_solutions.git
cd wellness_solutions/frontend
npm install
npm run build:wordpress
cd ..
cp .env.wordpress.example .env.wordpress
bash scripts/local-wordpress-up.sh
```

## WordPress After Bootstrap

1. Log in to `/wp-admin/`
2. Install `WooCommerce`
3. Install `LifterLMS`
4. Install `Paystack for WooCommerce`
5. Install `Elementor`
6. Configure `Brevo`
7. Connect `Bunny Stream`
8. Connect `Cal.com`
9. Connect `Pabbly` to `QuickBooks`

## What Git Does Not Reproduce

- Local Docker volumes
- The live WordPress database contents
- Installed plugin settings unless re-entered or exported
- `.env.wordpress`
- Built assets under `wordpress/wp-content/themes/wellness-solutions/assets/app`
- `frontend/node_modules`

## Reference Files

Versioned in GitHub:

- `WORDPRESS_SETUP_DATA.md`
- `WORK_PC_SETUP.md`

Client source documents currently local-only on this machine unless you push them with working Git credentials:

- `Jaffet-Platform-Proposal-Final.pdf`
- `WSK_Knowledge_Base.xlsx`
- `WSK_NotebookLM.docx`
