
import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'accent' | 'destructive';
  size?: 'sm' | 'md' | 'lg';
}

const sizeMap: Record<string, string> = {
  sm: 'h-9 px-4 text-sm',
  md: 'h-10 px-6 text-sm',
  lg: 'h-12 px-8 text-base',
};

const variantMap: Record<string, string> = {
  primary: 'btn-primary',
  secondary: 'btn-secondary',
  ghost: 'btn-ghost',
  accent: 'btn-accent',
  destructive: 'bg-red-600 text-white hover:bg-red-700 rounded-full font-bold border-none cursor-pointer inline-flex items-center justify-center transition-opacity',
};

export const Button: React.FC<ButtonProps> = ({
  className = '',
  variant = 'primary',
  size = 'md',
  ...props
}) => {
  const base = 'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none';
  const variantClass = variantMap[variant] ?? variantMap.primary;
  const sizeClass = sizeMap[size] ?? sizeMap.md;

  return (
    <button
      className={`${base} ${variantClass} ${sizeClass} ${className}`}
      {...props}
    />
  );
};