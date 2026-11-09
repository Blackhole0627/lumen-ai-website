import type { ReactNode } from 'react'

/** Two-line display heading: first line strong, second line muted. */
export function SectionHeading({
  id,
  lead,
  rest,
  tone = 'dark',
  className = '',
}: {
  id?: string
  lead: ReactNode
  rest?: ReactNode
  tone?: 'dark' | 'light'
  className?: string
}) {
  const strong = tone === 'dark' ? 'text-coal' : 'text-paper'
  const muted = tone === 'dark' ? 'text-slate' : 'text-paper/55'
  return (
    <h2 id={id} className={`text-h2 text-balance ${strong} ${className}`}>
      <span className="sm:block">{lead} </span>
      {rest && <span className={muted}>{rest}</span>}
    </h2>
  )
}
