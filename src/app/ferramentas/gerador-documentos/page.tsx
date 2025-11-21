'use client'

import { useState, useRef } from 'react'
import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'
import SEOHead from '@/components/SEOHead'
import { FaPrint, FaPenFancy } from 'react-icons/fa'

export default function GeradorDocumentosPage() {
    const [docType, setDocType] = useState('procuracao')
    const [formData, setFormData] = useState({
        outorgante_nome: '',
        outorgante_nacionalidade: '',
        outorgante_estado_civil: '',
        outorgante_profissao: '',
        outorgante_cpf: '',
        outorgante_rg: '',
        outorgante_endereco: '',
        outorgado_nome: '',
        outorgado_oab: '',
        outorgado_endereco: '',
        cidade: '',
        data: new Date().toISOString().split('T')[0]
    })

    const printRef = useRef<HTMLDivElement>(null)

    const handlePrint = () => {
        const content = printRef.current
        if (!content) return

        const printWindow = window.open('', '', 'height=600,width=800')
        if (!printWindow) return

        printWindow.document.write('<html><head><title>Documento Jurídico</title>')
        printWindow.document.write('<style>')
        printWindow.document.write(`
      body { font-family: 'Times New Roman', serif; padding: 40px; line-height: 1.6; color: #000; }
      h1 { text-align: center; text-transform: uppercase; font-size: 18px; margin-bottom: 40px; }
      p { margin-bottom: 15px; text-align: justify; }
      .signature { margin-top: 60px; text-align: center; border-top: 1px solid #000; width: 60%; margin-left: auto; margin-right: auto; padding-top: 10px; }
      .date { text-align: right; margin-top: 40px; margin-bottom: 40px; }
    `)
        printWindow.document.write('</style></head><body>')
        printWindow.document.write(content.innerHTML)
        printWindow.document.write('</body></html>')
        printWindow.document.close()
        printWindow.print()
    }

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value })
    }

    return (
        <>
            <SEOHead
                title="Gerador de Documentos Jurídicos - Genesys Tecnologia"
                description="Gere procurações, declarações e recibos jurídicos automaticamente. Ferramenta gratuita."
                keywords="gerador procuração, modelo procuração, recibo honorários, declaração hipossuficiência"
                canonical="https://genesys-tecnologia.com.br/ferramentas/gerador-documentos"
            />
            <div className="min-h-screen bg-slate-950 text-gray-300 print:bg-white print:text-black">
                <div className="print:hidden">
                    <PremiumHeader />
                </div>

                <main className="pt-32 pb-20 px-4 print:p-0">
                    <div className="max-w-6xl mx-auto grid lg:grid-cols-2 gap-12">

                        {/* Form Section (Hidden on Print) */}
                        <div className="print:hidden space-y-8">
                            <div>
                                <h1 className="text-3xl font-bold text-white mb-4 flex items-center gap-3">
                                    <FaPenFancy className="text-purple-500" />
                                    Gerador de Documentos
                                </h1>
                                <p className="text-gray-400">
                                    Preencha os dados e gere seu documento instantaneamente.
                                </p>
                            </div>

                            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
                                <label className="block text-sm font-medium text-gray-300 mb-2">Tipo de Documento</label>
                                <select
                                    value={docType}
                                    onChange={(e) => setDocType(e.target.value)}
                                    className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white focus:ring-2 focus:ring-purple-500 outline-none"
                                >
                                    <option value="procuracao">Procuração Ad Judicia</option>
                                    <option value="declaracao">Declaração de Hipossuficiência</option>
                                    <option value="recibo">Recibo de Honorários</option>
                                </select>
                            </div>

                            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
                                <h3 className="text-white font-semibold border-b border-slate-700 pb-2">Dados do Cliente (Outorgante)</h3>
                                <div className="grid grid-cols-2 gap-4">
                                    <input name="outorgante_nome" placeholder="Nome Completo" onChange={handleChange} className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white w-full" />
                                    <input name="outorgante_cpf" placeholder="CPF" onChange={handleChange} className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white w-full" />
                                    <input name="outorgante_nacionalidade" placeholder="Nacionalidade" onChange={handleChange} className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white w-full" />
                                    <input name="outorgante_estado_civil" placeholder="Estado Civil" onChange={handleChange} className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white w-full" />
                                    <input name="outorgante_profissao" placeholder="Profissão" onChange={handleChange} className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white w-full" />
                                    <input name="outorgante_rg" placeholder="RG" onChange={handleChange} className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white w-full" />
                                </div>
                                <input name="outorgante_endereco" placeholder="Endereço Completo" onChange={handleChange} className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white w-full" />
                            </div>

                            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
                                <h3 className="text-white font-semibold border-b border-slate-700 pb-2">Dados do Advogado (Outorgado)</h3>
                                <div className="grid grid-cols-2 gap-4">
                                    <input name="outorgado_nome" placeholder="Nome do Advogado" onChange={handleChange} className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white w-full" />
                                    <input name="outorgado_oab" placeholder="Número da OAB" onChange={handleChange} className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white w-full" />
                                </div>
                                <input name="outorgado_endereco" placeholder="Endereço do Escritório" onChange={handleChange} className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white w-full" />
                            </div>

                            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
                                <h3 className="text-white font-semibold border-b border-slate-700 pb-2">Local e Data</h3>
                                <div className="grid grid-cols-2 gap-4">
                                    <input name="cidade" placeholder="Cidade" onChange={handleChange} className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white w-full" />
                                    <input type="date" name="data" value={formData.data} onChange={handleChange} className="bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-white w-full" />
                                </div>
                            </div>

                            <button
                                onClick={handlePrint}
                                className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold py-4 rounded-lg hover:shadow-lg hover:shadow-purple-500/30 transition-all flex items-center justify-center gap-2"
                            >
                                <FaPrint />
                                Imprimir / Salvar PDF
                            </button>
                        </div>

                        {/* Preview Section */}
                        <div className="bg-white text-black p-12 rounded-xl shadow-2xl min-h-[800px] relative">
                            <div className="absolute top-4 right-4 text-xs text-gray-400 font-mono print:hidden">Preview A4</div>

                            <div ref={printRef} className="prose max-w-none font-serif">
                                {docType === 'procuracao' && (
                                    <>
                                        <h1 className="text-center font-bold uppercase text-xl mb-8">Procuração Ad Judicia</h1>
                                        <p className="text-justify mb-4">
                                            <strong>OUTORGANTE:</strong> {formData.outorgante_nome || '[NOME DO CLIENTE]'}, {formData.outorgante_nacionalidade || '[NACIONALIDADE]'}, {formData.outorgante_estado_civil || '[ESTADO CIVIL]'}, {formData.outorgante_profissao || '[PROFISSÃO]'}, portador(a) do RG nº {formData.outorgante_rg || '[RG]'} e inscrito(a) no CPF sob o nº {formData.outorgante_cpf || '[CPF]'}, residente e domiciliado(a) na {formData.outorgante_endereco || '[ENDEREÇO COMPLETO]'}.
                                        </p>
                                        <p className="text-justify mb-4">
                                            <strong>OUTORGADO:</strong> {formData.outorgado_nome || '[NOME DO ADVOGADO]'}, advogado(a) inscrito(a) na OAB sob o nº {formData.outorgado_oab || '[OAB]'}, com escritório profissional situado na {formData.outorgado_endereco || '[ENDEREÇO DO ESCRITÓRIO]'}, onde recebe intimações e notificações.
                                        </p>
                                        <p className="text-justify mb-4">
                                            <strong>PODERES:</strong> Pelo presente instrumento particular de mandato, o(a) OUTORGANTE confere ao(à) OUTORGADO amplos poderes para o foro em geral, com a cláusula &quot;ad judicia et extra&quot;, em qualquer Juízo, Instância ou Tribunal, podendo propor contra quem de direito, as ações competentes e defendê-lo(a) nas contrárias, seguindo umas e outras, até final decisão, usando os recursos legais e acompanhando-os, conferindo-lhe ainda, poderes especiais para receber citação, confessar, reconhecer a procedência do pedido, transigir, desistir, renunciar ao direito sobre o qual se funda a ação, receber, dar quitação, firmar compromisso e assinar declaração de hipossuficiência econômica, substabelecer esta a outrem, com ou sem reservas de iguais poderes, para agir em conjunto ou separadamente com o substabelecido.
                                        </p>
                                        <div className="mt-12 text-right">
                                            {formData.cidade || '[CIDADE]'}, {new Date(formData.data).toLocaleDateString('pt-BR', { day: 'numeric', month: 'long', year: 'numeric' })}.
                                        </div>
                                        <div className="mt-20 border-t border-black w-2/3 mx-auto pt-2 text-center">
                                            {formData.outorgante_nome || '[NOME DO CLIENTE]'}
                                        </div>
                                    </>
                                )}

                                {docType === 'declaracao' && (
                                    <>
                                        <h1 className="text-center font-bold uppercase text-xl mb-8">Declaração de Hipossuficiência</h1>
                                        <p className="text-justify mb-4">
                                            Eu, <strong>{formData.outorgante_nome || '[NOME DO CLIENTE]'}</strong>, {formData.outorgante_nacionalidade || '[NACIONALIDADE]'}, {formData.outorgante_estado_civil || '[ESTADO CIVIL]'}, {formData.outorgante_profissao || '[PROFISSÃO]'}, portador(a) do RG nº {formData.outorgante_rg || '[RG]'} e inscrito(a) no CPF sob o nº {formData.outorgante_cpf || '[CPF]'}, residente e domiciliado(a) na {formData.outorgante_endereco || '[ENDEREÇO COMPLETO]'},
                                        </p>
                                        <p className="text-justify mb-4">
                                            <strong>DECLARO</strong>, para os devidos fins de direito e sob as penas da lei, que não possuo condições financeiras de arcar com as custas processuais e honorários advocatícios sem prejuízo do meu próprio sustento e de minha família.
                                        </p>
                                        <p className="text-justify mb-4">
                                            Por ser expressão da verdade, firmo a presente declaração para que produza seus efeitos legais, requerendo, desde já, a concessão dos benefícios da Justiça Gratuita, nos termos do art. 98 e seguintes do Código de Processo Civil e da Lei nº 1.060/50.
                                        </p>
                                        <div className="mt-12 text-right">
                                            {formData.cidade || '[CIDADE]'}, {new Date(formData.data).toLocaleDateString('pt-BR', { day: 'numeric', month: 'long', year: 'numeric' })}.
                                        </div>
                                        <div className="mt-20 border-t border-black w-2/3 mx-auto pt-2 text-center">
                                            {formData.outorgante_nome || '[NOME DO CLIENTE]'}
                                        </div>
                                    </>
                                )}

                                {docType === 'recibo' && (
                                    <>
                                        <h1 className="text-center font-bold uppercase text-xl mb-8">Recibo de Honorários</h1>
                                        <p className="text-justify mb-4">
                                            Recebi de <strong>{formData.outorgante_nome || '[NOME DO CLIENTE]'}</strong>, inscrito(a) no CPF sob o nº {formData.outorgante_cpf || '[CPF]'}, a importância de R$ _________ (_______________________), referente a honorários advocatícios pelos serviços prestados no processo/caso: __________________________________________________.
                                        </p>
                                        <p className="text-justify mb-4">
                                            Pelo que firmo o presente recibo, dando plena, rasa e geral quitação da quantia recebida.
                                        </p>
                                        <div className="mt-12 text-right">
                                            {formData.cidade || '[CIDADE]'}, {new Date(formData.data).toLocaleDateString('pt-BR', { day: 'numeric', month: 'long', year: 'numeric' })}.
                                        </div>
                                        <div className="mt-20 border-t border-black w-2/3 mx-auto pt-2 text-center">
                                            {formData.outorgado_nome || '[NOME DO ADVOGADO]'}
                                            <br />
                                            OAB {formData.outorgado_oab || '[OAB]'}
                                        </div>
                                    </>
                                )}
                            </div>
                        </div>
                    </div>
                </main>

                <div className="print:hidden">
                    <Footer />
                </div>
            </div>
        </>
    )
}
