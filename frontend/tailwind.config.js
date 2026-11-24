/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        midnight: {
          bg: '#0B1120',
          card: '#151F32',
          border: '#23334A',
          hover: '#1B2841',
          muted: '#101726',
        },
        cyber: {
          cyan: '#06B6D4',
          'cyan-dark': '#0891B2',
          'cyan-light': '#22D3EE',
          success: '#22C55E',
          warning: '#F59E0B',
          danger: '#EF4444',
          text: '#E5EDF7',
          secondary: '#94A3B8',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
