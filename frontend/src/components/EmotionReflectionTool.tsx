"use client"

import type React from "react"

import { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent } from "@/components/ui/card"
import { Loader2, Heart, Sparkles, ArrowRight } from "lucide-react"

interface EmotionResult {
  emotion: string
  confidence: number
}

export default function EmotionReflectionTool() {
  const [isStarted, setIsStarted] = useState(false)
  const [text, setText] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<EmotionResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleStart = () => {
    setIsStarted(true)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!text.trim()) return

    setIsLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: text.trim() }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.message || errorData.detail || "Failed to analyze emotion")
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }

  const handleReset = () => {
    setText("")
    setResult(null)
    setError(null)
    setIsStarted(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-gray-100 to-gray-200 px-4 py-8">
      <div className="max-w-2xl mx-auto">
        <AnimatePresence mode="wait">
          {!isStarted ? (
            <motion.div
              key="hero"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.6 }}
              className="text-center space-y-8 pt-20"
            >
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.2, duration: 0.6 }}
                className="space-y-4"
              >

                <h1 className="text-4xl md:text-6xl font-bold text-black">
                  Emotion Reflection
                </h1>

                <p className="text-lg md:text-xl text-gray-600 max-w-lg mx-auto leading-relaxed">
                  Share your thoughts and discover the emotions behind your words with AI-powered analysis
                </p>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4, duration: 0.6 }}
              >
                <Button
                  onClick={handleStart}
                  size="lg"
                  className="bg-black hover:bg-gray-800 text-white px-8 py-6 text-lg rounded-full shadow-lg hover:shadow-xl transition-all duration-300 group"
                >
                  <span className="mr-2">Try it out</span>
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </Button>
              </motion.div>

              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.6, duration: 0.8 }}
                className="flex justify-center space-x-2 pt-8"
              >
                {[...Array(3)].map((_, i) => (
                  <motion.div
                    key={i}
                    animate={{
                      y: [0, -10, 0],
                      opacity: [0.4, 1, 0.4],
                    }}
                    transition={{
                      duration: 1.5,
                      repeat: Number.POSITIVE_INFINITY,
                      delay: i * 0.2,
                    }}
                  >
                    <Sparkles className="w-4 h-4 text-gray-400" />
                  </motion.div>
                ))}
              </motion.div>
            </motion.div>
          ) : (
            <motion.div
              key="app"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="space-y-8"
            >
              {/* Compact Header */}
              <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: 0.2, duration: 0.5 }}
                className="text-center space-y-2"
              >
                <h1 className="text-2xl md:text-3xl font-bold text-black">
                  Emotion Reflection
                </h1>
                <p className="text-gray-600">Share your thoughts and discover your emotions</p>
              </motion.div>

              {/* Main Form */}
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4, duration: 0.6 }}
              >
                <Card className="shadow-xl border-0 bg-white/80 backdrop-blur-sm">
                  <CardContent className="p-6 space-y-6">
                    <form onSubmit={handleSubmit} className="space-y-4">
                      <div className="space-y-2">
                        <label htmlFor="reflection" className="text-sm font-medium text-gray-700">
                          How are you feeling? Share your thoughts...
                        </label>
                        <Textarea
                          id="reflection"
                          placeholder="I feel nervous about my first job interview..."
                          value={text}
                          onChange={(e) => setText(e.target.value)}
                          className="min-h-32 resize-none border-gray-200 focus:border-black focus:ring-black transition-colors"
                          disabled={isLoading}
                        />
                      </div>

                      <div className="flex gap-3">
                        <Button
                          type="submit"
                          disabled={!text.trim() || isLoading}
                          className="flex-1 bg-black hover:bg-gray-800 disabled:opacity-50 transition-all duration-300 text-white"
                        >
                          {isLoading ? (
                            <>
                              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                              Analyzing...
                            </>
                          ) : (
                            "Analyze Emotion"
                          )}
                        </Button>

                        <Button
                          type="button"
                          variant="outline"
                          onClick={handleReset}
                          className="px-6 hover:bg-gray-50 transition-colors bg-transparent border-black text-black hover:text-black"
                        >
                          Reset
                        </Button>
                      </div>
                    </form>

                    {/* Error State */}
                    <AnimatePresence>
                      {error && (
                        <motion.div
                          initial={{ opacity: 0, scale: 0.95 }}
                          animate={{ opacity: 1, scale: 1 }}
                          exit={{ opacity: 0, scale: 0.95 }}
                          className="p-4 bg-red-50 border border-red-200 rounded-lg"
                        >
                          <p className="text-red-700 text-sm">{error}</p>
                        </motion.div>
                      )}
                    </AnimatePresence>

                    {/* Results */}
                    <AnimatePresence>
                      {result && (
                        <motion.div
                          initial={{ opacity: 0, y: 20, scale: 0.95 }}
                          animate={{ opacity: 1, y: 0, scale: 1 }}
                          exit={{ opacity: 0, y: -20, scale: 0.95 }}
                          transition={{ duration: 0.5 }}
                          className="space-y-4"
                        >
                          <div className="h-px bg-gradient-to-r from-transparent via-gray-200 to-transparent" />

                          <div className="text-center space-y-4">
                            <h3 className="text-lg font-semibold text-gray-800">Emotion Analysis</h3>

                            <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-6 space-y-4">
                              <motion.div
                                initial={{ scale: 0 }}
                                animate={{ scale: 1 }}
                                transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
                                className="text-center"
                              >
                                <div className="text-3xl font-bold text-black">
                                  {result.emotion}
                                </div>
                              </motion.div>

                              <div className="space-y-2">
                                <div className="flex justify-between text-sm text-gray-600">
                                  <span>Confidence</span>
                                  <span>{Math.round(result.confidence * 100)}%</span>
                                </div>
                                <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                                  <motion.div
                                    initial={{ width: 0 }}
                                    animate={{ width: `${result.confidence * 100}%` }}
                                    transition={{ delay: 0.5, duration: 1, ease: "easeOut" }}
                                    className="h-full bg-black rounded-full"
                                  />
                                </div>
                              </div>
                            </div>
                          </div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </CardContent>
                </Card>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
} 