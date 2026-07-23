import re

with open("aether-royale.html", "r") as f:
    content = f.read()

create3DBuilding_old = """function create3DBuilding(entity) {
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
        const base = new THREE.Mesh(new THREE.CylinderGeometry(r, r*1.1, r*2.5, 12), new THREE.MeshLambertMaterial({color: darkStone, side: THREE.DoubleSide}));
        base.rotation.x = Math.PI / 2;
        base.position.z = -r*1.25;
        group.add(base);
        const roof = new THREE.Mesh(new THREE.ConeGeometry(r*1.2, r*1.5, 12), new THREE.MeshLambertMaterial({color: primary, side: THREE.DoubleSide}));
        roof.rotation.x = Math.PI / 2;
        roof.position.z = -r*2.5 - r*0.75;
        group.add(roof);
    } else if (cardId === 'canhao') {
        const base = new THREE.Mesh(new THREE.BoxGeometry(r*1.5, r*1.5, r*0.5), new THREE.MeshLambertMaterial({color: wood, side: THREE.DoubleSide}));
        base.position.z = -r*0.25;
        group.add(base);
        const barrel = new THREE.Mesh(new THREE.CylinderGeometry(r*0.4, r*0.4, r*2, 12), new THREE.MeshLambertMaterial({color: 0x111111, side: THREE.DoubleSide}));
        barrel.position.set(0, r*0.5, -r*0.8);
        group.add(barrel);
    } else if (cardId === 'xbesta') {
        const base = new THREE.Mesh(new THREE.BoxGeometry(r*1.5, r*1.5, r*1.5), new THREE.MeshLambertMaterial({color: wood, side: THREE.DoubleSide}));
        base.position.z = -r*0.75;
        group.add(base);
        const bow = new THREE.Mesh(new THREE.TorusGeometry(r*1.2, r*0.15, 8, 16, Math.PI), new THREE.MeshLambertMaterial({color: wood, side: THREE.DoubleSide}));
        bow.position.set(0, 0, -r*1.5);
        group.add(bow);
    } else if (cardId === 'santuario') {
        const base = new THREE.Mesh(new THREE.BoxGeometry(r*1.5, r*0.5, r*1.5), new THREE.MeshLambertMaterial({color: 0x4b5563, side: THREE.DoubleSide}));
        base.position.z = -r*0.75;
        group.add(base);
        const stoneM = new THREE.Mesh(new THREE.BoxGeometry(r*1.2, r*0.2, r*2), new THREE.MeshLambertMaterial({color: stone, side: THREE.DoubleSide}));
        stoneM.position.set(0, 0, -r*1.5);
        group.add(stoneM);
    } else {
        const base = new THREE.Mesh(new THREE.BoxGeometry(r*1.8, r*1.8, r*1.5), new THREE.MeshLambertMaterial({color: primary, side: THREE.DoubleSide}));
        base.position.z = -r*0.75;
        group.add(base);
    }
    
    group.rotation.order = 'ZXY';
    return group;
}"""

create3DBuilding_new = """function create3DBuilding(entity) {
    if (!window.THREE) return null;
    const group = new THREE.Group();
    const isBlue = entity.team === 1;
    const primary = isBlue ? 0x1e3a8a : 0x7f1d1d;
    const stone = 0x94a3b8;
    const darkStone = 0x475569;
    const wood = 0x8b5a2b;
    
    let r = entity.radius * cellSize * 1.5; // Scaled up slightly for impact
    if (entity.isNexus) r *= 1.1;
    
    let cardId = entity.card ? entity.card.id : '';
    
    if (entity.isNexus || entity.icon === '🗼' || entity.icon === '🏰') {
        const base = new THREE.Mesh(new THREE.CylinderGeometry(r, r*1.1, r*2.5, 12), new THREE.MeshLambertMaterial({color: darkStone, side: THREE.DoubleSide}));
        base.rotation.x = Math.PI / 2;
        base.position.z = -r*1.25;
        group.add(base);
        
        // Door
        const door = new THREE.Mesh(new THREE.BoxGeometry(r*0.6, r*0.1, r*1.0), new THREE.MeshLambertMaterial({color: 0x3e2723, side: THREE.DoubleSide}));
        door.position.set(0, r*1.0, -r*0.5);
        group.add(door);

        const roof = new THREE.Mesh(new THREE.ConeGeometry(r*1.3, r*1.6, 12), new THREE.MeshLambertMaterial({color: primary, side: THREE.DoubleSide}));
        roof.rotation.x = Math.PI / 2;
        roof.position.z = -r*2.5 - r*0.8;
        group.add(roof);
    } else if (cardId === 'canhao') {
        const base = new THREE.Mesh(new THREE.BoxGeometry(r*1.6, r*1.6, r*0.6), new THREE.MeshLambertMaterial({color: wood, side: THREE.DoubleSide}));
        base.position.z = -r*0.3;
        group.add(base);
        const mount = new THREE.Mesh(new THREE.BoxGeometry(r*0.8, r*0.8, r*0.6), new THREE.MeshLambertMaterial({color: darkStone, side: THREE.DoubleSide}));
        mount.position.z = -r*0.9;
        group.add(mount);
        const barrel = new THREE.Mesh(new THREE.CylinderGeometry(r*0.4, r*0.4, r*2.2, 12), new THREE.MeshLambertMaterial({color: 0x111111, side: THREE.DoubleSide}));
        barrel.position.set(0, r*0.6, -r*1.2);
        group.add(barrel);
    } else if (cardId === 'xbesta') {
        const base = new THREE.Mesh(new THREE.BoxGeometry(r*1.5, r*1.5, r*1.5), new THREE.MeshLambertMaterial({color: wood, side: THREE.DoubleSide}));
        base.position.z = -r*0.75;
        group.add(base);
        const bowMat = new THREE.MeshLambertMaterial({color: 0xd4af37, side: THREE.DoubleSide});
        const bow = new THREE.Mesh(new THREE.TorusGeometry(r*1.2, r*0.15, 8, 16, Math.PI), bowMat);
        bow.position.set(0, 0, -r*1.5);
        group.add(bow);
        const arrow = new THREE.Mesh(new THREE.CylinderGeometry(r*0.05, r*0.05, r*1.8, 8), new THREE.MeshLambertMaterial({color: 0x94a3b8, side: THREE.DoubleSide}));
        arrow.position.set(0, r*0.8, -r*1.5);
        group.add(arrow);
    } else if (cardId === 'santuario') {
        const base = new THREE.Mesh(new THREE.BoxGeometry(r*1.8, r*1.8, r*0.5), new THREE.MeshLambertMaterial({color: 0x4b5563, side: THREE.DoubleSide}));
        base.position.z = -r*0.25;
        group.add(base);
        const stoneM = new THREE.Mesh(new THREE.BoxGeometry(r*1.4, r*0.4, r*2.2), new THREE.MeshLambertMaterial({color: stone, side: THREE.DoubleSide}));
        stoneM.position.set(0, 0, -r*1.5);
        group.add(stoneM);
        const cross = new THREE.Mesh(new THREE.BoxGeometry(r*0.8, r*0.2, r*0.2), new THREE.MeshLambertMaterial({color: 0x1e293b, side: THREE.DoubleSide}));
        cross.position.set(0, 0, -r*2.5);
        group.add(cross);
    } else {
        const base = new THREE.Mesh(new THREE.BoxGeometry(r*1.8, r*1.8, r*1.5), new THREE.MeshLambertMaterial({color: primary, side: THREE.DoubleSide}));
        base.position.z = -r*0.75;
        group.add(base);
    }
    
    group.rotation.order = 'ZXY';
    return group;
}"""

content = content.replace(create3DBuilding_old, create3DBuilding_new)

with open("aether-royale.html", "w") as f:
    f.write(content)
