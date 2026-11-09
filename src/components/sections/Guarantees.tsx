import { useEffect, useRef, useState } from 'react'
import { BRAND } from '../../config/brand'
import { GUARANTEES } from '../../content/site'
import { GuaranteeArt } from '../art/GuaranteeArt'
import { ArtBackdrop } from '../art/Primitives'
import { Container } from '../ui/Container'
import { ArrowLeft, ArrowRight } from '../ui/Icons'
import { SectionHeading } from '../ui/SectionHeading'

export function Guarantees() {
  const trackRef = useRef<HTMLUListElement>(null)
  const [index, setIndex] = useState(0)

  // Track which card is snapped to the start.
  useEffect(() => {
    const el = trackRef.current
    if (!el) return
    const onScroll = () => {
      const card = el.children[0] as HTMLElement | undefined
      if (!card) return
      const step = card.offsetWidth + 16
      setIndex(Math.round(el.scrollLeft / step))
    }
    el.addEventListener('scroll', onScroll, { passive: true })
    return () => el.removeEventListener('scroll', onScroll)
  }, [])

  const scrollTo = (i: number) => {
    const el = trackRef.current
    const card = el?.children[i] as HTMLElement | undefined
    if (el && card) el.scrollTo({ left: card.offsetLeft - el.offsetLeft - 16, behavior: 'smooth' })
  }

  const last = GUARANTEES.length - 1

  return (
    <section id="what" className="border-t border-line bg-bone text-graphite">
      <Container className="py-16 sm:py-28">
        <div className="flex items-end justify-between gap-8">
          <SectionHeading lead={`${GUARANTEES.length} commitments,`} rest={`and how ${BRAND.name} keeps them`} />
          <div className="hidden shrink-0 gap-2 md:flex">
            <button
              type="button"
              aria-label="Previous"
              disabled={index === 0}
              onClick={() => scrollTo(Math.max(0, index - 1))}
              className="grid h-10 w-10 place-items-center rounded-button bg-paper text-graphite transition hover:bg-bone-2 disabled:opacity-30"
            >
              <ArrowLeft className="h-4 w-4" />
            </button>
            <button
              type="button"
              aria-label="Next"
              disabled={index >= last}
              onClick={() => scrollTo(Math.min(last, index + 1))}
              className="grid h-10 w-10 place-items-center rounded-button bg-paper text-graphite transition hover:bg-bone-2 disabled:opacity-30"
            >
              <ArrowRight className="h-4 w-4" />
            </button>
          </div>
        </div>

        <div className="relative -mx-4">
          <span className="pointer-events-none absolute inset-y-0 end-0 z-10 w-16 bg-[linear-gradient(to_left,var(--color-bone),transparent)]" />
          <ul ref={trackRef} className="no-scrollbar mt-8 flex snap-x snap-mandatory gap-4 overflow-x-auto overscroll-x-contain scroll-ps-4 px-4">
            {GUARANTEES.map((g, i) => (
              <li
                key={g.title}
                className={`flex w-[calc(100vw-2.5rem)] shrink-0 snap-start flex-col transition-opacity duration-300 sm:w-[400px] ${i === index ? 'opacity-100' : 'opacity-70'}`}
              >
                <p className="text-body-m font-semibold text-coal">{g.title}</p>
                <p className="text-body-m mb-4 mt-1.5 text-quiet">{g.body}</p>
                <div className="mt-auto">
                  <ArtBackdrop seed={i + 1} className="aspect-[5/6]">
                    <GuaranteeArt kind={g.art} />
                  </ArtBackdrop>
                </div>
              </li>
            ))}
          </ul>
        </div>

        <div className="mt-5 flex justify-center gap-2">
          {GUARANTEES.map((g, i) => (
            <button
              key={g.title}
              type="button"
              aria-label={`Go to ${g.title}`}
              onClick={() => scrollTo(i)}
              className={`h-1.5 rounded-full transition-[width,background-color] duration-300 ${i === index ? 'w-5 bg-coal' : 'w-1.5 bg-line hover:bg-graphite'}`}
            />
          ))}
        </div>
      </Container>
    </section>
  )
}
