# Calm Product UI Design System

A reusable, framework-neutral design system for building minimal, modern, professional product interfaces. It turns a restrained visual aesthetic into implementation rules, semantic tokens, component guidance, and repeatable AI prompts.

## Source of truth

1. `DESIGN_PRINCIPLES.md` defines the intent.
2. `DESIGN_RULES.md` defines enforceable decisions.
3. `tokens/*.json` defines machine-readable values.
4. `components/*.md` defines component behavior and anatomy.
5. `prompts/` turns the system into repeatable generation and review workflows.

Project-specific requirements belong in `PROJECT_BRIEF_TEMPLATE.md`; they may extend the system but should not silently change its core rules.

## Use it in a project

1. Copy this `design-system/` directory into the project or add it as a shared package.
2. Fill in `PROJECT_BRIEF_TEMPLATE.md` and keep the file with the project.
3. Load the tokens into CSS variables, a theme provider, or the equivalent platform layer.
4. Build primitives before screens: Button, Input, Card, Navigation, and Table.
5. Use semantic tokens in components. Do not reference raw palette values from screen code.
6. Run `prompts/UI_AUDITOR.md` against each completed screen and resolve every high- or medium-severity finding.

## Token model

The JSON files use three layers:

- `primitive`: raw palette, type scale, spacing scale, radii, and shadow recipes.
- `semantic`: purpose-based aliases such as `bg.canvas`, `text.primary`, and `action.primary.bg`.
- `themes`: light and dark semantic values. Components consume semantic values only.

The `themes` values use `{token.path}` aliases so a token pipeline can resolve them, or they can be mapped directly by a small adapter.

## Non-negotiables

- Solid colors only. No gradients, glows, neon, radiant color treatments, or glassmorphism.
- One primary accent per project, with semantic status colors reserved for status meaning.
- Visible keyboard focus, logical heading structure, accessible names, and WCAG-conscious contrast.
- Responsive layouts must remain usable from 320px through large desktop widths.
- Motion is brief, purposeful, and never required to understand or complete a task.

## Suggested implementation mapping

| System file | Typical implementation |
| --- | --- |
| `tokens/colors.json` | CSS custom properties or theme object |
| `tokens/typography.json` | font-face setup, type utility classes |
| `tokens/spacing.json` | spacing utility scale and layout primitives |
| `tokens/radius.json` | component shape tokens |
| `tokens/elevation.json` | shadow and layering tokens |
| `components/*.md` | component API, states, anatomy, tests |

## Validation checklist

- [ ] No raw hex/rgb values appear in component code.
- [ ] Both themes render with readable text and visible boundaries.
- [ ] Every interactive control has hover, focus-visible, disabled, and error behavior where relevant.
- [ ] Content reflows at narrow widths without horizontal scrolling.
- [ ] Tables have a mobile strategy and do not rely on color alone.
- [ ] Loading, empty, success, and error states are designed.
- [ ] The UI Auditor prompt has been run on representative screens.
