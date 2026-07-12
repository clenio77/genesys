'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { FaCheck, FaTimes, FaRocket, FaStar, FaCrown, FaFire } from 'react-icons/fa'

export default function PricingSection() {
    const [billingPeriod, setBillingPeriod] = useState<'monthly' | 'annual'>('monthly')

    const tiers = [
        {
            id: 'basic',
            name: 'Basic',
            tagline: 'Para Começar',
            price: billingPeriod === 'monthly' ? 997 : 897,
            period: billingPeriod === 'monthly' ? '/mês' : '/mês (anual)',
            description: 'Ideal para advogados autônomos que querem começar com IA',
            icon: FaRocket,
            gradient: 'from-blue-600 to-cyan-600',
            features: [
                'Kermartin IA — módulo completo',
                'Até 100 análises/mês',
                'Busca com fontes e citações',
                'Upload de documentos',
                '1 usuário',
                'Suporte por email',
                'Acesso web'
            ],
            notIncluded: [
                'Implantação guiada Genesys',
                'Base privada customizada',
                'Integrações avançadas'
            ],
            cta: 'Começar Agora',
            popular: false
        },
        {
            id: 'professional',
            name: 'Professional',
            tagline: 'Mais Popular',
            price: billingPeriod === 'monthly' ? 2497 : 2247,
            originalPrice: billingPeriod === 'monthly' ? undefined : 2497,
            period: billingPeriod === 'monthly' ? '/mês' : '/mês (anual)',
            description: 'Para escritórios que querem produtividade máxima',
            icon: FaStar,
            gradient: 'from-purple-600 to-pink-600',
            popular: true,
            features: [
                'Tudo do Basic, mais:',
                'Análises ilimitadas',
                'Todos os módulos (penal, civil, trânsito, tributário)',
                'Base privada e RAG integrado',
                'OCR avançado (PDF, imagens)',
                'Até 5 usuários',
                'Suporte prioritário',
                'Integrações (Zapier)',
                'Relatórios avançados'
            ],
            cta: 'Começar Trial Grátis'
        },
        {
            id: 'enterprise',
            name: 'Enterprise',
            tagline: 'Solução Completa',
            price: billingPeriod === 'monthly' ? 4997 : 4497,
            originalPrice: billingPeriod === 'monthly' ? undefined : 4997,
            period: billingPeriod === 'monthly' ? '/mês' : '/mês (anual)',
            description: 'Para escritórios que precisam de tudo + customização',
            icon: FaCrown,
            gradient: 'from-amber-600 to-orange-600',
            popular: false,
            features: [
                'Tudo do Professional, mais:',
                'Análise ilimitada de documentos',
                'Automação de processos',
                'Fluxos de trabalho customizados',
                'API completa',
                'Usuários ilimitados',
                'Suporte dedicado (WhatsApp)',
                'Onboarding personalizado',
                'Treinamento da equipe',
                'SLA garantido',
                'White-label (opcional)',
                'Consultoria mensal incluída'
            ],
            cta: 'Falar com Especialista'
        }
    ]

    const foundingMemberOffer = {
        discount: 60,
        slots: 100,
        slotsRemaining: 87,
        benefits: [
            'Preço vitalício garantido',
            'Acesso a todas as novas features',
            'Suporte prioritário para sempre',
            'Consultoria inicial gratuita (R$ 5.000)',
            'Treinamento personalizado',
            'Badge exclusivo "Membro Fundador"'
        ]
    }

    const handleWhatsAppClick = (message: string) => {
        const text = encodeURIComponent(message)
        window.open(`https://wa.me/5534999788335?text=${text}`, '_blank')
    }

    return (
        <section id="pricing" className="py-20 px-4 bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="text-center mb-16">
                    <h2 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                        Escolha Seu Plano
                    </h2>
                    <p className="text-xl text-gray-300 max-w-3xl mx-auto mb-8">
                        Transforme sua prática jurídica com IA de ponta. Comece com 14 dias grátis.
                    </p>

                    {/* Billing Toggle */}
                    <div className="inline-flex items-center gap-4 bg-slate-800/50 backdrop-blur-sm rounded-full p-2 border border-slate-700">
                        <button
                            onClick={() => setBillingPeriod('monthly')}
                            className={`px-6 py-2 rounded-full font-semibold transition-all ${billingPeriod === 'monthly'
                                ? 'bg-gradient-to-r from-blue-600 to-cyan-600 text-white'
                                : 'text-gray-400 hover:text-white'
                                }`}
                        >
                            Mensal
                        </button>
                        <button
                            onClick={() => setBillingPeriod('annual')}
                            className={`px-6 py-2 rounded-full font-semibold transition-all ${billingPeriod === 'annual'
                                ? 'bg-gradient-to-r from-blue-600 to-cyan-600 text-white'
                                : 'text-gray-400 hover:text-white'
                                }`}
                        >
                            Anual
                            <span className="ml-2 text-xs bg-green-500 text-white px-2 py-1 rounded-full">
                                Economize 10%
                            </span>
                        </button>
                    </div>
                </div>

                {/* Founding Member Banner */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                    className="mb-12 bg-gradient-to-r from-amber-600 via-orange-600 to-red-600 rounded-2xl p-8 border-2 border-amber-400 shadow-2xl shadow-amber-500/50 relative overflow-hidden"
                >
                    <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl"></div>
                    <div className="relative z-10">
                        <div className="flex items-center gap-3 mb-4">
                            <FaFire className="text-4xl text-white animate-pulse" />
                            <h3 className="text-3xl font-bold text-white">
                                🎉 Oferta Especial: Membros Fundadores
                            </h3>
                        </div>
                        <p className="text-xl text-white/90 mb-6">
                            Seja um dos primeiros <strong>{foundingMemberOffer.slots} clientes</strong> e ganhe <strong>{foundingMemberOffer.discount}% de desconto VITALÍCIO</strong> + bônus exclusivos!
                        </p>

                        <div className="grid md:grid-cols-2 gap-6 mb-6">
                            <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6">
                                <div className="text-5xl font-bold text-white mb-2">
                                    R$ 997<span className="text-2xl">/mês</span>
                                </div>
                                <div className="text-white/80 line-through text-xl mb-2">
                                    De R$ 2.497/mês
                                </div>
                                <div className="text-green-300 font-bold text-lg">
                                    Economia de R$ 18.000/ano
                                </div>
                            </div>

                            <div className="space-y-2">
                                {foundingMemberOffer.benefits.slice(0, 3).map((benefit, idx) => (
                                    <div key={idx} className="flex items-center gap-2 text-white">
                                        <FaCheck className="text-green-300 flex-shrink-0" />
                                        <span>{benefit}</span>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="flex items-center justify-between flex-wrap gap-4">
                            <div className="flex items-center gap-4">
                                <div className="text-white">
                                    <div className="text-sm opacity-80">Vagas Restantes:</div>
                                    <div className="text-2xl font-bold">
                                        {foundingMemberOffer.slotsRemaining}/{foundingMemberOffer.slots}
                                    </div>
                                </div>
                                <div className="w-48 h-3 bg-white/20 rounded-full overflow-hidden">
                                    <div
                                        className="h-full bg-gradient-to-r from-green-400 to-green-600 transition-all duration-500"
                                        style={{ width: `${(foundingMemberOffer.slotsRemaining / foundingMemberOffer.slots) * 100}%` }}
                                    ></div>
                                </div>
                            </div>

                            <button
                                onClick={() => handleWhatsAppClick('Olá! Quero garantir minha vaga como Membro Fundador do Kermartin por R$ 997/mês!')}
                                className="bg-white text-orange-600 px-8 py-4 rounded-lg font-bold text-lg hover:shadow-2xl transition-all hover:scale-105 inline-flex items-center gap-2"
                            >
                                <FaCrown />
                                Garantir Minha Vaga
                            </button>
                        </div>
                    </div>
                </motion.div>

                {/* Pricing Cards */}
                <div className="grid md:grid-cols-3 gap-8 mb-16">
                    {tiers.map((tier, index) => {
                        const Icon = tier.icon
                        return (
                            <motion.div
                                key={tier.id}
                                initial={{ opacity: 0, y: 20 }}
                                whileInView={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.1 + 0.3 }}
                                className={`relative bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border transition-all duration-300 hover:shadow-2xl ${tier.popular
                                    ? 'border-purple-500 shadow-xl shadow-purple-500/20 scale-105'
                                    : 'border-slate-700 hover:border-cyan-500/50'
                                    }`}
                            >
                                {/* Popular Badge */}
                                {tier.popular && (
                                    <div className="absolute -top-4 left-1/2 -translate-x-1/2 bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-2 rounded-full font-bold text-sm shadow-lg">
                                        ⭐ Mais Popular
                                    </div>
                                )}

                                {/* Icon & Name */}
                                <div className="flex items-center gap-3 mb-4">
                                    <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${tier.gradient} flex items-center justify-center text-white text-xl`}>
                                        <Icon />
                                    </div>
                                    <div>
                                        <h3 className="text-2xl font-bold text-white">{tier.name}</h3>
                                        <p className="text-sm text-cyan-400">{tier.tagline}</p>
                                    </div>
                                </div>

                                {/* Description */}
                                <p className="text-gray-300 mb-6 text-sm">{tier.description}</p>

                                {/* Price */}
                                <div className="mb-6">
                                    {tier.originalPrice && (
                                        <div className="text-gray-500 line-through text-lg mb-1">
                                            R$ {tier.originalPrice.toLocaleString('pt-BR')}
                                        </div>
                                    )}
                                    <div className="flex items-baseline gap-2">
                                        <span className="text-5xl font-bold text-white">
                                            R$ {tier.price.toLocaleString('pt-BR')}
                                        </span>
                                        <span className="text-gray-400">{tier.period}</span>
                                    </div>
                                    {billingPeriod === 'annual' && tier.originalPrice && (
                                        <div className="text-green-400 font-semibold mt-2">
                                            Economize R$ {((tier.originalPrice - tier.price) * 12).toLocaleString('pt-BR')}/ano
                                        </div>
                                    )}
                                </div>

                                {/* CTA */}
                                <button
                                    onClick={() => handleWhatsAppClick(`Olá! Tenho interesse no plano ${tier.name} do Kermartin.`)}
                                    className={`block w-full bg-gradient-to-r ${tier.gradient} text-white px-6 py-4 rounded-lg font-bold text-center hover:shadow-lg transition-all duration-300 hover:scale-105 mb-6`}
                                >
                                    {tier.cta}
                                </button>

                                {/* Features */}
                                <div className="space-y-3">
                                    <div className="text-sm font-bold text-white mb-3">Incluído:</div>
                                    {tier.features.map((feature, idx) => (
                                        <div key={idx} className="flex items-start gap-2 text-gray-300">
                                            <FaCheck className="text-green-400 text-sm mt-1 flex-shrink-0" />
                                            <span className="text-sm">{feature}</span>
                                        </div>
                                    ))}

                                    {tier.notIncluded && tier.notIncluded.length > 0 && (
                                        <>
                                            <div className="text-sm font-bold text-gray-500 mt-6 mb-3">Não incluído:</div>
                                            {tier.notIncluded.map((feature, idx) => (
                                                <div key={idx} className="flex items-start gap-2 text-gray-500">
                                                    <FaTimes className="text-gray-600 text-sm mt-1 flex-shrink-0" />
                                                    <span className="text-sm">{feature}</span>
                                                </div>
                                            ))}
                                        </>
                                    )}
                                </div>
                            </motion.div>
                        )
                    })}
                </div>

                {/* Trust Badges */}
                <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
                    <div className="text-center">
                        <div className="text-3xl mb-2">🔒</div>
                        <div className="text-sm text-gray-400">Pagamento Seguro</div>
                    </div>
                    <div className="text-center">
                        <div className="text-3xl mb-2">✅</div>
                        <div className="text-sm text-gray-400">14 Dias Grátis</div>
                    </div>
                    <div className="text-center">
                        <div className="text-3xl mb-2">🚫</div>
                        <div className="text-sm text-gray-400">Sem Cartão de Crédito</div>
                    </div>
                    <div className="text-center">
                        <div className="text-3xl mb-2">💯</div>
                        <div className="text-sm text-gray-400">Garantia 30 Dias</div>
                    </div>
                </div>
            </div>
        </section>
    )
}
