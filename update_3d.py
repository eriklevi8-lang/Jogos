import re

with open("aether-royale.html", "r") as f:
    content = f.read()

three_troop_old = """function create3DTroop(entity) {
    if (!window.THREE) return null;
    const group = new THREE.Group();
    const isBlue = entity.team === 1;
    const bodyColor = isBlue ? 0x2563eb : 0xdc2626;
    
    let r = entity.radius * cellSize * 0.8;
    
    const bodyGeo = new THREE.CylinderGeometry(r*0.4, r*0.8, r*1.5, 12);
    const bodyMat = new THREE.MeshLambertMaterial({ color: bodyColor });
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    body.rotation.x = -Math.PI / 2; 
    body.position.z = -r*0.75;
    group.add(body);
    
    const headGeo = new THREE.SphereGeometry(r*0.6, 12, 12);
    const headMat = new THREE.MeshLambertMaterial({ color: 0xffffff });
    const head = new THREE.Mesh(headGeo, headMat);
    head.position.z = -r*1.5 - r*0.2;
    group.add(head);
    
    group.rotation.order = 'ZXY';
    return group;
}

function create3DBuilding(entity) {
    if (!window.THREE) return null;
    const group = new THREE.Group();
    const isBlue = entity.team === 1;
    const bodyColor = isBlue ? 0x1e3a8a : 0x7f1d1d;
    
    let r = entity.radius * cellSize;
    if (entity.isNexus) r *= 1.2;
    
    const baseGeo = new THREE.BoxGeometry(r*1.8, r*1.8, r*2);
    const baseMat = new THREE.MeshLambertMaterial({ color: bodyColor });
    const base = new THREE.Mesh(baseGeo, baseMat);
    base.position.z = -r;
    group.add(base);
    
    const topGeo = new THREE.BoxGeometry(r*2, r*2, r*0.5);
    const topMat = new THREE.MeshLambertMaterial({ color: 0x94a3b8 });
    const top = new THREE.Mesh(topGeo, topMat);
    top.position.z = -r*2 - r*0.25;
    group.add(top);
    
    group.rotation.order = 'ZXY';
    return group;
}"""

three_troop_new = """function create3DTroop(entity) {
    if (!window.THREE) return null;
    const group = new THREE.Group();
    const isBlue = entity.team === 1;
    const primary = isBlue ? 0x3b82f6 : 0xef4444;
    const skin = 0xffe4c4;
    const metal = 0x94a3b8;
    const dark = 0x1e293b;
    
    let r = entity.radius * cellSize * 0.8;
    let cardId = entity.card ? entity.card.id : '';
    
    // Default Humanoid Base
    let createHumanoid = (hasSword, hasBow) => {
        let g = new THREE.Group();
        // Body
        const bodyGeo = new THREE.CylinderGeometry(r*0.4, r*0.6, r*1.2, 8);
        const bodyMat = new THREE.MeshLambertMaterial({ color: primary });
        const body = new THREE.Mesh(bodyGeo, bodyMat);
        body.rotation.x = -Math.PI / 2; 
        body.position.z = -r*0.6;
        g.add(body);
        
        // Head
        const headGeo = new THREE.SphereGeometry(r*0.5, 8, 8);
        const headMat = new THREE.MeshLambertMaterial({ color: skin });
        const head = new THREE.Mesh(headGeo, headMat);
        head.position.z = -r*1.2 - r*0.2;
        g.add(head);
        
        if (hasSword) {
            const swordGeo = new THREE.BoxGeometry(r*0.2, r*1.5, r*0.1);
            const swordMat = new THREE.MeshLambertMaterial({ color: metal });
            const sword = new THREE.Mesh(swordGeo, swordMat);
            sword.position.set(r*0.8, r*0.5, -r*0.8);
            sword.rotation.x = Math.PI / 4;
            g.add(sword);
        }
        if (hasBow) {
            const bowGeo = new THREE.TorusGeometry(r*0.6, r*0.1, 4, 12, Math.PI);
            const bowMat = new THREE.MeshLambertMaterial({ color: 0x8b5a2b });
            const bow = new THREE.Mesh(bowGeo, bowMat);
            bow.position.set(0, r*0.8, -r*0.8);
            g.add(bow);
        }
        return g;
    };
    
    if (cardId === 'soldado') {
        group.add(createHumanoid(true, false));
    } else if (cardId === 'arqueiro') {
        group.add(createHumanoid(false, true));
    } else if (cardId === 'golem') {
        const bGeo = new THREE.BoxGeometry(r*2, r*1.5, r*2);
        const bMat = new THREE.MeshLambertMaterial({ color: 0x78716c });
        const body = new THREE.Mesh(bGeo, bMat);
        body.position.z = -r;
        group.add(body);
        const hGeo = new THREE.BoxGeometry(r*1.2, r*1.2, r*1.2);
        const head = new THREE.Mesh(hGeo, bMat);
        head.position.set(0, r*0.5, -r*2.2);
        group.add(head);
    } else if (cardId === 'dragao') {
        const body = new THREE.Mesh(new THREE.CylinderGeometry(r*0.6, r*0.8, r*2, 8), new THREE.MeshLambertMaterial({color: 0x10b981}));
        body.rotation.x = -Math.PI / 2;
        body.position.z = -r;
        group.add(body);
        const wingL = new THREE.Mesh(new THREE.BoxGeometry(r*2, r*0.1, r*1.5), new THREE.MeshLambertMaterial({color: 0x059669}));
        wingL.position.set(-r*1.5, 0, -r);
        group.add(wingL);
        const wingR = new THREE.Mesh(new THREE.BoxGeometry(r*2, r*0.1, r*1.5), new THREE.MeshLambertMaterial({color: 0x059669}));
        wingR.position.set(r*1.5, 0, -r);
        group.add(wingR);
    } else if (cardId === 'corredor') {
        const pig = new THREE.Mesh(new THREE.BoxGeometry(r*1.5, r*2.5, r*1.2), new THREE.MeshLambertMaterial({color: 0x8b5a2b}));
        pig.position.z = -r*0.6;
        group.add(pig);
        const rider = createHumanoid(false, false);
        rider.position.z = -r*0.5;
        group.add(rider);
    } else if (cardId === 'principe') {
        const horse = new THREE.Mesh(new THREE.BoxGeometry(r*1.2, r*2.5, r*1.5), new THREE.MeshLambertMaterial({color: 0xffffff}));
        horse.position.z = -r*0.75;
        group.add(horse);
        const rider = createHumanoid(false, false);
        rider.position.z = -r*0.8;
        group.add(rider);
        const lance = new THREE.Mesh(new THREE.CylinderGeometry(r*0.1, r*0.1, r*3, 8), new THREE.MeshLambertMaterial({color: 0xd4af37}));
        lance.rotation.x = Math.PI / 2;
        lance.position.set(r*0.8, r*1.5, -r*1.5);
        group.add(lance);
    } else if (cardId === 'valquiria') {
        const h = createHumanoid(false, false);
        const axe = new THREE.Mesh(new THREE.BoxGeometry(r*2.5, r*0.2, r*0.5), new THREE.MeshLambertMaterial({color: metal}));
        axe.position.set(0, 0, -r*1.5);
        h.add(axe);
        group.add(h);
    } else if (cardId === 'espectros') {
        const ghost = new THREE.Mesh(new THREE.ConeGeometry(r*0.8, r*2, 16), new THREE.MeshLambertMaterial({color: 0xe2e8f0, transparent: true, opacity: 0.7}));
        ghost.rotation.x = Math.PI / 2;
        ghost.position.z = -r;
        group.add(ghost);
    } else {
        group.add(createHumanoid(true, false));
    }
    
    group.rotation.order = 'ZXY';
    return group;
}

function create3DBuilding(entity) {
    if (!window.THREE) return null;
    const group = new THREE.Group();
    const isBlue = entity.team === 1;
    const primary = isBlue ? 0x1e3a8a : 0x7f1d1d;
    const stone = 0x94a3b8;
    const darkStone = 0x475569;
    const wood = 0x8b5a2b;
    
    let r = entity.radius * cellSize;
    if (entity.isNexus) r *= 1.2;
    
    let cardId = entity.card ? entity.card.id : '';
    
    if (entity.isNexus || entity.icon === '🗼' || entity.icon === '🏰') {
        const base = new THREE.Mesh(new THREE.CylinderGeometry(r, r*1.1, r*2.5, 12), new THREE.MeshLambertMaterial({color: darkStone}));
        base.rotation.x = Math.PI / 2;
        base.position.z = -r*1.25;
        group.add(base);
        const roof = new THREE.Mesh(new THREE.ConeGeometry(r*1.2, r*1.5, 12), new THREE.MeshLambertMaterial({color: primary}));
        roof.rotation.x = Math.PI / 2;
        roof.position.z = -r*2.5 - r*0.75;
        group.add(roof);
    } else if (cardId === 'canhao') {
        const base = new THREE.Mesh(new THREE.BoxGeometry(r*1.5, r*1.5, r*0.5), new THREE.MeshLambertMaterial({color: wood}));
        base.position.z = -r*0.25;
        group.add(base);
        const barrel = new THREE.Mesh(new THREE.CylinderGeometry(r*0.4, r*0.4, r*2, 12), new THREE.MeshLambertMaterial({color: 0x111111}));
        barrel.position.set(0, r*0.5, -r*0.8);
        group.add(barrel);
    } else if (cardId === 'xbesta') {
        const base = new THREE.Mesh(new THREE.BoxGeometry(r*1.5, r*1.5, r*1.5), new THREE.MeshLambertMaterial({color: wood}));
        base.position.z = -r*0.75;
        group.add(base);
        const bow = new THREE.Mesh(new THREE.TorusGeometry(r*1.2, r*0.15, 8, 16, Math.PI), new THREE.MeshLambertMaterial({color: wood}));
        bow.position.set(0, 0, -r*1.5);
        group.add(bow);
    } else if (cardId === 'santuario') {
        const base = new THREE.Mesh(new THREE.BoxGeometry(r*1.5, r*0.5, r*1.5), new THREE.MeshLambertMaterial({color: 0x4b5563}));
        base.position.z = -r*0.75;
        group.add(base);
        const stoneM = new THREE.Mesh(new THREE.BoxGeometry(r*1.2, r*0.2, r*2), new THREE.MeshLambertMaterial({color: stone}));
        stoneM.position.set(0, 0, -r*1.5);
        group.add(stoneM);
    } else {
        const base = new THREE.Mesh(new THREE.BoxGeometry(r*1.8, r*1.8, r*1.5), new THREE.MeshLambertMaterial({color: primary}));
        base.position.z = -r*0.75;
        group.add(base);
    }
    
    group.rotation.order = 'ZXY';
    return group;
}"""
content = content.replace(three_troop_old, three_troop_new)

with open("aether-royale.html", "w") as f:
    f.write(content)

