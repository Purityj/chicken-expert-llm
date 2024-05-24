/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/templates/*.html',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Roboto', 'sans-serif'],
      },
      gridTemplateColumns: {
        '70/30' : '70% 28%',
      },
    },
  },
  plugins: [],
}

