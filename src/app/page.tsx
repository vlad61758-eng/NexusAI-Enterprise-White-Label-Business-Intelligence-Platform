import { products } from "@/lib/products";
import Link from "next/link";
import { ArrowRight, Zap, Shield, Sparkles } from "lucide-react";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#0a0a0a] text-white selection:bg-purple-500/30">
      {/* Hero Section */}
      <div className="relative overflow-hidden pt-32 pb-20 lg:pt-48 lg:pb-32">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-[1000px] h-[500px] bg-purple-600/20 blur-[120px] rounded-full pointer-events-none" />

        <div className="container mx-auto px-4 relative z-10 text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 backdrop-blur-sm mb-8">
            <Sparkles className="w-4 h-4 text-purple-400" />
            <span className="text-sm font-medium text-gray-300">Next-Gen AI Solutions</span>
          </div>

          <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-8 bg-gradient-to-b from-white to-gray-400 bg-clip-text text-transparent">
            Automate Your Business<br />With Premium AI
          </h1>

          <p className="text-lg md:text-xl text-gray-400 max-w-2xl mx-auto mb-12">
            Unlock 10x growth with our ready-to-use, high-ticket AI bots and micro-SaaS products. Built for B2B excellence.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <a href="#products" className="px-8 py-4 rounded-xl bg-white text-black font-semibold hover:bg-gray-100 transition-colors flex items-center gap-2">
              Explore Products <ArrowRight className="w-5 h-5" />
            </a>
            <div className="flex items-center gap-2 text-gray-400 px-8 py-4">
              <Shield className="w-5 h-5" /> Instant Delivery
            </div>
          </div>
        </div>
      </div>

      {/* Features */}
      <div className="border-y border-white/5 bg-white/[0.02]">
        <div className="container mx-auto px-4 py-12">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div className="flex flex-col items-center gap-3">
              <div className="w-12 h-12 rounded-full bg-purple-500/10 flex items-center justify-center text-purple-400 mb-2">
                <Zap className="w-6 h-6" />
              </div>
              <h3 className="font-semibold text-lg">Plug & Play</h3>
              <p className="text-gray-400 text-sm">Deploy in minutes, not months.</p>
            </div>
            <div className="flex flex-col items-center gap-3">
              <div className="w-12 h-12 rounded-full bg-blue-500/10 flex items-center justify-center text-blue-400 mb-2">
                <Shield className="w-6 h-6" />
              </div>
              <h3 className="font-semibold text-lg">Secure & Private</h3>
              <p className="text-gray-400 text-sm">Your data and API keys stay yours.</p>
            </div>
            <div className="flex flex-col items-center gap-3">
              <div className="w-12 h-12 rounded-full bg-green-500/10 flex items-center justify-center text-green-400 mb-2">
                <Sparkles className="w-6 h-6" />
              </div>
              <h3 className="font-semibold text-lg">Premium Quality</h3>
              <p className="text-gray-400 text-sm">Enterprise-grade code & architecture.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Products Grid */}
      <div id="products" className="container mx-auto px-4 py-32">
        <div className="flex items-center justify-between mb-16">
          <h2 className="text-3xl md:text-5xl font-bold">Featured AI Solutions</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((product) => (
            <Link
              href={`/product/${product.id}`}
              key={product.id}
              className="group relative block p-[1px] rounded-2xl bg-gradient-to-b from-white/10 to-white/5 hover:from-purple-500/50 hover:to-blue-500/50 transition-all duration-500"
            >
              <div className="absolute inset-0 bg-gradient-to-b from-purple-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity rounded-2xl" />

              <div className="relative h-full bg-[#0a0a0a] rounded-2xl p-6 flex flex-col backdrop-blur-xl">
                {product.bestseller && (
                  <div className="absolute top-0 right-6 -translate-y-1/2 px-3 py-1 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full text-xs font-bold tracking-wide shadow-lg shadow-purple-500/20">
                    BESTSELLER
                  </div>
                )}

                <div className="w-12 h-12 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center mb-6 text-2xl group-hover:scale-110 transition-transform">
                  🤖
                </div>

                <h3 className="text-xl font-bold mb-2 group-hover:text-purple-400 transition-colors">
                  {product.name}
                </h3>

                <p className="text-gray-400 text-sm mb-8 flex-grow">
                  {product.shortDescription}
                </p>

                <div className="flex items-center justify-between mt-auto pt-6 border-t border-white/5">
                  <div className="text-2xl font-bold">
                    ${product.price} <span className="text-sm font-normal text-gray-500">{product.currency}</span>
                  </div>
                  <div className="w-10 h-10 rounded-full bg-white/5 flex items-center justify-center group-hover:bg-white group-hover:text-black transition-colors">
                    <ArrowRight className="w-5 h-5" />
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-white/10 py-12 text-center text-gray-500">
        <p>© 2026 AI Premium Store. All rights reserved.</p>
      </footer>
    </main>
  );
}
