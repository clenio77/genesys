'use client'

import { motion } from 'framer-motion'
import { useState } from 'react'
import { FaUser, FaEnvelope, FaPhone, FaBuilding, FaPaperPlane } from 'react-icons/fa'
import Input from './ui/Input'
import Button from './ui/Button'
import { staggerContainer, staggerItem } from '@/utils/animations'

export default function ContactSection() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    company: '',
    message: '',
  })
  
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSuccess, setIsSuccess] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    // Validação simples
    const newErrors: Record<string, string> = {}
    if (!formData.name) newErrors.name = 'Nome é obrigatório'
    if (!formData.email) newErrors.email = 'Email é obrigatório'
    if (!formData.message) newErrors.message = 'Mensagem é obrigatória'
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }
    
    setIsSubmitting(true)
    
    // Simular envio
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    setIsSubmitting(false)
    setIsSuccess(true)
    setFormData({ name: '', email: '', phone: '', company: '', message: '' })
    
    setTimeout(() => setIsSuccess(false), 5000)
  }

  const contactInfo = [
    {
      icon: FaEnvelope,
      title: 'Email',
      value: 'contato@genesys.tech',
      link: 'mailto:contato@genesys.tech',
    },
    {
      icon: FaPhone,
      title: 'Telefone',
      value: '+55 (11) 9999-9999',
      link: 'tel:+5511999999999',
    },
    {
      icon: FaBuilding,
      title: 'Endereço',
      value: 'São Paulo, SP - Brasil',
      link: '#',
    },
  ]

  return (
    <section id="contact" className="py-24 bg-gradient-to-b from-slate-900 to-slate-800 relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-5">
        <div className="absolute inset-0" style={{
          backgroundImage: `radial-gradient(circle at 2px 2px, white 1px, transparent 0)`,
          backgroundSize: '40px 40px',
        }} />
      </div>

      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        {/* Section Header */}
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <span className="inline-block px-4 py-2 bg-blue-500/10 border border-blue-500/30 rounded-full text-blue-400 text-sm font-medium mb-4">
            Entre em Contato
          </span>
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Vamos
            <span className="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent"> Conversar</span>
          </h2>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            Estamos prontos para transformar sua prática jurídica com IA
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 max-w-6xl mx-auto">
          {/* Contact Form */}
          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
          >
            <motion.div
              className="p-8 bg-slate-800/50 backdrop-blur-xl border border-slate-700/50 rounded-2xl"
              variants={staggerItem}
            >
              <h3 className="text-2xl font-bold text-white mb-6">Envie sua Mensagem</h3>
              
              <form onSubmit={handleSubmit} className="space-y-6">
                <Input
                  label="Nome Completo"
                  type="text"
                  placeholder="Seu nome"
                  value={formData.name}
                  onChange={(value) => setFormData({ ...formData, name: value })}
                  icon={FaUser}
                  error={errors.name}
                  required
                />
                
                <Input
                  label="Email"
                  type="email"
                  placeholder="seu@email.com"
                  value={formData.email}
                  onChange={(value) => setFormData({ ...formData, email: value })}
                  icon={FaEnvelope}
                  error={errors.email}
                  required
                />
                
                <Input
                  label="Telefone"
                  type="tel"
                  placeholder="(11) 99999-9999"
                  value={formData.phone}
                  onChange={(value) => setFormData({ ...formData, phone: value })}
                  icon={FaPhone}
                />
                
                <Input
                  label="Empresa"
                  type="text"
                  placeholder="Nome da empresa"
                  value={formData.company}
                  onChange={(value) => setFormData({ ...formData, company: value })}
                  icon={FaBuilding}
                />
                
                <div>
                  <label className="block text-sm font-medium text-gray-400 mb-2">
                    Mensagem <span className="text-red-400">*</span>
                  </label>
                  <motion.textarea
                    className="w-full px-4 py-3 bg-slate-800/50 backdrop-blur-sm border-2 border-slate-700 rounded-lg text-white placeholder-gray-500 focus:border-blue-500 focus:outline-none transition-all duration-300 resize-none"
                    rows={5}
                    placeholder="Como podemos ajudar?"
                    value={formData.message}
                    onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                    whileFocus={{ scale: 1.02 }}
                  />
                  {errors.message && (
                    <p className="mt-2 text-sm text-red-400">{errors.message}</p>
                  )}
                </div>
                
                <Button
                  variant="primary"
                  size="lg"
                  fullWidth
                  loading={isSubmitting}
                  onClick={() => {}}
                >
                  <FaPaperPlane className="inline mr-2" />
                  {isSubmitting ? 'Enviando...' : 'Enviar Mensagem'}
                </Button>
              </form>
              
              {/* Success Message */}
              {isSuccess && (
                <motion.div
                  className="mt-6 p-4 bg-green-500/10 border border-green-500/30 rounded-lg text-green-400 text-center"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                >
                  ✓ Mensagem enviada com sucesso! Entraremos em contato em breve.
                </motion.div>
              )}
            </motion.div>
          </motion.div>

          {/* Contact Info */}
          <motion.div
            className="space-y-8"
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
          >
            {contactInfo.map((info) => (
              <motion.a
                key={info.title}
                href={info.link}
                className="block p-6 bg-slate-800/50 backdrop-blur-xl border border-slate-700/50 rounded-2xl hover:border-blue-500/50 transition-all group"
                variants={staggerItem}
                whileHover={{ scale: 1.02, y: -5 }}
              >
                <div className="flex items-start space-x-4">
                  <div className="p-3 bg-gradient-to-br from-blue-600 to-cyan-600 rounded-lg group-hover:scale-110 transition-transform">
                    <info.icon className="text-2xl text-white" />
                  </div>
                  <div>
                    <h4 className="text-lg font-semibold text-white mb-1">{info.title}</h4>
                    <p className="text-gray-400">{info.value}</p>
                  </div>
                </div>
              </motion.a>
            ))}
            
            {/* Map Placeholder */}
            <motion.div
              className="p-6 bg-slate-800/50 backdrop-blur-xl border border-slate-700/50 rounded-2xl overflow-hidden"
              variants={staggerItem}
            >
              <div className="aspect-video bg-gradient-to-br from-blue-900/50 to-cyan-900/50 rounded-lg flex items-center justify-center">
                <p className="text-gray-400">Mapa de Localização</p>
              </div>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}

