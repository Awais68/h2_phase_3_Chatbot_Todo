/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}", "./app/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#00ffff",
          hover: "#00d4d4",
        },
        secondary: {
          DEFAULT: "#39ff14",
          hover: "#32d911",
        },
        accent: {
          DEFAULT: "#ff0080",
          hover: "#d4006b",
        },
        warning: "#ffb302",
        destructive: "#ff4444",
        success: "#00ff88",
        info: "#00bfff",
        background: "#0a0a0f",
        surface: "#12121a",
        card: "#16161f",
        border: "rgba(0, 255, 255, 0.2)",
        foreground: "#e0e0e0",
        "muted-foreground": "#888899",
      },
      fontFamily: {
        display: ["var(--font-display)", "Orbitron", "sans-serif"],
        mono: ["var(--font-mono)", "Roboto Mono", "monospace"],
        sans: ["var(--font-sans)", "Noto Sans", "system-ui", "sans-serif"],
      },
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
    },
  },
  plugins: [],
};
