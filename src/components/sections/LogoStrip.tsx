import { CUSTOMER_LOGOS } from '../../content/site'
import { Container } from '../ui/Container'

/** Placeholder customer wordmarks. Replace with real (licensed) client logos as SVGs. */
export function LogoStrip() {
  return (
    <section aria-label="Customers" className="border-t border-line">
      <Container>
        <p className="text-body-s pt-10 text-center text-quiet">Trusted by lenders, servicers and agencies across 14 markets</p>
        <ul className="flex flex-wrap py-6 sm:py-8">
          {CUSTOMER_LOGOS.map((name, i) => (
            <li
              key={name}
              className="flex h-20 w-1/2 items-center justify-center px-3 text-slate transition-colors duration-300 hover:text-graphite sm:w-1/3 md:w-1/4"
            >
              <span
                className="text-[20px] tracking-[-0.03em] sm:text-[22px]"
                style={{ fontWeight: [700, 500, 600, 800][i % 4], fontStyle: i % 3 === 2 ? 'italic' : undefined }}
              >
                {name}
              </span>
            </li>
          ))}
        </ul>
      </Container>
    </section>
  )
}
