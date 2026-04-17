import os

google_file = 'clash/google.yaml'
youtube_file = 'clash/youtube.yaml'

if not os.path.exists(google_file) or not os.path.exists(youtube_file):
    print('Files missing')
    exit(1)

# Read youtube.yaml suffixes
yt_suffixes = []
with open(youtube_file, 'r', encoding='utf-8') as f:
    for line in f:
        stripped = line.strip()
        if stripped.startswith('- DOMAIN-SUFFIX,'):
            yt_suffixes.append(stripped.split(',')[1].strip())

# Process google.yaml
with open(google_file, 'r', encoding='utf-8') as f:
    g_lines = f.readlines()

new_g_lines = []
removed_g_keywords = []
removed_g_redundant = []

for line in g_lines:
    stripped = line.strip()
    
    if stripped == '- DOMAIN-KEYWORD,google':
        removed_g_keywords.append('google')
        continue
        
    if stripped.startswith('- DOMAIN-KEYWORD,'):
        kw = stripped.split(',')[1].strip()
        if kw == 'appspot':
            new_g_lines.append('  - DOMAIN-SUFFIX,appspot.com\n')
        elif kw == 'blogspot':
            new_g_lines.append('  - DOMAIN-SUFFIX,blogspot.com\n')
        elif kw == 'gmail':
            new_g_lines.append('  - DOMAIN-SUFFIX,gmail.com\n')
        elif kw == 'gstatic':
            new_g_lines.append('  - DOMAIN-SUFFIX,gstatic.com\n')
        elif kw == 'recaptcha':
            new_g_lines.append('  - DOMAIN-SUFFIX,recaptcha.net\n')
            new_g_lines.append('  - DOMAIN-SUFFIX,recaptcha.com\n')
        else:
            new_g_lines.append(line)
        removed_g_keywords.append(kw)
        continue
        
    if stripped.startswith('- DOMAIN-SUFFIX,'):
        domain = stripped.split(',')[1].strip()
        parts = domain.split('.')
        is_redundant = False
        for i in range(len(parts)):
            suf = '.'.join(parts[i:])
            if suf in yt_suffixes:
                is_redundant = True
                break
        if is_redundant:
            removed_g_redundant.append(domain)
            continue
            
    new_g_lines.append(line)

with open(google_file, 'w', encoding='utf-8') as f:
    f.writelines(new_g_lines)

# Process youtube.yaml
with open(youtube_file, 'r', encoding='utf-8') as f:
    y_lines = f.readlines()

new_y_lines = []
removed_y_keywords = []

for line in y_lines:
    stripped = line.strip()
    if stripped == '- DOMAIN-KEYWORD,youtube':
        removed_y_keywords.append('youtube')
        continue
    new_y_lines.append(line)

with open(youtube_file, 'w', encoding='utf-8') as f:
    f.writelines(new_y_lines)

print(f'Processed google.yaml: removed {len(removed_g_keywords)} keywords and {len(removed_g_redundant)} overlapping youtube domains.')
print(f'Processed youtube.yaml: removed {len(removed_y_keywords)} keyword.')
