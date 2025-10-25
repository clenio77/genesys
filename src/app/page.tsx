import PremiumHeader from '@/components/PremiumHeader'
import HeroSection from '@/components/HeroSection'
import ServicesSection from '@/components/ServicesSection'
import AIShowcase from '@/components/AIShowcase'
import TeamSection from '@/components/TeamSection'
import KermartinSection from '@/components/KermartinSection'
import FloatingCertifications from '@/components/FloatingCertifications'
import WhatsAppFloat from '@/components/WhatsAppFloat'
import Footer from '@/components/Footer'

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-900">
      <PremiumHeader />
      <HeroSection />
      <ServicesSection />
      <AIShowcase />
      <TeamSection />
      <KermartinSection />
      <FloatingCertifications />
      <WhatsAppFloat />
      <Footer />
    </main>
  )
}