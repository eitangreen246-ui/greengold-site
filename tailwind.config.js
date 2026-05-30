/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./**/templates/**/*.html",
    "./core/**/*.py",
    "./cms/**/*.py",
    "./leads/**/*.py",
  ],
  theme: {
    extend: {
      colors: {
        // Brand palette (source of truth — see brand guideline doc)
        forest: {
          DEFAULT: "#1A4D2E", // primary — deep forest green
          700: "#1A4D2E",
          800: "#143d24",
          900: "#0f2e1b",
          600: "#2d7a4a",
          50: "#e9f2ec",
        },
        gold: {
          DEFAULT: "#D4AF37", // secondary — luxe gold (large/fills only)
          text: "#9A7B1E", // accessible gold for small text/links on white
          soft: "#f7f0d8",
        },
        neutralgray: "#B1B1B1",
        bg: "#F2F4F2", // off-white page background
        ink: "#1A1A1A", // body text
      },
      fontFamily: {
        serif: ["Fraunces", "Georgia", "serif"], // premium scientific headings
        sans: ["Inter", "system-ui", "Arial", "sans-serif"], // clean body/UI
      },
      maxWidth: {
        content: "72rem", // ~max-w-6xl content container
      },
      boxShadow: {
        card: "0 1px 2px rgba(16,40,24,0.04), 0 8px 24px rgba(16,40,24,0.06)",
        "card-hover": "0 2px 4px rgba(16,40,24,0.06), 0 16px 40px rgba(16,40,24,0.10)",
      },
    },
  },
  plugins: [],
};
