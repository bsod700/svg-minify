#!/usr/bin/env python3
"""
Professional SVG Minification Script - Batch Processing
Uses scour - Industry-standard Python SVG optimizer

Best practices applied:
- Batch process all SVGs in a folder
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
from glob import glob

# Configuration - Folder-based batch processing
INPUT_FOLDER = 'svg'           # Folder containing SVG files to minify
OUTPUT_FOLDER = 'svg minified' # Folder where minified SVGs will be saved

# Advanced options
MAKE_UNREADABLE = True  # Compress to single line and encode text for maximum obfuscation
REMOVE_METADATA = False  # Remove <metadata> tags (set to True to remove, False to preserve)
REMOVE_DESCRIPTIVE_ELEMENTS = False  # Remove <title> and <desc> tags (set to True to remove, False to preserve)


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
    # Remove comments (fixed regex to handle all cases)
    css_content = re.sub(r'/\*[^*]*\*+(?:[^/*][^*]*\*+)*/', '', css_content)
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


def generate_short_name(index):
    """Generate short names: a, b, c, ..., z, aa, ab, ..., zz, aaa, etc."""
    name = ''
    index += 1
    while index > 0:
        index -= 1
        name = chr(97 + (index % 26)) + name
        index //= 26
    return name


def extract_ids_and_classes(svg_content):
    """Extract all IDs and class names from SVG content"""
    ids = set()
    classes = set()
    
    # Extract IDs from id="..." attributes
    id_matches = re.findall(r'\bid=["\']([^"\']+)["\']', svg_content)
    ids.update(id_matches)
    
    # Extract classes from class="..." attributes
    class_matches = re.findall(r'\bclass=["\']([^"\']+)["\']', svg_content)
    for class_group in class_matches:
        # Split multiple classes
        classes.update(class_group.split())
    
    return sorted(ids), sorted(classes)


def create_name_mappings(ids, classes):
    """Create mappings from original names to minified names"""
    id_map = {}
    class_map = {}
    
    counter = 0
    for original_id in ids:
        id_map[original_id] = generate_short_name(counter)
        counter += 1
    
    counter = 0
    for original_class in classes:
        class_map[original_class] = generate_short_name(counter)
        counter += 1
    
    return id_map, class_map


def make_unreadable(svg_content):
    """Make SVG unreadable by compressing to single line only"""
    
    # Remove ALL line breaks and compress to single line
    svg_content = svg_content.replace('\n', ' ').replace('\r', '')
    
    # Remove spaces between closing and opening tags
    svg_content = re.sub(r'>\s+<', '><', svg_content)
    
    # Minimize multiple spaces to single space
    svg_content = re.sub(r'\s{2,}', ' ', svg_content)
    
    # Remove spaces before closing tags and self-closing tags
    svg_content = re.sub(r'\s+>', '>', svg_content)
    svg_content = re.sub(r'\s+/>', '/>', svg_content)
    
    return svg_content.strip()


def minify_ids_and_classes(svg_content):
    """Minify all ID and class names to short names and update all references"""
    # Extract all IDs and classes
    ids, classes = extract_ids_and_classes(svg_content)
    
    if not ids and not classes:
        return svg_content
    
    # Create mappings
    id_map, class_map = create_name_mappings(ids, classes)
    
    # Create a combined pattern for efficient replacement
    # Sort by length (longest first) to avoid partial replacements
    all_replacements = []
    
    # Build regex pattern for all ID replacements
    if id_map:
        sorted_ids = sorted(id_map.keys(), key=len, reverse=True)
        escaped_ids = [re.escape(id_name) for id_name in sorted_ids]
        id_pattern = '|'.join(escaped_ids)
        
        # Replace IDs in different contexts
        # 1. id="..." attributes
        svg_content = re.sub(
            rf'\bid=(["\'])({id_pattern})\1',
            lambda m: f'id={m.group(1)}{id_map[m.group(2)]}{m.group(1)}',
            svg_content
        )
        
        # 2. CSS selectors and url() references: #id
        svg_content = re.sub(
            rf'#({id_pattern})\b',
            lambda m: f'#{id_map[m.group(1)]}',
            svg_content
        )
    
    # Build regex pattern for all class replacements
    if class_map:
        sorted_classes = sorted(class_map.keys(), key=len, reverse=True)
        escaped_classes = [re.escape(cls) for cls in sorted_classes]
        class_pattern = '|'.join(escaped_classes)
        
        # 1. class="..." attributes - handle multiple classes
        def replace_classes(match):
            quote = match.group(1)
            classes_str = match.group(2)
            class_list = classes_str.split()
            new_classes = [class_map.get(c, c) for c in class_list]
            return f'class={quote}{" ".join(new_classes)}{quote}'
        
        svg_content = re.sub(
            rf'\bclass=(["\'])([^"\']+)\1',
            replace_classes,
            svg_content
        )
        
        # 2. CSS selectors: .class
        svg_content = re.sub(
            rf'\.({class_pattern})\b',
            lambda m: f'.{class_map[m.group(1)]}',
            svg_content
        )
    
    return svg_content


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
    
    # Conditionally remove metadata tags based on configuration
    if REMOVE_METADATA:
        svg_content = re.sub(r'<metadata[^>]*>.*?</metadata>', '', svg_content, flags=re.DOTALL)
    
    # Conditionally remove descriptive elements (title and desc) based on configuration
    if REMOVE_DESCRIPTIVE_ELEMENTS:
        svg_content = re.sub(r'<title[^>]*>.*?</title>', '', svg_content, flags=re.DOTALL)
        svg_content = re.sub(r'<desc[^>]*>.*?</desc>', '', svg_content, flags=re.DOTALL)
    
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


def is_scour_available():
    """Check if scour library is available"""
    try:
        import scour.scour
        return True
    except ImportError:
        return False


def minify_single_file(input_path, output_path, use_scour=False):
    """
    Minify a single SVG file
    
    Args:
        input_path: Path to input SVG file
        output_path: Path to output minified SVG file
        use_scour: Whether to use scour library
    
    Returns:
        tuple: (original_size, minified_size, success)
    """
    try:
        # Read the SVG file
        with open(input_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()
        
        original_size = len(svg_content.encode('utf-8'))
        
        # Try to use scour first (best practice), fallback to manual
        if use_scour:
            try:
                import scour.scour
                options = scour.scour.sanitizeOptions()
                # Best practice settings for animated SVGs
                options.remove_metadata = REMOVE_METADATA  # Configurable: remove or preserve metadata tags
                options.remove_descriptive_elements = REMOVE_DESCRIPTIVE_ELEMENTS  # Configurable: remove or preserve title and desc tags
                options.strip_comments = True
                options.strip_xml_prolog = True
                options.enable_viewboxing = True
                options.indent_type = None
                options.newlines = False
                options.strip_xml_space_attribute = True
                options.protect_ids_noninkscape = True
                
                optimized_content = scour.scour.scourString(svg_content, options)
                
                # Scour doesn't remove CSS comments, so we do it manually
                def minify_style_tag(match):
                    style_content = match.group(1)
                    minified = minify_css(style_content)
                    return f'<style>{minified}</style>'
                
                optimized_content = re.sub(
                    r'<style[^>]*>(.*?)</style>',
                    minify_style_tag,
                    optimized_content,
                    flags=re.DOTALL
                )
            except Exception:
                optimized_content = minify_svg_manual(svg_content)
        else:
            optimized_content = minify_svg_manual(svg_content)
        
        # Minify IDs and classes to very short names
        optimized_content = minify_ids_and_classes(optimized_content)
        
        # Make unreadable if enabled (compress to single line and encode text)
        if MAKE_UNREADABLE:
            optimized_content = make_unreadable(optimized_content)
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write the minified SVG
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(optimized_content)
        
        minified_size = len(optimized_content.encode('utf-8'))
        
        return original_size, minified_size, True
        
    except Exception as e:
        print(f'    [ERROR] Failed to process: {e}')
        return 0, 0, False


def main():
    """Main minification function with batch processing"""
    try:
        print('=' * 60)
        print('  SVG Batch Minification Tool')
        print('=' * 60)
        print()
        
        # Check if input folder exists
        if not os.path.exists(INPUT_FOLDER):
            print(f'[ERROR] Input folder not found: {INPUT_FOLDER}')
            print(f'[INFO] Creating folder: {INPUT_FOLDER}')
            os.makedirs(INPUT_FOLDER, exist_ok=True)
            print(f'[INFO] Please place your SVG files in the "{INPUT_FOLDER}" folder and run again.')
            sys.exit(0)
        
        # Find all SVG files in input folder
        svg_files = glob(os.path.join(INPUT_FOLDER, '*.svg'))
        
        if not svg_files:
            print(f'[ERROR] No SVG files found in "{INPUT_FOLDER}" folder')
            print(f'[INFO] Please place your SVG files in the "{INPUT_FOLDER}" folder and run again.')
            sys.exit(0)
        
        # Create output folder if it doesn't exist
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        
        # Check if scour is available
        use_scour = is_scour_available()
        if use_scour:
            print('[*] Using scour optimizer (best practice)')
        else:
            print('[*] Using manual optimization')
            print('[TIP] Install "scour" for better results: pip install scour')
        
        if MAKE_UNREADABLE:
            print('[*] Unreadable mode: ON (single-line compression)')
        
        print()
        
        print(f'[*] Found {len(svg_files)} SVG file(s) to process')
        print(f'[*] Input folder:  {INPUT_FOLDER}')
        print(f'[*] Output folder: {OUTPUT_FOLDER}')
        print()
        
        # Process each SVG file
        total_original = 0
        total_minified = 0
        success_count = 0
        failed_count = 0
        
        for i, input_path in enumerate(svg_files, 1):
            filename = os.path.basename(input_path)
            output_path = os.path.join(OUTPUT_FOLDER, filename)
            
            print(f'[{i}/{len(svg_files)}] Processing: {filename}')
            
            original_size, minified_size, success = minify_single_file(
                input_path, output_path, use_scour
            )
            
            if success:
                savings = original_size - minified_size
                ratio = calculate_compression_ratio(original_size, minified_size)
                print(f'    Original: {format_bytes(original_size)} -> '
                      f'Minified: {format_bytes(minified_size)} '
                      f'(saved {format_bytes(savings)}, {ratio}%)')
                total_original += original_size
                total_minified += minified_size
                success_count += 1
            else:
                failed_count += 1
            
            print()
        
        # Display summary
        print('=' * 60)
        print('  SUMMARY')
        print('=' * 60)
        print(f'  Files processed:    {success_count} successful, {failed_count} failed')
        print(f'  Total original:     {format_bytes(total_original)}')
        print(f'  Total minified:     {format_bytes(total_minified)}')
        
        if total_original > 0:
            total_savings = total_original - total_minified
            total_ratio = calculate_compression_ratio(total_original, total_minified)
            print(f'  Total saved:        {format_bytes(total_savings)} ({total_ratio}%)')
        
        print('=' * 60)
        print()
        print(f'[SUCCESS] All files processed! Minified SVGs saved in "{OUTPUT_FOLDER}" folder')
        print()
        
    except KeyboardInterrupt:
        print('\n[INFO] Process interrupted by user')
        sys.exit(0)
    except Exception as e:
        print(f'[ERROR] Error during minification: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

