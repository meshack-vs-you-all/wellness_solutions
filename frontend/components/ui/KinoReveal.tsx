import React from 'react';
import { Reveal } from 'react-kino';

type Props = {
  children: React.ReactNode;
  delay?: number;
  animation?: 'fade' | 'fade-up' | 'fade-down' | 'scale' | 'blur';
};

export function KinoReveal({ children, delay = 0, animation = 'fade-up' }: Props) {
  return (
    <Reveal animation={animation} delay={delay}>
      {children}
    </Reveal>
  );
}

