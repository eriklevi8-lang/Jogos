import re

with open('potion-mix.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_grid = """            // Draw grid
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
            ctx.lineWidth = 0.05;"""

new_grid = """            // Draw grid
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
            ctx.lineWidth = 0.05;"""

content = content.replace(old_grid, new_grid)

with open('potion-mix.html', 'w', encoding='utf-8') as f:
    f.write(content)
