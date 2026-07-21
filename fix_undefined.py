import re

with open('craft-match.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace cellToType[bestCell.str] with board[bestCell.r][bestCell.c].type
content = content.replace(
    "specialToCreate.push({r: bestCell.r, c: bestCell.c, type: cellToType[bestCell.str], special: specialType});",
    "specialToCreate.push({r: bestCell.r, c: bestCell.c, type: board[bestCell.r][bestCell.c].type, special: specialType});"
)

with open('craft-match.html', 'w', encoding='utf-8') as f:
    f.write(content)
