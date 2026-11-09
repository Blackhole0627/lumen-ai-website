import type { AnchorHTMLAttributes, ReactNode } from 'react'

type Variant = 'primary' | 'light' | 'outline'

const variants: Record<Variant, string> = {
  primary: 'bg-forest text-paper hover:bg-forest-deep',
  light: 'bg-bone text-forest hover:bg-paper',
  outline: 'text-quiet ring-1 ring-inset ring-line hover:text-graphite hover:bg-bone',
}

type Props = AnchorHTMLAttributes<HTMLAnchorElement> & {
  variant?: Variant
  children: ReactNode
}

export function Button({ variant = 'primary', className = '', children, ...rest }: Props) {
  return (
    <a
      className={`text-body-s inline-flex h-10 items-center gap-2 whitespace-nowrap rounded-button px-5 font-semibold transition-colors ${variants[variant]} ${className}`}
      {...rest}
    >
      {children}
    </a>
  )
}
