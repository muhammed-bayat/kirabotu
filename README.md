# Telegram Kira Botu

Bu Telegram botu, bir grup insan arasında kira ödemelerini takip etmek için kullanılabilir. Bot, ödeme kaydını tutar, borçları hesaplar ve aylık raporlar gönderir.

## Kullanım

1. Telegram'da [@BotFather](https://t.me/botfather)'a mesaj göndererek bir bot oluşturun.
2. `config.py.sample` dosyasının adını `config.py` olarak değiştirin ve botunuzun API anahtarını (`TOKEN`) ekleyin.
3. `pip install -r requirements.txt` komutunu kullanarak gerekli Python paketlerini yükleyin.
4. `python main.py` komutuyla botu çalıştırın.

## Komutlar

- `/start` - Botu başlatmak için kullanılır.
- `/pay` - Ödeme yapmak için kullanılır. Ödeme miktarı ve açıklaması girilmesi gerekiyor. Örnek: `/pay 250 market alışverişi`
- `/list_users` - Tüm kullanıcıları listeler.
- `/monthly_report` - Aylık rapor gönderir.
- `/summary` - Kullanıcının ödeme geçmişini görüntüler.
