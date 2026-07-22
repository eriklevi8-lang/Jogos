import React, { useEffect, useRef } from 'react';

interface ParticlesProps {
  scrollVelocityRef: React.MutableRefObject<number>;
}

export function ParticlesBackground({ scrollVelocityRef }: ParticlesProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let particles: {x: number, y: number, size: number, speedY: number, opacity: number}[] = [];
    const particleCount = 60;

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    window.addEventListener('resize', resize);
    resize();

    for(let i=0; i<particleCount; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        size: Math.random() * 2 + 1,
        speedY: Math.random() * 0.5 + 0.1,
        opacity: Math.random() * 0.5 + 0.2
      });
    }

    let animationFrameId: number;
    let currentScrollV = 0;

    const render = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      const targetV = scrollVelocityRef.current;
      currentScrollV += (targetV - currentScrollV) * 0.1;

      particles.forEach(p => {
        p.y -= p.speedY;
        p.x -= currentScrollV * 0.3 * (p.size / 2);

        if (p.y < 0) {
          p.y = canvas.height;
          p.x = Math.random() * canvas.width;
        }
        if (p.x < 0) p.x = canvas.width;
        if (p.x > canvas.width) p.x = 0;

        ctx.fillStyle = `rgba(255, 255, 255, ${p.opacity})`;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();
      });
      
      scrollVelocityRef.current *= 0.9;
      
      animationFrameId = requestAnimationFrame(render);
    };
    render();

    return () => {
      window.removeEventListener('resize', resize);
      cancelAnimationFrame(animationFrameId);
    };
  }, [scrollVelocityRef]);

  return <canvas ref={canvasRef} className="absolute inset-0 z-0 pointer-events-none" />;
}
