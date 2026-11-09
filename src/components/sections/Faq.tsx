import { FAQ } from '../../content/site'
import { Container } from '../ui/Container'
import { SectionHeading } from '../ui/SectionHeading'

export function Faq() {
  return (
    <section id="faq" className="border-t border-line bg-paper text-graphite">
      <Container className="grid gap-10 py-16 sm:py-28 lg:grid-cols-[minmax(0,420px)_1fr] lg:gap-24">
        <div>
          <SectionHeading lead={FAQ.heading.lead} rest={FAQ.heading.rest} />
          <p className="text-body-m mt-5 max-w-[54ch] text-quiet">{FAQ.sub}</p>
        </div>
        <div className="border-t border-line">
          {FAQ.items.map((item) => (
            <details key={item.q} className="faq-row group border-b border-line">
              <summary className="text-body-m flex cursor-pointer list-none items-center justify-between gap-6 py-5 font-medium text-coal transition-colors hover:text-forest">
                <h3 className="text-body-m m-0 font-medium">{item.q}</h3>
                <span className="relative h-4 w-4 shrink-0 text-quiet" aria-hidden>
                  <span className="absolute start-0 top-1/2 h-px w-4 -translate-y-1/2 bg-current" />
                  <span className="absolute left-1/2 top-0 h-4 w-px -translate-x-1/2 bg-current transition-transform duration-200 group-open:scale-y-0" />
                </span>
              </summary>
              <div className="pb-6">
                <p className="text-body-s max-w-[68ch] text-quiet">{item.a}</p>
              </div>
            </details>
          ))}
        </div>
      </Container>
    </section>
  )
}
