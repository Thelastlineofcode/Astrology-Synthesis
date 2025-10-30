#!/bin/bash
# Rename design assets to descriptive names
# Run from: docs/redesign/

echo "Renaming design assets..."

# Rename generated-image files (likely logo concepts)
mv "generated-image.png" "logo-concept-01.png" 2>/dev/null && echo "✓ logo-concept-01.png"
mv "generated-image (1).png" "logo-concept-02.png" 2>/dev/null && echo "✓ logo-concept-02.png"
mv "generated-image (2).png" "logo-concept-03.png" 2>/dev/null && echo "✓ logo-concept-03.png"
mv "generated-image (3).png" "logo-concept-04.png" 2>/dev/null && echo "✓ logo-concept-04.png"
mv "generated-image (4).png" "logo-concept-05.png" 2>/dev/null && echo "✓ logo-concept-05.png"

# Rename image files (likely planet renders or other assets)
mv "image.png" "asset-01.png" 2>/dev/null && echo "✓ asset-01.png"
mv "image (6).png" "asset-02.png" 2>/dev/null && echo "✓ asset-02.png"
mv "image (7).png" "asset-03.png" 2>/dev/null && echo "✓ asset-03.png"
mv "image (8).png" "asset-04.png" 2>/dev/null && echo "✓ asset-04.png"
mv "image (9).png" "asset-05.png" 2>/dev/null && echo "✓ asset-05.png"
mv "image (10).png" "asset-06.png" 2>/dev/null && echo "✓ asset-06.png"
mv "image (11).png" "asset-07.png" 2>/dev/null && echo "✓ asset-07.png"
mv "image (12).png" "asset-08.png" 2>/dev/null && echo "✓ asset-08.png"
mv "image (13).png" "asset-09.png" 2>/dev/null && echo "✓ asset-09.png"
mv "image (14).png" "asset-10.png" 2>/dev/null && echo "✓ asset-10.png"
mv "image (15).png" "asset-11.png" 2>/dev/null && echo "✓ asset-11.png"
mv "image (16).png" "asset-12.png" 2>/dev/null && echo "✓ asset-12.png"
mv "image (17).png" "asset-13.png" 2>/dev/null && echo "✓ asset-13.png"
mv "image (18).png" "asset-14.png" 2>/dev/null && echo "✓ asset-14.png"
mv "image (19).png" "asset-15.png" 2>/dev/null && echo "✓ asset-15.png"

echo ""
echo "✅ Renaming complete!"
echo ""
echo "Files renamed:"
echo "  - 5 logo concepts: logo-concept-01.png through logo-concept-05.png"
echo "  - 15 assets: asset-01.png through asset-15.png"
echo ""
echo "Next: Visually inspect files to further categorize them"
echo "  (e.g., planet renders, icons, UI components, etc.)"
