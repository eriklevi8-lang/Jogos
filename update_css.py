import re

with open('src/index.css', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the @theme and second body block
content = re.sub(r'@theme\s*\{[^}]+\}', '', content)
content = re.sub(r'body\s*\{\s*font-family:\s*var\(--font-body\);[^}]+\}', '', content)

with open('src/index.css', 'w', encoding='utf-8') as f:
    f.write(content)
