# صف نوبت آزمایشگاه

برای اجرای تست‌ها از ریشهٔ مخزن وارد پوشهٔ `part2` می‌شوم.

```bash
cd part2
python -m pip install -r requirements-dev.txt
pytest
```

برای اجرا، `cp .env.example .env` و سپس `docker compose up --build` را می‌زنم. فایل Collection در پوشهٔ `postman` است. در Postman مقدار `baseUrl` را روی `http://localhost:18000` می‌گذارم. تنظیم `APP_PORT` در `.env` باید با همین آدرس هماهنگ باشد.

`GET /health` وضعیت سرویس را نشان می‌دهد. با `POST /join` و بدنهٔ `{"name": "Ali"}` نوبت می‌گیرم و با `POST /next` نفر اول صف را خارج می‌کنم. فایل صف در volume به نام `queue-data` قرار دارد.
