/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["../templates/**/*.html", "../static/src/**/*.js", "./index.css"],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
};
