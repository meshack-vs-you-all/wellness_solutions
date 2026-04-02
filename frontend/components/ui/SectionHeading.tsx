import React from 'react';

type Props = {
  eyebrow?: string;
  title: string;
  subtitle?: string;
  align?: 'left' | 'center';
};

export function SectionHeading({ eyebrow, title, subtitle, align = 'left' }: Props) {
  const isCenter = align === 'center';
  return (
    <div style={{ textAlign: isCenter ? 'center' : 'left', maxWidth: isCenter ? 820 : 900, margin: isCenter ? '0 auto' : undefined }}>
      {eyebrow && (
        <div
          style={{
            color: 'var(--brand-primary)',
            fontWeight: 900,
            letterSpacing: 2,
            textTransform: 'uppercase',
            fontSize: '0.85rem',
            marginBottom: 12,
          }}
        >
          {eyebrow}
        </div>
      )}
      <h2 style={{ fontSize: 'clamp(2rem, 5vw, 3.6rem)', fontWeight: 950, letterSpacing: '-0.04em', margin: 0, lineHeight: 1.05 }}>
        {title}
      </h2>
      {subtitle && (
        <p style={{ color: '#a1a1aa', fontSize: 'clamp(1rem, 2.6vw, 1.25rem)', marginTop: 16, lineHeight: 1.7 }}>
          {subtitle}
        </p>
      )}
    </div>
  );
}

