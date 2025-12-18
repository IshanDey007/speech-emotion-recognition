'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Mic, Upload, BarChart3, Sparkles } from 'lucide-react'
import AudioUploader from '@/components/AudioUploader'
import EmotionResults from '@/components/EmotionResults'
import Dashboard from '@/components/Dashboard'
import Header from '@/components/Header'

export default function Home() {
  const [activeTab, setActiveTab] = useState<'analyze' | 'dashboard'>('analyze')
  const [results, setResults] = useState<any>(null)
  const [history, setHistory] = useState<any[]>([])

  const handleAnalysisComplete = (result: any) => {
    setResults(result)
    setHistory(prev => [result, ...prev].slice(0, 10)) // Keep last 10 results
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <Header />
      
      {/* Hero Section */}
      <section className="container mx-auto px-4 pt-24 pb-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center max-w-4xl mx-auto"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-purple-100 dark:bg-purple-900/30 rounded-full mb-6">
            <Sparkles className="w-4 h-4 text-purple-600 dark:text-purple-400" />
            <span className="text-sm font-medium text-purple-600 dark:text-purple-400">
              AI-Powered Emotion Analysis
            </span>
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold mb-6 gradient-text">
            Speech Emotion Recognition
          </h1>
          
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8">
            Analyze customer emotions from voice recordings to measure satisfaction
            and improve user experience with cutting-edge AI technology.
          </p>

          {/* Tab Navigation */}
          <div className="flex justify-center gap-4 mb-12">
            <button
              onClick={() => setActiveTab('analyze')}
              className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all ${
                activeTab === 'analyze'
                  ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/50'
                  : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'
              }`}
            >
              <Mic className="w-5 h-5" />
              Analyze Audio
            </button>
            
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all ${
                activeTab === 'dashboard'
                  ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/50'
                  : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'
              }`}
            >
              <BarChart3 className="w-5 h-5" />
              Dashboard
            </button>
          </div>
        </motion.div>

        {/* Content Area */}
        <div className="max-w-6xl mx-auto">
          {activeTab === 'analyze' ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.4 }}
            >
              <AudioUploader onAnalysisComplete={handleAnalysisComplete} />
              
              {results && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                  className="mt-8"
                >
                  <EmotionResults results={results} />
                </motion.div>
              )}
            </motion.div>
          ) : (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.4 }}
            >
              <Dashboard history={history} />
            </motion.div>
          )}
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-16">
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg"
          >
            <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center mb-4">
              <Mic className="w-6 h-6 text-purple-600 dark:text-purple-400" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Real-time Analysis</h3>
            <p className="text-gray-600 dark:text-gray-300">
              Instant emotion detection from audio files with high accuracy
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg"
          >
            <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center mb-4">
              <BarChart3 className="w-6 h-6 text-blue-600 dark:text-blue-400" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Visual Analytics</h3>
            <p className="text-gray-600 dark:text-gray-300">
              Beautiful charts and insights to understand customer sentiment
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-lg"
          >
            <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center mb-4">
              <Sparkles className="w-6 h-6 text-green-600 dark:text-green-400" />
            </div>
            <h3 className="text-xl font-semibold mb-2">7 Emotions</h3>
            <p className="text-gray-600 dark:text-gray-300">
              Detects anger, disgust, fear, happiness, sadness, surprise, and neutral
            </p>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-200 dark:border-gray-700 mt-16">
        <div className="container mx-auto px-4 py-8">
          <p className="text-center text-gray-600 dark:text-gray-400">
            Built with ❤️ for better customer experiences | © 2025 Speech Emotion Recognition
          </p>
        </div>
      </footer>
    </main>
  )
}