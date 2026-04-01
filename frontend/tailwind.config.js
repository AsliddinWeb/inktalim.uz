// Tailwind CSS konfiguratsiyasi — rang tizimi va dark mode
/** @type {import('tailwindcss').Config} */
export default {
  // Dark mode — html elementiga 'dark' class qo'shish orqali ishlaydi
  darkMode: 'class',

  // Tailwind qaysi fayllarda ishlatilganini kuzatish
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],

  theme: {
    extend: {
      // ─── Asosiy rang palitasi ───────────────────────────────────────────
      colors: {
        // Birlamchi rang — binafsha (purple)
        primary: {
          50:  '#F0EFFE',
          100: '#E0DFFE',
          200: '#C1BFFD',
          300: '#A39EFC',
          400: '#857EFA',
          500: '#6C63FF', // asosiy
          600: '#5A52D9',
          700: '#4840B3',
          800: '#352D8A',
          900: '#231C66',
        },
        // Ikkilamchi rang — oltin sariq (amber)
        secondary: {
          50:  '#FFFBEB',
          100: '#FEF3C7',
          200: '#FDE68A',
          300: '#FCD34D',
          400: '#FBBF24',
          500: '#F59E0B', // asosiy
          600: '#D97706',
          700: '#B45309',
          800: '#92400E',
          900: '#78350F',
        },
        // Muvaffaqiyat — emerald
        success: {
          50:  '#ECFDF5',
          100: '#D1FAE5',
          200: '#A7F3D0',
          300: '#6EE7B7',
          400: '#34D399',
          500: '#10B981', // asosiy
          600: '#059669',
          700: '#047857',
          800: '#065F46',
          900: '#064E3B',
        },
        // Xato rangi
        danger: {
          50:  '#FEF2F2',
          100: '#FEE2E2',
          200: '#FECACA',
          300: '#FCA5A5',
          400: '#F87171',
          500: '#EF4444', // asosiy
          600: '#DC2626',
          700: '#B91C1C',
          800: '#991B1B',
          900: '#7F1D1D',
        },
        // ─── Yuzalar ─────────────────────────────────────────────────────
        surface: {
          light: '#FFFFFF',
          dark:  '#1A1A2E',
        },
      },

      // ─── Shrift sozlamalari ────────────────────────────────────────────
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },

      // ─── Animatsiyalar ─────────────────────────────────────────────────
      transitionDuration: {
        DEFAULT: '200ms',
      },
      animation: {
        'fade-in':    'fadeIn 0.2s ease-out',
        'slide-in':   'slideIn 0.25s ease-out',
        'spin-slow':  'spin 1.5s linear infinite',
      },
      keyframes: {
        fadeIn: {
          '0%':   { opacity: '0', transform: 'translateY(-4px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideIn: {
          '0%':   { opacity: '0', transform: 'translateX(-8px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
      },

      // ─── Box shadow ────────────────────────────────────────────────────
      boxShadow: {
        'card':       '0 1px 3px rgba(108,99,255,0.08), 0 1px 2px rgba(108,99,255,0.05)',
        'card-hover': '0 10px 25px rgba(108,99,255,0.15), 0 4px 6px rgba(108,99,255,0.08)',
        'input':      '0 0 0 3px rgba(108,99,255,0.15)',
      },
    },
  },

  plugins: [
    require('@tailwindcss/forms')({
      strategy: 'class',
    }),
  ],
}
