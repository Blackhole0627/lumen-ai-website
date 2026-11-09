import { TEAM } from '../../content/site'
import { Container } from '../ui/Container'
import { SectionHeading } from '../ui/SectionHeading'

/** Portrait placeholder. Replace with real team photography (3:4). */
function Portrait({ hue }: { hue: number }) {
  return (
    <div
      className="relative aspect-[3/4] w-full overflow-hidden rounded-card"
      style={{ background: `linear-gradient(170deg, hsl(${hue} 18% 86%), hsl(${hue} 14% 70%))` }}
    >
      <svg viewBox="0 0 120 160" className="absolute inset-x-0 bottom-0 w-full text-paper/70" aria-hidden>
        <circle cx="60" cy="62" r="24" fill="currentColor" />
        <path d="M14 160c0-30 20-50 46-50s46 20 46 50z" fill="currentColor" />
      </svg>
    </div>
  )
}

export function Team() {
  return (
    <section id="founders" className="border-t border-line bg-paper text-graphite">
      <Container className="grid gap-10 py-16 sm:gap-16 sm:py-36 lg:grid-cols-2 lg:gap-24">
        <div>
          <SectionHeading lead={TEAM.heading.lead} rest={TEAM.heading.rest} />
          {TEAM.body.map((p, i) => (
            <p key={i} className={`text-body-l max-w-[460px] text-quiet ${i === 0 ? 'mt-8' : 'mt-5'}`}>
              {p}
            </p>
          ))}
        </div>
        <ul className="grid grid-cols-2 gap-x-4 gap-y-8 sm:grid-cols-3 sm:gap-x-5">
          {TEAM.people.map((p, i) => (
            <li key={i}>
              <Portrait hue={p.hue} />
              <p className="text-body-m mt-4 font-semibold text-coal">{p.name}</p>
              <p className="text-body-s text-quiet">{p.role}</p>
            </li>
          ))}
        </ul>
      </Container>
    </section>
  )
}
