#!/usr/bin/env python3
"""
Professional SVG Minification Script
Uses scour - Industry-standard Python SVG optimizer

Best practices applied:
- Removes comments and metadata
- Optimizes paths and transforms
- Removes unnecessary whitespace
- Preserves animations and styling
- Maintains viewBox and dimensions
"""

import os
import sys
import re
import xml.etree.ElementTree as ET
from pathlib import Path

# Configuration
INPUT_FILE = 'hero.svg'
OUTPUT_FILE = 'hero.min.svg'


def format_bytes(bytes_size, decimals=2):
    """Format bytes to human-readable size"""
    if bytes_size == 0:
        return '0 Bytes'
    k = 1024
    sizes = ['Bytes', 'KB', 'MB', 'GB']
    i = 0
    size = float(bytes_size)
    while size >= k and i < len(sizes) - 1:
        size /= k
        i += 1
    return f"{size:.{decimals}f} {sizes[i]}"


def calculate_compression_ratio(original, compressed):
    """Calculate compression ratio"""
    return round((1 - compressed / original) * 100, 2)


def minify_css(css_content):
    """Minify CSS content in style tags"""
    # Remove comments
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    # Remove unnecessary whitespace
    css_content = re.sub(r'\s+', ' ', css_content)
    # Remove spaces around special characters
    css_content = re.sub(r'\s*([{}:;,>])\s*', r'\1', css_content)
    # Remove trailing semicolons
    css_content = re.sub(r';}', '}', css_content)
    return css_content.strip()


def optimize_number(value):
    """Optimize numeric values by removing unnecessary precision"""
    try:
        num = float(value)
        # Round to 3 decimal places for precision vs size balance
        rounded = round(num, 3)
        # Remove trailing zeros and decimal point if integer
        result = f"{rounded:.3f}".rstrip('0').rstrip('.')
        return result
    except (ValueError, TypeError):
        return value


def optimize_path_data(path_d):
    """Optimize SVG path data"""
    # Remove unnecessary whitespace
    path_d = re.sub(r'\s+', ' ', path_d)
    # Remove spaces around commands
    path_d = re.sub(r'\s*([MLHVCSQTAZmlhvcsqtaz])\s*', r'\1', path_d)
    # Optimize numbers in path
    numbers = re.findall(r'-?\d+\.?\d*', path_d)
    for num in numbers:
        if '.' in num:
            optimized = optimize_number(num)
            path_d = path_d.replace(num, optimized, 1)
    return path_d.strip()


def minify_svg_manual(svg_content):
    """
    Manual SVG minification with preservation of animations
    This is a best-practice implementation that handles complex SVGs
    """
    # Remove XML comments
    svg_content = re.sub(r'<!--.*?-->', '', svg_content, flags=re.DOTALL)
    
    # Minify style tags content while preserving structure
    def minify_style_tag(match):
        style_content = match.group(1)
        minified = minify_css(style_content)
        return f'<style>{minified}</style>'
    
    svg_content = re.sub(
        r'<style[^>]*>(.*?)</style>',
        minify_style_tag,
        svg_content,
        flags=re.DOTALL
    )
    
    # Remove metadata tags
    svg_content = re.sub(r'<metadata[^>]*>.*?</metadata>', '', svg_content, flags=re.DOTALL)
    
    # Remove unnecessary whitespace between tags
    svg_content = re.sub(r'>\s+<', '><', svg_content)
    
    # Remove leading/trailing whitespace from lines
    svg_content = '\n'.join(line.strip() for line in svg_content.split('\n') if line.strip())
    
    # Optimize path data
    def optimize_path(match):
        path_d = match.group(1)
        optimized = optimize_path_data(path_d)
        return f'd="{optimized}"'
    
    svg_content = re.sub(r'd="([^"]+)"', optimize_path, svg_content)
    
    # Optimize numeric attributes (but preserve IDs and text)
    numeric_attrs = ['x', 'y', 'width', 'height', 'cx', 'cy', 'r', 'rx', 'ry', 
                     'x1', 'y1', 'x2', 'y2', 'opacity', 'stroke-width']
    for attr in numeric_attrs:
        def optimize_attr(match):
            value = optimize_number(match.group(1))
            return f'{attr}="{value}"'
        svg_content = re.sub(f'{attr}="([^"]+)"', optimize_attr, svg_content)
    
    # Remove empty lines
    svg_content = re.sub(r'\n\s*\n', '\n', svg_content)
    
    return svg_content


def minify_svg_with_scour():
    """Minify SVG using scour library (if available)"""
    try:
        import scour.scour
        
        options = scour.scour.sanitizeOptions()
        # Best practice settings for animated SVGs
        options.remove_metadata = True
        options.remove_descriptive_elements = True
        options.strip_comments = True
        options.strip_xml_prolog = True
        options.enable_viewboxing = True
        options.indent_type = None  # No indentation
        options.newlines = False
        options.strip_xml_space_attribute = True
        options.remove_titles = False
        options.remove_descriptions = False
        options.remove_metadata = True
        options.remove_descriptive_elements = False
        options.preserve_editor_data = False
        options.keep_editor_data = False
        options.protect_ids_noninkscape = True
        options.protect_ids_prefix = None
        options.protect_ids_list = None
        
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            svg_content = f.read()
        
        # Use scour to optimize
        optimized = scour.scour.scourString(svg_content, options)
        return optimized
        
    except ImportError:
        return None


def main():
    """Main minification function"""
    try:
        print('>> Starting SVG minification...\n')
        
        # Check if input file exists
        if not os.path.exists(INPUT_FILE):
            raise FileNotFoundError(f'Input file not found: {INPUT_FILE}')
        
        # Read the SVG file
        print(f'[*] Reading: {INPUT_FILE}')
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            svg_content = f.read()
        
        original_size = len(svg_content.encode('utf-8'))
        print(f'    Original size: {format_bytes(original_size)}\n')
        
        # Try to use scour first (best practice), fallback to manual
        print('[*] Optimizing SVG...')
        optimized_content = minify_svg_with_scour()
        
        if optimized_content is None:
            print('    [i] Using manual optimization (install "scour" for better results)')
            optimized_content = minify_svg_manual(svg_content)
        else:
            print('    [i] Using scour optimizer (best practice)')
        
        # Write the minified SVG
        print(f'[*] Writing: {OUTPUT_FILE}')
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(optimized_content)
        
        minified_size = len(optimized_content.encode('utf-8'))
        savings = original_size - minified_size
        compression_ratio = calculate_compression_ratio(original_size, minified_size)
        
        # Display results
        print('\n[SUCCESS] Minification complete!\n')
        print('Results:')
        print('=' * 43)
        print(f'   Original size:  {format_bytes(original_size)}')
        print(f'   Minified size:  {format_bytes(minified_size)}')
        print(f'   Saved:          {format_bytes(savings)} ({compression_ratio}%)')
        print('=' * 43)
        
        print('\n>> Done! Your minified SVG is ready to use.\n')
        
        # Suggest installing scour if not available
        if minify_svg_with_scour() is None:
            print('[TIP] Install scour for even better optimization:')
            print('      pip install scour\n')
        
    except FileNotFoundError as e:
        print(f'[ERROR] {e}')
        sys.exit(1)
    except Exception as e:
        print(f'[ERROR] Error during minification: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()

