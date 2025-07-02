/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", // Template at the project level
    "./**/templates/**/*.html", // Template at the app level 
    
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

