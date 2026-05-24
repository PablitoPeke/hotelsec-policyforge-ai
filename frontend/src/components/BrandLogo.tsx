type BrandLogoProps = {
  compact?: boolean
}

export function BrandLogo({ compact = false }: BrandLogoProps) {
  return (
    <div className={compact ? 'brand-logo brand-logo-compact' : 'brand-logo'} aria-hidden="true">
      <svg viewBox="0 0 64 64" role="img">
        <defs>
          <linearGradient id="hotelSecLogoGradient" x1="10" x2="54" y1="8" y2="58">
            <stop offset="0%" stopColor="#5eead4" />
            <stop offset="58%" stopColor="#14b8a6" />
            <stop offset="100%" stopColor="#2563eb" />
          </linearGradient>
        </defs>
        <path
          d="M32 6 52 13v15c0 13.5-7.8 24.4-20 30-12.2-5.6-20-16.5-20-30V13L32 6Z"
          fill="url(#hotelSecLogoGradient)"
        />
        <path
          d="M21 28h22v18H21V28Zm4 5v4h4v-4h-4Zm0 7v4h4v-4h-4Zm6-7v4h4v-4h-4Zm0 7v4h4v-4h-4Zm6-7v4h4v-4h-4Zm0 7v4h4v-4h-4Z"
          fill="#05201d"
          opacity="0.88"
        />
        <path
          d="M26 23h12l4 5H22l4-5Z"
          fill="#ffffff"
          opacity="0.9"
        />
        <path
          d="m27.5 19.5 3.2 3.2 6.8-7"
          fill="none"
          stroke="#ffffff"
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth="4"
        />
      </svg>
    </div>
  )
}
