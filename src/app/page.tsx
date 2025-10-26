import PremiumHeader from '@/components/PremiumHeader'
import HeroSection from '@/components/HeroSection'
import ServicesSection from '@/components/ServicesSection'
import AIShowcase from '@/components/AIShowcase'
import TestimonialsSection from '@/components/TestimonialsSection'
import TeamSection from '@/components/TeamSection'
import KermartinSection from '@/components/KermartinSection'
import ContactSection from '@/components/ContactSection'
import FloatingCertifications from '@/components/FloatingCertifications'
import WhatsAppFloat from '@/components/WhatsAppFloat'
import Footer from '@/components/Footer'

// Força renderização dinâmica para evitar erros de pre-render
export const dynamic = 'force-dynamic'

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-900">
      <PremiumHeader />
      <HeroSection />
      <ServicesSection />
      <AIShowcase />
      <TestimonialsSection />
      <TeamSection />
      <KermartinSection />
      <ContactSection />
      <FloatingCertifications />
      <WhatsAppFloat />
      <Footer />
    </main>
  )
}