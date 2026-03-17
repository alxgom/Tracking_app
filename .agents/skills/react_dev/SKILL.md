name: Web React/Next.js UI Best Practices
description: Guidelines for building clean, maintainable Web applications using React/Next.js.
---

# Web Best Practices

When building the Tracking Web App, you MUST adhere to these guidelines:

1. **Separation of Concerns:** Keep the UI React components entirely separate from backend API logic. Use a clear folder structure (e.g. `src/components`, `src/app`).
2. **Componentization:** Make heavy use of reusable React functional components. Break out components (Sidebar, Stopwatch, History List) to keep the codebase clean.
3. **Aesthetics & Styling:** Follow modern web design best practices (e.g., vibrant colors, dark modes, glassmorphism, dynamic animations). Use standard CSS or TailwindCSS based on project configuration. Ensure the UI looks premium.
4. **State Management:** Use robust state management (e.g., React `useState`, `useEffect`, Context API) to instantly refresh views when a database action occurs.
