import os

def inject_seo_tags():
    base_dir = '/Users/mac/Desktop/ryder-pro/template-1/pages'
    injection_string = "    {% include 'partials/seo.html' %}\n"
    
    count = 0
    for root, dirs, files in os.walk(base_dir):
        # Exclude partials and skeletons directory so we don't recursive loop or inject in fragments
        if 'partials' in root or 'skeletons' in root:
            continue
            
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                # Find <head> tag and insert after it
                modified = False
                for i, line in enumerate(lines):
                    if '<head>' in line:
                        # Check if already injected to avoid duplicates
                        if i + 1 < len(lines) and 'partials/seo.html' in lines[i+1]:
                            print(f"Skipping {file} - already injected")
                            break
                            
                        lines.insert(i + 1, injection_string)
                        modified = True
                        break
                        
                if modified:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.writelines(lines)
                    print(f"Injected SEO into {file}")
                    count += 1
                    
    print(f"\\nSuccessfully injected SEO into {count} templates.")

if __name__ == '__main__':
    inject_seo_tags()
