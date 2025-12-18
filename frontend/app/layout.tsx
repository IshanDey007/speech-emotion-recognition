import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Speech Emotion Recognition | Customer Satisfaction Analysis',
  description: 'AI-powered emotion detection from speech to measure and improve customer satisfaction',
  keywords: ['emotion recognition', 'speech analysis', 'customer satisfaction', 'AI', 'machine learning'],
  authors: [{ name: 'Ishan Dey' }],
  openGraph: {
    title: 'Speech Emotion Recognition',
    description: 'AI-powered emotion detection from speech',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}