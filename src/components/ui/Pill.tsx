import type { ReactNode } from 'react'
import { Check } from './Icons'

type Tone = 'ok' | 'neutral' | 'solid'

const tones: Record<Tone, string> = {
  ok: 'bg-ok-wash text-forest',
  neutral: 'bg-bone text-quiet',
  solid: 'bg-bone text-graphite',
}

export function Pill({ tone = 'neutral', icon, children }: { tone?: Tone; icon?: boolean; children: ReactNode }) {
  return (
    <span className={`text-body-s inline-flex shrink-0 items-center gap-1.5 rounded-full px-3 py-1 font-medium ${tones[tone]}`}>
      {icon && <Check className="h-3.5 w-3.5" />}
      {children}
    </span>
  )
}
