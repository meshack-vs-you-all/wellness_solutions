# Wellness Solutions Frontend

This frontend is wired to run standalone in development and to build into the WordPress theme shell in `../wordpress/wp-content/themes/wellness-solutions`.

## Run Locally

```bash
npm install
npm run dev
npm run build:wordpress
```

## Notes

- API calls in this frontend are still legacy placeholders and need to be mapped to WordPress routes.
- Static assets in `public/` are copied into the WordPress theme build output.
- In WordPress mode the app reads runtime config from `window.WellnessSolutionsConfig`.
