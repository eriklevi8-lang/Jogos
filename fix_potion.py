import re

with open('potion-mix.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace controls CSS
old_css_controls = """        .controls {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr 1fr;
            gap: 10px;
            padding: 10px 1rem 20px;
        }

        .control-btn {
            background: #5c5c5c;
            border: 4px solid black;
            box-shadow: inset -4px -4px 0px rgba(0,0,0,0.5), inset 4px 4px 0px rgba(255,255,255,0.4);
            color: white;
            font-size: 2rem;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .control-btn:active {
            background: #7d7d7d;
            box-shadow: inset 4px 4px 0px rgba(0,0,0,0.5), inset -4px -4px 0px rgba(255,255,255,0.2);
            transform: scale(0.95);
        }"""

new_css_controls = """        .controls-wrapper {
            padding: 10px 1rem 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
        }
        .d-pad {
            display: grid;
            grid-template-columns: 60px 60px 60px;
            grid-template-rows: 60px 60px;
            gap: 5px;
        }
        .control-btn {
            background: #7d7d7d;
            border: 4px solid black;
            box-shadow: inset -4px -4px 0px rgba(0,0,0,0.5), inset 4px 4px 0px rgba(255,255,255,0.4);
            color: white;
            font-size: 1.8rem;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            user-select: none;
            border-radius: 8px;
        }
        .control-btn:active {
            background: #9e9e9e;
            box-shadow: inset 4px 4px 0px rgba(0,0,0,0.5), inset -4px -4px 0px rgba(255,255,255,0.2);
            transform: scale(0.95);
        }
        .action-pad {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        #btn-action {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            font-size: 2.5rem;
            background: #4caf50;
        }
        #btn-action:active {
            background: #388e3c;
        }"""

content = content.replace(old_css_controls, new_css_controls)

# Replace controls HTML
old_html_controls = """<div class="controls">
            <div class="control-btn" id="btn-left">⬅️</div>
            <div class="control-btn" id="btn-rotate">🔄</div>
            <div class="control-btn" id="btn-right">➡️</div>
            <div class="control-btn" id="btn-down">⬇️</div>
        </div>"""

new_html_controls = """<div class="controls-wrapper">
            <div class="d-pad">
                <div style="grid-column: 2; grid-row: 1;" class="control-btn" id="btn-up">▲</div>
                <div style="grid-column: 1; grid-row: 2;" class="control-btn" id="btn-left">◀</div>
                <div style="grid-column: 2; grid-row: 2;" class="control-btn" id="btn-down">▼</div>
                <div style="grid-column: 3; grid-row: 2;" class="control-btn" id="btn-right">▶</div>
            </div>
            <div class="action-pad">
                <div class="control-btn" id="btn-rotate" style="width: 90px; height: 90px; border-radius: 50%; background: #4caf50; font-size: 3rem; margin-top: 10px;">↻</div>
            </div>
        </div>"""

content = content.replace(old_html_controls, new_html_controls)

# Ensure btn-up rotates and btn-rotate drops or rotates depending on preference. 
# Usually Up is rotate, right button is action (rotate or drop to bottom). Let's make btn-up rotate, and btn-rotate also rotate.
old_js_listeners = """document.getElementById('btn-left').addEventListener('click', () => { if(!isGameOver) playerMove(-1); });
        document.getElementById('btn-right').addEventListener('click', () => { if(!isGameOver) playerMove(1); });
        document.getElementById('btn-rotate').addEventListener('click', () => { if(!isGameOver) playerRotate(1); });
        document.getElementById('btn-down').addEventListener('click', () => { if(!isGameOver) playerDrop(); });"""

new_js_listeners = """document.getElementById('btn-left').addEventListener('click', () => { if(!isGameOver) playerMove(-1); });
        document.getElementById('btn-right').addEventListener('click', () => { if(!isGameOver) playerMove(1); });
        document.getElementById('btn-up').addEventListener('click', () => { if(!isGameOver) playerRotate(1); });
        document.getElementById('btn-down').addEventListener('click', () => { if(!isGameOver) playerDrop(); });
        document.getElementById('btn-rotate').addEventListener('click', () => { if(!isGameOver) playerRotate(1); });"""

content = content.replace(old_js_listeners, new_js_listeners)

with open('potion-mix.html', 'w', encoding='utf-8') as f:
    f.write(content)
