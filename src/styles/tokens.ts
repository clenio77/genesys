/**
 * Design System Tokens
 * Genesys Tecnologia - Elegância Jurídica encontra Inovação Tecnológica
 */

// ============================================================================
// COLORS - Paleta de Cores
// ============================================================================

export const colors = {
  // Jurídico (Seriedade e Confiança)
  juridico: {
    navyDark: '#0f172a',
    navy: '#1e293b',
    slate: '#334155',
    slateLight: '#475569',
    gold: '#d4af37',
    goldLight: '#f4d03f',
    burgundy: '#7c2d12',
    burgundyLight: '#991b1b',
  },

  // Tecnologia (Inovação e Modernidade)
  tech: {
    blue: '#3b82f6',
    blueLight: '#60a5fa',
    blueDark: '#2563eb',
    cyan: '#06b6d4',
    cyanLight: '#22d3ee',
    purple: '#8b5cf6',
    purpleLight: '#a78bfa',
    purpleDark: '#7c3aed',
    emerald: '#10b981',
    emeraldLight: '#34d399',
    amber: '#f59e0b',
    amberLight: '#fbbf24',
  },

  // Neutros
  neutral: {
    white: '#ffffff',
    black: '#000000',
    gray50: '#f9fafb',
    gray100: '#f3f4f6',
    gray200: '#e5e7eb',
    gray300: '#d1d5db',
    gray400: '#9ca3af',
    gray500: '#6b7280',
    gray600: '#4b5563',
    gray700: '#374151',
    gray800: '#1f2937',
    gray900: '#111827',
  },

  // Estados
  status: {
    success: '#10b981',
    warning: '#f59e0b',
    error: '#ef4444',
    info: '#3b82f6',
  },
}

// ============================================================================
// GRADIENTS - Gradientes
// ============================================================================

export const gradients = {
  hero: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  buttonPrimary: 'linear-gradient(135deg, #2563eb 0%, #7c3aed 100%)',
  buttonSecondary: 'linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%)',
  icon: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
  text: 'linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%)',
  card: 'linear-gradient(135deg, #1e293b 0%, #334155 100%)',
  overlay: 'linear-gradient(180deg, rgba(15, 23, 42, 0) 0%, rgba(15, 23, 42, 0.8) 100%)',
}

// ============================================================================
// TYPOGRAPHY - Tipografia
// ============================================================================

export const typography = {
  // Famílias de Fontes
  fontFamily: {
    playfair: '"Playfair Display", serif', // Títulos elegantes
    inter: '"Inter", sans-serif', // Corpo moderno
    jetbrains: '"JetBrains Mono", monospace', // Código técnico
  },

  // Tamanhos de Fonte
  fontSize: {
    xs: '0.75rem', // 12px
    sm: '0.875rem', // 14px
    base: '1rem', // 16px
    lg: '1.125rem', // 18px
    xl: '1.25rem', // 20px
    '2xl': '1.5rem', // 24px
    '3xl': '1.875rem', // 30px
    '4xl': '2.25rem', // 36px
    '5xl': '3rem', // 48px
    '6xl': '3.75rem', // 60px
    '7xl': '4.5rem', // 72px
    '8xl': '6rem', // 96px
    '9xl': '8rem', // 128px
  },

  // Pesos de Fonte
  fontWeight: {
    thin: '100',
    extralight: '200',
    light: '300',
    normal: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
    extrabold: '800',
    black: '900',
  },

  // Altura de Linha
  lineHeight: {
    none: '1',
    tight: '1.25',
    snug: '1.375',
    normal: '1.5',
    relaxed: '1.625',
    loose: '2',
  },

  // Espaçamento de Letras
  letterSpacing: {
    tighter: '-0.05em',
    tight: '-0.025em',
    normal: '0em',
    wide: '0.025em',
    wider: '0.05em',
    widest: '0.1em',
  },
}

// ============================================================================
// SPACING - Espaçamento
// ============================================================================

export const spacing = {
  px: '1px',
  0: '0',
  0.5: '0.125rem', // 2px
  1: '0.25rem', // 4px
  1.5: '0.375rem', // 6px
  2: '0.5rem', // 8px
  2.5: '0.625rem', // 10px
  3: '0.75rem', // 12px
  3.5: '0.875rem', // 14px
  4: '1rem', // 16px
  5: '1.25rem', // 20px
  6: '1.5rem', // 24px
  7: '1.75rem', // 28px
  8: '2rem', // 32px
  9: '2.25rem', // 36px
  10: '2.5rem', // 40px
  11: '2.75rem', // 44px
  12: '3rem', // 48px
  14: '3.5rem', // 56px
  16: '4rem', // 64px
  20: '5rem', // 80px
  24: '6rem', // 96px
  28: '7rem', // 112px
  32: '8rem', // 128px
  36: '9rem', // 144px
  40: '10rem', // 160px
  44: '11rem', // 176px
  48: '12rem', // 192px
  52: '13rem', // 208px
  56: '14rem', // 224px
  60: '15rem', // 240px
  64: '16rem', // 256px
  72: '18rem', // 288px
  80: '20rem', // 320px
  96: '24rem', // 384px
}

// ============================================================================
// BORDER RADIUS - Raios de Borda
// ============================================================================

export const borderRadius = {
  none: '0',
  sm: '0.125rem', // 2px
  base: '0.25rem', // 4px
  md: '0.375rem', // 6px
  lg: '0.5rem', // 8px
  xl: '0.75rem', // 12px
  '2xl': '1rem', // 16px
  '3xl': '1.5rem', // 24px
  full: '9999px',
}

// ============================================================================
// SHADOWS - Sombras
// ============================================================================

export const shadows = {
  sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
  base: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
  md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
  lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
  xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
  '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
  inner: 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
  none: 'none',
  glow: '0 0 20px rgba(59, 130, 246, 0.5)',
  glowPurple: '0 0 20px rgba(139, 92, 246, 0.5)',
  glowGold: '0 0 20px rgba(212, 175, 55, 0.5)',
}

// ============================================================================
// ANIMATIONS - Animações
// ============================================================================

export const animations = {
  // Durações
  duration: {
    fast: '150ms',
    normal: '300ms',
    slow: '500ms',
    slower: '1000ms',
  },

  // Timing Functions
  timing: {
    easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
    easeOut: 'cubic-bezier(0, 0, 0.2, 1)',
    easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
    linear: 'linear',
  },

  // Keyframes
  keyframes: {
    fadeIn: {
      from: { opacity: 0 },
      to: { opacity: 1 },
    },
    fadeOut: {
      from: { opacity: 1 },
      to: { opacity: 0 },
    },
    slideUp: {
      from: { transform: 'translateY(50px)', opacity: 0 },
      to: { transform: 'translateY(0)', opacity: 1 },
    },
    slideDown: {
      from: { transform: 'translateY(-50px)', opacity: 0 },
      to: { transform: 'translateY(0)', opacity: 1 },
    },
    scaleIn: {
      from: { transform: 'scale(0.9)', opacity: 0 },
      to: { transform: 'scale(1)', opacity: 1 },
    },
    float: {
      '0%, 100%': { transform: 'translateY(0)' },
      '50%': { transform: 'translateY(-20px)' },
    },
    glow: {
      '0%, 100%': { boxShadow: '0 0 20px rgba(59, 130, 246, 0.5)' },
      '50%': { boxShadow: '0 0 40px rgba(59, 130, 246, 0.8)' },
    },
  },
}

// ============================================================================
// BREAKPOINTS - Pontos de Quebra Responsivos
// ============================================================================

export const breakpoints = {
  xs: '320px',
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px',
}

// ============================================================================
// Z-INDEX - Camadas
// ============================================================================

export const zIndex = {
  base: 0,
  dropdown: 1000,
  sticky: 1020,
  fixed: 1030,
  modalBackdrop: 1040,
  modal: 1050,
  popover: 1060,
  tooltip: 1070,
}

// ============================================================================
// EXPORT DEFAULT - Exportação Padrão
// ============================================================================

const tokens = {
  colors,
  gradients,
  typography,
  spacing,
  borderRadius,
  shadows,
  animations,
  breakpoints,
  zIndex,
}

export default tokens

