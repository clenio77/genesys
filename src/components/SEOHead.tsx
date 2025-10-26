'use client'

import { useEffect } from 'react'

interface SEOHeadProps {
  title: string
  description: string
  keywords?: string
  ogImage?: string
  canonical?: string
}

export default function SEOHead({ 
  title, 
  description, 
  keywords = 'inteligência artificial, direito, advocacia, jurisprudência, análise jurídica, IA jurídica',
  ogImage = '/images/genesys-logo.jpg',
  canonical
}: SEOHeadProps) {
  useEffect(() => {
    // Update document title
    document.title = title
    
    // Update meta tags
    const updateMetaTag = (name: string, content: string, isProperty = false) => {
      const attribute = isProperty ? 'property' : 'name'
      let meta = document.querySelector(`meta[${attribute}="${name}"]`)
      
      if (!meta) {
        meta = document.createElement('meta')
        meta.setAttribute(attribute, name)
        document.head.appendChild(meta)
      }
      
      meta.setAttribute('content', content)
    }
    
    // Standard meta tags
    updateMetaTag('description', description)
    updateMetaTag('keywords', keywords)
    
    // Open Graph tags
    updateMetaTag('og:title', title, true)
    updateMetaTag('og:description', description, true)
    updateMetaTag('og:image', ogImage, true)
    updateMetaTag('og:type', 'website', true)
    
    // Twitter Card tags
    updateMetaTag('twitter:card', 'summary_large_image')
    updateMetaTag('twitter:title', title)
    updateMetaTag('twitter:description', description)
    updateMetaTag('twitter:image', ogImage)
    
    // Canonical URL
    if (canonical) {
      let link = document.querySelector('link[rel="canonical"]') as HTMLLinkElement
      
      if (!link) {
        link = document.createElement('link')
        link.setAttribute('rel', 'canonical')
        document.head.appendChild(link)
      }
      
      link.setAttribute('href', canonical)
    }
  }, [title, description, keywords, ogImage, canonical])
  
  return null
}

