$thresholdDate = (Get-Date).AddDays(-14)
$releases = gh release list --repo bpwhelan/GameSentenceMiner --limit 500 --json createdAt,tagName | ConvertFrom-Json


foreach ($release in $releases) {
    # Example line format: v1.2.3    Latest   2025-01-05
    #echo $releaseLine
    #$parts = $releaseLine -split "\s+"
    $tagName = $release.tagName
    $publishedDate = [DateTime]$release.createdAt
    echo $release
    
    if ($publishedDate -lt $thresholdDate) {
        gh release delete $tagName --repo bpwhelan/GameSentenceMiner
        gh tag delete $tagName --repo bpwhelan/GameSentenceMiner
    }
}