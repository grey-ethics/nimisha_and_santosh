// tailwind.config.cjs
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'office-blue': '#1A4E8A',      // pick exact shade
        'office-blue-dark': '#123963',
        'office-red': '#B3261E',
        'office-red-dark': '#7A1A15'
      }
    },
  },
  plugins: [],
}
