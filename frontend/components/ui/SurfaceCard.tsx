import React from 'react';

type Props = {
  children: React.ReactNode;
  className?: string;
  style?: React.CSSProperties;
  variant?: 'dark' | 'glass' | 'outline';
};

export function SurfaceCard({ children, className = '', style, variant = 'dark' }: Props) {
  const base: React.CSSProperties = {
    borderRadius: 24,
    border: '1px solid #222',
    padding: 22,
    background: 'var(--dark)',
  };

  const variants: Record<string, React.CSSProperties> = {
    dark: base,
    outline: { ...base, background: 'transparent', border: '1px solid rgba(255,255,255,0.14)' },
    glass: {
      ...base,
      background: 'rgba(255,255,255,0.04)',
      border: '1px solid rgba(255,255,255,0.12)',
      backdropFilter: 'blur(10px)',
    },
  };

  return (
    <div className={className} style={{ ...(variants[variant] ?? base), ...style }}>
      {children}
    </div>
  );
}

