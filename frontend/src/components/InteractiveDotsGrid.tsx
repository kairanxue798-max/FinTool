import { useEffect, useRef } from 'react'
import { gsap } from 'gsap'
import './InteractiveDotsGrid.css'

interface Dot {
  x: number
  y: number
  element: HTMLDivElement
}

function InteractiveDotsGrid() {
  const containerRef = useRef<HTMLDivElement>(null)
  const dotsRef = useRef<Dot[]>([])
  const mouseRef = useRef({ x: 0, y: 0 })
  const animationFrameRef = useRef<number>()

  useEffect(() => {
    if (!containerRef.current) return

    const container = containerRef.current
    const dots: Dot[] = []
    
    // Grid configuration
    const cols = 20
    const rows = 15
    const spacing = 60
    const startX = (window.innerWidth - (cols - 1) * spacing) / 2
    const startY = (window.innerHeight - (rows - 1) * spacing) / 2

    // Create dots grid
    const centerX = window.innerWidth / 2
    const centerY = window.innerHeight / 2
    
    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < cols; col++) {
        const x = startX + col * spacing
        const y = startY + row * spacing
        
        // Skip center area for dollar icon
        const distanceFromCenter = Math.sqrt(
          Math.pow(x - centerX, 2) + Math.pow(y - centerY, 2)
        )
        
        if (distanceFromCenter < 100) {
          continue // Skip dots near center
        }

        const dot = document.createElement('div')
        dot.className = 'interactive-dot'
        
        gsap.set(dot, {
          x: x,
          y: y,
          scale: 0.5,
          opacity: 0.3,
        })

        container.appendChild(dot)
        dots.push({ x, y, element: dot })
      }
    }

    dotsRef.current = dots

    // Mouse move handler
    const handleMouseMove = (e: MouseEvent) => {
      mouseRef.current = {
        x: e.clientX,
        y: e.clientY,
      }
    }

    window.addEventListener('mousemove', handleMouseMove)

    // Animation loop
    const animate = () => {
      dots.forEach((dot) => {
        const dx = mouseRef.current.x - dot.x
        const dy = mouseRef.current.y - dot.y
        const distance = Math.sqrt(dx * dx + dy * dy)
        const maxDistance = 200

        if (distance < maxDistance) {
          const force = (maxDistance - distance) / maxDistance
          const angle = Math.atan2(dy, dx)
          const moveX = Math.cos(angle) * force * 30
          const moveY = Math.sin(angle) * force * 30
          const scale = 0.5 + force * 0.8
          const opacity = 0.3 + force * 0.7

          gsap.to(dot.element, {
            x: dot.x + moveX,
            y: dot.y + moveY,
            scale: scale,
            opacity: opacity,
            duration: 0.3,
            ease: 'power2.out',
          })
        } else {
          gsap.to(dot.element, {
            x: dot.x,
            y: dot.y,
            scale: 0.5,
            opacity: 0.3,
            duration: 0.5,
            ease: 'power2.out',
          })
        }
      })

      animationFrameRef.current = requestAnimationFrame(animate)
    }

    animate()

    // Handle window resize
    const handleResize = () => {
      // Recalculate positions on resize
      const newStartX = (window.innerWidth - (cols - 1) * spacing) / 2
      const newStartY = (window.innerHeight - (rows - 1) * spacing) / 2
      const newCenterX = window.innerWidth / 2
      const newCenterY = window.innerHeight / 2

      // Rebuild dots array with new positions
      const newDots: Dot[] = []
      dots.forEach((dot, index) => {
        const row = Math.floor(index / cols)
        const col = index % cols
        const newX = newStartX + col * spacing
        const newY = newStartY + row * spacing
        
        const distanceFromCenter = Math.sqrt(
          Math.pow(newX - newCenterX, 2) + Math.pow(newY - newCenterY, 2)
        )
        
        if (distanceFromCenter >= 100) {
          dot.x = newX
          dot.y = newY
          gsap.set(dot.element, {
            x: newX,
            y: newY,
          })
          newDots.push(dot)
        } else {
          // Remove dot if it's now in center area
          if (dot.element.parentNode) {
            dot.element.parentNode.removeChild(dot.element)
          }
        }
      })
      dotsRef.current = newDots
    }

    window.addEventListener('resize', handleResize)

    return () => {
      window.removeEventListener('mousemove', handleMouseMove)
      window.removeEventListener('resize', handleResize)
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
      }
      dots.forEach((dot) => {
        if (dot.element.parentNode) {
          dot.element.parentNode.removeChild(dot.element)
        }
      })
    }
  }, [])

  return (
    <div className="interactive-dots-container" ref={containerRef}>
      <div className="dollar-icon-container">
        <div className="dollar-icon">$</div>
        <div className="dollar-glow"></div>
      </div>
    </div>
  )
}

export default InteractiveDotsGrid

