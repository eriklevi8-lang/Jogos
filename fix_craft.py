import re

with open('craft-match.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the HTML for stats-board goal-box
old_html = """<div class="stat-box goal-box">
                <span class="stat-label">Meta</span>
                <span class="stat-value goal-text" id="goal-desc">Colete 10 🪵 e 10 🪨</span>
                <div class="progress-bar">
                    <div class="progress-fill" id="progress-fill"></div>
                </div>
            </div>"""

new_html = """<div class="stat-box goal-box" style="flex: 2; align-items: flex-start;">
                <span class="stat-label">Meta</span>
                <div id="goal-container" style="display: flex; gap: 8px; margin: 4px 0 8px; flex-wrap: wrap;">
                    <!-- Preenchido via JS -->
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" id="progress-fill"></div>
                </div>
            </div>"""

content = content.replace(old_html, new_html)

# Replace the JS updateUI portion for goal-desc
old_js = """let desc = '';
            let pTotal = 0;
            let cTotal = 0;
            for (let t in levelData.targets) {
                let req = levelData.targets[t];
                let col = Math.min(req, collected[t] || 0);
                desc += `${col}/${req} ${ICONS[t]} `;
                pTotal += req;
                cTotal += col;
            }
            document.getElementById('goal-desc').innerText = desc;
            let p = Math.min(100, (cTotal / pTotal) * 100);"""

new_js = """let pTotal = 0;
            let cTotal = 0;
            let goalContainer = document.getElementById('goal-container');
            goalContainer.innerHTML = '';
            
            for (let t in levelData.targets) {
                let req = levelData.targets[t];
                let col = Math.min(req, collected[t] || 0);
                pTotal += req;
                cTotal += col;
                
                let div = document.createElement('div');
                div.style.display = 'flex';
                div.style.alignItems = 'center';
                div.style.background = 'rgba(0,0,0,0.5)';
                div.style.padding = '2px 6px';
                div.style.borderRadius = '4px';
                div.style.border = '2px solid #5c5c5c';
                
                let icon = document.createElement('span');
                icon.innerText = ICONS[t];
                icon.style.fontSize = '1.2rem';
                icon.style.marginRight = '4px';
                icon.style.filter = 'drop-shadow(1px 1px 0px rgba(0,0,0,0.8))';
                
                let text = document.createElement('span');
                text.innerText = `${col}/${req}`;
                text.style.fontSize = '1.2rem';
                text.style.color = col >= req ? '#00ffaa' : 'white';
                text.style.textShadow = '1px 1px 0 #000';
                
                div.appendChild(icon);
                div.appendChild(text);
                goalContainer.appendChild(div);
            }
            let p = Math.min(100, (cTotal / pTotal) * 100);"""

content = content.replace(old_js, new_js)

with open('craft-match.html', 'w', encoding='utf-8') as f:
    f.write(content)
