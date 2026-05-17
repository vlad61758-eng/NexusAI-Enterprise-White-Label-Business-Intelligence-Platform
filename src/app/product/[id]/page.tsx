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

            {/* Main Visual / Image Placeholder */}
            <div className="aspect-video bg-black border border-white/10 rounded-2xl relative overflow-hidden group">
              {/* This is a placeholder image from Unsplash suitable for code/AI projects */}
              {/* Replace the 'src' with your actual video or dashboard screenshot later */}
              <img
                src={`https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&q=80&w=1200&h=675`}
                alt={`${product.name} Interface`}
                className="w-full h-full object-cover opacity-80"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent" />
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
              <h2 className="text-2xl font-bold mb-8 flex items-center gap-2">
                <Terminal className="w-6 h-6 text-purple-400" /> What&apos;s inside
              </h2>

              <div className="space-y-10">
                {/* Core Features */}
                <div>
                  <h3 className="text-xl font-semibold text-white mb-4 border-b border-white/10 pb-2">Core Features</h3>
                  <ul className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {product.features.map((feature, i) => (
                      <li key={i} className="flex items-start gap-3 text-gray-400 bg-white/5 p-4 rounded-xl border border-white/5">
                        <CheckCircle2 className="w-5 h-5 text-green-400 shrink-0 mt-0.5" />
                        <span className="text-sm">{feature}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Included Files */}
                <div>
                  <h3 className="text-xl font-semibold text-white mb-4 border-b border-white/10 pb-2">Included in Archive</h3>
                  <div className="flex flex-wrap gap-3">
                    {product.includedFiles.map((file, i) => (
                      <div key={i} className="px-4 py-2 bg-purple-500/10 border border-purple-500/20 text-purple-300 rounded-lg text-sm font-mono flex items-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path><polyline points="14 2 14 8 20 8"></polyline></svg>
                        {file}
                      </div>
                    ))}
                  </div>
                </div>

                {/* Quick Start */}
                <div>
                  <h3 className="text-xl font-semibold text-white mb-4 border-b border-white/10 pb-2">Quick Start Guide</h3>
                  <div className="space-y-3">
                    {product.setupInstructions.map((step, i) => (
                      <div key={i} className="flex items-start gap-4 p-4 bg-black/40 border border-white/5 rounded-xl">
                        <div className="flex items-center justify-center w-8 h-8 rounded-full bg-white/10 text-white font-bold text-sm shrink-0">
                          {i + 1}
                        </div>
                        <p className="text-gray-300 text-sm mt-1">{step}</p>
                      </div>
                    ))}
                  </div>
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
