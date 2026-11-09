import { BRAND } from '../../config/brand'
import { RESULTS } from '../../content/site'
import { useInView } from '../../hooks/useInView'
import { Container } from '../ui/Container'
import { Logo } from '../ui/Logo'
import { SectionHeading } from '../ui/SectionHeading'

type Case = (typeof RESULTS.groups)[number]['cases'][number]

function Bar({ label, value, ours, animate }: { label: React.ReactNode; value: number; ours?: boolean; animate: boolean }) {
  return (
    <div>
      <div className="flex items-baseline justify-between gap-3">
        <span className="text-body-s flex items-center gap-2 text-graphite">{label}</span>
        <span className="text-body-l font-medium tabular-nums text-coal">{value}%</span>
      </div>
      <span className="mt-1.5 block h-2 overflow-hidden rounded-full bg-bone-2">
        <span
          className={`block h-full rounded-full transition-[width] duration-[1400ms] ease-[var(--ease-reveal)] ${ours ? 'bg-forest' : 'bg-slate'}`}
          style={{ width: animate ? `${value}%` : '0%' }}
        />
      </span>
    </div>
  )
}

function CaseCard({ c }: { c: Case }) {
  const { ref, inView } = useInView<HTMLDivElement>()
  return (
    <div ref={ref} className="rounded-card border border-line bg-paper p-5 sm:p-6">
      <p className="text-caption uppercase tracking-[0.08em] text-forest">{c.client}</p>
      <p className="text-body-s mt-1 text-quiet">{c.segment}</p>
      <p className="text-caption mt-4 text-quiet">Share of balance collected</p>
      <div className="mt-2.5 space-y-4">
        <Bar label={c.baseline.label} value={c.baseline.value} animate={inView} />
        <Bar label={<Logo className="scale-[0.8] origin-left text-forest" />} value={c.ours} ours animate={inView} />
      </div>
    </div>
  )
}

export function Results() {
  return (
    <section id="results" className="text-graphite">
      <Container className="py-8 sm:py-16">
        <div className="rounded-card bg-bone px-5 py-8 sm:px-10 sm:py-10">
          <SectionHeading lead={RESULTS.heading.lead} rest={RESULTS.heading.rest} />
          <p className="text-body-l mt-4 max-w-[58ch] text-balance text-quiet sm:mt-5">{RESULTS.sub}</p>

          <ul className="mt-8 grid grid-cols-2 gap-x-5 gap-y-8 sm:mt-10 sm:gap-x-6 lg:grid-cols-4">
            {RESULTS.stats.map((s) => (
              <li key={s.label}>
                <p className={`text-display-ml tabular-nums ${s.accent ? 'text-forest' : 'text-coal'}`}>{s.value}</p>
                <p className="text-body-s mt-2.5 text-balance text-quiet sm:max-w-[30ch]">{s.label}</p>
              </li>
            ))}
          </ul>

          <hr className="mt-12 border-0 border-t border-line sm:mt-14" />

          <div className="mt-10 sm:mt-12">
            <p className="text-body-m max-w-[70ch] text-quiet">{RESULTS.intro}</p>
            <div className="mt-10 space-y-10 sm:mt-12 sm:space-y-12">
              {RESULTS.groups.map((g) => (
                <div key={g.title}>
                  <h3 className="text-h3 text-coal">{g.title}</h3>
                  <p className="text-body-s mt-2 max-w-[64ch] text-quiet">{g.note}</p>
                  <div className="mt-5 grid gap-4 sm:grid-cols-2">
                    {g.cases.map((c) => (
                      <CaseCard key={c.client} c={c} />
                    ))}
                  </div>
                </div>
              ))}
            </div>
            <p className="text-caption mt-8 text-quiet">Figures are illustrative placeholders for {BRAND.name}. Replace with verified client data before launch.</p>
          </div>
        </div>
      </Container>
    </section>
  )
}
