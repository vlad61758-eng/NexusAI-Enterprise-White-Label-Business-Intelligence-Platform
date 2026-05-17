"use client";

import { useState } from "react";
import { Wallet, Loader2, Send, Copy, CheckCircle2 } from "lucide-react";

interface CryptoPaymentProps {
  price: number;
  currency: string;
}

export default function CryptoPayment({ price, currency }: CryptoPaymentProps) {
  const [status, setStatus] = useState<"idle" | "details" | "payment" | "verifying" | "success" | "error">("idle");
  const [email, setEmail] = useState("");
  const [telegram, setTelegram] = useState("");
  const [txHash, setTxHash] = useState("");
  const [copied, setCopied] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  // Placeholder wallet address that you will replace later
  const walletAddress = "TRXYourFutureCryptoWalletAddressHere...";

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

  const handleVerifyTransaction = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!txHash) return;

    setStatus("verifying");

    try {
      // Simulate API call to check blockchain
      const res = await fetch('/api/verify-transaction', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ txHash, email, telegram, expectedAmount: price })
      });

      const data = await res.json();

      if (data.success) {
        setStatus("success");
      } else {
        setStatus("error");
        setErrorMessage(data.message || "Транзакцію не знайдено або сума не співпадає.");
      }
    } catch (err) {
      setStatus("error");
      setErrorMessage("Помилка з'єднання з сервером.");
    }
  };

  if (status === "success") {
    return (
      <div className="flex flex-col items-center justify-center p-6 bg-green-500/10 border border-green-500/20 rounded-xl text-center">
        <div className="w-16 h-16 bg-green-500/20 rounded-full flex items-center justify-center text-green-400 mb-4">
          <CheckCircle2 className="w-8 h-8" />
        </div>
        <h3 className="font-bold text-green-400 mb-2 text-lg">Оплата успішна!</h3>
        <p className="text-sm text-gray-300 mb-2">
          Дякуємо за покупку. Ми автоматично відправили архів та ліцензію на:
        </p>
        <p className="font-semibold text-white mb-1">{email}</p>
        <p className="font-semibold text-white mb-4">{telegram}</p>
        <p className="text-xs text-gray-500">
          Якщо ви не отримаєте файл протягом 5 хвилин, зверніться до нашої підтримки (контакти внизу сайту).
        </p>
      </div>
    );
  }

  if (status === "error") {
    return (
      <div className="flex flex-col items-center justify-center p-6 bg-red-500/10 border border-red-500/20 rounded-xl text-center">
        <h3 className="font-bold text-red-400 mb-2 text-lg">Помилка перевірки</h3>
        <p className="text-sm text-gray-300 mb-4">{errorMessage}</p>
        <button
          onClick={() => setStatus("payment")}
          className="py-2 px-4 bg-white/10 hover:bg-white/20 text-white rounded-lg text-sm transition-colors"
        >
          Спробувати ще раз
        </button>
      </div>
    );
  }

  if (status === "verifying") {
    return (
      <div className="flex flex-col items-center justify-center p-8 bg-white/5 border border-white/10 rounded-xl text-center">
        <Loader2 className="w-10 h-10 text-purple-400 animate-spin mb-4" />
        <h3 className="font-bold text-white mb-2">Шукаємо вашу транзакцію...</h3>
        <p className="text-sm text-gray-400">
          Ми перевіряємо блокчейн на наявність переказу з вашим хешем. Це може зайняти 1-3 хвилини. Не закривайте цю сторінку.
        </p>
      </div>
    );
  }

  if (status === "payment") {
    return (
      <div className="p-6 bg-white/5 border border-white/10 rounded-xl">
        <h3 className="font-bold text-white mb-4">Відправте кошти</h3>
        <p className="text-sm text-gray-400 mb-4">
          Відправте рівно <strong className="text-white">{price} {currency}</strong> на адресу нижче.
          Переконайтесь, що використовуєте правильну мережу (наприклад, TRC20 для USDT).
        </p>

        <div className="mb-6">
          <label className="block text-xs font-medium text-gray-500 mb-2">Адреса гаманця</label>
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
              title="Скопіювати адресу"
            >
              {copied ? <CheckCircle2 className="w-5 h-5" /> : <Copy className="w-5 h-5" />}
            </button>
          </div>
        </div>

        <form onSubmit={handleVerifyTransaction} className="mt-6 pt-6 border-t border-white/10">
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Я відправив кошти. Мій хеш транзакції (TxID):
          </label>
          <input
            type="text"
            required
            value={txHash}
            onChange={(e) => setTxHash(e.target.value)}
            className="w-full bg-black/50 border border-white/10 rounded-lg py-3 px-4 text-sm text-white focus:outline-none focus:border-purple-500 transition-colors mb-4"
            placeholder="Наприклад: a1b2c3d4..."
          />
          <button
            type="submit"
            className="w-full py-4 px-6 bg-purple-600 hover:bg-purple-700 text-white font-bold rounded-xl transition-colors flex items-center justify-center gap-2"
          >
            <Send className="w-5 h-5" />
            Підтвердити оплату
          </button>
        </form>
      </div>
    );
  }

  if (status === "details") {
    return (
      <form onSubmit={handleProceedToPayment} className="p-6 bg-white/5 border border-white/10 rounded-xl space-y-4">
        <h3 className="font-bold text-white mb-2">Куди відправити ваш продукт?</h3>
        <p className="text-xs text-gray-400 mb-4">
          Вкажіть дані, щоб система знала, куди автоматично надіслати архів та ліцензію після перевірки оплати в блокчейні.
        </p>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">Ваш Email *</label>
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
          <label className="block text-sm font-medium text-gray-300 mb-1">Telegram (@username) *</label>
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
          Продовжити до оплати
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
