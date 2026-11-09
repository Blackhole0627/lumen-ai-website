import { Closing, Footer } from './components/sections/Closing'
import { Faq } from './components/sections/Faq'
import { Features } from './components/sections/Features'
import { Guarantees } from './components/sections/Guarantees'
import { Header } from './components/sections/Header'
import { Hero } from './components/sections/Hero'
import { Industries } from './components/sections/Industries'
import { LogoStrip } from './components/sections/LogoStrip'
import { Quote } from './components/sections/Quote'
import { Reach } from './components/sections/Reach'
import { Results } from './components/sections/Results'
import { Security } from './components/sections/Security'
import { Team } from './components/sections/Team'
import { VoiceStage } from './components/sections/VoiceStage'

export default function App() {
  return (
    <>
      <Header />
      <main>
        <Hero />
        <VoiceStage />
        <LogoStrip />
        <Guarantees />
        <Results />
        <Quote />
        <Features />
        <Industries />
        <Reach />
        <Security />
        <Team />
        <Faq />
        <Closing />
      </main>
      <Footer />
    </>
  )
}
