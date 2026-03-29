<?php

if (!defined('ABSPATH')) {
    exit;
}

get_header();
?>
<main class="wellness-solutions-shell">
    <div id="wellness-solutions-app"></div>
    <?php if (!file_exists(get_stylesheet_directory() . '/assets/app/.vite/manifest.json') && !(defined('WS_VITE_DEV_SERVER') && WS_VITE_DEV_SERVER)) : ?>
        <section class="wellness-solutions-missing-build">
            <h1><?php esc_html_e('Wellness Solutions theme is installed.', 'wellness-solutions'); ?></h1>
            <p><?php esc_html_e('Build the frontend before using this theme in production.', 'wellness-solutions'); ?></p>
            <p><code>cd frontend && npm install && npm run build:wordpress</code></p>
        </section>
    <?php endif; ?>
</main>
<?php
get_footer();
