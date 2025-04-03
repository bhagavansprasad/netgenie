/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./src/components/LoginPage.css", // Add this line
    "./src/components/dashboard.jsx", // Add this line
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}