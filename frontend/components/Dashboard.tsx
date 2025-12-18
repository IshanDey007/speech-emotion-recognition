'use client'

import { motion } from 'framer-motion'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts'
import { TrendingUp, Users, Activity, Award } from 'lucide-react'

interface DashboardProps {
  history: any[]
}

export default function Dashboard({ history }: DashboardProps) {
  if (history.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-12 text-center"
      >
        <Activity className="w-16 h-16 mx-auto mb-4 text-gray-400" />
        <h3 className="text-2xl font-semibold mb-2">No Data Yet</h3>
        <p className="text-gray-600 dark:text-gray-400">
          Analyze some audio files to see your dashboard statistics
        </p>
      </motion.div>
    )
  }

  // Calculate statistics
  const totalAnalyses = history.length
  const avgSatisfaction = history.reduce((sum, item) => sum + item.satisfaction_score, 0) / totalAnalyses
  
  const emotionCounts = history.reduce((acc, item) => {
    acc[item.emotion] = (acc[item.emotion] || 0) + 1
    return acc
  }, {} as Record<string, number>)

  const mostCommonEmotion = Object.entries(emotionCounts).sort(([, a], [, b]) => b - a)[0]

  const emotionData = Object.entries(emotionCounts).map(([emotion, count]) => ({
    emotion: emotion.charAt(0).toUpperCase() + emotion.slice(1),
    count,
  }))

  const satisfactionTrend = history.slice(0, 10).reverse().map((item, index) => ({
    index: index + 1,
    score: item.satisfaction_score,
  }))

  return (
    <div className="space-y-6">
      {/* Stats Cards */}
      <div className="grid md:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6"
        >
          <div className="flex items-center justify-between mb-2">
            <Users className="w-8 h-8 text-purple-600" />
            <span className="text-3xl font-bold">{totalAnalyses}</span>
          </div>
          <p className="text-gray-600 dark:text-gray-400">Total Analyses</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6"
        >
          <div className="flex items-center justify-between mb-2">
            <TrendingUp className="w-8 h-8 text-blue-600" />
            <span className="text-3xl font-bold">{avgSatisfaction.toFixed(1)}</span>
          </div>
          <p className="text-gray-600 dark:text-gray-400">Avg Satisfaction</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6"
        >
          <div className="flex items-center justify-between mb-2">
            <Award className="w-8 h-8 text-yellow-600" />
            <span className="text-2xl font-bold capitalize">{mostCommonEmotion[0]}</span>
          </div>
          <p className="text-gray-600 dark:text-gray-400">Most Common</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6"
        >
          <div className="flex items-center justify-between mb-2">
            <Activity className="w-8 h-8 text-green-600" />
            <span className="text-3xl font-bold">{Object.keys(emotionCounts).length}</span>
          </div>
          <p className="text-gray-600 dark:text-gray-400">Unique Emotions</p>
        </motion.div>
      </div>

      {/* Charts */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Emotion Distribution */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6"
        >
          <h3 className="text-xl font-semibold mb-4">Emotion Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={emotionData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="emotion" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#8b5cf6" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Satisfaction Trend */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6"
        >
          <h3 className="text-xl font-semibold mb-4">Satisfaction Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={satisfactionTrend}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="index" label={{ value: 'Analysis #', position: 'insideBottom', offset: -5 }} />
              <YAxis domain={[0, 10]} />
              <Tooltip />
              <Line type="monotone" dataKey="score" stroke="#3b82f6" strokeWidth={2} dot={{ r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* Recent Analyses */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
        className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6"
      >
        <h3 className="text-xl font-semibold mb-4">Recent Analyses</h3>
        <div className="space-y-3">
          {history.slice(0, 5).map((item, index) => (
            <div
              key={index}
              className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg"
            >
              <div className="flex items-center gap-4">
                <div className="w-10 h-10 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center">
                  <span className="text-lg font-bold text-purple-600 dark:text-purple-400">
                    {index + 1}
                  </span>
                </div>
                <div>
                  <p className="font-semibold capitalize">{item.emotion}</p>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {new Date(item.timestamp).toLocaleString()}
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-sm text-gray-600 dark:text-gray-400">Satisfaction</p>
                <p className="text-xl font-bold">{item.satisfaction_score.toFixed(1)}/10</p>
              </div>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  )
}