import { BRAND } from '../../config/brand'
import { CERTS, TRUST_NOTE } from '../../content/site'
import { Container } from '../ui/Container'
import { ArrowRight, Shield } from '../ui/Icons'

/** Generic certification badge. Replace with official badge artwork once certificates are held. */
function Badge({ label }: { label: string }) {
  return (
    <span className="grid h-12 w-12 shrink-0 place-items-center rounded-full border border-line bg-bone text-forest">
      <span className="text-[9px] font-bold uppercase leading-tight tracking-wide">{label.split(' ')[0]}</span>
    </span>
  )
}

export function Security() {
  return (
    <section id="security" className="border-t border-line">
      <Container>
        <ul className="grid grid-cols-1 divide-y divide-line sm:grid-cols-2 sm:divide-y-0 lg:grid-cols-4">
          {CERTS.map((c, i) => (
            <li
              key={c}
              className={`flex items-center gap-3 py-3 text-graphite sm:gap-4 sm:px-5 sm:py-10 ${i % 2 === 0 ? 'sm:ps-0 lg:ps-5' : ''} ${i === 0 ? 'lg:ps-0' : ''} ${
                i < CERTS.length - 1 ? 'sm:border-e sm:border-line' : ''
              } ${i >= 2 ? 'sm:border-t lg:border-t-0' : ''}`}
            >
              <Badge label={c} />
              <span className="text-body-m">{c}</span>
            </li>
          ))}
        </ul>
      </Container>
      <div className="border-t border-line">
        <Container className="py-6 sm:py-7">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between sm:gap-8">
            <span className="text-body-s max-w-[60ch] text-quiet">{TRUST_NOTE}</span>
            <a
              href={BRAND.trustCenterUrl}
              className="group text-body-m flex w-full shrink-0 items-center justify-center gap-2 rounded-button bg-forest px-5 py-3.5 font-semibold text-paper transition hover:bg-forest-deep sm:w-auto"
            >
              <Shield className="h-4 w-4" />
              Trust Center
              <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
            </a>
          </div>
        </Container>
      </div>
    </section>
  )
}
