import { useMemo } from 'react'
import { FEATURES } from '../../content/site'
import { useScrollSpy } from '../../hooks/useScrollSpy'
import { FeatureArt } from '../art/FeatureArt'
import { ArtBackdrop } from '../art/Primitives'
import { Container } from '../ui/Container'
import { SectionHeading } from '../ui/SectionHeading'

export function Features() {
  const ids = useMemo(() => FEATURES.map((f) => f.id), [])
  const active = useScrollSpy(ids, 220)

  return (
    <section id="features" className="border-t border-line bg-paper text-graphite">
      <Container className="py-16 sm:py-28">
        <SectionHeading lead="From first contact" rest="to final payment" />

        <div className="mt-6 grid gap-5 sm:mt-10 lg:grid-cols-[minmax(0,300px)_1fr] lg:gap-24">
          <nav className="sticky top-[60px] z-10 -mx-5 min-w-0 bg-paper/95 px-5 py-2 backdrop-blur sm:top-[68px] lg:top-28 lg:mx-0 lg:self-start lg:bg-transparent lg:px-0 lg:py-0" aria-label="Product stages">
            <ul className="no-scrollbar flex gap-x-5 gap-y-1 overflow-x-auto lg:flex-col">
              {FEATURES.map((f, i) => (
                <li key={f.id} className="shrink-0">
                  <a
                    href={`#${f.id}`}
                    className={`text-body-m lg:text-body-l flex items-center gap-3 whitespace-nowrap py-1 font-medium transition-colors duration-300 ${
                      active === f.id ? 'text-coal' : 'text-slate hover:text-quiet'
                    }`}
                  >
                    <span className="text-caption hidden w-5 tabular-nums lg:inline">{String(i + 1).padStart(2, '0')}</span>
                    {f.nav}
                  </a>
                </li>
              ))}
            </ul>
          </nav>

          <ul className="grid gap-14 sm:gap-20">
            {FEATURES.map((f, i) => (
              <li key={f.id} id={f.id} className="scroll-mt-32">
                <ArtBackdrop seed={i + 7} className="px-4 py-10 sm:p-10">
                  <div className="flex min-h-[300px] items-center justify-center sm:min-h-[360px]">
                    <div className="w-full">
                      <FeatureArt kind={f.art} />
                    </div>
                  </div>
                </ArtBackdrop>
                <div className="mt-4 grid gap-3.5 sm:mt-6 sm:gap-4 xl:grid-cols-[minmax(0,300px)_1fr] xl:gap-10">
                  <h3 className="text-h2-s text-pretty text-coal">{f.title}</h3>
                  <p className="text-body-m max-w-[62ch] text-quiet">{f.body}</p>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </Container>
    </section>
  )
}
