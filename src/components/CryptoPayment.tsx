"use client";

import { useState } from "react";
import { Wallet, Loader2, Download } from "lucide-react";

interface CryptoPaymentProps {
  price: number;
  currency: string;
}

export default function CryptoPayment({ price, currency }: CryptoPaymentProps) {
  const [status, setStatus] = useState<"idle" | "connecting" | "paying" | "success">("idle");

  const handlePayment = async () => {
    if (status === "idle") {
      setStatus("connecting");
      // Mock wallet connection
      await new Promise(resolve => setTimeout(resolve, 1000));
      setStatus("paying");
      // Mock transaction
      await new Promise(resolve => setTimeout(resolve, 2000));
      setStatus("success");
    }
  };

  if (status === "success") {
    return (
      <div className="flex flex-col items-center justify-center p-6 bg-green-500/10 border border-green-500/20 rounded-xl">
        <div className="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center text-white mb-4">
          <Download className="w-6 h-6" />
        </div>
        <h3 className="font-bold text-green-400 mb-2">Payment Successful!</h3>
        <p className="text-sm text-gray-400 text-center mb-4">
          Your files are ready. Redirecting to download page...
        </p>
        <button
          className="w-full py-3 bg-green-500 hover:bg-green-600 text-white font-bold rounded-xl transition-colors"
          onClick={() => alert("Downloading archive... (Mock)")}
        >
          Download Now
        </button>
      </div>
    );
  }

  return (
    <button
      onClick={handlePayment}
      disabled={status !== "idle"}
      className="w-full py-4 px-6 bg-white text-black font-bold rounded-xl hover:bg-gray-200 transition-colors flex items-center justify-center gap-3 disabled:opacity-70"
    >
      {status === "idle" && (
        <>
          <Wallet className="w-5 h-5" />
          Pay ${price} ${currency} with Crypto (Web3)
        </>
      )}
      {status === "connecting" && (
        <>
          <Loader2 className="w-5 h-5 animate-spin" />
          Connecting Wallet...
        </>
      )}
      {status === "paying" && (
        <>
          <Loader2 className="w-5 h-5 animate-spin" />
          Confirming Transaction...
        </>
      )}
    </button>
  );
}
