# Aesthetic Design System

A reusable, implementation-ready UI design system for calm, minimal, modern product interfaces.

The system is designed to make a consistent product aesthetic repeatable across projects. It combines design principles, enforceable rules, semantic tokens, component guidance, and AI-assisted generation and auditing prompts.

## What this system provides

- Neutral light and dark themes
- Solid accent color foundations
- Semantic color, typography, spacing, radius, and elevation tokens
- Guidance for buttons, inputs, cards, navigation, and tables
- Responsive behavior from 320px through large desktop widths
- Accessibility requirements for contrast, keyboard use, focus, labels, errors, and reduced motion
- Reusable project briefs for adapting the system to a specific product
- UI generation and audit prompts for consistent AI-assisted workflows

## Repository structure

```text
design-system/
├── DESIGN_PRINCIPLES.md       # Design intent and philosophy
├── DESIGN_RULES.md             # Allowed, preferred, and prohibited patterns
├── PROJECT_BRIEF_TEMPLATE.md   # Per-project customization template
├── tokens/
│   ├── colors.json             # Primitive palette and light/dark semantics
│   ├── typography.json         # Type families, scale, weights, and styles
│   ├── spacing.json            # Spacing and layout dimensions
│   ├── radius.json             # Shape tokens
│   └── elevation.json          # Shadow and layering tokens
├── components/                 # Component anatomy, states, and behavior
└── prompts/
    ├── UI_GENERATOR.md         # Prompt for implementation-ready UI specs
    └── UI_AUDITOR.md           # Prompt for design-system compliance reviews
```

## Quick start

1. Copy the `design-system/` directory into your product repository or shared package.
2. Complete `design-system/PROJECT_BRIEF_TEMPLATE.md` for the project.
3. Map the semantic tokens into CSS variables, a theme object, or the equivalent platform layer.
4. Build the documented primitives before composing full screens.
5. Use semantic tokens in components instead of raw color values.
6. Audit representative screens with `design-system/prompts/UI_AUDITOR.md`.

## Design direction

The system favors quiet confidence: clear hierarchy, restrained color, consistent spacing, readable typography, and purposeful interaction. It explicitly excludes gradients, radiant color treatments, glows, neon, glassmorphism, decorative noise, and unnecessary visual effects.

## Themes and customization

Light and dark themes are defined in `design-system/tokens/colors.json`. A project may supply one solid brand accent, but project customization should happen through semantic token mapping and content—not by creating arbitrary component variants or changing the core rules.

## Validation

Before shipping a screen, verify:

- Both themes are readable and have visible boundaries.
- Keyboard focus is visible and interaction order is logical.
- Important meaning is not conveyed by color alone.
- Layouts reflow without breaking primary tasks on narrow screens.
- Loading, empty, success, error, and destructive-action states are covered.
- No prohibited visual treatments or raw palette values were introduced.

See [`design-system/README.md`](design-system/README.md) for the complete implementation guide.
