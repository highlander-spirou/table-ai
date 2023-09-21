/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["../templates/**/*.html", "./index.css"],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
};
