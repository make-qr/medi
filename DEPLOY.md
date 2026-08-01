# Deploy — medi.omeglechat.online

## 1. GitHub repo

Tạo repo (public) `medi.omeglechat.online` hoặc monorepo path — push nhánh `main`.

## 2. GitHub Pages

Workflow `.github/workflows/pages.yml` build Jekyll → `gh-pages` với CNAME `medi.omeglechat.online`.

## 3. Cloudflare DNS

| Type | Name | Target |
|------|------|--------|
| CNAME | `medi` | `<user>.github.io` (hoặc Pages custom domain target) |

Bật proxy nếu anh dùng cùng pattern với blog.

## 4. Kiểm tra

- https://medi.omeglechat.online/
- https://medi.omeglechat.online/loneliness-vs-solitude/
- https://medi.omeglechat.online/ads.txt
- https://medi.omeglechat.online/sitemap.xml

## Local

```bash
./preview.sh   # port 4001
```
