# Report Automation (Monthly Ads Reporting)

Tool tự động lấy dữ liệu từ Meta Ads, Google Ads, TikTok Ads, chuẩn hóa và lưu vào BigQuery, sau đó tạo Google Sheet report, cập nhật Metabase dashboard, và xuất Google Slides theo template mỗi tháng.

## Tính năng chính
- Chu kỳ báo cáo theo tháng dương lịch.
- Chuẩn hóa dữ liệu đa nền tảng về schema thống nhất.
- Lưu dữ liệu vào BigQuery (`ads_daily_fact`, `ads_monthly_summary`).
- Tạo Google Sheet report theo template.
- Xuất Google Slides theo template.
- Mỗi khách hàng có folder/report riêng.

## Cấu trúc thư mục
- `src/report_automation`: mã nguồn chính
- `config/clients.example.yaml`: mẫu cấu hình khách hàng
- `sql/`: schema BigQuery

## Thiết lập nhanh
1. Tạo virtual env và cài dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Chuẩn bị service account JSON và set env:
   - `GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json`
3. Tạo file cấu hình khách hàng:
   - copy `config/clients.example.yaml` -> `config/clients.yaml`
   - hoặc dùng form: `report-automation init-config --output config/clients.yaml`
4. Tạo file credentials Ads:
   - copy `config/ads_credentials.form.yaml` -> `config/ads_credentials.yaml`
5. Chạy job (mặc định lấy tháng trước):
   ```bash
   report-automation run --config config/clients.yaml --credentials config/ads_credentials.yaml
   ```

## Demo data (giả lập)
Đặt biến môi trường `DEMO_DATA=1` để sinh dữ liệu giả lập từ 3 nền tảng mà không cần gọi API:
```bash
DEMO_DATA=1 report-automation run --config config/clients.yaml --credentials config/ads_credentials.yaml
```

## Chạy theo lịch (Cloud Run Jobs + Scheduler)
- Deploy batch job bằng `scripts/deploy_cloud_run.sh`.
- Cloud Scheduler trigger vào 02:00 AM ngày 1 hằng tháng (giờ VN), gọi Cloud Run Jobs API.
- `JOB_ARGS` mặc định: `run,--config,config/clients.yaml,--credentials,config/ads_credentials.yaml`.

## Mẫu template theo objective
Thiết lập `objective` trong `config/clients.yaml` để hệ thống tự tạo template mẫu:
- `ecom`: tập trung Revenue/ROAS/Orders/AOV
- `lead`: tập trung Leads/CPL/Quality
- `branding`: tập trung Reach/Impressions/CPM/Video Views
- `social`: tập trung Engagement/ER/Community

Nếu bạn muốn dùng template riêng, hãy điền `sheet_template_id` và `slides_template_id`. Nếu để trống, hệ thống sẽ tự tạo template theo `objective`.

## Web Admin (Next.js + Postgres + Metabase)
Thư mục `web/` chứa app quản trị:
- Auth: email/password (admin)
- Quản lý khách hàng, templates, lịch chạy, logs
- Embed Metabase dashboard theo từng client

Thiết lập nhanh:
1. Copy `.env.example` -> `.env`
2. Set `DATABASE_URL` và `JWT_SECRET`
3. Chạy migrate + seed admin:
   ```bash
   cd web
   npm install
   npx prisma migrate dev
   npm run seed
   npm run dev
   ```
4. Truy cập:
   - Login: `http://localhost:3000/login`
   - Dashboard: `http://localhost:3000/dashboard`

Seed mặc định:
- `ADMIN_EMAIL=admin@agency.local`
- `ADMIN_PASSWORD=changeme`

## Metabase (BI thay cho Looker)
Metabase không cần API tạo dashboard. Bạn có thể:
1. Tạo 1 dashboard mẫu trên Metabase.
2. Bật embed và lấy URL.
3. Lưu embed URL vào client (`metabaseEmbedUrl`) để hiển thị trong app.

## Deploy scripts (GCP)
- `scripts/create_secrets.sh`: tạo Secret Manager entries từ file token.
- `scripts/deploy_cloud_run.sh`: build image, deploy Cloud Run Job, tạo Scheduler trigger.

## CI/CD (GitHub Actions)
Workflow nằm ở `Report automation/.github/workflows/deploy.yml` và yêu cầu secrets:
- `GCP_PROJECT_ID`
- `GCP_WIF_PROVIDER`
- `GCP_SERVICE_ACCOUNT`

Workflow sẽ build/test, build & push image lên Artifact Registry, deploy Cloud Run Job, và đảm bảo Scheduler job.

## Lưu ý
- Metabase thường refresh theo truy vấn; hệ thống chỉ đảm bảo dữ liệu BigQuery được cập nhật.
- Các connector Ads hiện là adapter skeleton (ready-to-fill), bạn chỉ cần thay phần TODO bằng logic gọi API thật và map dữ liệu về `AdsDailyRow`.
