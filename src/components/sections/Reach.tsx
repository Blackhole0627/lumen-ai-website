import { REACH } from '../../content/site'
import { Container } from '../ui/Container'
import { Flag } from '../ui/Flag'
import { SectionHeading } from '../ui/SectionHeading'

export function Reach() {
  return (
    <section id="reach" className="border-t border-line bg-paper text-graphite">
      <Container className="grid gap-8 py-16 sm:gap-16 sm:py-28 lg:grid-cols-2 lg:gap-24">
        <div>
          <SectionHeading lead={REACH.heading.lead} rest={REACH.heading.rest} />
          <p className="text-body-l mt-6 max-w-[460px] text-quiet sm:mt-8">{REACH.sub}</p>
        </div>
        <div className="space-y-8 sm:space-y-10">
          {REACH.regions.map((region) => (
            <div key={region.name}>
              <p className="text-body-s text-quiet">{region.name}</p>
              <ul className="mt-4 grid grid-cols-2 gap-2 sm:flex sm:flex-wrap">
                {region.markets.map(([name, code]) => (
                  <li key={code} className="flex items-center gap-3 rounded-xl bg-bone p-2.5 pe-3.5">
                    <Flag code={code} className="size-8 shrink-0 sm:size-11" />
                    <span className="text-body-m font-medium text-graphite sm:whitespace-nowrap">{name}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </Container>
    </section>
  )
}
