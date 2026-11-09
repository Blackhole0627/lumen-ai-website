# Marketing site (React + TypeScript + Vite + Tailwind v4)

Landing-page rebuild modelled on the layout and interaction patterns of the reference site,
with original placeholder copy and visuals.

## Run

```bash
npm install
npm run dev      # http://localhost:5173
npm run build    # type-check + production build to dist/
```

## Where things live

| What | File |
| --- | --- |
| Brand name, CTA / sign-in / trust-center URLs | `src/config/brand.ts` |
| All page copy (nav, hero, transcripts, FAQ, …) | `src/content/site.ts` |
| Colours, type scale, radii, shadows, motion | `src/index.css` (`@theme`) |
| Page sections, in page order | `src/App.tsx` → `src/components/sections/*` |
| Product mock-ups inside cards | `src/components/art/*` |

## Placeholders to replace before launch

- **Logo**: `src/components/ui/Logo.tsx` (swap for the client's SVG).
- **Font**: Inter Tight (free) stands in for a licensed brand font. Change `--font-text` in `src/index.css`.
- **Customer logos**: text wordmarks in `LogoStrip.tsx`. Use real logos only with permission.
- **Team portraits, voice orbs, card backgrounds**: generated gradients/silhouettes; drop in licensed photography.
- **Certification badges**: generic badges in `Security.tsx`. Use official artwork only once certified.
- **Results figures & testimonial**: illustrative; replace with verified client data.
