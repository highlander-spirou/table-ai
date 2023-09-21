/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["../templates/**/*.html", "./index.css", "./main.js"],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
};
