<?php
/**
 * Configuration file for Pablo Cirre Portfolio
 * Handles dynamic path generation for local and production environments
 */

$host = $_SERVER['HTTP_HOST'] ?? '';

// OS Check: Local is Windows (WAMP), Remote is Linux.
if (strtoupper(substr(PHP_OS, 0, 3)) === 'WIN') {
    define('BASE_URL', '/PabloCirre');
} else {
    define('BASE_URL', '');
}

if (!function_exists('pc_social_profiles')) {
    function pc_social_profiles(): array
    {
        return [
            'linkedin' => [
                'name' => 'LinkedIn',
                'url' => 'https://es.linkedin.com/in/pablocirre',
            ],
            'github' => [
                'name' => 'GitHub',
                'url' => 'https://github.com/PabloCirre',
            ],
            'x' => [
                'name' => 'X',
                'url' => 'https://x.com/PabloCirre',
                'handle' => '@PabloCirre',
            ],
            'instagram' => [
                'name' => 'Instagram',
                'url' => 'https://www.instagram.com/pablocirre/',
            ],
        ];
    }
}

if (!function_exists('pc_social_profile_urls')) {
    function pc_social_profile_urls(): array
    {
        return array_values(array_map(
            static fn(array $profile): string => $profile['url'],
            pc_social_profiles()
        ));
    }
}

if (!function_exists('pc_social_x_handle')) {
    function pc_social_x_handle(): string
    {
        $profiles = pc_social_profiles();
        return (string) ($profiles['x']['handle'] ?? '@PabloCirre');
    }
}
?>
