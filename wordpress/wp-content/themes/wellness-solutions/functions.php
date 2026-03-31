<?php

if (!defined('ABSPATH')) {
    exit;
}

function wellness_solutions_theme_setup(): void
{
    add_theme_support('title-tag');
    add_theme_support('post-thumbnails');
    add_theme_support('html5', array('search-form', 'comment-form', 'comment-list', 'gallery', 'caption', 'style', 'script'));

    register_nav_menus(
        array(
            'primary' => __('Primary Menu', 'wellness-solutions'),
        )
    );
}
add_action('after_setup_theme', 'wellness_solutions_theme_setup');

function wellness_solutions_theme_asset_path(string $relative = ''): string
{
    $base = get_stylesheet_directory() . '/assets/app';
    return $relative ? $base . '/' . ltrim($relative, '/') : $base;
}

function wellness_solutions_theme_asset_uri(string $relative = ''): string
{
    $base = get_stylesheet_directory_uri() . '/assets/app';
    return $relative ? $base . '/' . ltrim($relative, '/') : $base;
}

function wellness_solutions_theme_runtime_config(): array
{
    $uploads = wp_get_upload_dir();

    return array(
        'appMode' => 'wordpress',
        'routerMode' => 'hash',
        'appBasePath' => '/',
        'apiBaseUrl' => esc_url_raw(rest_url('wellness-solutions/v1')),
        'apiTimeout' => 30000,
        'publicAssetBaseUrl' => esc_url_raw(wellness_solutions_theme_asset_uri()),
        'mediaBaseUrl' => esc_url_raw($uploads['baseurl'] ?? ''),
        'authScheme' => 'Bearer',
        'wpRestNonce' => wp_create_nonce('wp_rest'),
        'siteUrl' => esc_url_raw(home_url('/')),
        'themeUrl' => esc_url_raw(get_stylesheet_directory_uri()),
    );
}

function wellness_solutions_collect_manifest_css(array $manifest, array $entry, array &$styles = array()): void
{
    if (!empty($entry['css'])) {
        foreach ($entry['css'] as $css_file) {
            $styles[$css_file] = $css_file;
        }
    }

    if (empty($entry['imports'])) {
        return;
    }

    foreach ($entry['imports'] as $import_key) {
        if (isset($manifest[$import_key])) {
            wellness_solutions_collect_manifest_css($manifest, $manifest[$import_key], $styles);
        }
    }
}

function wellness_solutions_enqueue_theme_app(): void
{
    $runtime_config = wellness_solutions_theme_runtime_config();
    $runtime_json = wp_json_encode($runtime_config, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);

    wp_enqueue_style(
        'wellness-solutions-theme',
        get_stylesheet_uri(),
        array(),
        wp_get_theme()->get('Version')
    );

    if (defined('WS_VITE_DEV_SERVER') && WS_VITE_DEV_SERVER) {
        $vite_server = untrailingslashit((string) WS_VITE_DEV_SERVER);

        wp_enqueue_script(
            'wellness-solutions-vite-client',
            $vite_server . '/@vite/client',
            array(),
            null,
            true
        );
        wp_script_add_data('wellness-solutions-vite-client', 'type', 'module');

        wp_enqueue_script(
            'wellness-solutions-app',
            $vite_server . '/index.tsx',
            array('wellness-solutions-vite-client'),
            null,
            true
        );
        wp_script_add_data('wellness-solutions-app', 'type', 'module');
        wp_add_inline_script('wellness-solutions-app', 'window.WellnessSolutionsConfig = ' . $runtime_json . ';', 'before');

        return;
    }

    $manifest_path = wellness_solutions_theme_asset_path('.vite/manifest.json');
    if (!file_exists($manifest_path)) {
        return;
    }

    $manifest = json_decode((string) file_get_contents($manifest_path), true);
    if (!is_array($manifest) || empty($manifest['index.html']['file'])) {
        return;
    }

    $entry = $manifest['index.html'];
    $styles = array();
    wellness_solutions_collect_manifest_css($manifest, $entry, $styles);

    foreach ($styles as $index => $css_file) {
        wp_enqueue_style(
            'wellness-solutions-app-' . $index,
            wellness_solutions_theme_asset_uri($css_file),
            array(),
            null
        );
    }

    wp_enqueue_script(
        'wellness-solutions-app',
        wellness_solutions_theme_asset_uri($entry['file']),
        array(),
        null,
        true
    );
    wp_script_add_data('wellness-solutions-app', 'type', 'module');
    wp_add_inline_script('wellness-solutions-app', 'window.WellnessSolutionsConfig = ' . $runtime_json . ';', 'before');
}
add_action('wp_enqueue_scripts', 'wellness_solutions_enqueue_theme_app');

function wellness_solutions_register_rest_routes(): void
{
    register_rest_route(
        'wellness-solutions/v1',
        '/health',
        array(
            'methods' => WP_REST_Server::READABLE,
            'permission_callback' => '__return_true',
            'callback' => static function (): WP_REST_Response {
                return new WP_REST_Response(
                    array(
                        'ok' => true,
                        'service' => 'wellness-solutions',
                        'timestamp' => time(),
                    ),
                    200
                );
            },
        )
    );

    register_rest_route(
        'wellness-solutions/v1',
        '/config',
        array(
            'methods' => WP_REST_Server::READABLE,
            'permission_callback' => '__return_true',
            'callback' => static function (): WP_REST_Response {
                return new WP_REST_Response(
                    array(
                        'restNamespace' => 'wellness-solutions/v1',
                        'restBaseUrl' => esc_url_raw(rest_url('wellness-solutions/v1')),
                        'siteUrl' => esc_url_raw(home_url('/')),
                        'themeUrl' => esc_url_raw(get_stylesheet_directory_uri()),
                    ),
                    200
                );
            },
        )
    );

    register_rest_route(
        'wellness-solutions/v1',
        '/me',
        array(
            'methods' => WP_REST_Server::READABLE,
            'permission_callback' => static function (): bool {
                return is_user_logged_in();
            },
            'callback' => static function (): WP_REST_Response {
                $user = wp_get_current_user();
                if (!$user || !$user->exists()) {
                    return new WP_REST_Response(array('error' => 'not_authenticated'), 401);
                }

                return new WP_REST_Response(
                    array(
                        'id' => (int) $user->ID,
                        'email' => (string) $user->user_email,
                        'displayName' => (string) $user->display_name,
                        'roles' => array_values((array) $user->roles),
                    ),
                    200
                );
            },
        )
    );
}
add_action('rest_api_init', 'wellness_solutions_register_rest_routes');
