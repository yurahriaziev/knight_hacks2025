import { useState } from "react";
import { Zap, Rocket, Sparkles, ArrowRight } from "lucide-react";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header";

export default function LandingPage() {
  const [problem, setProblem] = useState("")
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-[#F8FAFC] text-[#0F172A] relative overflow-hidden font-[Poppins]">
      {/* Decorative Blobs */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-20 left-10 w-32 h-32 bg-[#2F88FC]/20 rounded-full blur-3xl animate-pulse" />
        <div
          className="absolute top-40 right-20 w-40 h-40 bg-[#31E3CB]/20 rounded-full blur-3xl animate-pulse"
          style={{ animationDelay: "1s" }}
        />
        <div
          className="absolute bottom-20 left-1/4 w-36 h-36 bg-[#2F88FC]/10 rounded-full blur-3xl animate-pulse"
          style={{ animationDelay: "2s" }}
        />
      </div>

      {/* Header */}
      <Header />

      {/* Main Content */}
      <main className="relative z-10 container mx-auto px-4 py-12 md:py-10">
        <div className="max-w-4xl mx-auto">
          {/* Hero Section */}
          <div className="text-center mb-12 space-y-6">
            {/* Floating Tag */}
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-[#2F88FC]/10 text-[#2F88FC] rounded-full text-sm font-medium mb-4">
              <Zap className="w-4 h-4" />
              <span>Physics made visual</span>
            </div>

            {/* Hero Title */}
            <h2 className="text-4xl md:text-6xl lg:text-7xl font-bold leading-tight">
              See your{" "}
              <span className="relative text-[#2F88FC] inline-block">
                physics problems
                <svg
                  className="absolute -bottom-2 left-0 w-full"
                  viewBox="0 0 200 12"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M2 10C50 2 150 2 198 10"
                    stroke="#31E3CB"
                    strokeWidth="3"
                    strokeLinecap="round"
                  />
                </svg>
              </span>{" "}
              come to life
            </h2>

            {/* Description */}
            <p className="text-lg md:text-xl text-[#475569] max-w-2xl mx-auto">
              Just describe your physics problem and watch it transform into an
              interactive simulation. No more confusing diagrams or abstract
              concepts! 🚀
            </p>
          </div>

          {/* Input Card */}
          <div className="relative max-w-3xl mx-auto">
            {/* Floating decoration blocks */}
            <div className="absolute -top-6 -left-6 w-12 h-12 bg-[#31E3CB]/30 rounded-2xl rotate-12 opacity-30 hidden md:block" />
            <div className="absolute -bottom-4 -right-4 w-16 h-16 bg-[#2F88FC]/20 rounded-2xl -rotate-12 opacity-30 hidden md:block" />

            <div className="relative bg-white border border-[#E2E8F0] rounded-3xl p-6 md:p-8 shadow-xl hover:shadow-2xl transition-shadow">
              <div className="space-y-6">
                {/* Label */}
                <div className="space-y-3 text-left">
                  <label
                    htmlFor="problem"
                    className="text-lg font-semibold flex items-center gap-2 text-[#0F172A]"
                  >
                    <Rocket className="w-5 h-5 text-[#2F88FC]" />
                    Describe your physics problem
                  </label>
                  <textarea
                    id="problem"
                    placeholder="e.g., A 5kg box slides down a 40° incline with friction coefficient 0.3..."
                    value={problem}
                    onChange={(e) => setProblem(e.target.value)}
                    className="w-full min-h-[180px] border-2 border-[#E2E8F0] focus:border-[#2F88FC] rounded-2xl p-4 text-gray-700 resize-none focus:ring-2 focus:ring-[#31E3CB]/30 outline-none transition"
                  />
                </div>

                {/* Button */}
                <button
                    onClick={() => navigate('/simulate')}
                  className="cursor-pointer w-full bg-gradient-to-r from-[#2F88FC] to-[#31E3CB] hover:from-[#31E3CB] hover:to-[#2F88FC] text-white font-semibold py-4 rounded-2xl text-lg shadow-lg hover:shadow-xl transition-all transform hover:scale-[1.02]"
                >
                  See My Problem in Action
                  <ArrowRight className="inline-block w-5 h-5 ml-2" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
