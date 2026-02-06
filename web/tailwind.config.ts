import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        display: ["'Space Grotesk'", "sans-serif"],
        body: ["'Plus Jakarta Sans'", "sans-serif"],
      },
      colors: {
        ink: "#0B0D12",
        sand: "#F7F4EF",
        moss: "#114B3E",
        clay: "#D8C7A8",
        ember: "#FF6A3D",
      },
      backgroundImage: {
        grid: "linear-gradient(to right, rgba(11, 13, 18, 0.08) 1px, transparent 1px), linear-gradient(to bottom, rgba(11, 13, 18, 0.08) 1px, transparent 1px)",
      },
    },
  },
  plugins: [],
};

export default config;
