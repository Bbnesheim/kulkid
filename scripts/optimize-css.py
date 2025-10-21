#!/usr/bin/env python3
"""
CSS Optimization Script for Shopify Theme
Removes unused CSS rules based on template analysis
"""

import re
import os
from pathlib import Path

def get_used_classes():
    """Scan templates for actually used CSS classes"""
    used_classes = set()
    used_ids = set()
    
    # Define directories to scan
    template_dirs = ['templates', 'sections', 'snippets', 'layout']
    
    for dir_name in template_dirs:
        if os.path.exists(dir_name):
            for root, dirs, files in os.walk(dir_name):
                for file in files:
                    if file.endswith('.liquid'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                
                                # Find class attributes (handle Liquid syntax)
                                class_matches = re.findall(r'class=["\']([^"\']+)["\']', content)
                                for match in class_matches:
                                    # Clean up liquid syntax and get actual classes
                                    clean_match = re.sub(r'{[^}]*}', ' ', match)  # Remove liquid variables
                                    classes = [cls.strip() for cls in clean_match.split() if cls.strip() and not cls.startswith('{') and not cls.startswith('%')]
                                    used_classes.update(classes)
                                
                                # Find id attributes
                                id_matches = re.findall(r'id=["\']([^"\']+)["\']', content)
                                used_ids.update(id_matches)
                                
                        except Exception as e:
                            print(f"Error reading {file_path}: {e}")
    
    return used_classes, used_ids

def optimize_css_file(input_file, output_file, used_classes, used_ids):
    """Remove unused CSS rules from a CSS file"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # Split CSS into rules
    rules = []
    current_rule = ""
    brace_count = 0
    
    for char in css_content:
        current_rule += char
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                rules.append(current_rule.strip())
                current_rule = ""
    
    # Add any remaining content
    if current_rule.strip():
        rules.append(current_rule.strip())
    
    # Keep essential rules and used classes
    essential_patterns = [
        r':root\s*{',  # CSS variables
        r'@media',     # Media queries
        r'@keyframes', # Animations
        r'html\s*{',   # HTML element
        r'body\s*{',   # Body element
        r'\*\s*{',     # Universal selector
        r'\.visually-hidden',  # Accessibility
        r'\.skip-to-content',  # Accessibility
        r'\.page-width',       # Layout
        r'\.section',          # Layout sections
    ]
    
    optimized_rules = []
    
    for rule in rules:
        # Keep essential CSS
        if any(re.search(pattern, rule, re.IGNORECASE) for pattern in essential_patterns):
            optimized_rules.append(rule)
            continue
            
        # Check if rule uses any classes we found in templates
        rule_uses_known_class = False
        
        # Extract selectors from the rule
        if '{' in rule:
            selectors_part = rule.split('{')[0].strip()
            
            # Check for class selectors
            class_selectors = re.findall(r'\.([a-zA-Z0-9_-]+)', selectors_part)
            for class_name in class_selectors:
                if class_name in used_classes:
                    rule_uses_known_class = True
                    break
            
            # Check for ID selectors
            id_selectors = re.findall(r'#([a-zA-Z0-9_-]+)', selectors_part)
            for id_name in id_selectors:
                if id_name in used_ids:
                    rule_uses_known_class = True
                    break
        
        if rule_uses_known_class:
            optimized_rules.append(rule)
    
    # Write optimized CSS
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(optimized_rules))
    
    original_size = len(css_content)
    optimized_size = sum(len(rule) for rule in optimized_rules)
    savings = original_size - optimized_size
    
    print(f"Original size: {original_size} bytes")
    print(f"Optimized size: {optimized_size} bytes")
    print(f"Savings: {savings} bytes ({savings/original_size*100:.1f}%)")
    
    return savings

def main():
    print("Scanning templates for used CSS classes...")
    used_classes, used_ids = get_used_classes()
    
    print(f"Found {len(used_classes)} used classes and {len(used_ids)} used IDs")
    
    # Optimize base.css
    if os.path.exists('assets/base.css'):
        print("Optimizing base.css...")
        savings = optimize_css_file(
            'assets/base.css', 
            'assets/base-optimized.css', 
            used_classes, 
            used_ids
        )
        print(f"Created assets/base-optimized.css with {savings} bytes savings")
    
    # List top used classes for reference
    print(f"\nTop 20 most common classes found:")
    common_classes = sorted(used_classes)[:20]
    for cls in common_classes:
        print(f"  .{cls}")

if __name__ == "__main__":
    main()