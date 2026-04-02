import React from 'react';

type Props = {
  children: React.ReactNode;
  maxWidth?: number;
  className?: string;
  style?: React.CSSProperties;
};

export function Container({ children, maxWidth = 1200, className = '', style }: Props) {
  return (
    <div
      className={className}
      style={{
        maxWidth,
        margin: '0 auto',
        padding: '0 20px',
        ...style,
      }}
    >
      {children}
    </div>
  );
}

