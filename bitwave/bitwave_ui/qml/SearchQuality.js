.pragma library

// Catalog availability, independent of the selected download quality.
function rank(quality) {
    var q = String(quality || "").toUpperCase().replace(/_/g, "-")
    if (q === "HI-RES" || q === "HIRES" || q === "HI-RES-LOSSLESS") return 4
    if (q === "LOSSLESS") return 3
    if (q === "HIGH") return 2
    if (q === "LOW") return 1
    return 0
}
function isHiRes(row) { return !!row && rank(row.quality) === 4 }
function audioResult(row) { return !!row && (row.kind === "album" || row.kind === "track") }
function select(rows, onlyHiRes) {
    return (rows || []).filter(function(row) { return !onlyHiRes || isHiRes(row) })
}
function byQuality(rows, ascending) {
    return rows.map(function(row, i) { return {row: row, index: i} })
        .sort(function(a, b) {
            var delta = rank(a.row.quality) - rank(b.row.quality)
            return delta ? (ascending ? delta : -delta) : a.index - b.index
        }).map(function(item) { return item.row })
}
