import { useState } from "react";
import Header from "../components/Header";

export default function LandingPage() {
  const [problem, setProblem] = useState("");

  const handleExample = () => {
    setProblem("A 5kg box slides down a 40° incline with friction.");
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#F5F5F5] relative overflow-hidden">
      {/* Dotted Background */}
      <Header />
      <div className=" inset-0 bg-[radial-gradient(circle_at_1px_1px,_#d4d4d4_1px,_transparent_0)] [background-size:16px_16px] opacity-40 pointer-events-none" />

      {/* Header */}

      {/* Main Section */}
      <main className="flex flex-col items-center justify-center flex-1 px-6 text-center relative z-10">
        {/* Tagline */}
        <h2 className="text-4xl font-extrabold text-[#41514E] mb-3 animate-fade-in-down">
          Visualize Your Physics Problem
        </h2>
        <p className="text-[#2F88FC] mb-8 max-w-xl text-lg">
          Transform complex word problems into interactive 3D simulations
        </p>

        {/* Floating Card */}
        <div className="bg-white/70 backdrop-blur-sm border border-[#31E3CB]/30 rounded-2xl shadow-xl p-6 w-full max-w-xl">
          <textarea
            placeholder="e.g. A 5kg box slides down a 40° incline..."
            value={problem}
            onChange={(e) => setProblem(e.target.value)}
            className="w-full h-40 p-4 rounded-lg border-2 border-[#2F88FC]/40 focus:border-[#31E3CB] focus:ring-4 focus:ring-[#31E3CB]/30 bg-white/70 text-gray-800 resize-none placeholder-gray-400 transition"
          />

          <div className="flex items-center justify-between mt-4">
            <button
              onClick={handleExample}
              className="px-3 py-1 text-sm rounded-full bg-[#31E3CB]/20 text-[#41514E] font-medium hover:bg-[#31E3CB]/30 transition"
            >
              Try Example
            </button>

            <button className="bg-gradient-to-r from-[#2F88FC] to-[#31E3CB] hover:from-[#31E3CB] hover:to-[#2F88FC] text-white font-semibold px-8 py-3 rounded-lg shadow-lg hover:shadow-xl hover:scale-105 transition-all">
              See My Problem
            </button>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="text-center text-sm text-[#41514E]/70 py-4 relative z-10">
        Built with 💡 FastAPI × React × Tailwind
      </footer>
    </div>
  );
}
