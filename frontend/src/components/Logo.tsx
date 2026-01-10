'use client'

import Image from 'next/image'
import { motion } from 'framer-motion'

interface LogoProps {
    showText?: boolean
    size?: 'sm' | 'md' | 'lg'
    className?: string
}

export default function Logo({ showText = true, size = 'md', className = '' }: LogoProps) {
    const sizes = {
        sm: { img: 32, text: 'text-lg' },
        md: { img: 40, text: 'text-xl' },
        lg: { img: 56, text: 'text-3xl' },
    }

    return (
        <motion.div
            className={`flex items-center gap-3 ${className}`}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
        >
            {/* Logo Image */}
            <div className="relative">
                <Image
                    src="/logo.svg"
                    alt="Mission Impossible Logo"
                    width={sizes[size].img}
                    height={sizes[size].img}
                    className="drop-shadow-[0_0_10px_rgba(0,255,255,0.5)]"
                    priority
                />
                {/* Pulse ring */}
                <motion.div
                    className="absolute inset-0 rounded-full border-2 border-cyan-400/50"
                    animate={{
                        scale: [1, 1.3, 1],
                        opacity: [0.5, 0, 0.5],
                    }}
                    transition={{
                        duration: 2,
                        repeat: Infinity,
                        ease: 'easeInOut',
                    }}
                />
            </div>

            {/* Text Logo */}
            {showText && (
                <div className="flex flex-col">
                    <span
                        className={`${sizes[size].text} font-extrabold italic tracking-wide`}
                        style={{
                            fontFamily: '"New Rocker", cursive',
                            color: '#3D85C6', /* Dark silver */
                            textShadow: '0 0 3px rgba(0, 255, 255, 0.6), 0 0 20px rgba(0, 255, 255, 0.4), 0 0 30px rgba(0, 255, 255, 0.2)',
                        }}
                    >
                        MissionImpossible
                    </span>
                </div>
            )}
        </motion.div>
    )
}
