import type { Metadata } from 'next'
import { Inter, Playfair_Display, JetBrains_Mono } from 'next/font/google'
import './globals.css'

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

const playfair = Playfair_Display({ 
  subsets: ['latin'],
  variable: '--font-playfair',
  display: 'swap',
})

const jetbrains = JetBrains_Mono({ 
  subsets: ['latin'],
  variable: '--font-jetbrains',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'Genesys Tecnologia - Inteligência Artificial Jurídica',
  description: 'Inteligência Artificial que Redefine a Análise Jurídica. Transformamos dados jurídicos em insights poderosos através de IA avançada.',
  keywords: 'inteligência artificial, direito, advocacia, jurisprudência, análise jurídica, IA jurídica',
  authors: [{ name: 'Genesys Tecnologia' }],
  creator: 'Genesys Tecnologia',
  publisher: 'Genesys Tecnologia',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL('https://genesys-tecnologia.com.br'),
  alternates: {
    canonical: '/',
  },
  openGraph: {
    title: 'Genesys Tecnologia - Inteligência Artificial Jurídica',
    description: 'Inteligência Artificial que Redefine a Análise Jurídica',
    url: 'https://genesys-tecnologia.com.br',
    siteName: 'Genesys Tecnologia',
    images: [
      {
        url: '/images/genesys-logo.jpg',
        width: 1200,
        height: 630,
        alt: 'Genesys Tecnologia',
      },
    ],
    locale: 'pt_BR',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Genesys Tecnologia - Inteligência Artificial Jurídica',
    description: 'Inteligência Artificial que Redefine a Análise Jurídica',
    images: ['/images/genesys-logo.jpg'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  verification: {
    google: 'your-google-verification-code',
  },
  category: 'technology',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-BR" className={`${inter.variable} ${playfair.variable} ${jetbrains.variable}`}>
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta name="theme-color" content="#3b82f6" />
        <meta name="mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="default" />
        <meta name="apple-mobile-web-app-title" content="Genesys" />
        <meta name="msapplication-TileColor" content="#3b82f6" />
        <meta name="msapplication-tap-highlight" content="no" />
        <link rel="apple-touch-icon" href="/images/genesys-logo.jpg" />
        <link rel="icon" type="image/jpeg" sizes="192x192" href="/images/genesys-logo.jpg" />
        <link rel="icon" type="image/jpeg" sizes="512x512" href="/images/genesys-logo.jpg" />
        <link rel="manifest" href="/manifest.json" />
      </head>
      <body className={`${inter.className} antialiased`}>
        {children}
      </body>
    </html>
  )
}