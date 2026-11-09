// Only the flags used on the page are bundled. Add codes to this pattern when adding markets.
const FLAGS = import.meta.glob<string>('/node_modules/flag-icons/flags/1x1/{gb,es,de,fr,it,br,nl,ae,pl,pt,tr,mx,us,in}.svg', {
  eager: true,
  query: '?url',
  import: 'default',
})

export function Flag({ code, className = '', style }: { code: string; className?: string; style?: React.CSSProperties }) {
  const src = FLAGS[`/node_modules/flag-icons/flags/1x1/${code}.svg`]
  return (
    <span className={`inline-block overflow-hidden rounded-full bg-bone-2 ${className}`} style={style} aria-hidden>
      {src && <img src={src} alt="" className="block h-full w-full object-cover" />}
    </span>
  )
}
