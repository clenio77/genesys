import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Genesys Tecnologia - Inteligência Artificial Jurídica',
  description: 'Transforme sua prática jurídica com soluções de IA de última geração. Análise inteligente, automação avançada e insights precisos para decisões estratégicas.',
  keywords: [
    'IA Jurídica',
    'Inteligência Artificial',
    'Advocacia',
    'Legal Tech',
    'Automação Jurídica',
    'Análise de Contratos',
    'Pesquisa Jurisprudencial',
    'Genesys',
    'Tecnologia Jurídica',
  ],
  authors: [{ name: 'Genesys Tecnologia' }],
  creator: 'Genesys Tecnologia',
  publisher: 'Genesys Tecnologia',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL('https://genesys.tech'),
  alternates: {
    canonical: '/',
  },
  openGraph: {
    title: 'Genesys Tecnologia - Inteligência Artificial Jurídica',
    description: 'Transforme sua prática jurídica com soluções de IA de última geração.',
    url: 'https://genesys.tech',
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
    description: 'Transforme sua prática jurídica com soluções de IA de última geração.',
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
    yandex: 'your-yandex-verification-code',
  },
}

