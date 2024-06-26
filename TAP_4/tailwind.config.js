/** @type {import('tailwindcss').Config} */

const withMT = require("@material-tailwind/html/utils/withMT");

module.exports = withMT({
  mode: 'jit',
  content: ["./templates/**/*.{html,htm}"],
  theme: {
    extend: {},
  },
  plugins: [],
})

