import type { FeatureArt as Kind } from '../../content/site'
import { Pill } from '../ui/Pill'
import { Bot, Check, Shield } from '../ui/Icons'
import { Avatar, Panel, Progress, Row, Rows } from './Primitives'

function Channels() {
  const steps = [
    { day: 'Day 1', ch: 'SMS', note: 'Friendly reminder', state: 'Delivered' },
    { day: 'Day 3', ch: 'Voice', note: '18:30, best hour', state: 'Answered' },
    { day: 'Day 3', ch: 'WhatsApp', note: 'Plan summary', state: 'Read' },
    { day: 'Day 8', ch: 'Email', note: 'Only if unpaid', state: 'Scheduled', dim: true },
  ]
  return (
    <div className="mx-auto grid max-w-[520px] gap-2">
      {steps.map((s) => (
        <Panel key={s.ch + s.day} tone={s.dim ? 'bone' : 'paper'} className={`flex items-center gap-3 px-4 py-3 ${s.dim ? 'opacity-70' : ''}`}>
          <span className="text-body-s w-14 shrink-0 tabular-nums text-quiet">{s.day}</span>
          <span className="min-w-0 flex-1">
            <span className="text-body-m block font-medium text-coal">{s.ch}</span>
            <span className="text-body-s block text-quiet">{s.note}</span>
          </span>
          <Pill tone={s.dim ? 'neutral' : 'ok'} icon={!s.dim}>
            {s.state}
          </Pill>
        </Panel>
      ))}
    </div>
  )
}

function Numbers() {
  const nums = [
    { n: '+44 7700 900 412', score: 86, note: 'Answered twice, evenings' },
    { n: '+44 7700 900 087', score: 41, note: 'Voicemail only' },
    { n: '+44 20 7946 0331', score: 8, note: 'Wrong person, suppressed' },
  ]
  return (
    <div className="mx-auto grid max-w-[520px] gap-2">
      {nums.map((x, i) => (
        <Panel key={x.n} className={`px-4 py-3.5 ${i === 2 ? 'opacity-60' : ''}`}>
          <div className="flex items-center gap-3">
            <span className="text-body-m flex-1 font-medium tabular-nums text-coal">{x.n}</span>
            <span className="text-body-s font-medium tabular-nums text-forest">{x.score}</span>
          </div>
          <Progress value={x.score} className="mt-2.5" />
          <span className="text-body-s mt-2 block text-quiet">{x.note}</span>
        </Panel>
      ))}
    </div>
  )
}

function Identity() {
  return (
    <div className="mx-auto grid max-w-[520px] gap-2">
      <Panel className="px-4 py-3.5">
        <div className="flex items-start gap-3">
          <Avatar text={<Bot className="h-4 w-4" />} tone="moss" />
          <p className="text-body-m text-graphite">Hello, I’m an automated assistant. Before we continue, could you confirm your date of birth?</p>
        </div>
      </Panel>
      <Rows>
        {['Disclosed as automated', 'Date of birth matched', 'Postcode matched'].map((t) => (
          <div key={t} className="flex items-center gap-3 px-4 py-3">
            <Check className="h-4 w-4 text-forest" />
            <span className="text-body-m flex-1 text-graphite">{t}</span>
          </div>
        ))}
      </Rows>
      <div className="flex justify-center">
        <Pill tone="ok">
          <Shield className="h-3.5 w-3.5" /> Identity confirmed, account unlocked
        </Pill>
      </div>
    </div>
  )
}

function Budget() {
  return (
    <div className="mx-auto grid max-w-[520px] gap-2">
      <Rows>
        <Row label="Monthly income" value="£1,850" />
        <Row label="Essential outgoings" value="£1,610" />
        <Row label="Available" value="£240" strong />
      </Rows>
      <Panel className="px-4 py-3.5">
        <span className="text-body-s text-quiet">Recommended plan</span>
        <p className="text-display-s mt-0.5 tabular-nums text-coal">£60 / month</p>
        <Progress value={25} className="mt-3" />
        <span className="text-body-s mt-2 block text-quiet">25% of available income</span>
      </Panel>
    </div>
  )
}

function Offer() {
  const opts = [
    { t: '4 monthly instalments', s: '£60 each', chosen: true },
    { t: 'Settle in full', s: '£240 today' },
    { t: 'Payment holiday', s: 'Not eligible', dim: true },
  ]
  return (
    <div className="mx-auto grid max-w-[520px] gap-2">
      {opts.map((o) => (
        <Panel key={o.t} tone={o.chosen ? 'paper' : 'bone'} className={`flex items-center gap-3 px-4 py-3 ${o.dim ? 'opacity-55' : ''}`}>
          <span className="min-w-0 flex-1">
            <span className="text-body-m block font-medium text-coal">{o.t}</span>
            <span className="text-body-s block text-quiet">{o.s}</span>
          </span>
          {o.chosen && <Pill tone="ok" icon>Agreed</Pill>}
        </Panel>
      ))}
      <Panel tone="bone" className="flex items-center gap-3 px-4 py-3">
        <Pill>Policy 3.1</Pill>
        <span className="text-body-s flex-1 text-quiet">Up to 4 instalments for balances under £500</span>
      </Panel>
    </div>
  )
}

function Schedule() {
  const rows = [
    { m: 'Oct 28', a: '£60.00', s: 'Paid', ok: true },
    { m: 'Nov 28', a: '£60.00', s: 'Paid', ok: true },
    { m: 'Dec 28', a: '£60.00', s: 'Missed · check-in sent', warn: true },
    { m: 'Jan 28', a: '£60.00', s: 'Upcoming' },
  ]
  return (
    <div className="mx-auto max-w-[520px]">
      <Panel className="divide-y divide-line-soft">
        {rows.map((r) => (
          <div key={r.m} className="flex items-center gap-3 px-4 py-3">
            <span className="text-body-m w-16 shrink-0 tabular-nums text-quiet">{r.m}</span>
            <span className="text-body-m flex-1 font-medium tabular-nums text-coal">{r.a}</span>
            <span
              className={`text-body-s rounded-full px-3 py-1 font-medium ${r.ok ? 'bg-ok-wash text-forest' : r.warn ? 'bg-rust-wash text-rust' : 'bg-bone text-quiet'}`}
            >
              {r.s}
            </span>
          </div>
        ))}
      </Panel>
    </div>
  )
}

function Portal() {
  return (
    <div className="mx-auto w-[260px] rounded-[28px] bg-coal p-2 shadow-[var(--shadow-lift)]">
      <div className="overflow-hidden rounded-[22px] bg-paper">
        <div className="bg-forest px-4 pb-5 pt-6 text-paper">
          <p className="text-caption text-paper/70">Outstanding balance</p>
          <p className="text-display-s mt-1 tabular-nums">£180.00</p>
        </div>
        <div className="space-y-2 p-3">
          <Rows>
            <Row label="Next payment" value="Jan 28" />
            <Row label="Amount" value="£60" />
          </Rows>
          <span className="text-body-s flex h-10 items-center justify-center rounded-button bg-forest font-semibold text-paper">Accept plan</span>
          <span className="text-body-s flex h-10 items-center justify-center rounded-button bg-bone font-semibold text-graphite">Pay now</span>
        </div>
      </div>
    </div>
  )
}

function Qa() {
  const checks = [
    { t: 'Automated disclosure', s: 100 },
    { t: 'Identity before details', s: 100 },
    { t: 'Vulnerability handling', s: 96 },
    { t: 'Offer within policy', s: 100 },
  ]
  return (
    <div className="mx-auto grid max-w-[520px] gap-2">
      <Panel className="flex items-center gap-3 px-4 py-3.5">
        <span className="text-body-m flex-1 font-medium text-coal">Call #48 210 · scored</span>
        <Pill tone="ok" icon>Pass</Pill>
      </Panel>
      <Panel className="divide-y divide-line-soft">
        {checks.map((c) => (
          <div key={c.t} className="px-4 py-3">
            <div className="flex items-center gap-3">
              <span className="text-body-m flex-1 text-graphite">{c.t}</span>
              <span className="text-body-s font-medium tabular-nums text-coal">{c.s}%</span>
            </div>
            <Progress value={c.s} className="mt-2" />
          </div>
        ))}
      </Panel>
    </div>
  )
}

function Audit() {
  const ev = [
    { t: '10:02', e: 'Call started, recording on' },
    { t: '10:03', e: 'Identity verified' },
    { t: '10:06', e: 'Plan offered under Policy v18' },
    { t: '10:08', e: 'Customer accepted, SMS sent' },
    { t: '10:11', e: 'First payment received' },
  ]
  return (
    <div className="mx-auto max-w-[520px]">
      <Panel className="px-4 py-4">
        <ol className="relative space-y-3 border-s border-line ps-5">
          {ev.map((x) => (
            <li key={x.t} className="relative">
              <span className="absolute -start-[25px] top-1.5 h-2.5 w-2.5 rounded-full bg-moss ring-4 ring-paper" />
              <span className="text-body-s tabular-nums text-quiet">{x.t}</span>
              <p className="text-body-m text-graphite">{x.e}</p>
            </li>
          ))}
        </ol>
      </Panel>
      <div className="mt-2 flex justify-center">
        <Pill tone="ok" icon>Export ready for review</Pill>
      </div>
    </div>
  )
}

const MAP: Record<Kind, () => React.JSX.Element> = {
  channels: Channels,
  numbers: Numbers,
  identity: Identity,
  budget: Budget,
  offer: Offer,
  schedule: Schedule,
  portal: Portal,
  qa: Qa,
  audit: Audit,
}

export function FeatureArt({ kind }: { kind: Kind }) {
  const C = MAP[kind]
  return <C />
}
