import { BRAND } from '../../config/brand'

/** Placeholder wordmark: four-bar voice glyph + brand name. Replace with the client's SVG logo. */
export function Logo({ className = '' }: { className?: string }) {
  return (
    <span className={`inline-flex items-center gap-2 ${className}`}>
      <svg viewBox="0 0 24 24" className="h-[22px] w-[22px]" aria-hidden>
        <rect width="24" height="24" rx="6" fill="currentColor" />
        <g fill="var(--color-mint)">
          <rect x="5" y="9" width="2.4" height="6" rx="1.2" />
          <rect x="9" y="6" width="2.4" height="12" rx="1.2" />
          <rect x="13" y="7.5" width="2.4" height="9" rx="1.2" />
          <rect x="17" y="10" width="2.4" height="4" rx="1.2" />
        </g>
      </svg>
      <span className="text-[19px] font-semibold tracking-[-0.03em]">{BRAND.name}</span>
    </span>
  )
}
