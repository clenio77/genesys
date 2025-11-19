import type { Metadata } from 'next'
import { Inter, Playfair_Display, JetBrains_Mono } from 'next/font/google'
import './globals.css'
import GoogleAnalytics from '@/components/GoogleAnalytics'

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
        url: '/images/genesys-logo.png',
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
    images: ['/images/genesys-logo.png'],
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
  manifest: '/manifest.json',
  icons: {
    icon: '/favicon.ico',
    apple: '/images/genesys-logo.png',
  },
  appleWebApp: {
    capable: true,
    statusBarStyle: 'default',
    title: 'Genesys',
  },
}

export const viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  themeColor: '#3b82f6',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-BR" className={`${inter.variable} ${playfair.variable} ${jetbrains.variable}`}>
      <body className={`${inter.className} antialiased`}>
        {process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID && (
          <GoogleAnalytics GA_MEASUREMENT_ID={process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID} />
        )}
        {children}
      </body>
    </html>
  )
}