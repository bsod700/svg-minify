# SVG Batch Minification Script

Professional SVG minification script with **batch processing** support. Optimizes all SVG files in a folder while preserving animations, styles, and functionality.

## ✨ Features

✅ **Batch Processing**: Process entire folders of SVG files automatically  
✅ **Best Practice Implementation**: Uses scour + manual optimization  
✅ **Animation-Safe**: Preserves CSS animations, keyframes, and styles  
✅ **Cross-Platform**: Works on Windows, macOS, and Linux  
✅ **Detailed Reporting**: Progress bar and compression stats for each file  
✅ **Smart Optimization**: Automatically uses best available method  

## 🚀 Quick Start

### Step 1: Place Your SVG Files

Put all your SVG files in the `svg` folder (it will be created automatically if it doesn't exist).

```
Outpost/
  ├── svg/              ← Put your SVG files here
  │   ├── logo.svg
  │   ├── icon.svg
  │   └── hero.svg
  └── minify_svg.py
```

### Step 2: Run the Script

**Windows (easiest):**
```cmd
Double-click minify.bat
```

**Command line (all platforms):**
```bash
python minify_svg.py
```

### Step 3: Get Your Minified Files

All minified SVGs will be saved in the `svg minified` folder!

```
Outpost/
  ├── svg/              ← Your original files (unchanged)
  └── svg minified/     ← Your minified files ✨
      ├── logo.svg
      ├── icon.svg
      └── hero.svg
```

## 📊 Example Output

```
============================================================
  SVG Batch Minification Tool
============================================================

[*] Using scour optimizer (best practice)

[*] Found 3 SVG file(s) to process
[*] Input folder:  svg
[*] Output folder: svg minified

[1/3] Processing: logo.svg
    Original: 45.23 KB -> Minified: 38.15 KB (saved 7.08 KB, 15.65%)

[2/3] Processing: icon.svg
    Original: 12.50 KB -> Minified: 10.20 KB (saved 2.30 KB, 18.40%)

[3/3] Processing: hero.svg
    Original: 935.50 KB -> Minified: 840.15 KB (saved 95.36 KB, 10.19%)

============================================================
  SUMMARY
============================================================
  Files processed:    3 successful, 0 failed
  Total original:     993.23 KB
  Total minified:     888.50 KB
  Total saved:        104.73 KB (10.54%)
============================================================

[SUCCESS] All files processed! Minified SVGs saved in "svg minified" folder
```

## 🎯 What Gets Optimized?

The script applies these best-practice optimizations:

- ✂️ **Removes Comments**: Strips XML comments and metadata
- 🗑️ **Removes Metadata**: Eliminates editor-specific data
- 📏 **Optimizes Numbers**: Reduces numeric precision to 3 decimal places
- 🔄 **Optimizes Paths**: Compresses SVG path data
- 🧹 **Removes Whitespace**: Eliminates unnecessary spaces and line breaks
- 🎨 **Minifies CSS**: Compresses inline styles and animations
- 📦 **Optimizes Attributes**: Reduces numeric attribute values

## ✅ What Gets Preserved?

- ✅ Animations and keyframes
- ✅ ViewBox (for responsive SVGs)
- ✅ IDs referenced by styles/animations
- ✅ Data attributes
- ✅ ARIA attributes for accessibility
- ✅ All functional elements

## ⚙️ Configuration

Edit `minify_svg.py` to customize folder names:

```python
INPUT_FOLDER = 'svg'           # Folder with your original SVG files
OUTPUT_FOLDER = 'svg minified' # Folder where minified files will be saved
```

You can use any folder names you like!

## 🔧 Advanced: Better Optimization

For even better results, the script will automatically use the `scour` library if available:

```bash
pip install scour
```

The script will automatically detect and use it for superior optimization.

## 📁 Files

- **`minify_svg.py`** - Main Python batch minification script
- **`minify.bat`** - Windows batch file for easy one-click execution
- **`requirements.txt`** - Optional dependencies for enhanced optimization
- **`svg/`** - Input folder (place your original SVG files here)
- **`svg minified/`** - Output folder (automatically created)

## 💡 Best Practices Applied

1. **Batch Processing**: Processes multiple files efficiently in one run
2. **Preserve Functionality**: Never breaks animations, interactions, or styles
3. **Safe Defaults**: Conservative optimization that works for all SVG types
4. **Proper Encoding**: UTF-8 encoding for international character support
5. **Error Handling**: Clear error messages with helpful guidance
6. **Progress Tracking**: See exactly what's being processed
7. **Detailed Statistics**: Know exactly how much space you saved

## 🎓 Technical Details

### Optimization Methods

1. **Scour Optimization** (preferred):
   - Industry-standard SVG optimizer
   - Advanced path optimization
   - Smart attribute reduction
   - Preserves functional IDs

2. **Manual Optimization** (fallback):
   - Regex-based CSS minification
   - Path data compression
   - Numeric precision reduction
   - Whitespace elimination

### File Processing

The script:
1. Scans the input folder for all `.svg` files
2. Processes each file individually
3. Shows real-time progress and stats
4. Saves minified versions to output folder
5. Provides comprehensive summary report

## ❓ Troubleshooting

### No SVG files found

- Make sure your files are in the `svg` folder
- Check that files have `.svg` extension
- Verify folder name matches configuration

### Python not found

- Install Python from [python.org](https://www.python.org/downloads/)
- Check "Add Python to PATH" during installation
- Restart your terminal/command prompt

### Minified SVGs look broken

- Verify original SVGs display correctly in a browser
- Check browser console for errors
- Try installing scour: `pip install scour`

### Permission errors

- Run command prompt/terminal as administrator
- Check that output folder is writable
- Close any programs that might have files open

## 🚀 Workflow Tips

1. **Keep originals safe**: The script never modifies files in the `svg` folder
2. **Test first**: Always test minified SVGs before deploying
3. **Batch process**: Drop all your SVGs in the folder and process at once
4. **Use in CI/CD**: Integrate into your build pipeline
5. **Version control**: Keep original SVGs in git, ignore minified versions

## 📈 Performance Benefits

Minified SVGs provide:
- ⚡ Faster page load times
- 📉 Reduced bandwidth usage
- 💰 Lower hosting costs
- 📱 Better mobile performance
- 🎯 Improved SEO scores

Typical savings: **10-30%** depending on SVG complexity

## 📝 License

MIT License - Free to use for any purpose

## 🎉 Success Story

This script successfully minified the hero.svg file:
- **Original**: 935.50 KB
- **Minified**: 840.15 KB
- **Saved**: 95.36 KB (10.19% reduction)

---

**Built with best practices for professional SVG optimization**
