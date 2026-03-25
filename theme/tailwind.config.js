/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // Templates
    '../templates/**/*.{html,js}',
    '../**/templates/**/*.{html,js}',
    // Python files
    '../**/*.py',
    // Static files
    '../static/**/*.{js,css}',
    // Theme files
    './static_src/**/*.{js,css}',
  ],
  safelist: [
    // Form input classes
    {
      pattern: /^(mt|mb|mr|ml|my|mx|px|py|p|m)-(0|0.5|1|1.5|2|3|4|5|6|8|10|12|16|20|24|32|40|48|56|64)$/,
      variants: ['sm', 'md', 'lg'],
    },
    {
      pattern: /^(w|h)-(0|0.5|1|1.5|2|3|4|5|6|8|10|12|16|20|24|32|40|48|56|64|full|screen)$/,
    },
    {
      pattern: /^(border|bg|text)-(primary|secondary|accent|gray|red|yellow|green|blue)(-\d{2,3})?$/,
    },
    {
      pattern: /^(rounded|shadow)(-(?:sm|md|lg|xl|2xl|3xl|full))?$/,
    },
    {
      pattern: /^(hover|focus|active|disabled|group-hover):./,
    },
    // Specific form classes
    'form-input',
    'form-select',
    'form-checkbox',
    'form-radio',
    // Layout classes
    'flex',
    'items-center',
    'justify-between',
    'space-x-4',
    'space-y-4',
    'grid',
    'grid-cols-1',
    'grid-cols-2',
    'grid-cols-3',
    'gap-4',
    'gap-6',
    // Typography
    'text-sm',
    'text-base',
    'text-lg',
    'text-xl',
    'text-2xl',
    'font-medium',
    'font-semibold',
    'font-bold',
    // States
    'focus:outline-none',
    'focus:ring',
    'focus:ring-opacity-50',
    'focus:border-primary-500',
    'focus:ring-primary-500',
    'hover:bg-primary-700',
    'hover:bg-gray-700',
    'bg-primary',
    'text-primary',
    'bg-secondary',
    'text-secondary',
    'hover:bg-primary-700',
    'hover:bg-secondary-700',
    'focus:ring-primary-400',
    'focus:ring-secondary-400',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#4F46E5',
          50: '#FFFFFF',
          100: '#F5F5FF',
          200: '#E2E1FF',
          300: '#CECBFF',
          400: '#BAB6FF',
          500: '#A7A1FF',
          600: '#938CFF',
          700: '#7F77FF',
          800: '#6B62FF',
          900: '#574DFF',
        },
        secondary: {
          DEFAULT: '#EC4899',
          50: '#FFFFFF',
          100: '#FEF6FA',
          200: '#FCDCEA',
          300: '#FAC2DA',
          400: '#F8A8CA',
          500: '#F68EBA',
          600: '#F474AA',
          700: '#F25A9A',
          800: '#F0408A',
          900: '#EE267A',
        },
        accent: {
          DEFAULT: '#E9C46A',
          50: '#FDF9F0',
          100: '#FBF3E1',
          200: '#F7E7C3',
          300: '#F3DBA5',
          400: '#EFCF87',
          500: '#EBC369',
          600: '#E7B74B',
          700: '#E9C46A',
          800: '#BA9C54',
          900: '#89733E',
        },
      },
      fontFamily: {
        sans: ['Inter var', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'Noto Sans', 'sans-serif'],
      },
      spacing: {
        '128': '32rem',
      },
      maxWidth: {
        '8xl': '88rem',
      },
      height: {
        'screen-1/2': '50vh',
        'screen-3/4': '75vh',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ],
}
