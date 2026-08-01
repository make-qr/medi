# OmegleChat Medi

**Live:** https://medi.omeglechat.online  
**Source:** `du-an/ca-nhan-anh/omeglechat/medi.omeglechat.online/`  
**Kế hoạch nội dung:** [KE-HOACH-NOI-DUNG.md](KE-HOACH-NOI-DUNG.md)

Health-light essays (loneliness, sleep, gentle habits, aging mind) in the OmegleChat blog voice — connection-first, not a clinic.

## Local preview

```bash
./preview.sh
# → http://localhost:4001/
```

## Build

```bash
bundle install
bundle exec jekyll build
```

## Deploy

Push `main` → GitHub Pages (workflow `.github/workflows/pages.yml`).  
DNS: CNAME `medi` → Pages (same pattern as `blog.omeglechat.online`).

## CTA

Soft chat CTA → `https://omeglechat.online/chat.html`  
Stories/guides → `https://blog.omeglechat.online`
