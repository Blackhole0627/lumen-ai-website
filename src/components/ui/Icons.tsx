import type { SVGProps } from 'react'

type P = SVGProps<SVGSVGElement>
const base = { fill: 'none', stroke: 'currentColor', strokeWidth: 1.8, strokeLinecap: 'round', strokeLinejoin: 'round' } as const

export const Check = (p: P) => (
  <svg viewBox="0 0 16 16" {...base} {...p}><path d="M3.5 8.5l3 3 6-7" /></svg>
)
export const ArrowRight = (p: P) => (
  <svg viewBox="0 0 16 16" {...base} {...p}><path d="M3 8h10M9 4l4 4-4 4" /></svg>
)
export const ArrowLeft = (p: P) => (
  <svg viewBox="0 0 16 16" {...base} {...p}><path d="M13 8H3M7 4L3 8l4 4" /></svg>
)
export const ChevronDown = (p: P) => (
  <svg viewBox="0 0 16 16" {...base} {...p}><path d="M4 6l4 4 4-4" /></svg>
)
export const Globe = (p: P) => (
  <svg viewBox="0 0 16 16" {...base} strokeWidth={1.4} {...p}>
    <circle cx="8" cy="8" r="6.2" /><path d="M1.8 8h12.4M8 1.8c1.8 1.9 2.6 4 2.6 6.2S9.8 12.3 8 14.2C6.2 12.3 5.4 10.2 5.4 8S6.2 3.7 8 1.8z" />
  </svg>
)
export const Shield = (p: P) => (
  <svg viewBox="0 0 16 16" {...base} strokeWidth={1.5} {...p}><path d="M8 1.8l5 2v4c0 3-2.1 5.4-5 6.4-2.9-1-5-3.4-5-6.4v-4l5-2z" /><path d="M5.8 8l1.6 1.6 3-3.2" /></svg>
)
export const Clock = (p: P) => (
  <svg viewBox="0 0 16 16" {...base} strokeWidth={1.5} {...p}><circle cx="8" cy="8" r="6" /><path d="M8 4.8V8l2.2 1.4" /></svg>
)
export const Play = (p: P) => (
  <svg viewBox="0 0 16 16" fill="currentColor" {...p}><path d="M5 3.5v9l7.5-4.5z" /></svg>
)
export const Pause = (p: P) => (
  <svg viewBox="0 0 16 16" fill="currentColor" {...p}><rect x="4" y="3.5" width="2.8" height="9" rx=".8" /><rect x="9.2" y="3.5" width="2.8" height="9" rx=".8" /></svg>
)
export const Plug = (p: P) => (
  <svg viewBox="0 0 16 16" {...base} strokeWidth={1.5} {...p}><path d="M6 2v3M10 2v3M4.5 5h7v2.5a3.5 3.5 0 01-7 0V5zM8 11v3" /></svg>
)
export const Bot = (p: P) => (
  <svg viewBox="0 0 16 16" {...base} strokeWidth={1.5} {...p}><rect x="3" y="5" width="10" height="8" rx="2.5" /><path d="M8 2.5V5M6 9h.01M10 9h.01" /></svg>
)
