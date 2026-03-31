<?php

declare(strict_types=1);

define('WP_INSTALLING', true);

require '/var/www/html/wp-load.php';
require_once ABSPATH . 'wp-admin/includes/upgrade.php';
require_once ABSPATH . 'wp-admin/includes/post.php';
require_once ABSPATH . 'wp-includes/rewrite.php';

$siteTitle = getenv('WORDPRESS_SITE_TITLE') ?: 'Wellness Solutions Local';
$adminUser = getenv('WORDPRESS_ADMIN_USER') ?: 'admin';
$adminPassword = getenv('WORDPRESS_ADMIN_PASSWORD') ?: 'ChangeMe123!';
$adminEmail = getenv('WORDPRESS_ADMIN_EMAIL') ?: 'dev@wellness.local';
$themeSlug = 'wellness-solutions';

if (!is_blog_installed()) {
    wp_install($siteTitle, $adminUser, $adminEmail, true, '', $adminPassword);
}

$theme = wp_get_theme($themeSlug);
if (!$theme->exists()) {
    fwrite(STDERR, "Theme '{$themeSlug}' was not found.\n");
    exit(1);
}

if (get_option('template') !== $themeSlug || get_option('stylesheet') !== $themeSlug) {
    switch_theme($themeSlug);
}

global $wp_rewrite;
$wp_rewrite->set_permalink_structure('/%postname%/');
flush_rewrite_rules();

function ensure_page(string $slug, string $title, string $template = ''): int
{
    $page = get_page_by_path($slug);
    $pageId = $page ? (int) $page->ID : 0;

    if ($pageId === 0) {
        $pageId = wp_insert_post(
            [
                'post_type' => 'page',
                'post_status' => 'publish',
                'post_title' => $title,
                'post_name' => $slug,
            ],
            true
        );

        if (is_wp_error($pageId)) {
            fwrite(STDERR, $pageId->get_error_message() . "\n");
            exit(1);
        }
    } else {
        $updateResult = wp_update_post(
            [
                'ID' => $pageId,
                'post_status' => 'publish',
                'post_title' => $title,
                'post_name' => $slug,
            ],
            true
        );

        if (is_wp_error($updateResult)) {
            fwrite(STDERR, $updateResult->get_error_message() . "\n");
            exit(1);
        }
    }

    if ($template !== '') {
        update_post_meta($pageId, '_wp_page_template', $template);
    }

    return $pageId;
}

// Core React shell entrypoints. These slugs can map to different app routes (hash router)
// while still being distinct WordPress pages for SEO, navigation, and permissions.
$shellTemplate = 'page-app-shell.php';
ensure_page('wellness-app', 'Wellness App', $shellTemplate);
ensure_page('login', 'Login', $shellTemplate);
ensure_page('join', 'Join / Sign up', $shellTemplate);
ensure_page('dashboard', 'Member Dashboard', $shellTemplate);
ensure_page('programmes', 'Corrective Programmes', $shellTemplate);
ensure_page('membership', 'Membership', $shellTemplate);
ensure_page('book', 'Book a Session', $shellTemplate);
ensure_page('movement-diagnostic', 'Movement Diagnostic', $shellTemplate);
