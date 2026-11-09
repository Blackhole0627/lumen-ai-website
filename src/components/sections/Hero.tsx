import { useEffect, useState } from 'react'
import { BRAND } from '../../config/brand'
import { HERO } from '../../content/site'
import { Button } from '../ui/Button'
import { Container } from '../ui/Container'

const BARS = [0.45, 0.7, 1, 0.6, 0.85, 0.4, 0.95, 0.55, 0.75, 0.5, 0.9, 0.35, 0.8, 0.6, 1, 0.45, 0.7]

/** Animated voice waveform that sits above the headline. */
function WaveMark() {
  return (
    <div className="mb-6 flex justify-center sm:mb-8" aria-hidden>
      <span className="inline-flex h-9 items-center gap-[3px] text-moss">
        {BARS.map((h, i) => (
          <span
            key={i}
            className="waveform-bar block w-[3px] rounded-full bg-current"
            style={{ height: `${h * 100}%`, animationDelay: `${(i * 0.09) % 1.2}s` }}
          />
        ))}
      </span>
    </div>
  )
}

export function Hero() {
  const [i, setI] = useState(0)

  useEffect(() => {
    const t = setInterval(() => setI((v) => (v + 1) % HERO.claims.length), 2600)
    return () => clearInterval(t)
  }, [])

  return (
    <section id="top" className="text-graphite">
      <Container className="pb-6 pt-10 text-center sm:pb-14 sm:pt-16">
        <WaveMark />
        <h1 className="text-h1 reveal-rise mx-auto text-balance text-coal">
          <span>{HERO.lead} </span>
          <span className="text-slate">{HERO.joiner} </span>
          <br className="hidden sm:block" />
          {/* All claims share one grid cell so the line width never jumps; only the active one is shown. */}
          <span className="inline-grid text-forest" aria-live="polite">
            {HERO.claims.map((claim, idx) => (
              <span
                key={claim}
                aria-hidden={idx !== i}
                className={`claim-word col-start-1 row-start-1 ${idx === i ? 'is-active' : ''}`}
              >
                {claim}
              </span>
            ))}
          </span>
        </h1>
        <p className="text-body-l reveal-rise reveal-delay-1 mx-auto mt-5 max-w-[720px] text-balance text-quiet">{HERO.sub}</p>
        <div className="reveal-rise reveal-delay-2 mt-7 flex justify-center gap-2 sm:mt-9">
          <Button href={BRAND.getStartedUrl}>{HERO.cta}</Button>
          <Button href="#features" variant="outline">
            See how it works
          </Button>
        </div>
      </Container>
    </section>
  )
}
