import { BRAND } from '../../config/brand'
import { CLOSING, FOOTER } from '../../content/site'
import { Button } from '../ui/Button'
import { Container } from '../ui/Container'
import { Logo } from '../ui/Logo'
import { SectionHeading } from '../ui/SectionHeading'

export function Closing() {
  return (
    <section id="contact-cta" className="bg-forest text-paper">
      <Container className="py-16 text-center sm:py-40">
        <SectionHeading tone="light" lead={CLOSING.heading.lead} rest={CLOSING.heading.rest} className="mx-auto max-w-[820px]" />
        <p className="text-body-m sm:text-body-l mx-auto mt-4 max-w-lg text-paper/70">{CLOSING.sub}</p>
        <Button href="#" variant="light" className="mt-8">
          {CLOSING.cta}
        </Button>
      </Container>
    </section>
  )
}

export function Footer() {
  return (
    <footer className="bg-forest text-paper">
      <Container className="flex flex-col gap-4 border-t border-paper/15 py-6 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex flex-col gap-3">
          <Logo className="text-forest-deep [&>span]:text-paper" />
          <p className="text-body-s max-w-[46ch] text-paper/70">{FOOTER.blurb}</p>
        </div>
        <span className="flex gap-x-8">
          {FOOTER.links.map((l) => (
            <a key={l.label} href={l.href} className="text-body-s text-paper/70 transition-colors hover:text-paper">
              {l.label}
            </a>
          ))}
        </span>
      </Container>
      <Container className="flex flex-wrap items-center gap-x-8 gap-y-3 border-t border-paper/15 py-6">
        <p className="text-body-s text-paper/60">
          © {BRAND.year} {BRAND.name}. All rights reserved.
        </p>
        <div className="flex flex-wrap items-center gap-x-5 gap-y-1">
          {FOOTER.legal.map((l) => (
            <a key={l.label} href={l.href} className="text-body-s text-paper/60 transition-colors hover:text-paper">
              {l.label}
            </a>
          ))}
        </div>
      </Container>
    </footer>
  )
}
