<?php
/**
 * ZIP Helper for Sitemap Extractor
 */

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    exit;
}

$data = json_decode(file_get_contents('php://input'), true);
$urls = $data['urls'] ?? [];

if (empty($urls)) {
    exit;
}

$zip = new ZipArchive();
$filename = tempnam(sys_get_temp_dir(), 'zip');

if ($zip->open($filename, ZipArchive::CREATE) !== TRUE) {
    exit("cannot open <$filename>\n");
}

$content = implode("\n", $urls);
$zip->addFromString("sitemap_urls.txt", $content);
$zip->close();

header('Content-Type: application/zip');
header('Content-Disposition: attachment; filename="sitemap_urls.zip"');
header('Content-Length: ' . filesize($filename));

readfile($filename);
unlink($filename);
