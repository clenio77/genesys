'use client'

import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'
import PricingSection from '@/components/PricingSection'
import SEOHead from '@/components/SEOHead'
import { FaQuestionCircle, FaRocket, FaShieldAlt, FaHeadset } from 'react-icons/fa'

export default function PricingPage() {
    const faqs = [
        {
            question: 'Como funciona o trial gratuito?',
            answer: 'Você tem 14 dias de acesso completo ao plano Professional, sem necessidade de cartão de crédito. Pode cancelar a qualquer momento.'
        },
        {
            question: 'Posso mudar de plano depois?',
            answer: 'Sim! Você pode fazer upgrade ou downgrade a qualquer momento. As mudanças são aplicadas imediatamente.'
        },
        {
            question: 'O que acontece se eu cancelar?',
            answer: 'Você mantém acesso até o final do período pago. Seus dados ficam salvos por 90 dias caso queira voltar.'
        },
        {
            question: 'Vocês oferecem desconto para pagamento anual?',
            answer: 'Sim! Pagando anualmente você economiza 10% em todos os planos.'
        },
        {
            question: 'Posso adicionar mais usuários depois?',
            answer: 'Sim! Usuários adicionais custam R$ 297/mês cada no plano Professional e são ilimitados no Enterprise.'
        },
        {
            question: 'A Genesys faz a implantação do Kermartin?',
            answer: 'Sim. Nos planos Professional e Enterprise, a Genesys conduz diagnóstico, parametrização, treinamento e governança. O Basic é self-service para começar rapidamente.'
        },
        {
            question: 'A oferta de Membro Fundador é realmente vitalícia?',
            answer: 'Sim! O preço de R$ 997/mês é garantido para sempre, mesmo quando aumentarmos os preços no futuro.'
        }
    ]

    const features = [
        {
            icon: FaRocket,
            title: 'Implantação Guiada',
            description: 'Basic: self-service em minutos. Professional e Enterprise incluem onboarding e implantação Genesys.'
        },
        {
            icon: FaShieldAlt,
            title: '100% Seguro',
            description: 'Seus dados são criptografados e protegidos. Conformidade total com LGPD.'
        },
        {
            icon: FaHeadset,
            title: 'Suporte Dedicado',
            description: 'Nossa equipe está sempre disponível para ajudar você a ter sucesso.'
        }
    ]

    return (
        <>
            <SEOHead
                title="Planos e Preços - Kermartin IA | Genesys Tecnologia"
                description="Escolha o plano ideal de IA jurídica para seu escritório. A partir de R$ 997/mês. Trial gratuito de 14 dias. Oferta especial para Membros Fundadores."
                keywords="preços kermartin, planos ia jurídica, assinatura kermartin, trial gratuito, membro fundador"
                canonical="https://genesys-tecnologia.com.br/pricing"
            />
            <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
                <PremiumHeader />

                {/* Hero Section */}
                <section className="pt-32 pb-12 px-4">
                    <div className="max-w-4xl mx-auto text-center">
                        <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-blue-400 via-cyan-400 to-purple-400 bg-clip-text text-transparent">
                            Planos Simples e Transparentes
                        </h1>
                        <p className="text-xl md:text-2xl text-gray-300 mb-8">
                            Planos do Kermartin IA. Implantação e operação guiada pela Genesys nos planos Professional e Enterprise.
                        </p>
                    </div>
                </section>

                {/* Pricing Section */}
                <PricingSection />

                {/* Features Grid */}
                <section className="py-20 px-4">
                    <div className="max-w-7xl mx-auto">
                        <h2 className="text-4xl font-bold text-center mb-12 text-white">
                            Por que escolher Kermartin + Genesys?
                        </h2>
                        <div className="grid md:grid-cols-3 gap-8">
                            {features.map((feature, idx) => {
                                const Icon = feature.icon
                                return (
                                    <div
                                        key={idx}
                                        className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border border-slate-700 hover:border-cyan-500/50 transition-all"
                                    >
                                        <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-blue-600 to-cyan-600 flex items-center justify-center text-white text-2xl mb-6">
                                            <Icon />
                                        </div>
                                        <h3 className="text-xl font-bold text-white mb-3">{feature.title}</h3>
                                        <p className="text-gray-300">{feature.description}</p>
                                    </div>
                                )
                            })}
                        </div>
                    </div>
                </section>

                {/* FAQ Section */}
                <section className="py-20 px-4 bg-slate-900/50">
                    <div className="max-w-4xl mx-auto">
                        <div className="text-center mb-12">
                            <FaQuestionCircle className="text-5xl text-cyan-400 mx-auto mb-4" />
                            <h2 className="text-4xl font-bold text-white mb-4">
                                Perguntas Frequentes
                            </h2>
                            <p className="text-gray-300">
                                Tire suas dúvidas sobre nossos planos
                            </p>
                        </div>

                        <div className="space-y-4">
                            {faqs.map((faq, idx) => (
                                <details
                                    key={idx}
                                    className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700 hover:border-cyan-500/50 transition-all group"
                                >
                                    <summary className="font-bold text-white cursor-pointer list-none flex items-center justify-between gap-4">
                                        <span className="min-w-0 flex-1">{faq.question}</span>
                                        <span className="text-cyan-400 group-open:rotate-180 transition-transform flex-shrink-0">
                                            ▼
                                        </span>
                                    </summary>
                                    <p className="text-gray-300 mt-4 leading-relaxed">
                                        {faq.answer}
                                    </p>
                                </details>
                            ))}
                        </div>
                    </div>
                </section>

                {/* CTA Final */}
                <section className="py-20 px-4">
                    <div className="max-w-4xl mx-auto text-center bg-gradient-to-r from-blue-600 to-cyan-600 rounded-3xl p-12">
                        <h2 className="text-4xl font-bold text-white mb-4">
                            Pronto para transformar sua prática jurídica?
                        </h2>
                        <p className="text-xl text-blue-100 mb-8">
                            Comece seu trial gratuito de 14 dias agora. Sem cartão de crédito.
                        </p>
                        <div className="flex flex-wrap justify-center gap-4">
                            <button
                                onClick={() => {
                                    const text = encodeURIComponent('Olá! Quero começar meu trial gratuito do Kermartin!')
                                    window.open(`https://wa.me/5534999788335?text=${text}`, '_blank')
                                }}
                                className="bg-white text-blue-600 px-8 py-4 rounded-lg font-bold hover:shadow-xl transition-all hover:scale-105"
                            >
                                Começar Trial Grátis
                            </button>
                            <button
                                onClick={() => {
                                    const text = encodeURIComponent('Olá! Gostaria de agendar uma demo do Kermartin.')
                                    window.open(`https://wa.me/5534999788335?text=${text}`, '_blank')
                                }}
                                className="bg-blue-800 text-white px-8 py-4 rounded-lg font-bold hover:shadow-xl transition-all hover:scale-105"
                            >
                                Agendar Demo
                            </button>
                        </div>
                    </div>
                </section>

                <Footer />
            </div>
        </>
    )
}
