
import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
}

/** Card — sits on the surface layer. Switches to dark surface in dark mode. */
export const Card: React.FC<CardProps> = ({ children, className = '' }) => {
  return (
    <div className={`bg-white dark:bg-[var(--dark)] border border-neutral-200 dark:border-[#1a1a1a] rounded-xl shadow-md dark:shadow-black/30 overflow-hidden ${className}`}>
      {children}
    </div>
  );
};

export const CardHeader: React.FC<CardProps> = ({ children, className = '' }) => {
  return (
    <div className={`px-6 py-4 border-b border-neutral-200 dark:border-[#1a1a1a] ${className}`}>
      {children}
    </div>
  );
};

export const CardContent: React.FC<CardProps> = ({ children, className = '' }) => {
  return <div className={`p-6 ${className}`}>{children}</div>;
};

export const CardFooter: React.FC<CardProps> = ({ children, className = '' }) => {
  return (
    <div className={`px-6 py-4 bg-neutral-50 dark:bg-[var(--surface-black)] border-t border-neutral-200 dark:border-[#1a1a1a] ${className}`}>
      {children}
    </div>
  );
};