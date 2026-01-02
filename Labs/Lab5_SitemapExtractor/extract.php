<?php
/**
 * Sitemap Extractor Backend
 * Recursively fetches URLs from a sitemap XML.
 */

header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['error' => 'Method not allowed']);
    exit;
}

$data = json_decode(file_get_contents('php://input'), true);
$sitemapUrl = $data['url'] ?? '';

if (empty($sitemapUrl) || !filter_var($sitemapUrl, FILTER_VALIDATE_URL)) {
    echo json_encode(['error' => 'Invalid Sitemap URL']);
    exit;
}

class SitemapExtractor
{
    private $urls = [];
    private $processedSitemaps = [];

    public function extract($url)
    {
        if (in_array($url, $this->processedSitemaps)) {
            return;
        }
        $this->processedSitemaps[] = $url;

        $content = @file_get_contents($url);
        if ($content === false) {
            return;
        }

        try {
            $xml = new SimpleXMLElement($content);
        } catch (Exception $e) {
            return;
        }

        // Check for sitemap index
        if ($xml->getName() === 'sitemapindex') {
            foreach ($xml->sitemap as $sitemap) {
                if (isset($sitemap->loc)) {
                    $this->extract((string) $sitemap->loc);
                }
            }
        }
        // Check for standard sitemap
        elseif ($xml->getName() === 'urlset') {
            foreach ($xml->url as $urlItem) {
                if (isset($urlItem->loc)) {
                    $this->urls[] = (string) $urlItem->loc;
                }
            }
        }
    }

    public function getUrls()
    {
        return array_unique($this->urls);
    }
}

$extractor = new SitemapExtractor();
$extractor->extract($sitemapUrl);
$allUrls = $extractor->getUrls();

if (empty($allUrls)) {
    echo json_encode(['error' => 'No URLs found in sitemap.']);
} else {
    echo json_encode([
        'success' => true,
        'count' => count($allUrls),
        'urls' => $allUrls
    ]);
}
