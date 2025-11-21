'use client'

import { useState } from 'react'
import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'
import SEOHead from '@/components/SEOHead'
import { FaCheckCircle, FaTimesCircle, FaSearch, FaBuilding } from 'react-icons/fa'

export default function ValidadorCNJPage() {
    const [cnj, setCnj] = useState('')
    const [result, setResult] = useState<{ valid: boolean; details?: any } | null>(null)

    const formatCNJ = (value: string) => {
        // Remove tudo que não é número
        const numbers = value.replace(/\D/g, '')

        // Aplica máscara NNNNNNN-DD.AAAA.J.TR.OOOO
        // Ex: 5001234-12.2024.8.13.0024
        let formatted = numbers
        if (numbers.length > 7) formatted = numbers.slice(0, 7) + '-' + numbers.slice(7)
        if (numbers.length > 9) formatted = formatted.slice(0, 10) + '.' + formatted.slice(10)
        if (numbers.length > 13) formatted = formatted.slice(0, 15) + '.' + formatted.slice(15)
        if (numbers.length > 14) formatted = formatted.slice(0, 17) + '.' + formatted.slice(17)
        if (numbers.length > 16) formatted = formatted.slice(0, 20) + '.' + formatted.slice(20)

        return formatted.slice(0, 25)
    }

    const getOrgao = (j: string) => {
        const orgaos: { [key: string]: string } = {
            '1': 'Supremo Tribunal Federal',
            '2': 'Conselho Nacional de Justiça',
            '3': 'Superior Tribunal de Justiça',
            '4': 'Justiça Federal',
            '5': 'Justiça do Trabalho',
            '6': 'Justiça Eleitoral',
            '7': 'Justiça Militar da União',
            '8': 'Justiça dos Estados e do DF',
            '9': 'Justiça Militar Estadual'
        }
        return orgaos[j] || 'Órgão Desconhecido'
    }

    const validateCNJ = () => {
        const cleanCNJ = cnj.replace(/\D/g, '')

        if (cleanCNJ.length !== 20) {
            setResult({ valid: false, details: { error: 'Número deve ter 20 dígitos' } })
            return
        }

        // Formato: NNNNNNN-DD.AAAA.J.TR.OOOO
        // N = Sequencial (7)
        // D = Dígito Verificador (2)
        // A = Ano (4)
        // J = Órgão (1)
        // T = Tribunal (2)
        // O = Unidade de Origem (4)

        const sequencial = cleanCNJ.slice(0, 7)
        const digito = cleanCNJ.slice(7, 9)
        const ano = cleanCNJ.slice(9, 13)
        const orgao = cleanCNJ.slice(13, 14)
        const tribunal = cleanCNJ.slice(14, 16)
        const origem = cleanCNJ.slice(16, 20)

        // Algoritmo Módulo 97
        // R1 = (NNNNNNN % 97)
        // R2 = ((R1 . AAAA . J . TR) % 97)
        // R3 = ((R2 . OOOO . 00) % 97)
        // DV = 98 - (R3 % 97)

        const num1 = sequencial
        const num2 = ano + orgao + tribunal
        const num3 = origem + '00'

        const r1 = BigInt(num1) % BigInt(97)
        const r2 = BigInt(r1.toString() + num2) % BigInt(97)
        const r3 = BigInt(r2.toString() + num3) % BigInt(97)

        const calculatedDigit = BigInt(98) - r3

        const isValid = calculatedDigit === BigInt(digito)

        if (isValid) {
            setResult({
                valid: true,
                details: {
                    sequencial,
                    digito,
                    ano,
                    orgao: getOrgao(orgao),
                    tribunal: `Tribunal ${tribunal}`,
                    origem
                }
            })
        } else {
            setResult({ valid: false, details: { error: `Dígito inválido. Esperado: ${calculatedDigit.toString().padStart(2, '0')}` } })
        }
    }

    return (
        <>
            <SEOHead
                title="Validador de Processos CNJ - Genesys Tecnologia"
                description="Valide a numeração única de processos judiciais (CNJ). Identifique o tribunal e ano do processo."
                keywords="validador cnj, consulta processo, numeração única, tribunal de justiça"
                canonical="https://genesys-tecnologia.com.br/ferramentas/validador-cnj"
            />
            <div className="min-h-screen bg-slate-950 text-gray-300">
                <PremiumHeader />

                <main className="pt-32 pb-20 px-4">
                    <div className="max-w-2xl mx-auto">
                        <div className="text-center mb-10">
                            <div className="inline-flex p-4 rounded-full bg-emerald-600/20 mb-4">
                                <FaCheckCircle className="text-3xl text-emerald-500" />
                            </div>
                            <h1 className="text-3xl md:text-4xl font-bold text-white mb-4">
                                Validador CNJ
                            </h1>
                            <p className="text-gray-400">
                                Verifique se a numeração do processo é válida.
                            </p>
                        </div>

                        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-xl">
                            <div className="space-y-6">
                                <div>
                                    <label className="block text-sm font-medium text-gray-300 mb-2">
                                        Número do Processo
                                    </label>
                                    <div className="relative">
                                        <input
                                            type="text"
                                            value={cnj}
                                            onChange={(e) => setCnj(formatCNJ(e.target.value))}
                                            placeholder="0000000-00.0000.0.00.0000"
                                            className="w-full bg-slate-800 border border-slate-700 rounded-lg pl-12 pr-4 py-4 text-xl text-white font-mono tracking-wider focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all"
                                        />
                                        <FaSearch className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500" />
                                    </div>
                                    <p className="text-xs text-gray-500 mt-2">
                                        Digite apenas os números. A formatação é automática.
                                    </p>
                                </div>

                                <button
                                    onClick={validateCNJ}
                                    className="w-full bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold py-4 rounded-lg hover:shadow-lg hover:shadow-emerald-500/30 transition-all transform hover:scale-[1.02]"
                                >
                                    Validar Processo
                                </button>
                            </div>

                            {result && (
                                <div className={`mt-8 p-6 rounded-xl border animate-fade-in ${result.valid ? 'bg-emerald-900/20 border-emerald-500/30' : 'bg-red-900/20 border-red-500/30'}`}>
                                    <div className="flex items-center gap-4 mb-4">
                                        {result.valid ? (
                                            <FaCheckCircle className="text-4xl text-emerald-500" />
                                        ) : (
                                            <FaTimesCircle className="text-4xl text-red-500" />
                                        )}
                                        <div>
                                            <h3 className={`text-xl font-bold ${result.valid ? 'text-emerald-400' : 'text-red-400'}`}>
                                                {result.valid ? 'Numeração Válida' : 'Numeração Inválida'}
                                            </h3>
                                            {!result.valid && (
                                                <p className="text-red-300 text-sm">{result.details.error}</p>
                                            )}
                                        </div>
                                    </div>

                                    {result.valid && (
                                        <div className="grid grid-cols-2 gap-4 mt-6 border-t border-emerald-500/20 pt-4">
                                            <div>
                                                <p className="text-xs text-gray-400 mb-1">Ano do Processo</p>
                                                <p className="text-lg font-semibold text-white">{result.details.ano}</p>
                                            </div>
                                            <div>
                                                <p className="text-xs text-gray-400 mb-1">Justiça</p>
                                                <p className="text-lg font-semibold text-white">{result.details.orgao}</p>
                                            </div>
                                            <div className="col-span-2">
                                                <p className="text-xs text-gray-400 mb-1">Detalhes da Origem</p>
                                                <div className="flex items-center gap-2 text-emerald-300">
                                                    <FaBuilding />
                                                    <span>Tribunal {result.details.tribunal.replace('Tribunal ', '')} / Vara {result.details.origem}</span>
                                                </div>
                                            </div>
                                        </div>
                                    )}
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
