'use client'

import { motion } from 'framer-motion'
import { IconType } from 'react-icons'
import { FaStar } from 'react-icons/fa'

interface ServiceCardProps {
  title: string
  description: string
  icon: IconType
  features: string[]
  badge?: string
  gradient: string
  delay?: number
}

export default function ServiceCard({
  title,
  description,
  icon: Icon,
  features,
  badge,
  gradient,
  delay = 0,
}: ServiceCardProps) {
  return (
    <motion.div
      className="group relative"
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6, delay }}
    >
      {/* Glow Effect */}
      <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-2xl opacity-0 group-hover:opacity-100 blur transition-all duration-500" />
      
      {/* Card */}
      <div className="relative h-full p-8 bg-slate-900/80 backdrop-blur-xl border border-slate-700/50 rounded-2xl hover:border-blue-500/50 transition-all duration-300">
        {/* Badge */}
        {badge && (
          <div className="absolute top-4 right-4">
            <span className="px-3 py-1 bg-gradient-to-r from-amber-500 to-orange-500 text-white text-xs font-bold rounded-full flex items-center space-x-1">
              <FaStar className="text-xs" />
              <span>{badge}</span>
            </span>
          </div>
        )}

        {/* Icon */}
        <motion.div
          className={`inline-flex p-4 bg-gradient-to-br ${gradient} rounded-xl mb-6`}
          whileHover={{ scale: 1.1, rotate: 5 }}
          transition={{ type: 'spring', stiffness: 300 }}
        >
          <Icon className="text-4xl text-white" />
        </motion.div>

        {/* Title */}
        <h3 className="text-2xl font-bold text-white mb-3 group-hover:text-blue-400 transition-colors">
          {title}
        </h3>

        {/* Description */}
        <p className="text-gray-400 mb-6 leading-relaxed">
          {description}
        </p>

        {/* Features */}
        <ul className="space-y-3 mb-6">
          {features.map((feature, index) => (
            <motion.li
              key={index}
              className="flex items-start space-x-3 text-gray-300"
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: delay + 0.1 * index }}
            >
              <svg
                className="w-5 h-5 text-blue-500 mt-0.5 flex-shrink-0"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M5 13l4 4L19 7"
                />
              </svg>
              <span className="text-sm">{feature}</span>
            </motion.li>
          ))}
        </ul>

        {/* CTA Button */}
        <motion.button
          className="w-full py-3 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-semibold rounded-lg hover:shadow-lg hover:shadow-blue-500/50 transition-all"
          whileHover={{ scale: 1.02, y: -2 }}
          whileTap={{ scale: 0.98 }}
        >
          Saiba Mais
        </motion.button>

        {/* Decorative Elements */}
        <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 rounded-full blur-3xl -z-10 group-hover:bg-blue-500/20 transition-all duration-500" />
        <div className="absolute bottom-0 left-0 w-32 h-32 bg-cyan-500/10 rounded-full blur-3xl -z-10 group-hover:bg-cyan-500/20 transition-all duration-500" />
      </div>
    </motion.div>
  )
}

