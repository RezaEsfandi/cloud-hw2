# صف نوبت آزمایشگاه

برای اجرای تست‌ها از ریشهٔ مخزن وارد پوشهٔ `part2` می‌شوم.

```bash
cd part2
python -m pip install -r requirements-dev.txt
pytest
```

برای اجرا، `cp .env.example .env` و سپس `docker compose up --build` را می‌زنم. همین فایل بالا آوردن سه نمونه را هم پشتیبانی می‌کند. فایل Collection در پوشهٔ `postman` است. در Postman مقدار `baseUrl` را روی `http://localhost:18000` می‌گذارم. تنظیم `APP_PORT` در `.env` باید با همین آدرس هماهنگ باشد.

`GET /health` وضعیت سرویس را نشان می‌دهد. با `POST /join` و بدنهٔ `{"name": "Ali"}` نوبت می‌گیرم و با `POST /next` نفر اول صف را خارج می‌کنم. فایل صف در volume به نام `queue-data` قرار دارد.

### آزمایش سه نمونه

از داخل `part2` ابتدا `cp .env.example .env` را اجرا می‌کنم و سپس سرویس را با سه نمونه بالا می‌آورم.

```bash
docker compose up -d --build --scale app=3
docker compose ps
docker compose logs proxy
```

برای آزمایش از پروژهٔ Compose جدا و صف خالی استفاده می‌کنم. این اجرا از پورت دیگری استفاده می‌کند تا با سرویس اصلی تداخل پیدا نکند.

```bash
APP_PORT=18001 docker compose -p cc-hw2-race up -d --build --scale app=3
python3 tools/concurrent_join.py --url http://localhost:18001 --drain
python3 tools/concurrent_join.py --url http://localhost:18001 --concurrent-next
```

خروجی هر دو آزمایش باید `"passed": true` داشته باشد. اجرای اول ۲۰۰ شمارهٔ نوبت و ۲۰۰ نام را بررسی می‌کند. اجرای دوم برداشت هم‌زمان و پاسخ `404 empty` پس از آخرین برداشت را می‌سنجد.
