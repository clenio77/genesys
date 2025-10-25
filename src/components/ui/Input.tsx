'use client'

import { motion } from 'framer-motion'
import { useState } from 'react'
import { IconType } from 'react-icons'

interface InputProps {
  label?: string
  type?: string
  placeholder?: string
  value?: string
  onChange?: (value: string) => void
  icon?: IconType
  error?: string
  disabled?: boolean
  required?: boolean
  className?: string
}

export default function Input({
  label,
  type = 'text',
  placeholder,
  value,
  onChange,
  icon: Icon,
  error,
  disabled = false,
  required = false,
  className = '',
}: InputProps) {
  const [isFocused, setIsFocused] = useState(false)
  const [hasValue, setHasValue] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value
    setHasValue(newValue.length > 0)
    onChange?.(newValue)
  }

  return (
    <div className={`relative ${className}`}>
      {/* Label */}
      {label && (
        <motion.label
          className={`block text-sm font-medium mb-2 transition-colors ${
            error ? 'text-red-400' : isFocused ? 'text-blue-400' : 'text-gray-400'
          }`}
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          {label}
          {required && <span className="text-red-400 ml-1">*</span>}
        </motion.label>
      )}

      {/* Input Container */}
      <div className="relative">
        {/* Icon */}
        {Icon && (
          <div className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400">
            <Icon className="text-xl" />
          </div>
        )}

        {/* Input Field */}
        <motion.input
          type={type}
          placeholder={placeholder}
          value={value}
          onChange={handleChange}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          disabled={disabled}
          className={`
            w-full px-4 py-3 bg-slate-800/50 backdrop-blur-sm border-2 rounded-lg
            text-white placeholder-gray-500 transition-all duration-300
            focus:outline-none
            ${Icon ? 'pl-12' : ''}
            ${error ? 'border-red-500' : isFocused ? 'border-blue-500' : 'border-slate-700'}
            ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
          `}
          whileFocus={{ scale: 1.02 }}
        />

        {/* Animated Border */}
        <motion.div
          className="absolute bottom-0 left-0 h-0.5 bg-gradient-to-r from-blue-500 to-cyan-500"
          initial={{ width: 0 }}
          animate={{ width: isFocused ? '100%' : 0 }}
          transition={{ duration: 0.3 }}
        />

        {/* Floating Label Effect */}
        {placeholder && !label && (
          <motion.span
            className={`absolute left-4 pointer-events-none transition-all duration-300 ${
              Icon ? 'left-12' : 'left-4'
            }`}
            animate={{
              top: isFocused || hasValue ? '-10px' : '50%',
              fontSize: isFocused || hasValue ? '12px' : '16px',
              y: isFocused || hasValue ? 0 : '-50%',
            }}
          >
            {placeholder}
          </motion.span>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <motion.p
          className="mt-2 text-sm text-red-400 flex items-center space-x-1"
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path
              fillRule="evenodd"
              d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
              clipRule="evenodd"
            />
          </svg>
          <span>{error}</span>
        </motion.p>
      )}

      {/* Success Indicator */}
      {!error && hasValue && (
        <motion.div
          className="absolute right-4 top-1/2 transform -translate-y-1/2"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', stiffness: 300 }}
        >
          <svg className="w-5 h-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
            <path
              fillRule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
              clipRule="evenodd"
            />
          </svg>
        </motion.div>
      )}
    </div>
  )
}

