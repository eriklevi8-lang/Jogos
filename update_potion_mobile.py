import re

with open('potion-mix.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Make buttons more responsive and fix their touch handling
css_old = """        .control-btn {
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
        }"""

css_new = """        .control-btn {
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
            -webkit-user-select: none;
            touch-action: none;
            border-radius: 8px;
            transition: transform 0.05s;
        }
        .control-btn.active-btn {
            background: #9e9e9e;
            box-shadow: inset 4px 4px 0px rgba(0,0,0,0.5), inset -4px -4px 0px rgba(255,255,255,0.2);
            transform: scale(0.95);
        }
        .d-pad {
            display: grid;
            grid-template-columns: 65px 65px 65px;
            grid-template-rows: 65px 65px;
            gap: 5px;
        }"""

content = content.replace(css_old, css_new)

# Ensure the d-pad grid sizes are correct, wait I just changed .d-pad in the css_new but I should also replace the old .d-pad to avoid duplication.
old_dpad = """        .d-pad {
            display: grid;
            grid-template-columns: 60px 60px 60px;
            grid-template-rows: 60px 60px;
            gap: 5px;
        }"""
content = content.replace(old_dpad, "")


js_old = """        document.getElementById('btn-left').addEventListener('click', () => { if(!isGameOver) playerMove(-1); });
        document.getElementById('btn-right').addEventListener('click', () => { if(!isGameOver) playerMove(1); });
        document.getElementById('btn-up').addEventListener('click', () => { if(!isGameOver) playerRotate(1); });
        document.getElementById('btn-down').addEventListener('click', () => { if(!isGameOver) playerDrop(); });
        document.getElementById('btn-rotate').addEventListener('click', () => { if(!isGameOver) playerRotate(1); });"""

js_new = """        const btnActions = {
            'btn-left': () => { if(!isGameOver) playerMove(-1); },
            'btn-right': () => { if(!isGameOver) playerMove(1); },
            'btn-up': () => { if(!isGameOver) playerRotate(1); },
            'btn-down': () => { if(!isGameOver) playerDrop(); },
            'btn-rotate': () => { if(!isGameOver) playerRotate(1); }
        };

        function attachButton(id, actionFn, repeat = false) {
            const btn = document.getElementById(id);
            if (!btn) return;
            
            let holdInterval, holdTimeout;

            const start = (e) => {
                if (e.cancelable) e.preventDefault();
                btn.classList.add('active-btn');
                actionFn();
                if (repeat) {
                    holdTimeout = setTimeout(() => {
                        holdInterval = setInterval(actionFn, 100);
                    }, 250);
                }
            };
            const stop = (e) => {
                if (e.cancelable) e.preventDefault();
                btn.classList.remove('active-btn');
                clearTimeout(holdTimeout);
                clearInterval(holdInterval);
            };

            btn.addEventListener('touchstart', start, {passive: false});
            btn.addEventListener('touchend', stop, {passive: false});
            btn.addEventListener('touchcancel', stop, {passive: false});
            
            btn.addEventListener('mousedown', start);
            btn.addEventListener('mouseup', stop);
            btn.addEventListener('mouseleave', stop);
        }

        attachButton('btn-left', btnActions['btn-left'], true);
        attachButton('btn-right', btnActions['btn-right'], true);
        attachButton('btn-down', btnActions['btn-down'], true);
        attachButton('btn-up', btnActions['btn-up'], false);
        attachButton('btn-rotate', btnActions['btn-rotate'], false);"""

content = content.replace(js_old, js_new)

with open('potion-mix.html', 'w', encoding='utf-8') as f:
    f.write(content)
