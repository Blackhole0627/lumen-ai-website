import { Fragment } from 'react'
import { QUOTE } from '../../content/site'
import { useScrollProgress } from '../../hooks/useScrollProgress'
import { Container } from '../ui/Container'

/** Pull quote whose characters fill from light to dark as the reader scrolls. */
export function Quote() {
  const { ref, progress } = useScrollProgress<HTMLQuoteElement>()
  const chars = Array.from(QUOTE.text)
  const filled = Math.round(progress * chars.length)
  const words = QUOTE.text.split(' ')

  let cursor = 0
  return (
    <section className="bg-paper text-graphite">
      <Container className="py-16 sm:py-36">
        <figure className="mx-auto max-w-3xl text-center">
          <blockquote ref={ref} className="text-quote text-balance" aria-label={QUOTE.text}>
            <span aria-hidden>
              {words.map((word, wi) => {
                const start = cursor
                cursor += word.length + 1
                return (
                  <Fragment key={wi}>
                    <span className="whitespace-nowrap">
                      {Array.from(word).map((ch, ci) => (
                        <span key={ci} className={`transition-colors duration-300 ${start + ci < filled ? 'text-coal' : 'text-line'}`}>
                          {ch}
                        </span>
                      ))}
                    </span>
                    {wi < words.length - 1 ? ' ' : ''}
                  </Fragment>
                )
              })}
            </span>
          </blockquote>
          <figcaption className="mt-10">
            <span className="mx-auto grid h-12 w-12 place-items-center rounded-full bg-forest-wash text-body-s font-semibold text-forest">HC</span>
            <p className="text-body-s mt-4 font-semibold text-graphite">{QUOTE.name}</p>
            <p className="text-body-s text-quiet">{QUOTE.role}</p>
          </figcaption>
        </figure>
      </Container>
    </section>
  )
}
