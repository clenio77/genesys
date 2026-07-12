'use client'

import { useState, useEffect, useRef } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { FaGraduationCap, FaChevronDown, FaArrowRight } from 'react-icons/fa'
import PremiumHeader from '@/components/PremiumHeader'
import Footer from '@/components/Footer'
import SEOHead from '@/components/SEOHead'

// ─── Animation Hook ───────────────────────────────────────
function useInView() {
  const ref = useRef<HTMLDivElement>(null)
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        setIsVisible(true)
        observer.unobserve(entry.target)
      }
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' })

    const current = ref.current
    if (current) observer.observe(current)
    return () => { if (current) observer.unobserve(current) }
  }, [])

  return { ref, isVisible }
}

// ─── Animated Section Component ───────────────────────────
function AnimatedSection({ children, className = '', delay = 0 }: { children: React.ReactNode, className?: string, delay?: number }) {
  const { ref, isVisible } = useInView()
  return (
    <div
      ref={ref}
      className={`transition-all duration-700 ease-out ${className}`}
      style={{
        opacity: isVisible ? 1 : 0,
        transform: isVisible ? 'translateY(0)' : 'translateY(30px)',
        transitionDelay: `${delay}ms`,
      }}
    >
      {children}
    </div>
  )
}

// ─── Counter Animation ────────────────────────────────────
function AnimatedCounter({ target, prefix = '', suffix = '' }: { target: number, prefix?: string, suffix?: string }) {
  const [count, setCount] = useState(0)
  const { ref, isVisible } = useInView()

  useEffect(() => {
    if (!isVisible) return
    let current = 0
    const step = Math.ceil(target / 40)
    const timer = setInterval(() => {
      current += step
      if (current >= target) {
        current = target
        clearInterval(timer)
      }
      setCount(current)
    }, 30)
    return () => clearInterval(timer)
  }, [isVisible, target])

  return <span ref={ref}>{prefix}{count}{suffix}</span>
}

// ─── FAQ Item Component ───────────────────────────────────
function FAQItem({ question, answer }: { question: string, answer: string }) {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div
      className={`border rounded-xl overflow-hidden transition-all duration-300 ${
        isOpen ? 'border-amber-500/30 bg-slate-800/50' : 'border-slate-700/50 bg-slate-800/30'
      }`}
    >
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-6 py-5 text-left flex justify-between items-center gap-4 hover:bg-slate-700/30 transition-colors"
      >
        <span className="font-semibold text-white">{question}</span>
        <FaChevronDown
          className={`text-amber-400 flex-shrink-0 transition-transform duration-300 ${
            isOpen ? 'rotate-180' : ''
          }`}
        />
      </button>
      <div
        className={`overflow-hidden transition-all duration-300 ${
          isOpen ? 'max-h-60 opacity-100' : 'max-h-0 opacity-0'
        }`}
      >
        <div className="px-6 pb-5 text-gray-300 leading-relaxed">
          {answer}
        </div>
      </div>
    </div>
  )
}

// ═══════════════════════════════════════════════════════════
// MAIN PAGE COMPONENT
// ═══════════════════════════════════════════════════════════
export default function CursoIACriminalPage() {
  const HOTMART_URL = 'https://hotmart.com/pt-br/marketplace/produtos/curso-avancado-de-ia-aplicado-a-lei-11-343/T105354363U'

  const painPoints = [
    {
      icon: '⚠️',
      title: 'Medo de Alucinação da IA',
      desc: 'Processual inventado, jurisprudência falsa, "citação" que não existe. Um erro assim destrói credibilidade e pode custar o caso do seu cliente.',
    },
    {
      icon: '📄',
      title: 'IA que Entrega Peça Rasa',
      desc: 'Petição curta, genérica, sem fundamentação técnica. Parece redação de formulário — e o juiz percebe na primeira página.',
    },
    {
      icon: '🧠',
      title: 'Esgotamento e Perda de Contexto',
      desc: 'Processo com mil páginas, cansaço mental extremo e o risco real de não flagrar uma nulidade grave: violação de domicílio, cadeia de custódia, tortura.',
    },
  ]

  const methodSteps = [
    {
      num: 1,
      title: 'Leitura Forçada do Processo',
      desc: 'A máquina é obrigada a ancorar em autos reais — não em achismos ou base genérica da internet. Cada informação precisa ter lastro processual.',
    },
    {
      num: 2,
      title: 'Cruzamento com a Sua Doutrina',
      desc: 'Você alimenta o repertório de doutrinas e jurisprudências que quer ver refletido na peça. A IA trabalha com seu arsenal teórico.',
    },
    {
      num: 3,
      title: 'Redação Subtópico a Subtópico',
      desc: 'Estrutura técnica rigorosa: Apresentar (fatos) → Fundamentar (direito aplicável) → Concluir (pedido do tópico). Sem atalhos.',
    },
  ]

  const modules = [
    {
      tag: 'Módulo 1',
      title: 'Fundamentos da IA e NotebookLM',
      desc: 'O conceito de "Janela de Contexto", por que o NotebookLM do Google é superior para volume e profundidade na criminalística e como usá-lo estrategicamente.',
      featured: false,
    },
    {
      tag: 'Módulo 2',
      title: 'Ambiente e Arquivos Mestres',
      desc: 'Preparação completa do ambiente, fracionamento de processos pesados (limite de 200MB) e instalação dos Arquivos Mestres de Análise e Regras de Escrita.',
      featured: false,
    },
    {
      tag: 'Módulos 3 e 4',
      title: 'Doutrina, Jurisprudência e Audiências',
      desc: 'Estratégias avançadas de alimentação da IA com materiais direcionados e a técnica exclusiva de conversão e transcrição de Audiências de Vídeo (AIJ) em segundos.',
      featured: false,
    },
    {
      tag: '🔥 Módulo Prático · Execução',
      title: 'Relatório de Análise + Peças Criminais Completas',
      desc: 'Geração do Relatório de Análise identificando nulidades (violação de domicílio, quebra de cadeia de custódia, tortura) e redação passo a passo de Defesas Preliminares e Alegações Finais — tudo com os Arquivos Mestres em ação.',
      featured: true,
    },
  ]

  const testimonials = [
    {
      text: 'Eu gastava uma manhã inteira para montar uma Defesa Preliminar. Agora, com os Arquivos Mestres e o NotebookLM, faço em menos de uma hora — com fundamentação que eu mesmo confiro e assino com confiança.',
      name: 'Dr. Rafael M.',
      role: 'Advogado Criminalista · SP',
      initials: 'RM',
    },
    {
      text: 'O diferencial é que a IA não inventa nada. Ela puxa exatamente o que está no processo e cruza com a doutrina que eu forneço. Achei nulidades em processos antigos que tinham passado batido.',
      name: 'Dra. Ana S.',
      role: 'Defensora Criminal · MG',
      initials: 'AS',
    },
  ]

  const faqData = [
    {
      q: 'Preciso saber programar ou ter experiência com IA?',
      a: 'Não. O curso parte do zero e é desenhado para advogados. O Dr. José Firmino traduz toda a parte técnica para linguagem prática, com exemplos reais da advocacia criminal.',
    },
    {
      q: 'O NotebookLM é pago? Preciso de quais ferramentas?',
      a: 'O NotebookLM do Google tem versão gratuita que já é suficiente para o método. Tudo que você precisa é de um navegador e uma conta Google. O curso detalha o passo a passo completo de configuração.',
    },
    {
      q: 'A IA pode realmente "alucinar" menos com esse método?',
      a: 'Sim. Os Arquivos Mestres funcionam como guardrails: a IA é forçada a ler o processo real e fundamentar cada ponto no que existe nos autos. O método de redação subtópico a subtópico impede que ela "invente" para preencher lacunas.',
    },
    {
      q: 'Funciona para qualquer área criminal?',
      a: 'O método é focado em advocacia criminal ampla — desde defesas preliminares até alegações finais. Os exemplos práticos cobrem nulidades, cadeia de custódia, violação de domicílio, tortura, entre outros.',
    },
    {
      q: 'Como acesso o curso após a compra?',
      a: 'O acesso é imediato pela plataforma Hotmart. Você recebe login e senha no e-mail cadastrado logo após a confirmação do pagamento. Todo conteúdo fica disponível 24/7 para estudar no seu ritmo.',
    },
  ]

  return (
    <>
      <SEOHead
        title="Curso IA Lei de Drogas — Método Firmino | Genesys Tecnologia"
        description="Curso avançado de IA aplicado à Lei de Drogas (11.343) com NotebookLM e Arquivos Mestres. Reduza horas de trabalho para minutos com peças robustas."
        keywords="IA advocacia criminal, NotebookLM, curso advogado, inteligência artificial jurídica, Genesys, Dr. José Firmino, engenharia de prompts, peças criminais, Lei de Drogas"
        canonical="https://genesys.ia.br/curso-ia-lei-de-drogas"
      />

      <div className="min-h-screen bg-gradient-to-b from-slate-900 via-[#0a0e1a] to-slate-900">
        <PremiumHeader />

        {/* ═══════════ HERO ═══════════ */}
        <section className="pt-32 lg:pt-40 pb-16 px-4 relative overflow-hidden">
          {/* Background Effects */}
          <div className="absolute inset-0 pointer-events-none">
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[600px] bg-blue-600/5 rounded-full blur-3xl" />
            <div className="absolute bottom-0 right-0 w-[400px] h-[400px] bg-amber-500/3 rounded-full blur-3xl" />
            <div className="absolute inset-0 opacity-[0.02]" style={{
              backgroundImage: 'linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)',
              backgroundSize: '60px 60px',
            }} />
          </div>

          <div className="max-w-5xl mx-auto relative z-10 text-center">
            {/* Badge */}
            <AnimatedSection>
              <div className="inline-flex items-center gap-2 px-4 py-1.5 text-xs font-bold tracking-wider uppercase text-amber-400 border border-amber-500/20 rounded-full bg-amber-500/5 mb-6">
                <span className="w-2 h-2 rounded-full bg-amber-400 animate-pulse" />
                Novo curso · IA aplicada à Lei de Drogas
              </div>
            </AnimatedSection>

            {/* Headline */}
            <AnimatedSection delay={150}>
              <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-[3.2rem] font-bold font-playfair leading-[1.15] mb-6 max-w-[900px] mx-auto">
                Da manhã inteira para{' '}
                <span className="bg-gradient-to-r from-amber-400 via-yellow-300 to-amber-500 bg-clip-text text-transparent">
                  40 minutos
                </span>
                . Do dia complexo para{' '}
                <span className="bg-gradient-to-r from-amber-400 via-yellow-300 to-amber-500 bg-clip-text text-transparent">
                  3 a 4 horas
                </span>
                {' '}— com peças criminais <em className="not-italic text-blue-300">à prova de alucinações</em>.
              </h1>
            </AnimatedSection>

            {/* Sub-headline */}
            <AnimatedSection delay={300}>
              <p className="text-lg text-gray-400 max-w-[700px] mx-auto mb-8 leading-relaxed">
                O segredo não é o ChatGPT genérico. É dominar o{' '}
                <strong className="text-white">NotebookLM do Google</strong>, sua enorme{' '}
                <strong className="text-white">janela de contexto</strong> e a{' '}
                <strong className="text-white">Engenharia de Contexto</strong> — para a máquina funcionar como assistente técnico, não como advogado substituto.
              </p>
            </AnimatedSection>

            {/* CTA Buttons */}
            <AnimatedSection delay={450}>
              <div className="flex flex-wrap gap-4 justify-center mb-4">
                <a
                  href={HOTMART_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="group bg-gradient-to-r from-amber-500 to-amber-600 text-slate-900 px-8 py-4 rounded-full font-bold text-lg hover:shadow-xl hover:shadow-amber-500/30 transition-all hover:scale-105 flex items-center gap-2"
                >
                  <FaGraduationCap />
                  Garantir minha vaga agora
                  <FaArrowRight className="group-hover:translate-x-1 transition-transform" />
                </a>
                <a
                  href="#metodo"
                  className="bg-transparent text-white border border-white/15 px-6 py-4 rounded-full font-semibold hover:border-amber-500/50 hover:text-amber-400 transition-all backdrop-blur-sm"
                >
                  Como o método funciona ↓
                </a>
              </div>
            </AnimatedSection>

            {/* Ethical Note */}
            <AnimatedSection delay={600}>
              <p className="text-sm text-gray-500 italic max-w-[520px] mx-auto mt-4">
                ⚖️ A IA aqui é ferramenta de produtividade e revisão técnica. A responsabilidade profissional, a leitura crítica e a assinatura continuam sendo suas.
              </p>
            </AnimatedSection>

            {/* Social Proof */}
            <AnimatedSection delay={750}>
              <div className="flex flex-wrap items-center justify-center gap-8 sm:gap-12 mt-12 pt-8 border-t border-white/5">
                {[
                  { value: 15, prefix: '+', suffix: '', label: 'Anos de Advocacia Criminal' },
                  { value: 90, prefix: '', suffix: '%', label: 'Redução de Tempo' },
                  { value: 0, prefix: '', suffix: '', label: 'Alucinações (com guardrails)' },
                  { value: 100, prefix: '', suffix: '%', label: 'Prático e Aplicável' },
                ].map((item, i) => (
                  <div key={i} className="text-center">
                    <div className="text-2xl sm:text-3xl font-bold bg-gradient-to-r from-amber-400 to-yellow-300 bg-clip-text text-transparent">
                      <AnimatedCounter target={item.value} prefix={item.prefix} suffix={item.suffix} />
                    </div>
                    <span className="text-xs text-gray-500 uppercase tracking-wider font-medium block mt-1">
                      {item.label}
                    </span>
                  </div>
                ))}
              </div>
            </AnimatedSection>
          </div>
        </section>

        {/* ═══════════ DORES ═══════════ */}
        <section id="dores" className="py-20 px-4 bg-slate-900/60 border-t border-b border-white/5">
          <div className="max-w-6xl mx-auto">
            <AnimatedSection>
              <div className="text-center mb-12">
                <span className="text-xs font-bold tracking-[0.15em] uppercase text-blue-400 block mb-3">O Problema</span>
                <h2 className="text-3xl md:text-4xl font-bold font-playfair mb-3">
                  Você não está &ldquo;preguiçoso&rdquo;. Está <em className="not-italic text-red-400">exposto</em>.
                </h2>
                <p className="text-gray-400 max-w-[600px] mx-auto text-lg">
                  Prazo apertado, processos gigantescos e IA que inventa dados. O risco é a sua reputação profissional em jogo.
                </p>
              </div>
            </AnimatedSection>

            <div className="grid md:grid-cols-3 gap-5">
              {painPoints.map((pain, i) => (
                <AnimatedSection key={i} delay={i * 100}>
                  <div className="group bg-gradient-to-br from-slate-800/80 to-slate-900/80 border border-slate-700/50 rounded-2xl p-7 h-full relative overflow-hidden transition-all duration-300 hover:-translate-y-1 hover:border-red-500/20 hover:shadow-lg hover:shadow-red-500/5">
                    <div className="absolute top-0 left-0 w-full h-[3px] bg-gradient-to-r from-red-500 to-orange-500 opacity-60" />
                    <div className="w-12 h-12 rounded-xl bg-red-500/10 flex items-center justify-center text-xl mb-4">
                      {pain.icon}
                    </div>
                    <h3 className="text-lg font-bold text-white mb-2">{pain.title}</h3>
                    <p className="text-gray-400 text-sm leading-relaxed">{pain.desc}</p>
                  </div>
                </AnimatedSection>
              ))}
            </div>

            <AnimatedSection delay={400}>
              <div className="text-center mt-10">
                <a
                  href={HOTMART_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 bg-gradient-to-r from-amber-500 to-amber-600 text-slate-900 px-7 py-3.5 rounded-full font-bold hover:shadow-lg hover:shadow-amber-500/25 transition-all hover:scale-105"
                >
                  Quero o método seguro no NotebookLM
                  <FaArrowRight />
                </a>
              </div>
            </AnimatedSection>
          </div>
        </section>

        {/* ═══════════ MÉTODO ═══════════ */}
        <section id="metodo" className="py-20 px-4">
          <div className="max-w-4xl mx-auto">
            <AnimatedSection>
              <div className="text-center mb-12">
                <span className="text-xs font-bold tracking-[0.15em] uppercase text-blue-400 block mb-3">A Solução</span>
                <h2 className="text-3xl md:text-4xl font-bold font-playfair mb-3">
                  Arquivos Mestres: o &ldquo;cérebro&rdquo; que{' '}
                  <span className="text-amber-400">obriga a IA a trabalhar certo</span>
                </h2>
                <p className="text-gray-400 max-w-[600px] mx-auto text-lg">
                  Você recebe arquivos pré-programados de <strong className="text-white">Análise de Processo</strong> (com guardrails de segurança) e <strong className="text-white">Regras de Escrita</strong>. Nada de &ldquo;inventar&rdquo; fora do processo.
                </p>
              </div>
            </AnimatedSection>

            <div className="space-y-4 max-w-[800px] mx-auto">
              {methodSteps.map((step, i) => (
                <AnimatedSection key={i} delay={i * 120}>
                  <div className="group flex gap-5 items-start p-6 bg-gradient-to-br from-slate-800/60 to-slate-900/60 border border-slate-700/50 rounded-2xl transition-all duration-300 hover:translate-x-1 hover:border-amber-500/20 hover:shadow-lg hover:shadow-amber-500/5">
                    <div className="flex-shrink-0 w-11 h-11 flex items-center justify-center bg-gradient-to-br from-amber-500 to-amber-600 text-slate-900 font-extrabold rounded-xl text-sm">
                      {step.num}
                    </div>
                    <div>
                      <h3 className="text-lg font-bold text-white mb-1">{step.title}</h3>
                      <p className="text-gray-400 text-sm leading-relaxed">{step.desc}</p>
                    </div>
                  </div>
                </AnimatedSection>
              ))}
            </div>
          </div>
        </section>

        {/* ═══════════ MÓDULOS ═══════════ */}
        <section id="modulos" className="py-20 px-4 bg-slate-900/60 border-t border-b border-white/5">
          <div className="max-w-5xl mx-auto">
            <AnimatedSection>
              <div className="text-center mb-12">
                <span className="text-xs font-bold tracking-[0.15em] uppercase text-blue-400 block mb-3">Conteúdo do Curso</span>
                <h2 className="text-3xl md:text-4xl font-bold font-playfair mb-3">O que você vai dominar</h2>
                <p className="text-gray-400 max-w-[600px] mx-auto text-lg">
                  Do conceito à execução real. Cada módulo entrega técnica aplicável na sua prática criminal.
                </p>
              </div>
            </AnimatedSection>

            <div className="grid md:grid-cols-2 gap-5">
              {modules.map((mod, i) => (
                <AnimatedSection key={i} delay={i * 100}>
                  <div className={`p-7 rounded-2xl border transition-all duration-300 hover:-translate-y-1 relative overflow-hidden h-full ${
                    mod.featured
                      ? 'md:col-span-2 border-amber-500/30 bg-gradient-to-br from-slate-800/90 to-slate-900/90 hover:shadow-lg hover:shadow-amber-500/10'
                      : 'border-slate-700/50 bg-gradient-to-br from-slate-800/60 to-slate-900/60 hover:border-blue-500/20 hover:shadow-lg hover:shadow-blue-500/5'
                  }`}
                    style={mod.featured ? { gridColumn: '1 / -1' } : {}}
                  >
                    {mod.featured && (
                      <div className="absolute top-0 left-0 w-full h-[3px] bg-gradient-to-r from-amber-400 to-yellow-300" />
                    )}
                    <span className={`inline-block text-[0.7rem] uppercase tracking-[0.1em] font-bold px-2.5 py-1 rounded-md mb-3 ${
                      mod.featured
                        ? 'text-amber-400 bg-amber-500/10'
                        : 'text-cyan-400 bg-cyan-500/10'
                    }`}>
                      {mod.tag}
                    </span>
                    <h3 className="text-lg font-bold text-white mb-2">{mod.title}</h3>
                    <p className="text-gray-400 text-sm leading-relaxed">{mod.desc}</p>
                  </div>
                </AnimatedSection>
              ))}
            </div>
          </div>
        </section>

        {/* ═══════════ AUTORIDADE ═══════════ */}
        <section id="autoridade" className="py-20 px-4">
          <div className="max-w-5xl mx-auto">
            <AnimatedSection>
              <div className="grid md:grid-cols-[280px_1fr] gap-10 items-center">
                {/* Photo */}
                <div className="relative rounded-2xl overflow-hidden shadow-2xl mx-auto md:mx-0 max-w-[280px]">
                  <Image
                    src="/images/firmino-curso.png"
                    alt="Dr. José Firmino — Advogado Criminalista e Especialista em IA"
                    width={400}
                    height={400}
                    className="object-cover object-top aspect-square"
                  />
                  <div className="absolute bottom-0 left-0 w-full h-2/5 bg-gradient-to-t from-slate-900/60 to-transparent" />
                </div>

                {/* Content */}
                <div>
                  <span className="text-xs font-bold tracking-[0.15em] uppercase text-blue-400 block mb-2">Quem é o Instrutor</span>
                  <h2 className="text-3xl md:text-4xl font-bold font-playfair mb-4 text-left">Dr. José Firmino</h2>

                  <div className="flex flex-wrap gap-2 mb-5">
                    {[
                      { icon: '⚖️', label: 'Advogado Criminalista' },
                      { icon: '💻', label: 'Programador' },
                      { icon: '🧠', label: 'Engenheiro de Prompts' },
                      { icon: '🏢', label: 'Sócio-Fundador Genesys' },
                    ].map((badge, i) => (
                      <span key={i} className="inline-flex items-center gap-1.5 px-3 py-1 text-xs font-semibold text-blue-300 bg-blue-500/10 border border-blue-500/20 rounded-full">
                        {badge.icon} {badge.label}
                      </span>
                    ))}
                  </div>

                  <p className="text-gray-400 mb-3 leading-relaxed">
                    Mais de 15 anos de atuação real na advocacia criminal de alto nível — de nulidades complexas a júris de grande repercussão. Ao mesmo tempo, programador com domínio técnico em Engenharia de Prompts e Engenharia de Contexto.
                  </p>
                  <p className="text-gray-400 mb-6 leading-relaxed">
                    É a combinação rara de quem litiga na trincheira e desenha sistemas com a precisão de quem codifica. O método não nasceu em slides bonitos — nasceu na prática real da advocacia criminal.
                  </p>

                  <a
                    href={HOTMART_URL}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 bg-gradient-to-r from-amber-500 to-amber-600 text-slate-900 px-7 py-3.5 rounded-full font-bold hover:shadow-lg hover:shadow-amber-500/25 transition-all hover:scale-105"
                  >
                    Comprar com segurança pela Hotmart
                    <FaArrowRight />
                  </a>
                </div>
              </div>
            </AnimatedSection>
          </div>
        </section>

        {/* ═══════════ DEPOIMENTOS ═══════════ */}
        <section className="py-20 px-4 bg-slate-900/60 border-t border-b border-white/5">
          <div className="max-w-4xl mx-auto">
            <AnimatedSection>
              <div className="text-center mb-12">
                <span className="text-xs font-bold tracking-[0.15em] uppercase text-blue-400 block mb-3">Resultados Reais</span>
                <h2 className="text-3xl md:text-4xl font-bold font-playfair">O que dizem advogados que usam o método</h2>
              </div>
            </AnimatedSection>

            <div className="grid md:grid-cols-2 gap-5">
              {testimonials.map((t, i) => (
                <AnimatedSection key={i} delay={i * 150}>
                  <div className="p-7 bg-gradient-to-br from-slate-800/60 to-slate-900/60 border border-slate-700/50 rounded-2xl relative h-full">
                    <div className="absolute top-3 left-5 text-5xl font-playfair text-amber-400/20 leading-none">&ldquo;</div>
                    <p className="text-gray-300 italic text-sm leading-relaxed mb-5 pt-6">{t.text}</p>
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center font-bold text-white text-sm">
                        {t.initials}
                      </div>
                      <div>
                        <div className="font-semibold text-white text-sm">{t.name}</div>
                        <div className="text-xs text-gray-500">{t.role}</div>
                      </div>
                    </div>
                  </div>
                </AnimatedSection>
              ))}
            </div>
          </div>
        </section>

        {/* ═══════════ GARANTIA ═══════════ */}
        <section className="py-20 px-4">
          <div className="max-w-3xl mx-auto">
            <AnimatedSection>
              <div className="text-center p-10 bg-gradient-to-br from-slate-800/60 to-slate-900/60 border border-green-500/20 rounded-3xl relative overflow-hidden">
                <div className="absolute top-0 left-0 w-full h-[3px] bg-gradient-to-r from-green-500 to-emerald-400" />
                <div className="text-5xl mb-4">🛡️</div>
                <h3 className="text-2xl font-bold font-playfair text-emerald-400 mb-3">Garantia incondicional de 7 dias</h3>
                <p className="text-gray-400 max-w-[520px] mx-auto leading-relaxed">
                  Se nos primeiros 7 dias você sentir que o método não é para a sua prática, basta solicitar o reembolso integral pela plataforma Hotmart — sem burocracia, sem perguntas.
                </p>
              </div>
            </AnimatedSection>
          </div>
        </section>

        {/* ═══════════ FAQ ═══════════ */}
        <section id="faq" className="py-20 px-4 bg-slate-900/60 border-t border-b border-white/5">
          <div className="max-w-3xl mx-auto">
            <AnimatedSection>
              <div className="text-center mb-12">
                <span className="text-xs font-bold tracking-[0.15em] uppercase text-blue-400 block mb-3">Dúvidas Frequentes</span>
                <h2 className="text-3xl md:text-4xl font-bold font-playfair">Perguntas que advogados fazem antes de entrar</h2>
              </div>
            </AnimatedSection>

            <div className="space-y-3">
              {faqData.map((item, i) => (
                <AnimatedSection key={i} delay={i * 80}>
                  <FAQItem question={item.q} answer={item.a} />
                </AnimatedSection>
              ))}
            </div>
          </div>
        </section>

        {/* ═══════════ CTA FINAL ═══════════ */}
        <section className="py-20 px-4 relative">
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[400px] bg-amber-500/3 rounded-full blur-3xl pointer-events-none" />

          <div className="max-w-3xl mx-auto relative z-10">
            <AnimatedSection>
              <div className="text-center p-10 md:p-14 bg-gradient-to-br from-slate-800 to-slate-900 border border-amber-500/20 rounded-3xl shadow-xl shadow-amber-500/5 relative overflow-hidden">
                <div className="absolute top-0 left-0 w-full h-[3px] bg-gradient-to-r from-amber-400 to-yellow-300" />

                <h2 className="text-2xl md:text-3xl font-bold font-playfair mb-4">
                  Pare de perder tempo com tarefas que a IA faz{' '}
                  <span className="text-amber-400">melhor e mais rápido</span>
                </h2>
                <p className="text-gray-400 max-w-[480px] mx-auto mb-8 text-lg">
                  Eleve o nível da sua advocacia criminal com uso avançado de inteligência artificial — com limites claros, técnica explícita e peças que sustentam o contraditório.
                </p>
                <a
                  href={HOTMART_URL}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="group inline-flex items-center gap-2 bg-gradient-to-r from-amber-500 to-amber-600 text-slate-900 px-9 py-4 rounded-full font-bold text-lg hover:shadow-xl hover:shadow-amber-500/30 transition-all hover:scale-105"
                >
                  <FaGraduationCap />
                  Garantir minha vaga agora
                  <FaArrowRight className="group-hover:translate-x-1 transition-transform" />
                </a>
                <p className="text-xs text-gray-500 mt-4">
                  Pagamento seguro via Hotmart · Acesso imediato · Garantia de 7 dias
                </p>
              </div>
            </AnimatedSection>
          </div>
        </section>

        {/* ═══════════ BRAND BAR ═══════════ */}
        <div className="text-center py-6 border-t border-white/5">
          <p className="text-xs text-gray-500">
            Um curso da{' '}
            <Link href="/" className="text-blue-400 font-semibold hover:text-blue-300 transition-colors">
              Genesys Tecnologia
            </Link>
            {' '}— Inteligência Artificial Jurídica
          </p>
        </div>

        <Footer />
      </div>
    </>
  )
}
