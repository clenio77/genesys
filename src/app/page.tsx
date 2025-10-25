import Header from '@/components/Header'
import ProductCarousel from '@/components/ProductCarousel'
import KermartinSection from '@/components/KermartinSection'
import TeamSection from '@/components/TeamSection'
import Footer from '@/components/Footer'
import FloatingCertifications from '@/components/FloatingCertifications'
import WhatsAppFloat from '@/components/WhatsAppFloat'

export default function Home() {
  return (
    <main className="min-h-screen">
      <Header />
      <ProductCarousel />
      <KermartinSection />
      <TeamSection />
      <Footer />
      <FloatingCertifications />
      <WhatsAppFloat />
    </main>
  )
}