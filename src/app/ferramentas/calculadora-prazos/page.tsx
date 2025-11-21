'use client'

import { useState } from 'react'
import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'
import SEOHead from '@/components/SEOHead'
import { FaCalendarAlt, FaCalculator, FaInfoCircle } from 'react-icons/fa'

export default function CalculadoraPrazosPage() {
    const [startDate, setStartDate] = useState('')
    const [days, setDays] = useState('')
    const [type, setType] = useState('uteis')
    const [result, setResult] = useState<string | null>(null)

    const calculateDeadline = () => {
        if (!startDate || !days) return

        const start = new Date(startDate)
        // Ajuste de fuso horário para garantir a data correta
        const userTimezoneOffset = start.getTimezoneOffset() * 60000
        const date = new Date(start.getTime() + userTimezoneOffset)

        let count = 0
        const totalDays = parseInt(days)

        // Adiciona 1 dia para começar a contagem no dia seguinte (regra processual padrão: exclui o dia do começo)
        date.setDate(date.getDate() + 1)

        while (count < totalDays) {
            if (type === 'uteis') {
                const dayOfWeek = date.getDay()
                // 0 = Domingo, 6 = Sábado
                if (dayOfWeek !== 0 && dayOfWeek !== 6) {
                    count++
                }
            } else {
                count++
            }

            if (count < totalDays) {
                date.setDate(date.getDate() + 1)
            }
        }

        // Se o dia final cair em fim de semana, prorroga para o próximo dia útil
        while (date.getDay() === 0 || date.getDay() === 6) {
            date.setDate(date.getDate() + 1)
        }

        setResult(date.toLocaleDateString('pt-BR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }))
    }

    return (
        <>
            <SEOHead
                title="Calculadora de Prazos Processuais - Genesys Tecnologia"
                description="Calcule prazos processuais (CPC/CPP) em dias úteis ou corridos. Ferramenta gratuita para advogados."
                keywords="calculadora prazos, contagem prazo processual, novo cpc, dias úteis"
                canonical="https://genesys-tecnologia.com.br/ferramentas/calculadora-prazos"
            />
            <div className="min-h-screen bg-slate-950 text-gray-300">
                <PremiumHeader />

                <main className="pt-32 pb-20 px-4">
                    <div className="max-w-2xl mx-auto">
                        <div className="text-center mb-10">
                            <div className="inline-flex p-4 rounded-full bg-blue-600/20 mb-4">
                                <FaCalendarAlt className="text-3xl text-blue-500" />
                            </div>
                            <h1 className="text-3xl md:text-4xl font-bold text-white mb-4">
                                Calculadora de Prazos
                            </h1>
                            <p className="text-gray-400">
                                Simule a data final do seu prazo processual.
                            </p>
                        </div>

                        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-xl">
                            <div className="space-y-6">
                                <div>
                                    <label className="block text-sm font-medium text-gray-300 mb-2">
                                        Data de Publicação/Intimação
                                    </label>
                                    <input
                                        type="date"
                                        value={startDate}
                                        onChange={(e) => setStartDate(e.target.value)}
                                        className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-medium text-gray-300 mb-2">
                                        Prazo em Dias
                                    </label>
                                    <input
                                        type="number"
                                        value={days}
                                        onChange={(e) => setDays(e.target.value)}
                                        placeholder="Ex: 15"
                                        className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-medium text-gray-300 mb-2">
                                        Tipo de Contagem
                                    </label>
                                    <div className="grid grid-cols-2 gap-4">
                                        <button
                                            onClick={() => setType('uteis')}
                                            className={`px-4 py-3 rounded-lg font-medium transition-all ${type === 'uteis'
                                                    ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/25'
                                                    : 'bg-slate-800 text-gray-400 hover:bg-slate-700'
                                                }`}
                                        >
                                            Dias Úteis (CPC)
                                        </button>
                                        <button
                                            onClick={() => setType('corridos')}
                                            className={`px-4 py-3 rounded-lg font-medium transition-all ${type === 'corridos'
                                                    ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/25'
                                                    : 'bg-slate-800 text-gray-400 hover:bg-slate-700'
                                                }`}
                                        >
                                            Dias Corridos
                                        </button>
                                    </div>
                                </div>

                                <button
                                    onClick={calculateDeadline}
                                    className="w-full bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-bold py-4 rounded-lg hover:shadow-lg hover:shadow-blue-500/30 transition-all transform hover:scale-[1.02] flex items-center justify-center gap-2"
                                >
                                    <FaCalculator />
                                    Calcular Prazo
                                </button>
                            </div>

                            {result && (
                                <div className="mt-8 p-6 bg-slate-800/50 rounded-xl border border-blue-500/30 animate-fade-in">
                                    <p className="text-sm text-gray-400 mb-1">Data Final do Prazo:</p>
                                    <p className="text-2xl font-bold text-white capitalize">{result}</p>
                                    <div className="mt-4 flex items-start gap-2 text-xs text-yellow-500 bg-yellow-500/10 p-3 rounded-lg">
                                        <FaInfoCircle className="mt-0.5 flex-shrink-0" />
                                        <p>
                                            Atenção: Esta calculadora considera apenas finais de semana.
                                            Feriados nacionais, estaduais ou municipais e suspensões de expediente
                                            devem ser verificados manualmente.
                                        </p>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                </main>

                <Footer />
            </div>
        </>
    )
}
