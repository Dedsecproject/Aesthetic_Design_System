# Design Rules

## Allowed / preferred / prohibited

| Area | Preferred | Allowed when justified | Prohibited |
| --- | --- | --- | --- |
| Color | Neutral foundation + one solid accent | A second accent for a documented product need | Gradients, radiant colors, neon, glow effects |
| Surfaces | Flat canvas, solid surface, 1px boundaries | One restrained elevation level for transient UI | Glassmorphism, translucent panels as decoration |
| Shape | Small, consistent radii | Larger radius for a prominent container | Random radius values, pill-shaped everything |
| Type | System or product sans, clear scale, sentence case | Monospace for data/code | Decorative display type for product UI, all caps paragraphs |
| Layout | Grid, alignment, whitespace, max-width | Full-bleed content when content benefits | Arbitrary offsets, dense edge-to-edge control clusters |
| Motion | 120–200ms state changes, reduced-motion support | 200–300ms for larger layout transitions | Motion that blocks work, looping decoration, parallax |
| Imagery | Functional, relevant, accessible | Brand illustration with a clear role | Stock-photo filler, decorative noise |

## Color and contrast

- Use `bg.canvas` for the page, `bg.surface` for containers, and `bg.subtle` for quiet grouping.
- Use `text.primary` for essential content and `text.secondary` for supporting content. Do not use muted text for required instructions.
- Use `action.primary.*` for the single most important action in a region. Use secondary or quiet actions for alternatives.
- Status colors communicate meaning and must be paired with text, icons, or patterns.
- Do not communicate state with color alone.
- Verify normal text at 4.5:1 and large text at 3:1 minimum; target stronger contrast for essential UI and boundaries.

## Layout and responsive behavior

- Base spacing on the 4px scale; prefer 8px increments for major layout gaps.
- Keep a readable content measure: roughly 60–75 characters per line for prose.
- Use a page gutter of 16px on small screens, 24px at medium widths, and up to 32px on large screens.
- At narrow widths, stack secondary actions, allow labels to wrap, and move low-priority columns into a details view.
- Never require horizontal scrolling for primary tasks unless the content is inherently tabular or canvas-like.
- Preserve touch targets at least 44×44 CSS px where practical.

## Typography

- Use sentence case for labels, headings, buttons, tabs, and navigation.
- Use weight and size to create hierarchy; do not rely on color alone.
- Keep body text at 16px or larger where space permits. Do not set long-form text below 14px.
- Use tabular numerals for comparable figures and timestamps.
- Do not truncate essential content. If truncation is unavoidable, provide the full value on focus/hover and in accessible text.

## Interaction and accessibility

- Every control needs a visible `:focus-visible` treatment.
- Every icon-only control needs an accessible name and a tooltip only as supplemental help.
- Disabled controls should remain understandable and must not be the only place an error is explained.
- Errors identify the field, explain the problem, and state how to fix it.
- Loading states preserve layout and communicate what is happening.
- Respect `prefers-reduced-motion` and provide a non-motion equivalent.
