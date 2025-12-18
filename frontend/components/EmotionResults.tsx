'use client'

import { motion } from 'framer-motion'
import { Smile, Frown, Meh, AlertCircle, Heart, Zap, User } from 'lucide-react'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'

const EMOTION_CONFIG = {
  anger: { icon: AlertCircle, color: '#ef4444', label: 'Anger' },
  disgust: { icon: Frown, color: '#10b981', label: 'Disgust' },
  fear: { icon: AlertCircle, color: '#8b5cf6', label: 'Fear' },
  happiness: { icon: Smile, color: '#f59e0b', label: 'Happiness' },
  sadness: { icon: Frown, color: '#3b82f6', label: 'Sadness' },
  surprise: { icon: Zap, color: '#ec4899', label: 'Surprise' },
  neutral: { icon: Meh, color: '#6b7280', label: 'Neutral' },
}

interface EmotionResultsProps {
  results: {
    emotion: string
    confidence: number
    probabilities: Record<string, number>
    satisfaction_score: number
    timestamp: string
  }
}

export default function EmotionResults({ results }: EmotionResultsProps) {
  const { emotion, confidence, probabilities, satisfaction_score } = results

  const chartData = Object.entries(probabilities).map(([key, value]) => ({
    name: EMOTION_CONFIG[key as keyof typeof EMOTION_CONFIG]?.label || key,
    value: value * 100,
    color: EMOTION_CONFIG[key as keyof typeof EMOTION_CONFIG]?.color || '#6b7280',
  }))

  const EmotionIcon = EMOTION_CONFIG[emotion as keyof typeof EMOTION_CONFIG]?.icon || User
  const emotionColor = EMOTION_CONFIG[emotion as keyof typeof EMOTION_CONFIG]?.color || '#6b7280'

  const getSatisfactionLevel = (score: number) => {
    if (score >= 8) return { label: 'Excellent', color: 'text-green-600', bg: 'bg-green-100' }
    if (score >= 6) return { label: 'Good', color: 'text-blue-600', bg: 'bg-blue-100' }
    if (score >= 4) return { label: 'Fair', color: 'text-yellow-600', bg: 'bg-yellow-100' }
    return { label: 'Poor', color: 'text-red-600', bg: 'bg-red-100' }
  }

  const satisfactionLevel = getSatisfactionLevel(satisfaction_score)

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8"
    >
      <h2 className="text-2xl font-bold mb-6">Analysis Results</h2>

      <div className="grid md:grid-cols-2 gap-8">
        {/* Primary Emotion */}
        <div>
          <div className="flex items-center gap-4 mb-6">
            <div
              className="w-16 h-16 rounded-full flex items-center justify-center"
              style={{ backgroundColor: `${emotionColor}20` }}
            >
              <EmotionIcon className="w-8 h-8" style={{ color: emotionColor }} />
            </div>
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">Detected Emotion</p>
              <h3 className="text-3xl font-bold capitalize">{emotion}</h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {(confidence * 100).toFixed(1)}% confidence
              </p>
            </div>
          </div>

          {/* Confidence Bar */}
          <div className="mb-6">
            <div className="flex justify-between text-sm mb-2">
              <span className="text-gray-600 dark:text-gray-400">Confidence Level</span>
              <span className="font-semibold">{(confidence * 100).toFixed(1)}%</span>
            </div>
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${confidence * 100}%` }}
                transition={{ duration: 1, ease: 'easeOut' }}
                className="h-3 rounded-full"
                style={{ backgroundColor: emotionColor }}
              />
            </div>
          </div>

          {/* Satisfaction Score */}
          <div className={`${satisfactionLevel.bg} rounded-xl p-4`}>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-700">Satisfaction Score</p>
                <p className={`text-3xl font-bold ${satisfactionLevel.color}`}>
                  {satisfaction_score.toFixed(1)}/10
                </p>
              </div>
              <div className={`px-4 py-2 ${satisfactionLevel.bg} rounded-lg`}>
                <span className={`font-semibold ${satisfactionLevel.color}`}>
                  {satisfactionLevel.label}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Emotion Distribution Chart */}
        <div>
          <h4 className="text-lg font-semibold mb-4">Emotion Distribution</h4>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value.toFixed(1)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip formatter={(value: number) => `${value.toFixed(2)}%`} />
            </PieChart>
          </ResponsiveContainer>

          {/* Probability List */}
          <div className="mt-6 space-y-2">
            {Object.entries(probabilities)
              .sort(([, a], [, b]) => b - a)
              .map(([key, value]) => {
                const config = EMOTION_CONFIG[key as keyof typeof EMOTION_CONFIG]
                return (
                  <div key={key} className="flex items-center justify-between text-sm">
                    <div className="flex items-center gap-2">
                      <div
                        className="w-3 h-3 rounded-full"
                        style={{ backgroundColor: config?.color }}
                      />
                      <span className="capitalize">{config?.label || key}</span>
                    </div>
                    <span className="font-medium">{(value * 100).toFixed(2)}%</span>
                  </div>
                )
              })}
          </div>
        </div>
      </div>
    </motion.div>
  )
}