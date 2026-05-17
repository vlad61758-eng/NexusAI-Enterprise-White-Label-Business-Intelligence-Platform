"use client";

import { useState } from "react";
import { Wallet, Loader2, Send, Copy, CheckCircle2 } from "lucide-react";

interface CryptoPaymentProps {
  price: number;
  currency: string;
}

export default function CryptoPayment({ price, currency }: CryptoPaymentProps) {
  const [status, setStatus] = useState<"idle" | "details" | "payment" | "verifying" | "success">("idle");
  const [email, setEmail] = useState("");
  const [telegram, setTelegram] = useState("");
  const [copied, setCopied] = useState(false);

  // Placeholder wallet address that you will replace later
  const walletAddress = "0xYourFutureCryptoWalletAddressHere...";

  const handleStartPayment = () => {
    setStatus("details");
  };

  const handleProceedToPayment = (e: React.FormEvent) => {
    e.preventDefault();
    if (email && telegram) {
      setStatus("payment");
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(walletAddress);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handlePaid = () => {
    setStatus("verifying");
    // Simulate a longer verification delay (e.g., 5 seconds)
    setTimeout(() => {
      setStatus("success");
    }, 5000);
  };

  if (status === "success") {
    return (
      <div className="flex flex-col items-center justify-center p-6 bg-green-500/10 border border-green-500/20 rounded-xl text-center">
        <div className="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center text-green-400 mb-4">
          <CheckCircle2 className="w-8 h-8" />
        </div>
        <h3 className="font-bold text-green-400 mb-2 text-lg">Transaction Verified!</h3>
        <p className="text-sm text-gray-300 mb-2">
          Thank you for your purchase. We have sent the archive and instructions to:
        </p>
        <p className="font-semibold text-white mb-1">{email}</p>
        <p className="font-semibold text-white mb-4">{telegram}</p>
        <p className="text-xs text-gray-500">
          If you don't receive it within 5 minutes, please contact support.
        </p>
      </div>
    );
  }

  if (status === "verifying") {
    return (
      <div className="flex flex-col items-center justify-center p-8 bg-white/5 border border-white/10 rounded-xl text-center">
        <Loader2 className="w-10 h-10 text-purple-400 animate-spin mb-4" />
        <h3 className="font-bold text-white mb-2">Verifying Transaction</h3>
        <p className="text-sm text-gray-400">
          Please wait while we confirm your payment on the blockchain. This usually takes 1-3 minutes.
        </p>
      </div>
    );
  }

  if (status === "payment") {
    return (
      <div className="p-6 bg-white/5 border border-white/10 rounded-xl">
        <h3 className="font-bold text-white mb-4">Send Payment</h3>
        <p className="text-sm text-gray-400 mb-4">
          Please send exactly <strong className="text-white">{price} {currency}</strong> to the address below.
          Make sure to use the correct network (e.g., ERC20, TRC20) depending on the agreed currency.
        </p>

        <div className="mb-6">
          <label className="block text-xs font-medium text-gray-500 mb-2">Wallet Address</label>
          <div className="flex items-center gap-2">
            <input
              type="text"
              readOnly
              value={walletAddress}
              className="w-full bg-black/50 border border-white/10 rounded-lg py-3 px-4 text-sm text-white focus:outline-none"
            />
            <button
              onClick={copyToClipboard}
              className="p-3 bg-purple-500/20 text-purple-400 hover:bg-purple-500/30 rounded-lg transition-colors flex-shrink-0"
            >
              {copied ? <CheckCircle2 className="w-5 h-5" /> : <Copy className="w-5 h-5" />}
            </button>
          </div>
        </div>

        <button
          onClick={handlePaid}
          className="w-full py-4 px-6 bg-purple-600 hover:bg-purple-700 text-white font-bold rounded-xl transition-colors flex items-center justify-center gap-2"
        >
          <Send className="w-5 h-5" />
          I have sent the payment
        </button>
      </div>
    );
  }

  if (status === "details") {
    return (
      <form onSubmit={handleProceedToPayment} className="p-6 bg-white/5 border border-white/10 rounded-xl space-y-4">
        <h3 className="font-bold text-white mb-2">Delivery Details</h3>
        <p className="text-xs text-gray-400 mb-4">Where should we send your product after payment?</p>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">Email Address *</label>
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full bg-black/50 border border-white/10 rounded-lg py-3 px-4 text-sm text-white focus:outline-none focus:border-purple-500 transition-colors"
            placeholder="you@company.com"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">Telegram Handle *</label>
          <input
            type="text"
            required
            value={telegram}
            onChange={(e) => setTelegram(e.target.value)}
            className="w-full bg-black/50 border border-white/10 rounded-lg py-3 px-4 text-sm text-white focus:outline-none focus:border-purple-500 transition-colors"
            placeholder="@yourhandle"
          />
        </div>

        <button
          type="submit"
          className="w-full mt-4 py-4 px-6 bg-white text-black font-bold rounded-xl hover:bg-gray-200 transition-colors flex items-center justify-center gap-2"
        >
          Continue to Payment
        </button>
      </form>
    );
  }

  return (
    <button
      onClick={handleStartPayment}
      className="w-full py-4 px-6 bg-white text-black font-bold rounded-xl hover:bg-gray-200 transition-colors flex items-center justify-center gap-3"
    >
      <Wallet className="w-5 h-5" />
      Pay {price} {currency} with Crypto
    </button>
  );
}
