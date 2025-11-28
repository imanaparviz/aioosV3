/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: '#4182ec',
        'background-light': '#f6f7f8',
        'background-dark': '#111721',
      },
      fontFamily: {
        display: ['Inter', 'sans-serif']
      },
    },
  },
  plugins: [],
}
