# Converting Mermaid Diagrams to PNG

All 4 flowcharts are saved as `.mmd` files in this directory. Here are several ways to convert them to PNG:

## 🎨 Option 1: Mermaid Live Editor (Easiest - No Install)

1. Go to: https://mermaid.live
2. Copy the contents of one of the `.mmd` files
3. Paste into the left panel in Mermaid Live
4. Click the download icon (⬇️) at the top right
5. Select "SVG" or "PNG"
6. Click "Download"

**Files to convert:**
- `1-application-flow.mmd` → Application Flow Chart
- `2-test-execution-flow.mmd` → Test Execution Detail
- `3-module-architecture.mmd` → Module Dependencies
- `4-data-flow.mmd` → Data Flow Through System

---

## 📦 Option 2: Command Line (For Automation)

Install mermaid-cli globally:
```bash
npm install -g @mermaid-js/mermaid-cli
```

Then convert all files at once:
```bash
mmdc -i 1-application-flow.mmd -o 1-application-flow.png
mmdc -i 2-test-execution-flow.mmd -o 2-test-execution-flow.png
mmdc -i 3-module-architecture.mmd -o 3-module-architecture.png
mmdc -i 4-data-flow.mmd -o 4-data-flow.png
```

Or use the batch script below (save as `convert.sh` on Linux/Mac or `convert.bat` on Windows):

**Linux/Mac (convert.sh):**
```bash
#!/bin/bash
for file in *.mmd; do
    mmdc -i "$file" -o "${file%.mmd}.png"
done
echo "All files converted to PNG!"
```

**Windows (convert.bat):**
```batch
@echo off
for %%f in (*.mmd) do (
    mmdc -i "%%f" -o "%%~nf.png"
)
echo All files converted to PNG!
```

---

## 🐳 Option 3: Docker (No Install Required)

If you have Docker:
```bash
docker run --rm -v $(pwd):/data minlag/mermaid-cli mmdc -i /data/1-application-flow.mmd -o /data/1-application-flow.png
```

---

## 🌐 Option 4: VS Code Extension

1. Install extension: "Markdown Preview Mermaid Support"
2. Open any `.mmd` file in VS Code
3. Right-click → "Export Diagram"
4. Choose PNG format

---

## ✅ Which Option to Use?

| Option | Best For | Effort |
|--------|----------|--------|
| **Mermaid Live** | Quick one-time conversion | ⭐ Easiest |
| **CLI** | Batch processing, automation | ⭐⭐ Easy |
| **Docker** | CI/CD pipelines | ⭐⭐⭐ Medium |
| **VS Code** | While editing | ⭐⭐ Easy |

---

## 📄 File Details

| Diagram | Filename | Best Use |
|---------|----------|----------|
| **Application Flow** | `1-application-flow.mmd` | Project overview, presentations |
| **Test Execution** | `2-test-execution-flow.mmd` | Understanding test logic |
| **Module Architecture** | `3-module-architecture.mmd` | Code structure, design docs |
| **Data Flow** | `4-data-flow.mmd` | System design, data pipeline |

---

## 🎯 Recommended Quick Steps

1. **Visit**: https://mermaid.live
2. **Drag and drop** the `.mmd` file into the left panel (or copy-paste contents)
3. **Click download icon** (⬇️) at the top right
4. **Select "SVG"** (better quality than PNG)
5. **Click Download**

That's it! You'll have high-quality, copyable diagrams.

---

## 💡 Pro Tips

- **SVG is better than PNG**: Smaller file size, scales infinitely, still viewable
- **Use for presentations**: Add PNG/SVG to your Senior Design presentation
- **Share with team**: All these diagrams fit perfectly in documentation
- **Version control**: Keep `.mmd` files in git, convert to images on demand

---

## 🐛 Troubleshooting

**Issue**: Mermaid Live shows error
- **Fix**: Check that the `.mmd` file uses valid Mermaid syntax (should be fine)

**Issue**: Downloaded image is blurry
- **Fix**: Download SVG instead of PNG, then convert SVG to PNG with better settings

**Issue**: CLI not working
- **Fix**: Ensure Node.js and npm are installed: `node --version && npm --version`

---

**All diagrams are ready to convert! Pick your favorite method above.** 🎨
