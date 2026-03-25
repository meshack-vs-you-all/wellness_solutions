#!/bin/bash
echo "🚀 Starting Vite Frontend..."
cd frontend
# Using pnpm since pnpm-lock.yaml is present
if command -v pnpm &> /dev/null
then
    pnpm install
else
    npm install
fi
npm run dev -- --host
