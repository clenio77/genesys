'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { FaFileAlt, FaCheckCircle, FaClock, FaUserTie, FaGavel, FaWhatsapp, FaArrowLeft, FaSignOutAlt, FaArrowRight, FaSpinner } from 'react-icons/fa'
import { IconType } from 'react-icons'
import SEOHead from '@/components/SEOHead'

// Map icon strings to components
const ICON_MAP: { [key: string]: IconType } = {
    'gavel': FaGavel,
    'file': FaFileAlt,
    'check': FaCheckCircle,
    'clock': FaClock,
    'user': FaUserTie
}

interface TimelineEvent {
    date: string
    title: string
    description: string
    icon_type: string
    status: string
}

interface Processo {
    id: number
    cnj: string
    title: string
    status: string
    last_update: string
    next_step: string
    lawyer_name: string
    timeline: TimelineEvent[]
}

export default function PortalClientePage() {
    const [isLoggedIn, setIsLoggedIn] = useState(false)
    const [cpf, setCpf] = useState('')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')
    const [processes, setProcesses] = useState<Processo[]>([])
    const [selectedProcess, setSelectedProcess] = useState<Processo | null>(null)

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)
        setError('')

        try {
            const res = await fetch('http://localhost:8001/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ cpf })
            })

            if (!res.ok) throw new Error('CPF não encontrado')

            const data = await res.json()
            if (data.token) {
                setIsLoggedIn(true)
                fetchProcesses()
            }
        } catch {
            setError('CPF inválido ou não encontrado. Tente 123.456.789-00')
        } finally {
            setLoading(false)
        }
    }

    const fetchProcesses = async () => {
        try {
            const res = await fetch('http://localhost:8001/api/processos')
            const data = await res.json()

            // Format dates for display
            const formattedData = data.map((p: Processo) => ({
                ...p,
                last_update: new Date(p.last_update).toLocaleDateString('pt-BR'),
                timeline: p.timeline.map((t: TimelineEvent) => ({
                    ...t,
                    date: new Date(t.date).toLocaleDateString('pt-BR')
                }))
            }))
            setProcesses(formattedData)
        } catch (err) {
            console.error('Erro ao buscar processos', err)
            setError('Erro ao conectar com o servidor.')
        }
    }

    const formatCPF = (value: string) => {
        return value
            .replace(/\D/g, '')
            .replace(/(\d{3})(\d)/, '$1.$2')
            .replace(/(\d{3})(\d)/, '$1.$2')
            .replace(/(\d{3})(\d{1,2})/, '$1-$2')
            .replace(/(-\d{2})\d+?$/, '$1')
    }

    return (
        <>
            <SEOHead
                title="Portal do Cliente - Genesys Tecnologia"
                description="Acompanhe seus processos em tempo real, de forma simples e transparente."
                keywords="portal do cliente, acompanhamento processual, consulta processo, advocacia digital"
                canonical="https://genesys-tecnologia.com.br/portal-cliente"
            />

            <div className="min-h-screen bg-slate-50 text-slate-900 font-sans">
                {/* Header Simplificado para o Cliente */}
                <header className="bg-white shadow-sm sticky top-0 z-50">
                    <div className="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between">
                        <a href="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
                            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-bold">G</div>
                            <span className="font-bold text-xl text-slate-800">Portal do Cliente</span>
                        </a>
                        <div className="flex items-center gap-4">
                            {!isLoggedIn && (
                                <a
                                    href="/"
                                    className="text-slate-500 hover:text-blue-600 flex items-center gap-2 text-sm font-medium transition-colors"
                                >
                                    <FaArrowLeft /> Voltar ao Site
                                </a>
                            )}
                            {isLoggedIn && (
                                <button
                                    onClick={() => { setIsLoggedIn(false); setSelectedProcess(null); setCpf(''); }}
                                    className="text-slate-500 hover:text-red-600 flex items-center gap-2 text-sm font-medium transition-colors"
                                >
                                    <FaSignOutAlt /> Sair
                                </button>
                            )}
                        </div>
                    </div>
                </header>

                <main className="max-w-5xl mx-auto px-4 py-8">
                    <AnimatePresence mode="wait">
                        {!isLoggedIn ? (
                            /* TELA DE LOGIN */
                            <motion.div
                                key="login"
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -20 }}
                                className="max-w-md mx-auto mt-20"
                            >
                                <div className="bg-white p-8 rounded-2xl shadow-xl border border-slate-100">
                                    <div className="text-center mb-8">
                                        <h1 className="text-2xl font-bold text-slate-800 mb-2">Bem-vindo</h1>
                                        <p className="text-slate-500">Digite seu CPF para consultar seus processos</p>
                                    </div>

                                    <form onSubmit={handleLogin} className="space-y-6">
                                        <div>
                                            <label className="block text-sm font-medium text-slate-700 mb-2">CPF</label>
                                            <input
                                                type="text"
                                                value={cpf}
                                                onChange={(e) => setCpf(formatCPF(e.target.value))}
                                                placeholder="000.000.000-00"
                                                className="w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all text-lg"
                                                maxLength={14}
                                                disabled={loading}
                                            />
                                        </div>

                                        {error && (
                                            <div className="p-3 bg-red-50 text-red-600 text-sm rounded-lg border border-red-100">
                                                {error}
                                            </div>
                                        )}

                                        <button
                                            type="submit"
                                            disabled={loading}
                                            className="w-full bg-blue-600 text-white font-bold py-3 rounded-lg hover:bg-blue-700 transition-colors shadow-lg shadow-blue-500/30 disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center"
                                        >
                                            {loading ? <FaSpinner className="animate-spin" /> : 'Acessar Processos'}
                                        </button>
                                    </form>

                                    <div className="mt-6 text-center">
                                        <p className="text-xs text-slate-400">
                                            Ambiente Seguro • Criptografia de Ponta a Ponta
                                        </p>
                                    </div>
                                </div>
                            </motion.div>
                        ) : !selectedProcess ? (
                            /* LISTA DE PROCESSOS */
                            <motion.div
                                key="list"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                            >
                                <h2 className="text-2xl font-bold text-slate-800 mb-6">Seus Processos</h2>
                                <div className="grid gap-4">
                                    {processes.map((processo) => (
                                        <div
                                            key={processo.id}
                                            onClick={() => setSelectedProcess(processo)}
                                            className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 hover:shadow-md hover:border-blue-300 transition-all cursor-pointer group"
                                        >
                                            <div className="flex justify-between items-start mb-4">
                                                <div>
                                                    <span className="inline-block px-3 py-1 rounded-full bg-blue-100 text-blue-700 text-xs font-bold mb-2">
                                                        {processo.status}
                                                    </span>
                                                    <h3 className="text-lg font-bold text-slate-800 group-hover:text-blue-600 transition-colors">
                                                        {processo.title}
                                                    </h3>
                                                    <p className="text-sm text-slate-500 font-mono mt-1">{processo.cnj}</p>
                                                </div>
                                                <FaArrowRight className="text-slate-300 group-hover:text-blue-500 transition-colors" />
                                            </div>

                                            <div className="flex items-center gap-4 text-sm text-slate-600 border-t border-slate-100 pt-4">
                                                <div className="flex items-center gap-2">
                                                    <FaUserTie className="text-slate-400" />
                                                    {processo.lawyer_name}
                                                </div>
                                                <div className="flex items-center gap-2">
                                                    <FaClock className="text-slate-400" />
                                                    Última atualização: {processo.last_update}
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </motion.div>
                        ) : (
                            /* DETALHES DO PROCESSO */
                            <motion.div
                                key="details"
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: -20 }}
                            >
                                <button
                                    onClick={() => setSelectedProcess(null)}
                                    className="flex items-center gap-2 text-slate-500 hover:text-blue-600 mb-6 transition-colors"
                                >
                                    <FaArrowLeft /> Voltar para lista
                                </button>

                                <div className="grid lg:grid-cols-3 gap-8">
                                    {/* Coluna Principal - Timeline */}
                                    <div className="lg:col-span-2 space-y-8">
                                        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                                            <h1 className="text-2xl font-bold text-slate-800 mb-2">{selectedProcess.title}</h1>
                                            <p className="text-slate-500 font-mono mb-6">{selectedProcess.cnj}</p>

                                            <div className="relative pl-8 border-l-2 border-slate-200 space-y-8">
                                                {selectedProcess.timeline.map((event, idx) => {
                                                    const IconComponent = ICON_MAP[event.icon_type] || FaCheckCircle
                                                    return (
                                                        <div key={idx} className="relative">
                                                            {/* Dot */}
                                                            <div className={`absolute -left-[41px] top-0 w-6 h-6 rounded-full border-4 border-white flex items-center justify-center ${event.status === 'current' ? 'bg-blue-600 shadow-lg shadow-blue-500/30' : 'bg-slate-300'
                                                                }`}>
                                                                {event.status === 'current' && <div className="w-2 h-2 bg-white rounded-full animate-pulse" />}
                                                            </div>

                                                            <div className={`p-4 rounded-lg border ${event.status === 'current' ? 'bg-blue-50 border-blue-200' : 'bg-slate-50 border-slate-100'
                                                                }`}>
                                                                <div className="flex justify-between items-start mb-2">
                                                                    <h4 className={`font-bold flex items-center gap-2 ${event.status === 'current' ? 'text-blue-800' : 'text-slate-700'}`}>
                                                                        <IconComponent />
                                                                        {event.title}
                                                                    </h4>
                                                                    <span className="text-xs font-medium text-slate-500 bg-white px-2 py-1 rounded">
                                                                        {event.date}
                                                                    </span>
                                                                </div>
                                                                <p className="text-sm text-slate-600">
                                                                    {event.description}
                                                                </p>
                                                            </div>
                                                        </div>
                                                    )
                                                })}
                                            </div>
                                        </div>
                                    </div>

                                    {/* Sidebar - Resumo e Contato */}
                                    <div className="space-y-6">
                                        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                                            <h3 className="font-bold text-slate-800 mb-4">Próximos Passos</h3>
                                            <div className="p-4 bg-amber-50 border border-amber-100 rounded-lg text-amber-800 text-sm">
                                                {selectedProcess.next_step}
                                            </div>
                                        </div>

                                        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
                                            <h3 className="font-bold text-slate-800 mb-4">Seu Advogado</h3>
                                            <div className="flex items-center gap-3 mb-4">
                                                <div className="w-12 h-12 bg-slate-200 rounded-full flex items-center justify-center text-slate-500">
                                                    <FaUserTie size={20} />
                                                </div>
                                                <div>
                                                    <p className="font-bold text-slate-800">{selectedProcess.lawyer_name}</p>
                                                    <p className="text-xs text-slate-500">OAB/MG 123.456</p>
                                                </div>
                                            </div>
                                            <button className="w-full bg-green-500 text-white font-bold py-3 rounded-lg hover:bg-green-600 transition-colors flex items-center justify-center gap-2 shadow-lg shadow-green-500/20">
                                                <FaWhatsapp size={20} />
                                                Falar no WhatsApp
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </main>
            </div>
        </>
    )
}
