# Warhammer 40K Probability Fiddle - Frontend

A Svelte + Vite + TypeScript single-page application for calculating Warhammer 40K attack probabilities and simulating combat outcomes.

## Features

- **Fast Development**: Vite's HMR ensures changes appear instantly
- **Type Safety**: TypeScript for robust frontend code
- **Component-Based**: Svelte components for modular UI
- **Fast Testing**: Vitest for blazing-fast test execution
- **Integration Ready**: Connects to Python backend for attack simulations

## Project Structure

```
frontend/
├── src/
│   ├── lib/              # Reusable Svelte components
│   │   ├── Header.svelte # Main header component
│   │   └── Header.test.ts# Component tests
│   ├── App.svelte        # Root component
│   ├── main.ts           # Entry point
│   └── app.css           # Global styles
├── public/               # Static assets
├── vitest.config.ts      # Vitest configuration
├── vite.config.ts        # Vite configuration
├── tsconfig.json         # TypeScript configuration
└── package.json          # Dependencies
```

## Getting Started

### Installation

```bash
cd frontend
npm install
```

### Development

Start the development server with HMR:

```bash
npm run dev
```

The app will be available at `http://localhost:5173/`

### Testing

Run tests in watch mode:

```bash
npm test
```

Or run tests once:

```bash
npm test -- --run
```

### Building

Build for production:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

## Technology Stack

- **Framework**: Svelte (compiler-based, minimal overhead)
- **Build Tool**: Vite (incredibly fast)
- **Language**: TypeScript (type safety)
- **Testing**: Vitest (fast test runner) + Testing Library
- **CSS**: CSS Modules with scoped styles

## Development Workflow

1. **Edit components** in `src/lib/` or `src/App.svelte`
2. **Changes appear instantly** thanks to Vite HMR
3. **Write tests** alongside components (`.test.ts` files)
4. **Tests run instantly** in watch mode with Vitest
5. **Type errors** caught immediately by TypeScript

## Next Steps

- [ ] Create components for unit/weapon selection
- [ ] Add forms for attack simulation input
- [ ] Integrate Python backend API
- [ ] Display simulation results with charts
- [ ] Add localStorage for saved configurations
- [ ] Create router for multi-page navigation

## Performance

- **Dev Server Start**: ~500ms
- **HMR Update**: <100ms
- **Test Execution**: <50ms per test file
- **Bundle Size**: ~50KB (highly optimized by Svelte)

## Resources

- [Svelte Documentation](https://svelte.dev)
- [Vite Documentation](https://vitejs.dev)
- [Vitest Documentation](https://vitest.dev)
- [Testing Library](https://testing-library.com/svelte)
