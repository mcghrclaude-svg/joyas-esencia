/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        // Tokens placeholder. Reemplazar cuando exista definicion de
        // marca real. Ver ADR-002 en docs/ADR.md: todo el estilo se
        // resuelve via Tailwind, sin CSS custom.
        brand: {
          DEFAULT: "#8a6d3b",
          light: "#c9a876",
          dark: "#5c4826",
        },
      },
    },
  },
  plugins: [],
};
