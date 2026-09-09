# Buttons

## Purpose and anatomy

Button = optional leading icon + visible label + optional trailing icon. Use a link for navigation and a button for an action.

## Variants

- **Primary:** one per region for the main task; `action.primary.*`.
- **Secondary:** important alternative; solid surface with a boundary.
- **Quiet:** low-emphasis action; transparent until hover.
- **Danger:** destructive action; use sparingly and confirm irreversible work.

## Rules

- Minimum 40px control height; use 44px or larger for touch-first contexts.
- Keep labels short and verb-led: “Save changes”, “Add member”.
- Do not use icon-only buttons when a text label fits. Icon-only buttons require an accessible name.
- States: default, hover, active, focus-visible, disabled, loading.
- Loading preserves width, disables repeat submission, and exposes status to assistive technology.
- Never use a gradient, glow, or color-only state.
