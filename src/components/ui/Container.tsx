import type { ReactNode } from 'react'

type Props = { children: ReactNode; className?: string }

export function Container({ children, className = '' }: Props) {
  return <div className={`mx-auto w-full max-w-[1320px] px-5 sm:px-10 lg:px-14 ${className}`}>{children}</div>
}
