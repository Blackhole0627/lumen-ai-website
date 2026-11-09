import type { ReactNode } from 'react'

/** Small building blocks for the product mock-ups shown in cards. */

export function Panel({ children, className = '', tone = 'paper' }: { children: ReactNode; className?: string; tone?: 'paper' | 'bone' | 'bone-2' }) {
  const bg = tone === 'paper' ? 'bg-paper' : tone === 'bone' ? 'bg-bone' : 'bg-bone-2'
  return <div className={`rounded-2xl ${bg} shadow-[var(--shadow-card)] ${className}`}>{children}</div>
}

export function Row({ label, value, strong }: { label: ReactNode; value: ReactNode; strong?: boolean }) {
  return (
    <div className="flex items-center gap-3 px-4 py-3">
      <span className={`text-body-m flex-1 ${strong ? 'font-medium text-coal' : 'text-quiet'}`}>{label}</span>
      <span className="text-body-m font-medium tabular-nums text-coal">{value}</span>
    </div>
  )
}

export function Rows({ children }: { children: ReactNode }) {
  return <Panel className="divide-y divide-line-soft">{children}</Panel>
}

export function Avatar({ text, tone = 'wash', size = 32 }: { text: ReactNode; tone?: 'wash' | 'moss'; size?: number }) {
  return (
    <span
      className={`text-body-s grid shrink-0 place-items-center rounded-full font-medium ${tone === 'wash' ? 'bg-forest-wash text-forest' : 'bg-moss text-paper'}`}
      style={{ width: size, height: size }}
    >
      {text}
    </span>
  )
}

export function Progress({ value, className = '' }: { value: number; className?: string }) {
  return (
    <span className={`block h-1.5 overflow-hidden rounded-full bg-bone-2 ${className}`}>
      <span className="block h-full rounded-full bg-moss transition-[width] duration-1000" style={{ width: `${value}%` }} />
    </span>
  )
}

/**
 * Card backdrop: a blurred abstract gradient stands in for the photographic backgrounds
 * used on the reference site. Swap for licensed photography when available.
 */
export function ArtBackdrop({ seed, children, className = '' }: { seed: number; children: ReactNode; className?: string }) {
  const h = (seed * 47) % 360
  return (
    <div className={`relative overflow-hidden rounded-card bg-bone-2 ${className}`}>
      <div
        className="absolute inset-0 scale-125 blur-[10px]"
        style={{
          background: `radial-gradient(60% 50% at ${20 + (seed * 13) % 60}% ${15 + (seed * 29) % 50}%, hsl(${h} 25% 80%), transparent),
                       radial-gradient(50% 60% at ${80 - (seed * 17) % 50}% 85%, hsl(${(h + 40) % 360} 22% 74%), transparent),
                       linear-gradient(160deg, #eceae3, #dcdcd3)`,
        }}
      />
      <div className="relative h-full">{children}</div>
    </div>
  )
}
