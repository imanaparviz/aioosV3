/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        "primary": "#4182ec",
        "primary-blue": "#0052cc",
        "secondary-gray": "#5E6C84",
        "success": "#28a745",
        "success-green": "#00875A",
        "warning": "#ffc107",
        "warning-yellow": "#FFAB00",
        "error": "#dc3545",
        "error-red": "#DE350B",
        "danger": "#E74C3C",
        "background-light": "#f6f7f8",
        "background-dark": "#111721",
        "card-light": "#ffffff",
        "card-dark": "#1f2937",
        "container-light": "#ffffff",
        "container-dark": "#1D283A",
        "surface-light": "#ffffff",
        "surface-dark": "#1a222e",
        "text-light": "#0e131b",
        "text-dark": "#f3f4f6",
        "subtext-light": "#4d6a99",
        "subtext-dark": "#a0aec0",
        "border-light": "#e7ecf3",
        "border-dark": "#334155"
      },
      fontFamily: {
        "display": ["Inter", "sans-serif"]
      },
      borderRadius: {
        "DEFAULT": "0.25rem",
        "lg": "0.5rem",
        "xl": "0.75rem",
        "full": "9999px"
      },
    },
  },
  plugins: [require('@tailwindcss/forms')],
}
