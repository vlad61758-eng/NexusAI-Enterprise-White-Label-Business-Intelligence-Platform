#!/bin/bash
echo "========================================"
echo "🚀 Розпочинаємо встановлення Premium CRM Bot..."
echo "========================================"

# Перевірка наявності файлів конфігурації
if [ ! -f "config.env" ]; then
    echo "❌ Помилка: Не знайдено файл config.env"
    echo "Будь ласка, створіть config.env, додайте туди BOT_TOKEN і повторіть спробу."
    exit 1
fi

echo "📦 Оновлення пакетів та встановлення Python..."
sudo apt update -y
sudo apt install python3 python3-pip python3-venv -y

echo "🐍 Створення віртуального середовища..."
python3 -m venv venv
source venv/bin/activate

echo "📚 Встановлення залежностей..."
pip install --upgrade pip
pip install -r requirements.txt

# Шляхи для сервісу
BOT_DIR=$(pwd)
SERVICE_FILE="/etc/systemd/system/premium_crm_bot.service"
USER_NAME=$(whoami)

echo "⚙️ Створення systemd сервісу для безперебійної роботи (24/7)..."
sudo bash -c "cat > $SERVICE_FILE" <<EOF
[Unit]
Description=Premium CRM Telegram Bot
After=network.target

[Service]
User=$USER_NAME
WorkingDirectory=$BOT_DIR
ExecStart=$BOT_DIR/venv/bin/python $BOT_DIR/bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

echo "🔄 Перезавантаження systemd та запуск бота..."
sudo systemctl daemon-reload
sudo systemctl enable premium_crm_bot
sudo systemctl start premium_crm_bot

echo "========================================"
echo "✅ Встановлення успішно завершено!"
echo "Ваш бот працює у фоновому режимі."
echo "Щоб переглянути логи бота, використовуйте команду:"
echo "sudo journalctl -u premium_crm_bot -f"
echo "========================================"
