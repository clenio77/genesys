'use client'

import { motion } from 'framer-motion'
import { FaCheck, FaRocket, FaShieldAlt, FaSearch } from 'react-icons/fa'

export default function PricingSection() {
    const plans = [
        {
            name: 'Kermartin START',
            price: '197',
            period: '/mês',
            description: 'Para Advogados Autônomos',
            features: [
                'Jurimetria Básica',
                'Pesquisa Semântica',
                'Análise de até 50 processos/mês',
                'Suporte por Email',
                'Acesso App Mobile'
            ],
            highlight: false,
            icon: FaSearch,
            gradient: 'from-blue-500 to-cyan-500',
            cta: 'Começar Agora'
        },
        {
            name: 'Kermartin PRO',
            price: '697',
            period: '/mês',
            description: 'Para Escritórios Médios',
            features: [
                'Tudo do plano START',
                'Radar de Oportunidades',
                'Calculadora de Sentenças',
                'Monitoramento Diário',
                'Suporte Prioritário',
                'API de Integração'
            ],
            highlight: true,
            icon: FaRocket,
            gradient: 'from-purple-600 to-pink-600',
            cta: 'Assinar PRO'
        },
        {
            name: 'Genesys Blindagem',
            price: '250',
            setup: '+ R$ 1.500 Setup',
            period: '/mês',
            description: 'Segurança e Compliance',
            features: [
                'Selo de Site Seguro',
                'Monitoramento 24/7',
                'Adequação LGPD',
                'Proteção Anti-DDoS',
                'Backup Automático',
                'Relatório Mensal de Riscos'
            ],
            highlight: false,
            icon: FaShieldAlt,
            gradient: 'from-emerald-500 to-teal-500',
            cta: 'Proteger Meu Escritório'
        }
    ]

    const handleWhatsAppClick = (message: string) => {
        const text = encodeURIComponent(message)
        window.open(`https://wa.me/5534999788335?text=${text}`, '_blank')
    }

    return (
        <section id="pricing" className="py-24 bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900 relative overflow-hidden">
            {/* Background Decoration */}
            <div className="absolute inset-0 opacity-10">
                <div className="absolute top-0 left-0 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl" />
                <div className="absolute bottom-0 right-0 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl" />
            </div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
                {/* Header */}
                <div className="text-center mb-16">
                    <h2 className="text-4xl md:text-5xl font-bold mb-6">
                        <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                            Planos e Preços
                        </span>
                    </h2>
                    <p className="text-xl text-gray-300 max-w-3xl mx-auto">
                        Escolha a solução ideal para o momento do seu escritório
                    </p>
                </div>

                {/* Pricing Grid */}
                <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
                    {plans.map((plan, index) => (
                        <motion.div
                            key={plan.name}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.1 }}
                            className={`relative rounded-2xl p-8 ${plan.highlight
                                    ? 'bg-slate-800/80 border-2 border-purple-500/50 shadow-2xl shadow-purple-500/20'
                                    : 'bg-slate-800/40 border border-slate-700'
                                } backdrop-blur-sm flex flex-col`}
                        >
                            {plan.highlight && (
                                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 bg-gradient-to-r from-purple-600 to-pink-600 text-white px-4 py-1 rounded-full text-sm font-bold shadow-lg">
                                    Mais Popular
                                </div>
                            )}

                            {/* Plan Header */}
                            <div className="text-center mb-8">
                                <div className={`w-16 h-16 mx-auto rounded-2xl bg-gradient-to-br ${plan.gradient} flex items-center justify-center mb-6 shadow-lg`}>
                                    <plan.icon className="text-3xl text-white" />
                                </div>
                                <h3 className="text-2xl font-bold text-white mb-2">{plan.name}</h3>
                                <p className="text-gray-400 text-sm mb-6">{plan.description}</p>
                                <div className="flex items-end justify-center gap-1">
                                    <span className="text-sm text-gray-400 mb-4">R$</span>
                                    <span className="text-5xl font-bold text-white">{plan.price}</span>
                                    <span className="text-gray-400 mb-4">{plan.period}</span>
                                </div>
                                {plan.setup && (
                                    <div className="text-sm text-emerald-400 font-medium mt-2">
                                        {plan.setup}
                                    </div>
                                )}
                            </div>

                            {/* Features */}
                            <div className="flex-grow space-y-4 mb-8">
                                {plan.features.map((feature, i) => (
                                    <div key={i} className="flex items-start gap-3">
                                        <div className={`mt-1 w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0 bg-gradient-to-br ${plan.gradient} opacity-80`}>
                                            <FaCheck className="text-[10px] text-white" />
                                        </div>
                                        <span className="text-gray-300 text-sm">{feature}</span>
                                    </div>
                                ))}
                            </div>

                            {/* CTA Button */}
                            <button
                                onClick={() => handleWhatsAppClick(`Olá! Tenho interesse no plano ${plan.name}.`)}
                                className={`w-full py-4 rounded-xl font-bold transition-all duration-300 ${plan.highlight
                                        ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white hover:shadow-lg hover:shadow-purple-500/25 hover:scale-105'
                                        : 'bg-slate-700 text-white hover:bg-slate-600 hover:scale-105'
                                    }`}>
                                {plan.cta}
                            </button>
                        </motion.div>
                    ))}
                </div>

                {/* Special Offer Banner */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 }}
                    className="mt-16 max-w-4xl mx-auto bg-gradient-to-r from-blue-900/50 to-purple-900/50 rounded-3xl p-8 md:p-12 border border-blue-500/30 relative overflow-hidden"
                >
                    <div className="absolute top-0 right-0 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />

                    <div className="relative z-10 flex flex-col md:flex-row items-center justify-between gap-8">
                        <div className="text-center md:text-left">
                            <div className="inline-block px-4 py-1 rounded-full bg-blue-500/20 text-blue-300 text-sm font-bold mb-4 border border-blue-500/30">
                                OFERTA LIMITADA
                            </div>
                            <h3 className="text-3xl font-bold text-white mb-2">Membro Fundador</h3>
                            <p className="text-gray-300 mb-4 max-w-md">
                                Acesso Vitalício ao Kermartin PRO + Manutenção de Segurança por um preço exclusivo para os 10 primeiros escritórios.
                            </p>
                            <div className="flex items-center gap-4 justify-center md:justify-start">
                                <span className="text-gray-500 line-through text-lg">R$ 897</span>
                                <span className="text-4xl font-bold text-white">R$ 297<span className="text-lg text-gray-400 font-normal">/mês</span></span>
                            </div>
                        </div>
                        <button
                            onClick={() => handleWhatsAppClick('Olá! Quero garantir uma das 10 vagas de Membro Fundador por R$ 297.')}
                            className="px-8 py-4 bg-white text-blue-900 rounded-xl font-bold hover:bg-blue-50 transition-all hover:scale-105 shadow-xl whitespace-nowrap">
                            Garantir Minha Vaga
                        </button>
                    </div>
                </motion.div>
            </div>
        </section>
    )
}
