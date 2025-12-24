# SVG Minification Script

Professional SVG minification script with best practices. Optimizes SVG files while preserving animations, styles, and functionality.

## Features

✅ **Best Practice Implementation**: Manual optimization with proven techniques  
✅ **Animation-Safe**: Preserves CSS animations, keyframes, and styles  
✅ **Cross-Platform**: Works on Windows, macOS, and Linux  
✅ **Detailed Reporting**: Shows before/after sizes and compression ratio  
✅ **No Dependencies Required**: Works with standard Python (optional scour for better results)  

## Quick Start

### Windows

Simply double-click `minify.bat` or run from command line:

```cmd
minify.bat
```

### Command Line (All Platforms)

```bash
python minify_svg.py
```

## Results

The script successfully minified `hero.svg`:

```
Original size:  935.50 KB
Minified size:  842.13 KB
Saved:          93.37 KB (9.98%)
```

## What Gets Optimized?

The script applies these best-practice optimizations:

- ✂️ **Removes Comments**: Strips XML comments and metadata
- 🗑️ **Removes Metadata**: Eliminates editor-specific data
- 📏 **Optimizes Numbers**: Reduces numeric precision to 3 decimal places
- 🔄 **Optimizes Paths**: Compresses SVG path data
- 🧹 **Removes Whitespace**: Eliminates unnecessary spaces and line breaks
- 🎨 **Minifies CSS**: Compresses inline styles and animations
- 📦 **Optimizes Attributes**: Reduces numeric attribute values

## What Gets Preserved?

- ✅ Animations and keyframes
- ✅ ViewBox (for responsive SVGs)
- ✅ IDs referenced by styles/animations
- ✅ Data attributes
- ✅ ARIA attributes for accessibility
- ✅ All functional elements

## Configuration

Edit `minify_svg.py` to customize:

```python
INPUT_FILE = 'hero.svg'       # Change input filename
OUTPUT_FILE = 'hero.min.svg'   # Change output filename
```

## Advanced: Better Optimization with Scour

For even better results, install the industry-standard `scour` library:

```bash
pip install scour
```

Then run the script again. It will automatically use scour for enhanced optimization.

## Files

- `minify_svg.py` - Main Python minification script
- `minify.bat` - Windows batch file for easy execution
- `requirements.txt` - Optional dependencies for better optimization
- `hero.svg` - Original SVG file
- `hero.min.svg` - Minified output file

## Best Practices Applied

1. **Preserve Functionality**: Never breaks animations, interactions, or styles
2. **Safe Defaults**: Conservative optimization that works for all SVG types
3. **Proper Encoding**: UTF-8 encoding for international character support
4. **Error Handling**: Clear error messages with helpful guidance
5. **Cross-Platform**: Works on any system with Python installed
6. **Detailed Feedback**: Reports exact file size savings and compression ratio

## Technical Details

### Manual Optimization Process

1. Removes XML comments using regex
2. Minifies CSS in `<style>` tags while preserving keyframes
3. Optimizes SVG path `d` attribute values
4. Reduces numeric precision in coordinate attributes
5. Removes metadata tags
6. Eliminates unnecessary whitespace between tags
7. Preserves IDs, classes, and animation-related attributes

### Path Optimization

The script optimizes SVG paths by:
- Removing extra whitespace around path commands
- Reducing numeric precision to 3 decimal places
- Maintaining path accuracy while reducing file size

### CSS Minification

For `<style>` tags, the script:
- Removes CSS comments
- Eliminates unnecessary whitespace
- Preserves animation keyframes and timing
- Maintains selector specificity

## Troubleshooting

### Python not found

Install Python from [python.org](https://www.python.org/downloads/)  
Make sure to check "Add Python to PATH" during installation.

### The minified SVG looks broken

- Verify the original SVG displays correctly
- Check browser console for errors
- Try installing `scour` for more conservative optimization

### Permission errors when installing scour

Run the command prompt or terminal as administrator:

```bash
pip install scour
```

## Performance Tips

1. **Use minified SVGs in production** to reduce page load times
2. **Keep original SVGs for editing** - always work with the full version
3. **Test after minification** to ensure animations still work
4. **Consider SVG sprites** for multiple icons to reduce HTTP requests

## License

MIT License - Free to use for any purpose

## Support

For issues or questions, check that:
- Python is installed and in your PATH
- Input file exists and is valid SVG
- File permissions allow reading/writing
- The original SVG displays correctly in a browser

---

**Created with best practices for SVG optimization**
