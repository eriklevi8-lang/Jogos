import re

with open('craft-match.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update .cell styling to look like pixelated Minecraft dirt/stone blocks
new_cell_css = '''
        .cell {
            width: 100%;
            height: 100%;
            background: #7a4f2e;
            border: 3px solid #5c3a21;
            border-top-color: #8c5d38;
            border-left-color: #8c5d38;
            box-shadow: inset -2px -2px 0 rgba(0,0,0,0.4), inset 2px 2px 0 rgba(255,255,255,0.2);
            image-rendering: pixelated;
        }
'''

content = re.sub(
    r'\.cell\s*\{[^}]+\}',
    new_cell_css.strip(),
    content
)

new_stats_board = '''
        .stats-board {
            display: flex;
            justify-content: space-between;
            padding: 1rem;
            margin: 0.5rem 1rem;
            align-items: center;
            background: var(--color-dirt);
            border: var(--pixel-border) solid #3d2412;
            box-shadow: 
                inset calc(var(--pixel-border) * -1) calc(var(--pixel-border) * -1) 0px rgba(0,0,0,0.5),
                inset var(--pixel-border) var(--pixel-border) 0px rgba(255,255,255,0.2);
        }
'''

content = re.sub(
    r'\.stats-board\s*\{[^}]+\}',
    new_stats_board.strip(),
    content
)

with open('craft-match.html', 'w', encoding='utf-8') as f:
    f.write(content)
