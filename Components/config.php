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
?>