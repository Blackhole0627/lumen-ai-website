import { useEffect, useMemo, useRef, useState } from 'react'
import { VOICES, type Voice } from '../../content/site'
import { useInView } from '../../hooks/useInView'
import { Container } from '../ui/Container'
import { Flag } from '../ui/Flag'
import { ArrowLeft, ArrowRight, Pause, Play } from '../ui/Icons'

const LINE_MS = 1700
const HOLD_MS = 2600

/** Placeholder orb used instead of a portrait photo. */
function Orb({ voice, size, active }: { voice: Voice; size: number; active: boolean }) {
  return (
    <span
      className="relative grid place-items-center rounded-full font-semibold text-paper transition-[box-shadow] duration-500"
      style={{
        width: size,
        height: size,
        fontSize: size * 0.26,
        background: `radial-gradient(circle at 30% 25%, hsl(${voice.hue} 55% 62%), hsl(${voice.hue} 45% 32%) 70%)`,
        boxShadow: active ? '0 0 0 3px var(--color-mint), 0 10px 40px -8px rgba(44,236,154,.55)' : '0 0 0 1px rgba(255,255,255,.12)',
      }}
    >
      {voice.initials}
      <Flag code={voice.flag} className="absolute -bottom-0.5 -end-0.5 ring-2 ring-night" style={{ width: size * 0.32, height: size * 0.32 }} />
    </span>
  )
}

function Transcript({ voice, shown }: { voice: Voice; shown: number }) {
  const listRef = useRef<HTMLUListElement>(null)

  useEffect(() => {
    listRef.current?.scrollTo({ top: listRef.current.scrollHeight, behavior: 'smooth' })
  }, [shown])

  return (
    <figure className="w-full">
      <header className="text-body-m flex items-center justify-center gap-2.5 font-medium text-paper">
        <Flag code={voice.flag} className="h-5 w-5" />
        {voice.market} ({voice.language})
      </header>
      <ul
        ref={listRef}
        className="no-scrollbar mt-4 flex h-[340px] flex-col gap-2 overflow-y-auto pb-2 [mask-image:linear-gradient(to_top,#000_65%,transparent_100%)]"
      >
        <li className="mt-auto" aria-hidden />
        {voice.lines.map((line, idx) => {
          const visible = idx < shown
          const agent = line.who === 'agent'
          return (
            <li
              key={idx}
              className={`grid transition-all duration-500 ease-out ${visible ? 'grid-rows-[1fr] opacity-100' : 'grid-rows-[0fr] opacity-0'} ${agent ? 'justify-items-end' : 'justify-items-start'}`}
            >
              <div className="overflow-hidden">
                <span
                  className={`text-body-s relative inline-block max-w-[86%] px-3 py-2 pe-12 text-start font-medium ${
                    agent ? 'rounded-2xl rounded-ee-md bg-moss text-paper' : 'rounded-2xl rounded-es-md bg-paper text-graphite'
                  }`}
                >
                  <span className="sr-only">{agent ? 'Agent: ' : 'Customer: '}</span>
                  {line.text}
                  <span className={`text-caption absolute bottom-2 end-3 tabular-nums ${agent ? 'text-paper/60' : 'text-slate'}`}>{line.t}</span>
                </span>
              </div>
            </li>
          )
        })}
      </ul>
    </figure>
  )
}

export function VoiceStage() {
  const [active, setActive] = useState(0)
  const [shown, setShown] = useState(0)
  const [playing, setPlaying] = useState(true)
  const { ref, inView } = useInView<HTMLDivElement>({ threshold: 0.3 })
  const voice = VOICES[active]

  const go = (next: number) => {
    setActive((next + VOICES.length) % VOICES.length)
    setShown(0)
  }

  // Reveal transcript lines one by one, then move to the next voice.
  useEffect(() => {
    if (!playing || !inView) return
    const done = shown >= voice.lines.length
    const t = setTimeout(() => (done ? go(active + 1) : setShown((s) => s + 1)), done ? HOLD_MS : shown === 0 ? 500 : LINE_MS)
    return () => clearTimeout(t)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [shown, active, playing, inView])

  // Position orbs on an arc above the transcript; the active one sits at the apex.
  const positions = useMemo(() => {
    const n = VOICES.length
    return VOICES.map((_, i) => {
      let offset = i - active
      if (offset > n / 2) offset -= n
      if (offset < -n / 2) offset += n
      const angle = offset * 10 // degrees between orbs
      const rad = (angle * Math.PI) / 180
      const radius = 760
      const dist = Math.abs(offset)
      return {
        offset,
        x: Math.sin(rad) * radius,
        y: (1 - Math.cos(rad)) * radius,
        scale: offset === 0 ? 1 : Math.max(0.5, 0.74 - dist * 0.06),
        opacity: dist > 3 ? 0 : 1 - dist * 0.2,
      }
    })
  }, [active])

  return (
    <section className="text-graphite">
      <Container className="pb-12 sm:pb-20">
        <div ref={ref} className="relative overflow-hidden rounded-panel bg-night">
          {/* glow */}
          <span
            className="pointer-events-none absolute left-1/2 top-0 h-[420px] w-[820px] -translate-x-1/2 -translate-y-1/3 rounded-full opacity-50 blur-3xl"
            style={{ background: `radial-gradient(closest-side, hsl(${voice.hue} 70% 45% / .55), transparent)` }}
          />

          {/* Orbit */}
          <div className="relative h-[200px] sm:h-[220px]">
            {VOICES.map((v, i) => {
              const p = positions[i]
              return (
                <button
                  key={v.id}
                  type="button"
                  onClick={() => go(i)}
                  aria-label={`Play ${v.language} example`}
                  aria-pressed={i === active}
                  className="absolute left-1/2 top-12 -translate-x-1/2 transition-all duration-700 ease-[var(--ease-reveal)]"
                  style={{
                    transform: `translate(calc(-50% + ${p.x}px), ${p.y}px) scale(${p.scale})`,
                    opacity: p.opacity,
                    pointerEvents: p.opacity === 0 ? 'none' : 'auto',
                    zIndex: 10 - Math.abs(p.offset),
                  }}
                >
                  <Orb voice={v} size={88} active={i === active} />
                </button>
              )
            })}
          </div>

          {/* Caption */}
          <div className="relative z-10 px-6 text-center">
            <span className="text-body-l block font-medium text-paper">{voice.language}</span>
            <span className="text-body-s mx-auto mt-1.5 block min-h-[44px] max-w-[42ch] text-balance text-paper/60">{voice.summary}</span>
          </div>

          {/* Controls */}
          <div className="absolute end-3 top-3 z-20 flex gap-1.5 sm:end-5 sm:top-5">
            <button type="button" onClick={() => go(active - 1)} aria-label="Previous" className="grid h-9 w-9 place-items-center rounded-button bg-paper/10 text-paper transition hover:bg-paper/20">
              <ArrowLeft className="h-4 w-4" />
            </button>
            <button type="button" onClick={() => setPlaying((p) => !p)} aria-label={playing ? 'Pause' : 'Play'} className="grid h-9 w-9 place-items-center rounded-button bg-paper/10 text-paper transition hover:bg-paper/20">
              {playing ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
            </button>
            <button type="button" onClick={() => go(active + 1)} aria-label="Next" className="grid h-9 w-9 place-items-center rounded-button bg-paper/10 text-paper transition hover:bg-paper/20">
              <ArrowRight className="h-4 w-4" />
            </button>
          </div>

          {/* Transcript */}
          <div className="relative mx-auto w-[calc(100%-1rem)] pb-4 pt-4 sm:w-[min(640px,100%-6rem)] sm:pb-8">
            <div className="rounded-card bg-night-lift/70 p-3 ring-1 ring-paper/10 backdrop-blur sm:p-4">
              <Transcript key={voice.id} voice={voice} shown={shown} />
            </div>
          </div>
        </div>
      </Container>
    </section>
  )
}
