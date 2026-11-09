import { INDUSTRIES } from '../../content/site'
import { Container } from '../ui/Container'
import { ArrowRight } from '../ui/Icons'
import { SectionHeading } from '../ui/SectionHeading'

export function Industries() {
  return (
    <section id="industries" className="relative overflow-hidden border-t border-line bg-forest text-paper">
      {/* subtle grid texture */}
      <span
        aria-hidden
        className="pointer-events-none absolute inset-0 opacity-[0.07]"
        style={{
          backgroundImage: 'linear-gradient(var(--color-paper) 1px, transparent 1px), linear-gradient(90deg, var(--color-paper) 1px, transparent 1px)',
          backgroundSize: '56px 56px',
          maskImage: 'radial-gradient(ellipse at 80% 0%, #000 0%, transparent 60%)',
        }}
      />
      <Container className="relative py-16 sm:py-28">
        <SectionHeading tone="light" lead={INDUSTRIES.heading.lead} rest={INDUSTRIES.heading.rest} />
        <p className="text-body-l mt-6 max-w-[58ch] text-paper/75">{INDUSTRIES.sub}</p>

        <ul className="mt-14 grid gap-x-8 sm:mt-20 sm:grid-cols-2">
          {INDUSTRIES.items.map((item, i) => (
            <li key={item.name} className={`border-paper/20 pb-9 ${i === 0 ? '' : i === 1 ? 'border-t pt-9 sm:border-t-0 sm:pt-0' : 'border-t pt-9'}`}>
              <h3 className="text-h2 text-paper">{item.name}</h3>
              <p className="text-body-m mt-4 max-w-[46ch] font-medium text-paper">{item.lead}</p>
              <p className="text-body-m mt-2 max-w-[46ch] text-paper/70">{item.body}</p>
              {'cta' in item && item.cta && (
                <a href="#contact-cta" className="text-body-m group mt-5 inline-flex items-center gap-2 font-medium text-paper underline-offset-4 hover:underline">
                  {item.cta}
                  <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
                </a>
              )}
            </li>
          ))}
        </ul>
      </Container>
    </section>
  )
}
