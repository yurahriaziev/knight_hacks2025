import Header from "../components/Header";
import { SlidersHorizontal, RefreshCw, Play, Send } from "lucide-react";
import { useState } from "react";

export default function SimulationPage() {
  const [problem, setProblem] = useState(
    "A 5kg box slides down a 40° incline with friction coefficient 0.3."
  );

  const handleUpdate = () => {
    console.log("Problem updated:", problem)
  }

  return (
    <div className="h-screen flex flex-col bg-[#F8FAFC] text-[#0F172A] font-[Poppins] overflow-hidden">
      {/* Header */}
      <Header />

      {/* Main layout */}
      <main className="grid grid-cols-1 lg:grid-cols-2 flex-1 h-full">
        {/* LEFT PANEL */}
        <section className="relative flex flex-col justify-between px-12 py-8 h-full bg-[#F8FAFC] border-r border-[#E2E8F0] gap-y-4">
          {/* Background blobs */}
          <div className="absolute inset-0 overflow-hidden pointer-events-none">
            <div className="absolute top-10 left-10 w-40 h-40 bg-[#2F88FC]/15 rounded-full blur-3xl animate-pulse" />
            <div
              className="absolute bottom-20 right-10 w-60 h-60 bg-[#31E3CB]/15 rounded-full blur-3xl animate-pulse"
              style={{ animationDelay: "1s" }}
            />
          </div>

          {/* TOP SECTION – Editable Problem Text */}
          <div className="relative z-10 flex flex-col justify-center flex-[0.25] border border-[#E2E8F0] bg-white/80 backdrop-blur-md rounded-lg p-6 shadow-sm">
            <h2 className="text-2xl font-semibold flex items-center gap-3 mb-4">
              <SlidersHorizontal className="w-6 h-6 text-[#2F88FC]" />
              Simulation Controls
            </h2>

            <label className="text-sm font-medium text-[#2F88FC] mb-2 block">
              Problem Overview
            </label>
            <textarea
              value={problem}
              onChange={(e) => setProblem(e.target.value)}
              className="w-full h-28 resize-none border border-[#E2E8F0] rounded-xl p-3 text-gray-800 text-base bg-white/70 focus:outline-none focus:ring-2 focus:ring-[#31E3CB]/40 transition"
            />

            <button
              onClick={handleUpdate}
              className="cursor-pointer mt-4 self-start bg-gradient-to-r from-[#2F88FC] to-[#31E3CB] hover:from-[#31E3CB] hover:to-[#2F88FC] text-white font-semibold px-5 py-2.5 rounded-xl text-sm shadow-md hover:shadow-lg transition-all flex items-center gap-2 hover:scale-[1.03]"
            >
              <Send className="w-4 h-4" />
              Update Problem
            </button>
          </div>

          {/* BOTTOM SECTION – Sliders + Buttons */}
          <div className="relative z-10 flex flex-col justify-center flex-[0.75] border border-[#E2E8F0] bg-white/80 backdrop-blur-md rounded-md p-8 shadow-sm">
            {/* Sliders */}
            <div className="space-y-8 mb-10">
              <div>
                <label className="block text-base font-medium mb-1">
                  Mass (kg)
                </label>
                <input
                  type="range"
                  min="1"
                  max="20"
                  defaultValue="5"
                  className="w-full accent-[#31E3CB] h-2 bg-gray-200 rounded-full appearance-none cursor-pointer"
                />
              </div>

              <div>
                <label className="block text-base font-medium mb-1">
                  Incline Angle (°)
                </label>
                <input
                  type="range"
                  min="0"
                  max="90"
                  defaultValue="40"
                  className="w-full accent-[#2F88FC] h-2 bg-gray-200 rounded-full appearance-none cursor-pointer"
                />
              </div>

              <div>
                <label className="block text-base font-medium mb-1">
                  Friction Coefficient
                </label>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.05"
                  defaultValue="0.3"
                  className="w-full accent-[#31E3CB] h-2 bg-gray-200 rounded-full appearance-none cursor-pointer"
                />
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-4">
              <button className="cursor-pointer flex-1 bg-gradient-to-r from-[#2F88FC] to-[#31E3CB] hover:from-[#31E3CB] hover:to-[#2F88FC] text-white font-semibold py-3 rounded-xl text-base shadow-lg hover:shadow-xl transition-all transform hover:scale-[1.03] flex items-center justify-center gap-2">
                <Play className="w-5 h-5" />
                Replay Simulation
              </button>

              <button className="cursor-pointer flex-1 border-2 border-[#2F88FC] text-[#2F88FC] hover:bg-[#2F88FC]/10 font-semibold py-3 rounded-xl transition-all flex items-center justify-center gap-2">
                <RefreshCw className="w-5 h-5" />
                Reset
              </button>
            </div>
          </div>
        </section>

        {/* RIGHT PANEL */}
        <section className="relative flex items-center justify-center h-full bg-[#0F172A] overflow-hidden">
          {/* Dotted grid */}
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_1px_1px,_#31E3CB_1px,_transparent_0)] [background-size:20px_20px] opacity-10 pointer-events-none" />

          {/* Glow effect */}
          <div className="absolute w-64 h-64 bg-gradient-to-r from-[#2F88FC] to-[#31E3CB] blur-[120px] opacity-20" />

          {/* Simulation placeholder */}
          <div className="relative z-10 text-center">
            <h2 className="text-4xl font-bold text-white mb-3">
              3D Simulation View
            </h2>
            <p className="text-gray-300 text-lg max-w-sm mx-auto">
              Once the problem is processed, your interactive visualization will
              appear here.
            </p>
          </div>
        </section>
      </main>
    </div>
  );
}
