/** @type {import('tailwindcss').Config} */
export const content = [
  "./node_modules/flowbite-vue/**/*.{js,jsx,ts,tsx}",
  "./node_modules/flowbite/**/*.{js,jsx,ts,tsx}",
];
export const theme = {
  extend: {
    colors: {
      primary: "#4994c4",
    },
  },
};
export const plugins = [require("flowbite/plugin")];
