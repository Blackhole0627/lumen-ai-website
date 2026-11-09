import type { GuaranteeArt as Kind } from '../../content/site'
import { Pill } from '../ui/Pill'
import { Clock, Plug } from '../ui/Icons'
import { Avatar, Panel, Progress, Row, Rows } from './Primitives'

const WAVE = [5, 9, 14, 8, 18, 11, 6, 15, 20, 9, 13, 7, 17, 10, 5, 12, 16, 8, 11, 6]

function Rules() {
  return (
    <>
      <Panel className="flex items-center gap-3 px-4 py-3.5">
        <span className="text-body-m flex-1 font-medium text-coal">Policy v18</span>
        <Pill tone="ok" icon>Signed off</Pill>
      </Panel>
      <div className="space-y-2">
        <Panel className="px-4 py-3.5">
          <div className="flex items-start gap-3">
            <Avatar text="AI" tone="moss" />
            <p className="text-body-m text-graphite">I can split the £240 into four payments of £60.</p>
          </div>
        </Panel>
        <Panel tone="bone" className="flex items-center gap-3 px-4 py-3">
          <Pill>Rule 3.1</Pill>
          <span className="text-body-s flex-1 text-quiet">Max 4 instalments, no write-off</span>
        </Panel>
      </div>
      <Rows>
        <Row label="Edited by" value="K. Osei" />
        <Row label="Approved" value="02 Oct" />
      </Rows>
    </>
  )
}

function Log() {
  return (
    <>
      <Panel className="px-4 pb-4 pt-3">
        <div className="flex items-center gap-2.5">
          <Avatar text="JM" />
          <span className="text-body-m flex-1 font-medium text-coal">Jamie Moore</span>
          <span className="text-body-s tabular-nums text-quiet">01:48</span>
        </div>
        <p className="text-body-m mt-3 rounded-xl rounded-ss-sm bg-bone px-3.5 py-2.5 text-graphite">“I get paid on the 28th, I can do £90 then.”</p>
        <div className="mt-2 flex items-start gap-2.5">
          <p className="text-body-m flex-1 rounded-xl rounded-se-sm bg-moss px-3.5 py-2.5 text-paper">Great, I’ve set £90 for the 28th.</p>
          <Avatar text="AI" tone="moss" />
        </div>
      </Panel>
      <Rows>
        <Row label="Promise amount" value="£90" />
        <Row label="Promise date" value="28th" />
      </Rows>
      <div className="flex justify-center">
        <Pill tone="ok" icon>Synced to CRM · 01:49</Pill>
      </div>
    </>
  )
}

function Trace() {
  return (
    <>
      <Panel className="flex items-center gap-3 px-4 py-3.5">
        <span className="text-body-m flex-1 font-medium text-coal">Contact check · #20817</span>
        <span className="text-body-s tabular-nums text-quiet">3 sources</span>
      </Panel>
      <div className="space-y-1.5">
        <Panel className="flex items-center gap-3 px-4 py-3">
          <span className="text-body-m flex-1 font-medium text-coal">Bureau data</span>
          <Pill>2 numbers</Pill>
        </Panel>
        <Panel tone="bone" className="flex items-center gap-3 px-4 py-3">
          <span className="text-body-m flex-1 font-medium text-coal">Carrier lookup</span>
          <Pill tone="ok" icon>1 active</Pill>
        </Panel>
        <Panel tone="bone-2" className="flex items-center gap-3 px-4 py-3 opacity-65">
          <span className="text-body-m flex-1 font-medium text-coal">Address registry</span>
          <Pill>No change</Pill>
        </Panel>
      </div>
      <Panel className="px-4 py-3.5">
        <div className="flex items-center gap-3">
          <span className="text-body-m flex-1 font-medium text-coal">Account holder reached</span>
          <Pill tone="solid">
            <Clock className="h-3.5 w-3.5" /> 10:04
          </Pill>
        </div>
        <Progress value={66} className="mt-3" />
        <span className="text-body-s mt-2 block text-quiet">Second attempt, preferred hour</span>
      </Panel>
    </>
  )
}

function Voice() {
  return (
    <>
      <Panel className="flex divide-x divide-line-soft">
        <div className="min-w-0 flex-1 px-4 py-3.5">
          <p className="text-body-s text-quiet">Median reply</p>
          <p className="text-display-s mt-0.5 tabular-nums text-coal">0.7 s</p>
        </div>
        <div className="min-w-0 flex-1 px-4 py-3.5">
          <p className="text-body-s text-quiet">Interruptions</p>
          <p className="text-display-s mt-0.5 tabular-nums text-coal">0</p>
        </div>
      </Panel>
      <Panel className="px-3 py-3">
        <div className="flex items-center gap-3 rounded-full bg-moss px-4 py-2">
          <span className="text-body-s shrink-0 tabular-nums text-paper/60">01:12</span>
          <span className="flex h-6 flex-1 items-center justify-between">
            {WAVE.map((h, i) => (
              <span key={i} className={`w-[3px] rounded-full ${i < 11 ? 'bg-mint' : 'bg-paper/35'}`} style={{ height: h }} />
            ))}
          </span>
        </div>
        <p className="text-body-s mt-3 text-quiet">The customer pauses, the agent picks up without a gap or overlap.</p>
      </Panel>
      <Panel className="flex items-center gap-3 px-4 py-3.5">
        <span className="text-body-m flex-1 font-medium text-coal">Under 1 s</span>
        <span className="text-body-m font-medium tabular-nums text-coal">98% of turns</span>
      </Panel>
    </>
  )
}

function Deploy() {
  const opts = [
    { name: 'On-premise', note: 'Your hardware, your keys', tone: 'paper' as const },
    { name: 'Private cloud', note: 'Your region and tenancy', tone: 'bone' as const, chosen: true },
    { name: 'Managed', note: 'Fully run by us', tone: 'bone-2' as const, dim: true },
  ]
  return (
    <>
      <div className="space-y-1.5">
        {opts.map((o) => (
          <Panel key={o.name} tone={o.tone} className={`flex items-center gap-3 px-4 py-3 ${o.dim ? 'opacity-65' : ''}`}>
            <span className="min-w-0 flex-1">
              <span className="text-body-m block font-medium text-coal">{o.name}</span>
              <span className="text-body-s block text-quiet">{o.note}</span>
            </span>
            {o.chosen && <Pill tone="ok" icon>Selected</Pill>}
          </Panel>
        ))}
      </div>
      <Panel className="px-3 py-3">
        <div className="flex items-center gap-3">
          <Avatar text="KO" size={40} />
          <span className="min-w-0 flex-1">
            <span className="text-body-m block truncate font-medium text-coal">K. Osei</span>
            <span className="text-body-s block text-quiet">Solutions engineer, through go-live</span>
          </span>
        </div>
        <div className="mt-3 flex flex-wrap gap-1.5">
          {['Dialer', 'CRM', 'Payments'].map((t) => (
            <Pill key={t} tone="solid">
              <Plug className="h-3.5 w-3.5" /> {t}
            </Pill>
          ))}
        </div>
      </Panel>
    </>
  )
}

function Payment() {
  return (
    <>
      <Rows>
        <Row label="Live balance" value="£240.00" />
        <Row label="Plan agreed" value="4 × £60.00" />
      </Rows>
      <Panel className="px-4 py-4">
        <div className="flex items-center gap-3">
          <span className="text-body-m flex-1 font-medium text-coal">First payment received</span>
          <Pill tone="ok" icon>10:11</Pill>
        </div>
        <Progress value={25} className="mt-3" />
        <span className="text-body-s mt-2 block text-quiet">£60.00 taken during the call</span>
      </Panel>
      <div className="flex justify-center">
        <Pill tone="ok" icon>Outcome written back</Pill>
      </div>
    </>
  )
}

const MAP: Record<Kind, () => React.JSX.Element> = { rules: Rules, log: Log, trace: Trace, voice: Voice, deploy: Deploy, payment: Payment }

export function GuaranteeArt({ kind }: { kind: Kind }) {
  const C = MAP[kind]
  return (
    <div className="flex h-full flex-col justify-center gap-4 px-5 py-6 sm:px-6">
      <C />
    </div>
  )
}
