import { useState, useEffect } from "react";
import { DotLottieReact } from "@lottiefiles/dotlottie-react";

export default function Loader() {
  const messages = [
    "Understanding your problem...",
    "Building your scene...",
    "Making things right..."
  ];
  const [index, setIndex] = useState(0);

  // Loop through messages every 2.5s
  useEffect(() => {
    const interval = setInterval(() => {
      setIndex((prev) => (prev + 1) % messages.length);
    }, 2500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col items-center justify-center w-full h-full text-center">
      {/* Fading text */}
      <div className="h-6 mb-4">
        <p
          key={index}
          className="text-[#E2E8F0] text-lg tracking-wide transition-opacity duration-700 ease-in-out opacity-100 animate-fade"
        >
          {messages[index]}
        </p>
      </div>

      {/* Animation container */}
      <div className="flex items-center justify-center w-[400px] h-[400px] mx-auto">
        <DotLottieReact
          src="https://lottie.host/b5ff881e-9ba9-4dc4-92a6-eab85eb5bfe4/ycXX0i69go.lottie"
          loop
          autoplay
          style={{ width: "100%", height: "100%" }}
        />
      </div>
    </div>
  );
}
