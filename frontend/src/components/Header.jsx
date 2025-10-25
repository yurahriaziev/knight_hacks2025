import { Sparkles } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function Header() {
    const navigate = useNavigate()

    return (
        <header className="relative z-10 border-b border-[#E2E8F0]/50 backdrop-blur-sm bg-white/70">
            <div className="container mx-auto px-6 py-4 flex items-center justify-between">
            <div onClick={() => navigate('/')} className="cursor-pointer flex items-center gap-3">
                <div className="w-10 h-10 bg-[#2F88FC] rounded-xl flex items-center justify-center rotate-3 hover:rotate-6 transition-transform">
                <Sparkles className="w-6 h-6 text-white" />
                </div>
                <h1 className="text-2xl font-bold text-[#0F172A]">Visigen</h1>
            </div>

            <p className="text-sm md:text-base text-[#31E3CB] font-medium italic hidden sm:block">
                Turning word problems into simulations ✨
            </p>
            </div>
        </header>
    )
}