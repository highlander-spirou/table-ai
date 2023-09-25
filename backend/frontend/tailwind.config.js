/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html", "./templates/**/*.css", "./templates/**/*.js"],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
};
