/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bac: "#356c52",
      },
      fontFamily: {
        playfair: "'Playfair Display',serif",
        lato: "'Lato',serif",
      },
    },
  },
  plugins: [],
};
