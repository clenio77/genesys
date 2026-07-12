'use client'

import { FaShieldAlt, FaUserCheck, FaLock, FaFileContract, FaSearch, FaArrowRight, FaExclamationTriangle } from 'react-icons/fa'
import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'
import SEOHead from '@/components/SEOHead'
import { motion } from 'framer-motion'

export default function ComplianceLGPDPage() {
    const features = [
        {
            icon: FaSearch,
            title: 'Monitoramento 24/7',
            description: 'Vigilância contínua de dados e processos para garantir conformidade total',
            gradient: 'from-rose-600 to-red-600'
        },
        {
            icon: FaFileContract,
            title: 'Auditoria Automática',
            description: 'Relatórios detalhados de conformidade gerados automaticamente pela IA',
            gradient: 'from-red-600 to-orange-600'
        },
        {
            icon: FaExclamationTriangle,
            title: 'Alertas de Risco',
            description: 'Identificação proativa de vulnerabilidades e riscos de não-conformidade',
            gradient: 'from-orange-600 to-amber-600'
        },
        {
            icon: FaLock,
            title: 'Segurança Avançada',
            description: 'Criptografia de ponta a ponta e controle de acesso rigoroso',
            gradient: 'from-amber-600 to-yellow-600'
        }
    ]

    const benefits = [
        '100% de conformidade com LGPD',
        'Monitoramento em tempo real',
        'Redução de 80% em riscos',
        'Relatórios automáticos para DPO',
        'Mapeamento de dados pessoais',
        'Gestão de consentimento',
        'Anonimização automática',
        'Trilha de auditoria completa'
    ]

    const solutions = [
        {
            title: 'Mapeamento de Dados',
            description: 'Identifique e classifique dados pessoais em toda sua base automaticamente',
            icon: '🗺️',
            status: 'Automático'
        },
        {
            title: 'Gestão de Cookies',
            description: 'Controle de consentimento e cookies em conformidade com a lei',
            icon: '🍪',
            status: 'Integrado'
        },
        {
            title: 'Relatórios DPO',
            description: 'Geração automática de relatórios de impacto e conformidade',
            icon: '📋',
            status: 'Mensal'
        },
        {
            title: 'Prevenção de Vazamentos',
            description: 'Monitoramento ativo para evitar incidentes de segurança',
            icon: '🛡️',
            status: '24/7'
        }
    ]

    const stats = [
        { value: '100%', label: 'Conformidade', icon: '✅' },
        { value: '24/7', label: 'Monitoramento', icon: '👁️' },
        { value: '-80%', label: 'Riscos', icon: '📉' },
        { value: 'Zero', label: 'Multas', icon: '💰' }
    ]

    return (
        <>
            <SEOHead
                title="Governança, Compliance e LGPD - Genesys | Kermartin IA"
                description="Serviço complementar Genesys: anonimização, políticas de uso, RIPD e auditoria para operação segura do Kermartin IA."
                keywords="LGPD, compliance jurídico, proteção de dados, segurança da informação, DPO as a service"
                canonical="https://genesys-tecnologia.com.br/servicos/compliance-lgpd"
            />
            <div className="min-h-screen bg-gradient-to-b from-slate-900 via-slate-800 to-slate-900">
                <PremiumHeader />

                {/* Hero Section */}
                <section className="pt-32 pb-20 px-4">
                    <div className="max-w-7xl mx-auto">
                        <div className="grid lg:grid-cols-2 gap-12 items-center">
                            <motion.div
                                initial={{ opacity: 0, x: -50 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ duration: 0.6 }}
                            >
                                <div className="inline-flex items-center gap-2 px-4 py-2 bg-rose-500/10 border border-rose-500/30 rounded-full mb-6">
                                    <FaShieldAlt className="text-rose-400" />
                                    <span className="text-rose-300 text-sm font-medium">Segurança Jurídica</span>
                                </div>

                                <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-rose-400 via-red-400 to-rose-400 bg-clip-text text-transparent">
                                    Compliance e LGPD
                                </h1>

                                <p className="text-xl text-gray-300 mb-8 leading-relaxed">
                                    Serviço complementar da Genesys: governança de uso do Kermartin com anonimização,
                                    validação de entrada, controle de acesso e documentação LGPD para auditoria.
                                </p>

                                <div className="grid grid-cols-2 gap-4 mb-8">
                                    {stats.map((stat, idx) => (
                                        <div key={idx} className="bg-slate-800/50 rounded-lg p-4 text-center border border-slate-700">
                                            <div className="text-2xl mb-1">{stat.icon}</div>
                                            <div className="text-2xl font-bold text-rose-400">{stat.value}</div>
                                            <div className="text-xs text-gray-400 mt-1">{stat.label}</div>
                                        </div>
                                    ))}
                                </div>

                                <div className="flex flex-wrap gap-4">
                                    <button
                                        onClick={() => window.open('https://wa.me/5534998264603?text=Olá! Gostaria de conhecer a solução de Compliance e LGPD.', '_blank')}
                                        className="px-8 py-4 bg-gradient-to-r from-rose-600 to-red-600 text-white rounded-lg font-semibold hover:shadow-xl hover:shadow-rose-500/50 transition-all hover:scale-105 flex items-center gap-2"
                                    >
                                        Solicitar Diagnóstico
                                        <FaArrowRight />
                                    </button>
                                    <button
                                        onClick={() => window.open('https://wa.me/5534998264603?text=Olá! Gostaria de saber mais sobre preços de Compliance.', '_blank')}
                                        className="px-8 py-4 bg-slate-800 text-white rounded-lg font-semibold border border-slate-700 hover:border-rose-500/50 transition-all hover:scale-105"
                                    >
                                        Ver Planos
                                    </button>
                                </div>
                            </motion.div>

                            <motion.div
                                initial={{ opacity: 0, x: 50 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ duration: 0.6, delay: 0.2 }}
                                className="relative"
                            >
                                <div className="bg-gradient-to-br from-rose-600/20 to-red-600/20 rounded-3xl p-8 border border-rose-500/30 backdrop-blur-sm">
                                    <div className="space-y-4">
                                        {benefits.slice(0, 6).map((benefit, idx) => (
                                            <motion.div
                                                key={idx}
                                                initial={{ opacity: 0, x: 20 }}
                                                animate={{ opacity: 1, x: 0 }}
                                                transition={{ delay: 0.3 + idx * 0.1 }}
                                                className="flex items-center gap-3 text-gray-200"
                                            >
                                                <FaUserCheck className="text-green-400 flex-shrink-0" />
                                                <span>{benefit}</span>
                                            </motion.div>
                                        ))}
                                    </div>
                                </div>
                            </motion.div>
                        </div>
                    </div>
                </section>

                {/* Features Section */}
                <section className="py-20 px-4 bg-slate-900/50">
                    <div className="max-w-7xl mx-auto">
                        <div className="text-center mb-16">
                            <h2 className="text-4xl md:text-5xl font-bold mb-4 text-white">
                                Proteção Completa
                            </h2>
                            <p className="text-xl text-gray-400">
                                Tecnologia avançada para garantir sua segurança jurídica
                            </p>
                        </div>

                        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
                            {features.map((feature, idx) => (
                                <motion.div
                                    key={idx}
                                    initial={{ opacity: 0, y: 20 }}
                                    whileInView={{ opacity: 1, y: 0 }}
                                    viewport={{ once: true }}
                                    transition={{ delay: idx * 0.1 }}
                                    className="bg-slate-800/50 rounded-2xl p-6 border border-slate-700 hover:border-rose-500/50 transition-all hover:shadow-xl hover:shadow-rose-500/20"
                                >
                                    <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${feature.gradient} flex items-center justify-center mb-4`}>
                                        <feature.icon className="text-2xl text-white" />
                                    </div>
                                    <h3 className="text-xl font-bold text-white mb-2">{feature.title}</h3>
                                    <p className="text-gray-400">{feature.description}</p>
                                </motion.div>
                            ))}
                        </div>
                    </div>
                </section>

                {/* Solutions Section */}
                <section className="py-20 px-4">
                    <div className="max-w-7xl mx-auto">
                        <div className="text-center mb-16">
                            <h2 className="text-4xl md:text-5xl font-bold mb-4 text-white">
                                O Que Entregamos
                            </h2>
                            <p className="text-xl text-gray-400">
                                Soluções práticas para adequação imediata
                            </p>
                        </div>

                        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                            {solutions.map((solution, idx) => (
                                <motion.div
                                    key={idx}
                                    initial={{ opacity: 0, scale: 0.9 }}
                                    whileInView={{ opacity: 1, scale: 1 }}
                                    viewport={{ once: true }}
                                    transition={{ delay: idx * 0.1 }}
                                    className="bg-slate-800/50 rounded-xl p-6 border border-slate-700 hover:border-rose-500/50 transition-all"
                                >
                                    <div className="text-5xl mb-4 text-center">{solution.icon}</div>
                                    <h3 className="text-lg font-bold text-white mb-2 text-center">{solution.title}</h3>
                                    <p className="text-sm text-gray-400 mb-4 text-center">{solution.description}</p>
                                    <div className="bg-rose-500/10 border border-rose-500/30 rounded-lg p-2 text-center">
                                        <span className="text-rose-400 font-semibold text-sm">{solution.status}</span>
                                    </div>
                                </motion.div>
                            ))}
                        </div>
                    </div>
                </section>

                {/* CTA Section */}
                <section className="py-20 px-4">
                    <div className="max-w-4xl mx-auto">
                        <div className="bg-gradient-to-r from-rose-600 to-red-600 rounded-3xl p-12 text-center">
                            <h2 className="text-4xl font-bold text-white mb-4">
                                Evite multas e proteja sua reputação
                            </h2>
                            <p className="text-xl text-rose-100 mb-8">
                                Faça um diagnóstico gratuito de conformidade agora mesmo
                            </p>
                            <button
                                onClick={() => window.open('https://wa.me/5534998264603?text=Olá! Gostaria de agendar um diagnóstico de Compliance.', '_blank')}
                                className="bg-white text-rose-600 px-8 py-4 rounded-lg font-bold hover:shadow-xl transition-all hover:scale-105 inline-flex items-center gap-2"
                            >
                                Agendar Diagnóstico Gratuito
                                <FaArrowRight />
                            </button>
                        </div>
                    </div>
                </section>

                <Footer />
            </div>
        </>
    )
}
