/**
 * All page copy lives here so the client can rewrite it without touching components.
 * Every string below is placeholder copy written for this rebuild.
 */
import { BRAND } from '../config/brand'

const B = BRAND.name

export const NAV = [
  { label: 'Results', href: '#results' },
  { label: 'Product', href: '#features' },
  { label: 'Industries', href: '#industries' },
  { label: 'Security', href: '#security' },
  { label: 'Blog', href: '#' },
  { label: 'FAQ', href: '#faq' },
  { label: 'Careers', href: '#' },
]

export const LANGUAGES = ['EN', 'ES', 'DE', 'FR', 'IT', 'PT', 'NL', 'PL', 'TR', 'AR']

export const HERO = {
  lead: 'AI agents',
  joiner: 'for',
  claims: ['credit servicing', 'collections', 'onboarding', 'payments'],
  sub: 'Voice and messaging agents that handle applications, onboarding, payments and arrears inside the rules you set.',
  cta: 'Get Started',
}

/* ---------- Hero stage: orbit of voices + live transcript ---------- */

export type Line = { who: 'agent' | 'customer'; text: string; t: string }
export type Voice = {
  id: string
  language: string
  market: string
  flag: string // ISO code for flag-icons
  summary: string
  hue: number // used to tint the placeholder orb
  initials: string
  lines: Line[]
}

export const VOICES: Voice[] = [
  {
    id: 'en-gb',
    language: 'English',
    market: 'United Kingdom',
    flag: 'gb',
    hue: 152,
    initials: 'EN',
    summary: 'A missed card payment after a house move. The agent re-schedules without pressure.',
    lines: [
      { who: 'agent', text: 'Hi, this is an automated assistant calling for Northbank. Am I speaking with Daniel Hughes?', t: '0:01' },
      { who: 'customer', text: 'Yes, speaking.', t: '0:05' },
      { who: 'agent', text: 'Thanks, Daniel. For security, could you tell me the first line of your postcode?', t: '0:08' },
      { who: 'customer', text: 'It’s LS6. I only moved last month, actually.', t: '0:13' },
      { who: 'agent', text: 'Thanks, that matches. I’m calling about a card payment of £84 that was due on the 3rd.', t: '0:18' },
      { who: 'customer', text: 'Ah, the direct debit was still on my old account. Sorry about that.', t: '0:25' },
      { who: 'agent', text: 'No problem at all. Would you like to pay it now, or pick a date that suits you?', t: '0:31' },
      { who: 'customer', text: 'Friday would be easier, after payday.', t: '0:36' },
      { who: 'agent', text: 'Done. £84 on Friday the 14th. I’ll text you a link to update your bank details too.', t: '0:40' },
      { who: 'customer', text: 'Perfect, thank you.', t: '0:47' },
    ],
  },
  {
    id: 'es-es',
    language: 'Español',
    market: 'España',
    flag: 'es',
    hue: 18,
    initials: 'ES',
    summary: 'Un cliente pregunta por un recibo duplicado. El agente lo revisa y lo corrige en la llamada.',
    lines: [
      { who: 'agent', text: 'Buenos días, le llama un asistente automático de Banca Sol. ¿Hablo con Lucía Romero?', t: '0:01' },
      { who: 'customer', text: 'Sí, soy yo.', t: '0:04' },
      { who: 'agent', text: 'Gracias. Para verificar, ¿me confirma su fecha de nacimiento?', t: '0:07' },
      { who: 'customer', text: 'El 2 de marzo de 1988. Pero me han cobrado dos veces este mes.', t: '0:12' },
      { who: 'agent', text: 'Lo veo: hay un cargo duplicado de 46 €. Ya he pedido la devolución.', t: '0:19' },
      { who: 'customer', text: 'Vale, ¿y la cuota pendiente?', t: '0:25' },
      { who: 'agent', text: 'Con la devolución queda cubierta. No tiene nada pendiente.', t: '0:29' },
      { who: 'customer', text: 'Genial, muchas gracias.', t: '0:34' },
    ],
  },
  {
    id: 'de-de',
    language: 'Deutsch',
    market: 'Deutschland',
    flag: 'de',
    hue: 210,
    initials: 'DE',
    summary: 'Kurzarbeit, weniger Einkommen. Der Agent bietet eine Ratenpause im Rahmen der Regeln an.',
    lines: [
      { who: 'agent', text: 'Guten Tag, hier spricht ein digitaler Assistent der Rheinkredit. Spreche ich mit Jonas Weber?', t: '0:01' },
      { who: 'customer', text: 'Ja, das bin ich.', t: '0:05' },
      { who: 'agent', text: 'Danke. Zur Sicherheit: Wie lauten die letzten vier Ziffern Ihrer Kundennummer?', t: '0:08' },
      { who: 'customer', text: '4471. Ich bin gerade in Kurzarbeit, die Rate ist schwierig.', t: '0:14' },
      { who: 'agent', text: 'Verstanden. Ich kann die Rate für zwei Monate halbieren. Passt das?', t: '0:21' },
      { who: 'customer', text: 'Ja, das würde sehr helfen.', t: '0:27' },
      { who: 'agent', text: 'Ist eingetragen. Die Bestätigung kommt gleich per E-Mail.', t: '0:30' },
    ],
  },
  {
    id: 'fr-fr',
    language: 'Français',
    market: 'France',
    flag: 'fr',
    hue: 265,
    initials: 'FR',
    summary: 'Un premier retard de paiement. L’agent propose un échéancier en trois fois.',
    lines: [
      { who: 'agent', text: 'Bonjour, ici l’assistant automatique de Crédit Azur. Suis-je bien avec Camille Martin ?', t: '0:01' },
      { who: 'customer', text: 'Oui, c’est moi.', t: '0:04' },
      { who: 'agent', text: 'Merci. Pouvez-vous me confirmer votre code postal ?', t: '0:07' },
      { who: 'customer', text: '69003. Je sais, j’ai un retard sur ma mensualité.', t: '0:11' },
      { who: 'agent', text: 'Il reste 210 €. Je peux vous proposer trois versements de 70 €.', t: '0:17' },
      { who: 'customer', text: 'D’accord, ça me va.', t: '0:23' },
      { who: 'agent', text: 'C’est noté. Vous recevrez le récapitulatif par SMS.', t: '0:26' },
    ],
  },
  {
    id: 'it-it',
    language: 'Italiano',
    market: 'Italia',
    flag: 'it',
    hue: 95,
    initials: 'IT',
    summary: 'Il cliente è in viaggio. L’agente fissa un nuovo contatto senza insistere.',
    lines: [
      { who: 'agent', text: 'Buongiorno, sono l’assistente digitale di Banca Riva. Parlo con Marco Bianchi?', t: '0:01' },
      { who: 'customer', text: 'Sì, ma sono all’estero, non è un buon momento.', t: '0:05' },
      { who: 'agent', text: 'Capisco. Preferisce essere richiamato o ricevere un messaggio su WhatsApp?', t: '0:10' },
      { who: 'customer', text: 'WhatsApp, grazie.', t: '0:15' },
      { who: 'agent', text: 'Perfetto, le scrivo lì oggi pomeriggio. Buon viaggio!', t: '0:18' },
    ],
  },
  {
    id: 'pt-br',
    language: 'Português',
    market: 'Brasil',
    flag: 'br',
    hue: 48,
    initials: 'PT',
    summary: 'Pagamento via Pix durante a ligação, com comprovante enviado na hora.',
    lines: [
      { who: 'agent', text: 'Olá, aqui é a assistente virtual da Financeira Horizonte. Falo com Ana Souza?', t: '0:01' },
      { who: 'customer', text: 'Sim, sou eu.', t: '0:04' },
      { who: 'agent', text: 'Obrigada. Pode confirmar os três primeiros dígitos do seu CPF?', t: '0:07' },
      { who: 'customer', text: '512. É sobre a parcela atrasada?', t: '0:12' },
      { who: 'agent', text: 'Isso. São R$ 180. Posso enviar um Pix agora mesmo, se preferir.', t: '0:16' },
      { who: 'customer', text: 'Pode mandar.', t: '0:21' },
      { who: 'agent', text: 'Enviado. Assim que cair, mando o comprovante por WhatsApp.', t: '0:24' },
    ],
  },
  {
    id: 'nl-nl',
    language: 'Nederlands',
    market: 'Nederland',
    flag: 'nl',
    hue: 30,
    initials: 'NL',
    summary: 'Iemand anders neemt op. De agent deelt niets en vraagt alleen naar een beter moment.',
    lines: [
      { who: 'agent', text: 'Goedemiddag, u spreekt met de digitale assistent van Polder Finance. Spreek ik met Sanne de Vries?', t: '0:01' },
      { who: 'customer', text: 'Nee, dit is haar partner.', t: '0:06' },
      { who: 'agent', text: 'Dank u. Wanneer kan ik Sanne het beste bereiken?', t: '0:09' },
      { who: 'customer', text: 'Na zes uur is ze thuis.', t: '0:13' },
      { who: 'agent', text: 'Prima, dan bel ik later terug. Fijne dag nog.', t: '0:16' },
    ],
  },
  {
    id: 'ar-ae',
    language: 'العربية',
    market: 'UAE',
    flag: 'ae',
    hue: 175,
    initials: 'AR',
    summary: 'A customer asks for the balance in writing. The agent sends a secure statement link.',
    lines: [
      { who: 'agent', text: 'Good afternoon, this is the virtual assistant for Gulf Credit. Am I speaking with Omar Haddad?', t: '0:01' },
      { who: 'customer', text: 'Yes. Can you send me the balance in writing first?', t: '0:06' },
      { who: 'agent', text: 'Of course. I’ve sent a secure statement link to the mobile number on file.', t: '0:11' },
      { who: 'customer', text: 'Got it. I’ll pay through the app tonight.', t: '0:18' },
      { who: 'agent', text: 'Thank you. I’ll note that and check in tomorrow only if it hasn’t arrived.', t: '0:22' },
    ],
  },
]

/* ---------- Logo strip ---------- */
export const CUSTOMER_LOGOS = ['Northbank', 'Rheinkredit', 'Banca Sol', 'Polder Finance', 'Crédit Azur', 'Horizonte', 'Gulf Credit', 'Riva Group']

/* ---------- Guarantees carousel ---------- */
export type GuaranteeArt = 'rules' | 'log' | 'trace' | 'voice' | 'deploy' | 'payment'
export const GUARANTEES: { title: string; body: string; art: GuaranteeArt }[] = [
  { title: 'Stays inside your policy.', body: `${B} only offers what your rulebook allows. Every rule change is versioned, reviewed and signed off.`, art: 'rules' },
  { title: 'Every conversation on record.', body: 'Outcomes, promises and notes are written to your CRM the moment the call ends, with nothing typed by hand.', art: 'log' },
  { title: 'The right person, first.', body: 'Numbers are checked across approved data sources so the agent reaches the account holder, not a stranger.', art: 'trace' },
  { title: 'A voice people stay on the line for.', body: 'Sub-second replies, natural turn-taking and no talking over the customer.', art: 'voice' },
  { title: 'Runs where you need it.', body: 'Your data centre, your cloud tenancy or our managed platform, with an engineer assigned through launch.', art: 'deploy' },
  { title: 'Closes the loop on payment.', body: 'Connected to your systems, the agent sees the live balance, takes payment on the call and books the result.', art: 'payment' },
]

/* ---------- Results ---------- */
export const RESULTS = {
  heading: { lead: 'Measured on live portfolios', rest: 'not in a demo' },
  sub: 'Collections is sensitive, regulated and unforgiving. These are the numbers from production pilots.',
  stats: [
    { value: '+3.8 pts', label: 'higher recovery than the in-house call centre', accent: true },
    { value: '−55%', label: 'cost per account versus agencies and internal teams', accent: true },
    { value: '100%', label: 'of calls reviewed for compliance, not a sample', accent: false },
    { value: '0.7 s', label: 'median response time, faster than a natural pause', accent: false },
  ],
  intro: `${B} was designed for regulated conversations from the start. Below are side-by-side results from pilots, anonymised at the client’s request.`,
  groups: [
    {
      title: '+3–4 pts more collected',
      note: 'Head-to-head against the incumbent channel on the same segment and time window.',
      cases: [
        { client: 'Retail bank, Southern Europe', segment: '0–90 days past due', baseline: { label: 'Call centre', value: 72 }, ours: 76 },
        { client: 'Digital lender, multi-market', segment: '0–30 days past due', baseline: { label: 'Collection agency', value: 69 }, ours: 72 },
      ],
    },
    {
      title: 'Half the cost, same outcome',
      note: 'Where recovery matched, the cost per resolved account fell sharply.',
      cases: [
        { client: 'Consumer finance, Northern Europe', segment: '0–30 days past due', baseline: { label: 'Call centre', value: 74 }, ours: 74 },
        { client: 'Utility provider, UK', segment: 'Early arrears', baseline: { label: 'Outsourced team', value: 63 }, ours: 64 },
      ],
    },
  ],
}

export const QUOTE = {
  text: `We expected to babysit it. Instead ${B} handled our hardest early-arrears calls with more patience than we could staff for.`,
  name: 'Head of Collections',
  role: 'Retail bank (placeholder testimonial)',
}

/* ---------- Product lifecycle ---------- */
export type FeatureArt = 'channels' | 'numbers' | 'identity' | 'budget' | 'offer' | 'schedule' | 'portal' | 'qa' | 'audit'
export const FEATURES: { id: string; nav: string; title: string; body: string; art: FeatureArt }[] = [
  { id: 'contact', nav: 'Contact strategy', art: 'channels', title: 'Reach out when people are most likely to respond', body: 'Calls, WhatsApp, SMS, email and letters are sequenced per customer, learning which channel and hour work best while respecting contact limits.' },
  { id: 'right-party', nav: 'Skip tracing', art: 'numbers', title: 'Find a working number and the right person on it', body: 'Each number is ranked by its history: answered, wrong person, disconnected. Weak numbers are re-checked against approved sources before they are dialled again.' },
  { id: 'verification', nav: 'Verification', art: 'identity', title: 'Confirm identity before a single detail is shared', body: 'The agent introduces itself as automated, checks identity against your criteria and discloses nothing about the account until the check passes.' },
  { id: 'affordability', nav: 'Affordability', art: 'budget', title: 'Base every plan on what the customer can really pay', body: 'Income and outgoings are collected in conversation or through a secure form, then turned into a plan the customer can keep.' },
  { id: 'negotiation', nav: 'Negotiation', art: 'offer', title: 'Agree terms within the limits you approve', body: 'Instalments, settlements or payment holidays are offered strictly from the options your policy allows for that customer’s situation.' },
  { id: 'payments', nav: 'Payment tracking', art: 'schedule', title: 'Watch every instalment and follow up when one slips', body: 'Expected payments are matched against what arrives. A missed instalment triggers a friendly check-in that starts from where the plan stands.' },
  { id: 'self-service', nav: 'Customer portal', art: 'portal', title: 'Give customers their plan in writing, on their phone', body: 'A secure page shows the balance, schedule and payment options, so the customer can review and accept without another call.' },
  { id: 'review', nav: 'Quality assurance', art: 'qa', title: 'Review every call against every rule', body: 'Each conversation is scored for disclosures, tone, vulnerability handling and policy adherence, with flags routed to your team.' },
  { id: 'case-prep', nav: 'Auditability', art: 'audit', title: 'Show exactly what happened and under which rules', body: 'Recordings, transcripts, offers and the ruleset version in force are kept together, ready for an auditor or a complaint review.' },
]

/* ---------- Industries ---------- */
export const INDUSTRIES = {
  heading: { lead: 'Different sectors, different rules', rest: `${B} works to yours` },
  sub: 'Your team defines what an agent can offer, when it can make contact and what it must disclose. The agent follows that, every time.',
  items: [
    { name: 'Banks', lead: 'High volumes of early-stage arrears with strict conduct rules.', body: 'Policy, disclosures and vulnerability handling are configured by your compliance team, not improvised on the call.' },
    { name: 'Consumer finance', lead: 'Many small balances that are uneconomic to chase by hand.', body: 'Every account gets timely, personal contact, so small balances are resolved before they roll into later stages.' },
    { name: 'Fintechs', lead: 'Loan books that grow faster than any team can hire.', body: 'Capacity scales with your portfolio overnight, in every market you launch in.' },
    { name: 'Agencies & debt buyers', lead: 'A different rulebook for every client portfolio.', body: 'Each portfolio carries its own rules, scripts and reporting, so audits are straightforward.' },
    { name: 'Utilities', lead: 'Bills where a phone call can cost more than the debt.', body: 'Low-cost digital channels first, voice where it matters, with hardship support built in.' },
    { name: 'Telecoms', lead: 'Disconnection loses the customer as well as the debt.', body: 'Agree a path back to good standing before service is suspended.' },
    { name: 'Asset finance', lead: 'Restructuring often beats repossession for both sides.', body: 'Offer term changes based on asset value and customer circumstances, within your limits.' },
    { name: 'Your sector', lead: 'Insurance, healthcare, public services and more.', body: 'Bring your rules, tone and channels and we will map them in a working session.', cta: 'Talk about your sector' },
  ],
}

/* ---------- Reach ---------- */
export const REACH = {
  heading: { lead: '14 markets,', rest: '25 languages' },
  sub: 'One rulebook, applied everywhere, with each market’s regulation, holidays, calling hours and language layered on top.',
  regions: [
    { name: 'Europe, Middle East & Africa', markets: [['France', 'fr'], ['Germany', 'de'], ['Italy', 'it'], ['Netherlands', 'nl'], ['Poland', 'pl'], ['Portugal', 'pt'], ['Spain', 'es'], ['Türkiye', 'tr'], ['UAE', 'ae'], ['UK', 'gb']] },
    { name: 'Americas & Asia Pacific', markets: [['Brazil', 'br'], ['Mexico', 'mx'], ['USA', 'us'], ['India', 'in']] },
  ] as { name: string; markets: [string, string][] }[],
}

/* ---------- Security ---------- */
export const CERTS = ['ISO 27001', 'SOC 2 Type II', 'GDPR', 'EU AI Act']
export const TRUST_NOTE = 'Certificates, security policies and our subprocessor list are available in the Trust Center.'

/* ---------- Team ---------- */
export const TEAM = {
  heading: { lead: 'Why collections,', rest: 'and why now' },
  body: [
    'Most collections work is still manual: queues, scripts and spreadsheets. Customers in difficulty get rushed calls, and good accounts get chased too late.',
    'Voice AI is finally fast and reliable enough for conversations that matter. We are building the agent workforce that lenders can trust with them.',
  ],
  people: [
    { name: 'Founder name', role: 'CEO & co-founder', hue: 150 },
    { name: 'Founder name', role: 'CPO & co-founder', hue: 30 },
    { name: 'Founder name', role: 'CTO & co-founder', hue: 210 },
  ],
}

/* ---------- FAQ ---------- */
export const FAQ = {
  heading: { lead: 'Questions,', rest: 'answered' },
  sub: 'What collections and compliance teams usually ask in the first meeting.',
  items: [
    { q: 'Does the customer know they are speaking to an AI?', a: `Yes. ${B} identifies itself as an automated agent at the start of every conversation and confirms it if asked.` },
    { q: 'What happens if someone asks for a human?', a: 'The call is transferred to your team straight away, or a callback is booked if nobody is available, with a summary attached.' },
    { q: 'What if someone other than the customer answers?', a: 'The agent verifies identity before any account detail is mentioned. If the check fails it shares nothing and asks for a better time to call.' },
    { q: 'Who controls what the agent says and offers?', a: 'Your team. Offers, disclosures, contact hours and escalation rules are configured and approved by you, and every version is logged.' },
    { q: 'How many calls are checked for compliance?', a: 'All of them. Every conversation is scored against your rules and flagged items are routed for human review.' },
    { q: 'How do we show a regulator what happened?', a: 'Recordings, transcripts, offers made and the ruleset version in force are stored together and exportable per account.' },
    { q: 'How are customers in financial difficulty handled?', a: 'The agent listens for signs of vulnerability, runs affordability checks where required and follows your hardship policy, including referral to a person.' },
    { q: 'Which channels and languages are supported?', a: 'Voice, WhatsApp, SMS, RCS and email, in 25 languages across 14 markets.' },
    { q: 'How does our data get in and results get back?', a: 'Via secure file transfer, API or direct integration with your dialer and CRM. Outcomes are written back in near real time.' },
    { q: 'Where does it run?', a: 'On your infrastructure, in your private cloud or on our managed platform. You choose the region and hold the keys.' },
  ],
}

export const CLOSING = {
  heading: { lead: 'Thirty minutes', rest: 'with the team that builds it' },
  sub: 'Tell us how your portfolio is worked today and we will show you, on your own scenarios, what changes.',
  cta: 'Book a call',
}

export const FOOTER = {
  blurb: `${B} runs collections and payment conversations with AI agents, inside the rules set by your team.`,
  links: [
    { label: 'Glossary', href: '#' },
    { label: 'Careers', href: '#' },
    { label: 'LinkedIn', href: BRAND.linkedInUrl },
  ],
  legal: [
    { label: 'Privacy policy', href: '#' },
    { label: 'Terms of service', href: '#' },
    { label: 'Cookies', href: '#' },
  ],
}
