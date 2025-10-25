import { Variants } from 'framer-motion'

// Fade Animations
export const fadeIn: Variants = {
  initial: { opacity: 0 },
  animate: { opacity: 1 },
  exit: { opacity: 0 },
}

export const fadeInUp: Variants = {
  initial: { opacity: 0, y: 50 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: 50 },
}

export const fadeInDown: Variants = {
  initial: { opacity: 0, y: -50 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -50 },
}

export const fadeInLeft: Variants = {
  initial: { opacity: 0, x: -50 },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: -50 },
}

export const fadeInRight: Variants = {
  initial: { opacity: 0, x: 50 },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: 50 },
}

// Scale Animations
export const scaleIn: Variants = {
  initial: { opacity: 0, scale: 0.8 },
  animate: { opacity: 1, scale: 1 },
  exit: { opacity: 0, scale: 0.8 },
}

export const scaleUp: Variants = {
  initial: { scale: 0 },
  animate: { scale: 1 },
  exit: { scale: 0 },
}

// Slide Animations
export const slideInLeft: Variants = {
  initial: { x: '-100%' },
  animate: { x: 0 },
  exit: { x: '-100%' },
}

export const slideInRight: Variants = {
  initial: { x: '100%' },
  animate: { x: 0 },
  exit: { x: '100%' },
}

export const slideInUp: Variants = {
  initial: { y: '100%' },
  animate: { y: 0 },
  exit: { y: '100%' },
}

export const slideInDown: Variants = {
  initial: { y: '-100%' },
  animate: { y: 0 },
  exit: { y: '-100%' },
}

// Rotate Animations
export const rotateIn: Variants = {
  initial: { opacity: 0, rotate: -180 },
  animate: { opacity: 1, rotate: 0 },
  exit: { opacity: 0, rotate: 180 },
}

// Stagger Children
export const staggerContainer: Variants = {
  initial: {},
  animate: {
    transition: {
      staggerChildren: 0.1,
    },
  },
}

export const staggerItem: Variants = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
}

// Hover Effects
export const hoverScale = {
  scale: 1.05,
  transition: { type: 'spring', stiffness: 300 },
}

export const hoverGlow = {
  boxShadow: '0 0 20px rgba(59, 130, 246, 0.5)',
  transition: { duration: 0.3 },
}

export const hoverLift = {
  y: -5,
  transition: { type: 'spring', stiffness: 300 },
}

// Tap Effects
export const tapScale = {
  scale: 0.95,
}

// Pulse Animation
export const pulse: Variants = {
  initial: { scale: 1 },
  animate: {
    scale: [1, 1.05, 1],
    transition: {
      duration: 2,
      repeat: Infinity,
      ease: 'easeInOut',
    },
  },
}

// Bounce Animation
export const bounce: Variants = {
  initial: { y: 0 },
  animate: {
    y: [0, -10, 0],
    transition: {
      duration: 1,
      repeat: Infinity,
      ease: 'easeInOut',
    },
  },
}

// Shake Animation
export const shake: Variants = {
  initial: { x: 0 },
  animate: {
    x: [-5, 5, -5, 5, 0],
    transition: {
      duration: 0.5,
    },
  },
}

// Float Animation
export const float: Variants = {
  initial: { y: 0 },
  animate: {
    y: [0, -20, 0],
    transition: {
      duration: 3,
      repeat: Infinity,
      ease: 'easeInOut',
    },
  },
}

// Spin Animation
export const spin: Variants = {
  initial: { rotate: 0 },
  animate: {
    rotate: 360,
    transition: {
      duration: 2,
      repeat: Infinity,
      ease: 'linear',
    },
  },
}

// Page Transitions
export const pageTransition = {
  initial: { opacity: 0, x: -20 },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: 20 },
  transition: { duration: 0.3 },
}

// Modal Animations
export const modalBackdrop: Variants = {
  initial: { opacity: 0 },
  animate: { opacity: 1 },
  exit: { opacity: 0 },
}

export const modalContent: Variants = {
  initial: { opacity: 0, scale: 0.8, y: 50 },
  animate: { opacity: 1, scale: 1, y: 0 },
  exit: { opacity: 0, scale: 0.8, y: 50 },
}

// Card Flip
export const cardFlip: Variants = {
  initial: { rotateY: 0 },
  animate: { rotateY: 180 },
  exit: { rotateY: 0 },
}

// Gradient Animation
export const gradientShift = {
  backgroundPosition: ['0% 50%', '100% 50%', '0% 50%'],
  transition: {
    duration: 5,
    repeat: Infinity,
    ease: 'linear',
  },
}

// Text Reveal
export const textReveal: Variants = {
  initial: { width: 0 },
  animate: {
    width: '100%',
    transition: { duration: 0.5 },
  },
}

// Number Counter
export const numberCounter = (from: number, to: number, duration: number = 2) => ({
  initial: { value: from },
  animate: { value: to },
  transition: { duration, ease: 'easeOut' },
})

// Parallax Effect
export const parallax = (offset: number) => ({
  y: offset,
  transition: { type: 'spring', stiffness: 100 },
})

// Magnetic Effect
export const magnetic = (x: number, y: number) => ({
  x,
  y,
  transition: { type: 'spring', stiffness: 150, damping: 15 },
})

// Ripple Effect
export const ripple: Variants = {
  initial: { scale: 0, opacity: 1 },
  animate: {
    scale: 2,
    opacity: 0,
    transition: { duration: 0.6 },
  },
}

// Typewriter Effect
export const typewriter = (text: string, delay: number = 0.05) => ({
  initial: { width: 0 },
  animate: { width: 'auto' },
  transition: {
    duration: text.length * delay,
    ease: 'linear',
  },
})

// Smooth Scroll
export const smoothScroll = {
  type: 'spring',
  stiffness: 100,
  damping: 20,
}

// Default Transition
export const defaultTransition = {
  duration: 0.5,
  ease: 'easeInOut',
}

// Spring Transition
export const springTransition = {
  type: 'spring',
  stiffness: 300,
  damping: 30,
}

// Slow Transition
export const slowTransition = {
  duration: 1,
  ease: 'easeInOut',
}

