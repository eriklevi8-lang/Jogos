import re

with open("aether-royale.html", "r") as f:
    content = f.read()

new_cards = """    santuario: { id: 'santuario', name: 'Santuário dos Espectros', cost: 3, icon: '🪦', type: 'building', hp: 300, spawnCard: 'espectros', spawnRate: 3.1, deathSpawn: 4, lifetime: 30, radius: 1.0 },
    valquiria: { id: 'valquiria', name: 'Guerreira Giratória', cost: 4, icon: '🧝‍♀️', type: 'troop', count: 1, hp: 1200, damage: 110, atkSpeed: 1.4, speed: 2.5, range: 1.0, isAir: false, targetAir: false, targetBuildingOnly: false, radius: 0.5, aoe: true, aoeRadius: 1.5 },
    corredor: { id: 'corredor', name: 'Montador de Javali', cost: 4, icon: '🐗', type: 'troop', count: 1, hp: 1000, damage: 150, atkSpeed: 1.5, speed: 4.5, range: 0.8, isAir: false, targetAir: false, targetBuildingOnly: true, radius: 0.4, aoe: false },
    principe: { id: 'principe', name: 'Cavaleiro de Elite', cost: 5, icon: '🏇', type: 'troop', count: 1, hp: 1300, damage: 220, atkSpeed: 1.4, speed: 3.5, range: 1.0, isAir: false, targetAir: false, targetBuildingOnly: false, radius: 0.5, aoe: false },
    xbesta: { id: 'xbesta', name: 'Besta de Cerco', cost: 6, icon: '🏹', type: 'building', hp: 800, damage: 25, atkSpeed: 0.3, range: 12.0, lifetime: 40, targetAir: false, radius: 1.2 },
    veneno: { id: 'veneno', name: 'Nuvem Tóxica', cost: 4, icon: '🧪', type: 'spell', radius: 3.5, damage: 200, crownDmg: 60, isDot: true, duration: 4.0 },"""

content = content.replace("santuario: { id: 'santuario', name: 'Santuário dos Espectros', cost: 3, icon: '🪦', type: 'building', hp: 300, spawnCard: 'espectros', spawnRate: 3.1, deathSpawn: 4, lifetime: 30, radius: 1.0 }", new_cards)

with open("aether-royale.html", "w") as f:
    f.write(content)
