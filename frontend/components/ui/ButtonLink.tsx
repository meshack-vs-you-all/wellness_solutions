import React from 'react';
import { Link } from 'react-router-dom';

type Props = {
  to: string;
  children: React.ReactNode;
  variant?: 'primary' | 'ghost' | 'secondary' | 'accent';
  style?: React.CSSProperties;
  className?: string;
};

export function ButtonLink({ to, children, variant = 'primary', style, className = '' }: Props) {
  const classMap: Record<string, string> = {
    primary: 'btn-primary',
    secondary: 'btn-secondary',
    ghost: 'btn-ghost',
    accent: 'btn-accent',
  };

  return (
    <Link to={to} className={`${classMap[variant]} ${className}`} style={style}>
      {children}
    </Link>
  );
}

