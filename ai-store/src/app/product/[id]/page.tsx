import { products } from "@/lib/products";
import Link from "next/link";
import { ArrowLeft, CheckCircle2, Play, Terminal } from "lucide-react";
import CryptoPayment from "@/components/CryptoPayment";
import { notFound } from "next/navigation";

export default function ProductPage({ params }: { params: { id: string } }) {
  const product = products.find(p => p.id === params.id);

  if (!product) {
    notFound();
  }

  return (
    <main className="min-h-screen bg-[#0a0a0a] text-white selection:bg-purple-500/30 pb-20">
      {/* Header */}
      <header className="border-b border-white/10 bg-[#0a0a0a]/80 backdrop-blur-md sticky top-0 z-50">
        <div className="container mx-auto px-4 h-16 flex items-center">
          <Link href="/" className="text-gray-400 hover:text-white flex items-center gap-2 transition-colors">
            <ArrowLeft className="w-5 h-5" /> Back to Store
          </Link>
        </div>
      </header>

      <div className="container mx-auto px-4 pt-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">

          {/* Main Content */}
          <div className="lg:col-span-2 space-y-12">
            <div>
              <h1 className="text-4xl md:text-5xl font-bold mb-4">{product.name}</h1>
              <p className="text-xl text-gray-400">{product.description}</p>
            </div>

            {/* Video Placeholder */}
            <div className="aspect-video bg-white/5 border border-white/10 rounded-2xl flex flex-col items-center justify-center group cursor-pointer relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
              <div className="w-20 h-20 bg-purple-600 rounded-full flex items-center justify-center z-10 group-hover:scale-110 transition-transform shadow-[0_0_30px_rgba(147,51,234,0.5)]">
                <Play className="w-8 h-8 text-white ml-2" />
              </div>
              <span className="mt-4 text-gray-300 font-medium z-10">Watch Demo &quot;How it works&quot;</span>
            </div>

            {/* Screenshots Placeholder */}
            <div>
              <h2 className="text-2xl font-bold mb-6">Interface Screenshots</h2>
              <div className="grid grid-cols-2 gap-4">
                <div className="aspect-[4/3] bg-white/5 rounded-xl border border-white/10 flex items-center justify-center text-gray-500">
                  Dashboard View
                </div>
                <div className="aspect-[4/3] bg-white/5 rounded-xl border border-white/10 flex items-center justify-center text-gray-500">
                  Settings / Logs
                </div>
              </div>
            </div>

            {/* What's Inside & Instructions */}
            <div className="bg-white/[0.02] border border-white/5 rounded-2xl p-8">
              <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
                <Terminal className="w-6 h-6 text-purple-400" /> What&apos;s inside
              </h2>

              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-200 mb-3">Core Features:</h3>
                  <ul className="space-y-3">
                    {product.features.map((feature, i) => (
                      <li key={i} className="flex items-start gap-3 text-gray-400">
                        <CheckCircle2 className="w-5 h-5 text-green-400 shrink-0 mt-0.5" />
                        {feature}
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="pt-6 border-t border-white/10">
                  <h3 className="text-lg font-semibold text-gray-200 mb-3">Quick Start:</h3>
                  <p className="text-gray-400 font-mono text-sm bg-black/50 p-4 rounded-lg border border-white/10">
                    {product.setupInstructions}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Sidebar / Checkout */}
          <div className="lg:col-span-1">
            <div className="sticky top-24 bg-gradient-to-b from-white/10 to-white/5 border border-white/10 rounded-2xl p-6 backdrop-blur-xl">
              <div className="text-sm font-medium text-purple-400 mb-2">Lifetime Access</div>
              <div className="text-5xl font-bold mb-6">
                ${product.price} <span className="text-lg text-gray-500 font-normal">{product.currency}</span>
              </div>

              <div className="space-y-4 mb-8">
                <div className="flex items-center gap-2 text-sm text-gray-300">
                  <CheckCircle2 className="w-4 h-4 text-green-400" /> Full source code / executable
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-300">
                  <CheckCircle2 className="w-4 h-4 text-green-400" /> ReadMe & Video Instructions
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-300">
                  <CheckCircle2 className="w-4 h-4 text-green-400" /> Lifetime Updates
                </div>
              </div>

              <CryptoPayment price={product.price} currency={product.currency} />

              <div className="mt-4 text-center text-xs text-gray-500">
                Secured via Web3 & Smart Contracts
              </div>
            </div>
          </div>

        </div>
      </div>
    </main>
  );
}
